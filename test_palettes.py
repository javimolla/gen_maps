#!/usr/bin/env python3
"""
Script to test all available color palettes with custom frame settings
"""

import subprocess
import os
import sys
import time

# Configuration
LOCATION = "Valencia, Spain"
RADIUS = 0.8  # Smaller radius for more detail
FRAME_COLOR = "#DEBF78"  # Light golden color
FRAME_WIDTH = 8  # Smaller frame width
IMAGE_SIZE = 1000  # Image size

# Available palettes
PALETTES = [
    "neon_city",
    "cyberpunk", 
    "pastel_dream",
    "classic",
    "ocean",
    "sunset",
    "dark_mode",
    "forest"
]

def run_command(cmd):
    """Execute a command and return success status"""
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    """Generate maps for all palettes"""
    print(f"🎨 Testing all palettes with location: {LOCATION}")
    print(f"📐 Radius: {RADIUS}km, Frame: {FRAME_COLOR}, Width: {FRAME_WIDTH}px")
    print(f"📏 Image size: {IMAGE_SIZE}px")
    print("=" * 60)
    
    # Create output directory
    output_dir = "palette_tests"
    os.makedirs(output_dir, exist_ok=True)
    
    successful = 0
    failed = 0
    
    for i, palette in enumerate(PALETTES, 1):
        print(f"\n[{i}/{len(PALETTES)}] Generating map with palette: {palette}")
        
        # Generate output filename
        output_file = f"{output_dir}/{palette}_test.png"
        
        # Build command
        cmd = [
            "python3", "src/main.py",
            "--address", LOCATION,
            "--radius", str(RADIUS),
            "--palette", palette,
            "--frame-color", FRAME_COLOR,
            "--frame-width", str(FRAME_WIDTH),
            "--image-size", str(IMAGE_SIZE),
            "--export-image", output_file,
            "--output", f"{output_dir}/{palette}_map.html"
        ]
        
        # Execute command
        start_time = time.time()
        if run_command(cmd):
            elapsed = time.time() - start_time
            print(f"✅ Success! Generated: {output_file} ({elapsed:.1f}s)")
            successful += 1
        else:
            print(f"❌ Failed to generate map for palette: {palette}")
            failed += 1
        
        # Small delay between generations
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 60)
    print(f"🎯 SUMMARY:")
    print(f"   ✅ Successful: {successful}/{len(PALETTES)}")
    print(f"   ❌ Failed: {failed}/{len(PALETTES)}")
    
    if successful > 0:
        print(f"\n📁 Generated files are in: {output_dir}/")
        print("🖼️  PNG images:")
        for palette in PALETTES:
            png_file = f"{output_dir}/{palette}_test.png"
            if os.path.exists(png_file):
                size = os.path.getsize(png_file)
                print(f"   - {png_file} ({size:,} bytes)")
    
    print(f"\n🎨 Frame color used: {FRAME_COLOR}")
    print(f"📐 Frame width: {FRAME_WIDTH}px")
    print(f"🗺️  Location: {LOCATION} (radius: {RADIUS}km)")

if __name__ == "__main__":
    main()