#!/usr/bin/env python3
"""
Flask web server for the Generative Map Art web application
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import json
import subprocess
import uuid
from datetime import datetime
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from map_generator import MapGenerator
from color_palettes import COLOR_PALETTES, list_palettes

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = tempfile.mkdtemp()
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'output', 'web')
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# In-memory storage for imported palettes (temporary session storage)
imported_palettes = {}

@app.route('/')
def index():
    """Serve the main web application"""
    return send_file('index.html')

@app.route('/api/palettes')
def get_palettes():
    """Get available color palettes"""
    try:
        palettes_info = {}
        
        # Add built-in palettes
        for name in list_palettes():
            # Get representative colors for preview
            palette = COLOR_PALETTES[name]
            colors = []
            
            # Extract some representative colors from each palette
            if 'highway' in palette:
                highway_colors = [
                    palette['highway'].get('motorway'),
                    palette['highway'].get('primary'), 
                    palette['highway'].get('secondary'),
                    palette['highway'].get('tertiary')
                ]
                colors.extend([c for c in highway_colors if c])
            
            if 'building' in palette:
                if isinstance(palette['building'], dict):
                    building_color = palette['building'].get('yes') or palette['building'].get('residential')
                    if building_color:
                        colors.append(building_color)
                else:
                    colors.append(palette['building'])
            
            if 'natural' in palette:
                natural_color = palette['natural'].get('water') or palette['natural'].get('wood')
                if natural_color:
                    colors.append(natural_color)
            
            if 'landuse' in palette:
                landuse_colors = [
                    palette['landuse'].get('forest'),
                    palette['landuse'].get('grass'),
                    palette['landuse'].get('commercial')
                ]
                colors.extend([c for c in landuse_colors if c])
            
            # Ensure we have at least 5 colors for preview
            while len(colors) < 5:
                colors.append(colors[0] if colors else '#cccccc')
            
            palettes_info[name] = {
                'name': name,
                'display_name': name.replace('_', ' ').title(),
                'colors': colors[:5]
            }
        
        # Add imported palettes from memory
        for name, palette_data in imported_palettes.items():
            palettes_info[name] = {
                'name': name,
                'display_name': palette_data.get('display_name', name.replace('_', ' ').title()),
                'colors': palette_data.get('colors', [])[:5]
            }
        
        return jsonify(palettes_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_map():
    """Generate artistic map"""
    try:
        data = request.json
        
        # Extract parameters
        lat = float(data.get('lat'))
        lon = float(data.get('lon'))
        palette = data.get('palette', 'classic')
        seed = data.get('seed')
        radius = float(data.get('radius', 1.0))
        gradients = data.get('gradients', False)
        frame_color = data.get('frameColor', '#333')
        frame_width = int(data.get('frameWidth', 0))
        color_variation = float(data.get('colorVariation', 0.3))
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        output_file = os.path.join(OUTPUT_FOLDER, f'map_{file_id}.html')
        
        # Check if palette is imported, if so, create a temporary palette for generation
        if palette in imported_palettes:
            # For imported palettes, we need to create a basic palette structure
            # that MapGenerator can understand
            import tempfile
            from color_palettes import COLOR_PALETTES
            
            # Create a simple palette structure based on imported colors
            colors = imported_palettes[palette]['colors']
            temp_palette = {
                'highway': {
                    'motorway': colors[0] if len(colors) > 0 else '#333333',
                    'primary': colors[1] if len(colors) > 1 else colors[0] if len(colors) > 0 else '#333333',
                    'secondary': colors[2] if len(colors) > 2 else colors[0] if len(colors) > 0 else '#333333',
                    'tertiary': colors[3] if len(colors) > 3 else colors[0] if len(colors) > 0 else '#333333'
                },
                'building': colors[4] if len(colors) > 4 else colors[0] if len(colors) > 0 else '#cccccc',
                'natural': {
                    'water': colors[5] if len(colors) > 5 else colors[1] if len(colors) > 1 else '#87ceeb',
                    'wood': colors[6] if len(colors) > 6 else colors[2] if len(colors) > 2 else '#228b22'
                },
                'landuse': {
                    'forest': colors[7] if len(colors) > 7 else colors[2] if len(colors) > 2 else '#228b22',
                    'grass': colors[8] if len(colors) > 8 else colors[3] if len(colors) > 3 else '#90ee90',
                    'commercial': colors[9] if len(colors) > 9 else colors[4] if len(colors) > 4 else '#ffd700'
                }
            }
            
            # Temporarily add to COLOR_PALETTES
            COLOR_PALETTES[palette] = temp_palette
        
        # Create map generator
        generator = MapGenerator(
            palette_name=palette,
            seed=seed,
            use_gradients=gradients,
            frame_color=frame_color,
            frame_width=frame_width,
            color_variation=color_variation
        )
        
        # Generate map
        generator.generate_custom_map(
            location=(lat, lon),
            radius_km=radius,
            output_file=output_file
        )
        
        # Verify file was created
        if not os.path.exists(output_file):
            return jsonify({'error': 'Failed to generate map file'}), 500
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'file_path': f'/api/map/{file_id}',
            'message': 'Map generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/map/<file_id>')
def get_map(file_id):
    """Serve generated map file"""
    try:
        file_path = os.path.join(OUTPUT_FOLDER, f'map_{file_id}.html')
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            return jsonify({'error': 'Map not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export', methods=['POST'])
def export_image():
    """Export map as image"""
    try:
        data = request.json
        
        file_id = data.get('file_id')
        format_type = data.get('format', 'png')
        width = int(data.get('width', 1200))
        height = int(data.get('height', 1200))
        quality = float(data.get('quality', 0.9))
        
        # Get the HTML file
        html_file = os.path.join(OUTPUT_FOLDER, f'map_{file_id}.html')
        if not os.path.exists(html_file):
            return jsonify({'error': 'Map file not found'}), 404
        
        # Generate output image path - use same file_id as input
        image_file = os.path.join(OUTPUT_FOLDER, f'map_{file_id}.{format_type}')
        
        # Use existing screenshot functionality
        try:
            from playwright.sync_api import sync_playwright
            import time
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Set viewport
                page.set_viewport_size({"width": width, "height": height})
                
                # Load HTML file
                page.goto(f"file://{os.path.abspath(html_file)}")
                
                # Wait for load
                page.wait_for_load_state("networkidle")
                time.sleep(2)
                
                # Take screenshot
                screenshot_options = {
                    'path': image_file,
                    'full_page': False
                }
                
                if format_type in ['jpg', 'jpeg']:
                    screenshot_options['quality'] = int(quality * 100)
                    screenshot_options['type'] = 'jpeg'
                elif format_type == 'webp':
                    screenshot_options['quality'] = int(quality * 100)
                    screenshot_options['type'] = 'webp'
                else:  # png
                    screenshot_options['type'] = 'png'
                
                page.screenshot(**screenshot_options)
                browser.close()
            
            return jsonify({
                'success': True,
                'file_path': f'/api/download/map_{file_id}.{format_type}',
                'message': f'Image exported successfully as {format_type.upper()}'
            })
            
        except ImportError:
            return jsonify({'error': 'Playwright not installed. Install with: pip install playwright'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    """Download exported files"""
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search')
def search_places():
    """Search for places using Nominatim API"""
    try:
        query = request.args.get('q', '')
        if len(query) < 3:
            return jsonify([])
        
        import requests
        
        # Use Nominatim API
        url = 'https://nominatim.openstreetmap.org/search'
        params = {
            'format': 'json',
            'q': query,
            'limit': 5,
            'accept-language': 'en'
        }
        
        response = requests.get(url, params=params, headers={'User-Agent': 'GenerativeMapArt/1.0'})
        response.raise_for_status()
        
        results = response.json()
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                'display_name': result.get('display_name', ''),
                'lat': float(result.get('lat', 0)),
                'lon': float(result.get('lon', 0)),
                'type': result.get('type', ''),
                'importance': result.get('importance', 0)
            })
        
        return jsonify(formatted_results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/palette/import', methods=['POST'])
def import_palette():
    """Import custom palette (temporary session storage)"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read and parse JSON
        content = file.read().decode('utf-8')
        palette_data = json.loads(content)
        
        # Validate and extract palette information
        colors = []
        display_name = ""
        
        # Extract name from various possible locations  
        display_name = (
            palette_data.get('name') or 
            palette_data.get('display_name') or 
            palette_data.get('title') or
            ""
        )
        
        # Debug: log the imported palette structure
        print(f"DEBUG - Imported palette structure: {palette_data}")
        print(f"DEBUG - Extracted display_name: '{display_name}'")
        
        if 'colors' in palette_data:
            colors = palette_data['colors']
        elif 'palette' in palette_data and isinstance(palette_data['palette'], dict):
            # Handle exported palette format
            palette = palette_data['palette']
            
            # Extract colors from palette structure
            for category in ['highway', 'building', 'natural', 'landuse']:
                if category in palette:
                    if isinstance(palette[category], dict):
                        colors.extend([v for v in palette[category].values() if isinstance(v, str) and v.startswith('#')])
                    elif isinstance(palette[category], str) and palette[category].startswith('#'):
                        colors.append(palette[category])
        elif isinstance(palette_data, list):
            # Simple array of colors
            colors = palette_data
        elif isinstance(palette_data, dict) and len(palette_data) > 0:
            # Try to extract colors from any dict structure
            def extract_colors(obj):
                result = []
                if isinstance(obj, dict):
                    for v in obj.values():
                        if isinstance(v, str) and v.startswith('#'):
                            result.append(v)
                        elif isinstance(v, (dict, list)):
                            result.extend(extract_colors(v))
                elif isinstance(obj, list):
                    for item in obj:
                        if isinstance(item, str) and item.startswith('#'):
                            result.append(item)
                        elif isinstance(item, (dict, list)):
                            result.extend(extract_colors(item))
                return result
            colors = extract_colors(palette_data)
        
        if not colors:
            return jsonify({'error': 'No valid colors found in palette'}), 400
        
        # Use original name if available, otherwise generate unique name
        if display_name:
            palette_name = display_name.lower().replace(' ', '_').replace('-', '_')
            # Ensure uniqueness if already exists
            original_name = palette_name
            counter = 1
            while palette_name in imported_palettes or palette_name in COLOR_PALETTES:
                palette_name = f"{original_name}_{counter}"
                counter += 1
            # Format display name nicely (convert underscores to spaces and title case)
            final_display_name = display_name.replace('_', ' ').replace('-', ' ').title()
        else:
            timestamp = int(datetime.now().timestamp())
            palette_name = f"imported_{timestamp}"
            final_display_name = f"Imported Palette {timestamp}"
        
        # Store in memory
        imported_palettes[palette_name] = {
            'colors': colors[:10],  # Store up to 10 colors
            'display_name': final_display_name,
            'source': 'imported',
            'imported_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'palette_name': palette_name,
            'display_name': final_display_name,
            'colors': colors[:5],  # Return first 5 colors for preview
            'message': 'Palette imported and added to selection'
        })
        
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/palettes/clear', methods=['POST'])
def clear_imported_palettes():
    """Clear all imported palettes from memory"""
    try:
        global imported_palettes
        count = len(imported_palettes)
        imported_palettes.clear()
        
        return jsonify({
            'success': True,
            'message': f'Cleared {count} imported palettes',
            'cleared_count': count
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/palette/export/<palette_name>')
def export_palette(palette_name):
    """Export palette as JSON"""
    try:
        if palette_name not in COLOR_PALETTES:
            return jsonify({'error': 'Palette not found'}), 404
        
        palette_data = {
            'name': palette_name,
            'palette': COLOR_PALETTES[palette_name],
            'exported_at': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        # Create temporary file
        temp_file = os.path.join(UPLOAD_FOLDER, f'palette_{palette_name}.json')
        with open(temp_file, 'w') as f:
            json.dump(palette_data, f, indent=2)
        
        return send_file(temp_file, as_attachment=True, download_name=f'palette_{palette_name}.json')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Generative Map Art Web Server...")
    print("Open your browser to: http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET  /                     - Main web application")
    print("  GET  /api/palettes         - Get available palettes")
    print("  POST /api/generate         - Generate artistic map")
    print("  POST /api/export           - Export map as image")
    print("  GET  /api/search           - Search places")
    print("")
    
    app.run(debug=True, host='0.0.0.0', port=5000)