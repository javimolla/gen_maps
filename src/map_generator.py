"""
Custom map generator with OpenStreetMap data
"""

import folium
from folium import plugins
from color_palettes import get_color_for_element, get_gradient_colors, get_complementary_color, get_gradient_for_element
from osm_data import OSMDataFetcher
import base64
import io
import random
import colorsys

class MapGenerator:
    def __init__(self, palette_name="classic", seed=None, use_gradients=False, frame_color="#333", frame_width=0, color_variation=0.3):
        self.palette_name = palette_name
        self.use_gradients = use_gradients
        self.frame_color = frame_color
        self.frame_width = frame_width
        self.color_variation_intensity = color_variation
        self.osm_fetcher = OSMDataFetcher()
        # Seed for reproducible generative art
        import random
        if seed is not None:
            random.seed(seed)
            self.seed = seed
        else:
            self.seed = random.randint(0, 999999)
            random.seed(self.seed)
        
        # Generative parameters influenced by seed
        self.noise_factor = random.uniform(0.3, 0.8)
        self.color_variance = random.uniform(0.2, 0.6)
        self.density_threshold = random.uniform(0.001, 0.005)
        self.style_variation = random.choice(['organic', 'geometric', 'flow', 'structured'])
        
        print(f"Generative seed: {self.seed}, Style: {self.style_variation}")
    
    def create_map(self, lat, lon, radius_km, zoom_start=None):
        """
        Create a base map centered on specified coordinates with advanced styling
        """
        # Calculate appropriate zoom based on radius
        if zoom_start is None:
            # Very high zoom levels to minimize white space and fill the frame
            if radius_km <= 0.3:
                zoom_start = 19
            elif radius_km <= 0.5:
                zoom_start = 18
            elif radius_km <= 1:
                zoom_start = 17
            elif radius_km <= 2:
                zoom_start = 16
            elif radius_km <= 5:
                zoom_start = 15
            else:
                zoom_start = 14
        
        # Create base map with custom styling
        m = folium.Map(
            location=[lat, lon],
            zoom_start=zoom_start,
            tiles=None,
            zoom_control=False,
            attributionControl=False
        )
        
        # Base limpia sin tiles de fondo para mejor control visual
        if self.palette_name in ['cyberpunk', 'dark_mode']:
            folium.TileLayer(
                tiles='CartoDB dark_matter',
                attr='CartoDB',
                name='Base',
                overlay=False,
                control=False,
                opacity=0.1
            ).add_to(m)
        else:
            # Base muy sutil para no competir con nuestros elementos
            folium.TileLayer(
                tiles='CartoDB positron',
                attr='CartoDB', 
                name='Base',
                overlay=False,
                control=False,
                opacity=0.05
            ).add_to(m)
        
        # Add custom CSS for advanced effects
        css_style = self._get_custom_css()
        m.get_root().html.add_child(folium.Element(css_style))
        
        # Add circular frame only if frame_width > 0
        if self.frame_width > 0:
            frame_div = '<div class="circular-frame"></div>'
            m.get_root().html.add_child(folium.Element(frame_div))
        
        return m
    
    def add_elements_to_map(self, map_obj, osm_data):
        """
        Add OSM elements to map with custom colors
        """
        # Add landuse and natural first (background)
        self._add_polygons(map_obj, osm_data['landuse'], 'landuse')
        self._add_polygons(map_obj, osm_data['natural'], 'natural')
        
        # Add buildings
        self._add_buildings(map_obj, osm_data['buildings'])
        
        # Skip linear elements - only polygonal elements
        # self._add_highways(map_obj, osm_data['highways'])
        # self._add_railways(map_obj, osm_data['railways'])
    
    def _add_polygons(self, map_obj, elements, element_type):
        """
        Add polygons (areas) to map with depth effects
        """
        import random
        
        for element in elements:
            if len(element['coordinates']) < 3:
                continue
            
            subtype = element.get('subtype', 'unknown')
            color = get_color_for_element(self.palette_name, element_type, subtype)
            coords = element['coordinates']
            
            # Use gradient only if enabled
            if self.use_gradients:
                gradient = get_gradient_for_element(self.palette_name, element_type, subtype)
            else:
                gradient = color
            area = self._calculate_polygon_area(coords)
            
            # Generative prominence based on seed and style
            base_threshold = self.density_threshold
            style_modifier = {
                'organic': 0.7,
                'geometric': 1.3, 
                'flow': 0.5,
                'structured': 1.0
            }[self.style_variation]
            
            # Add some randomness for generative variety
            random_factor = random.uniform(0.5, 1.5)
            is_prominent = (
                area > (base_threshold * style_modifier * random_factor) or
                subtype in ['forest', 'park', 'nature_reserve', 'water', 'lake'] or
                (self.style_variation == 'organic' and random.random() < 0.3)
            )
            
            if is_prominent and element_type in ['landuse', 'natural']:
                # Subtle effect without multiple layers to reduce visual complexity
                pass  # Remove concentric waves
                
                # Main area with gradient
                style_dict = {
                    'fillColor': color,
                    'fillOpacity': 0.9,
                    'color': color,
                    'weight': 0.5,
                    'opacity': 0.8
                }
                
                # Add gradient background using CSS
                style_dict['fillColor'] = gradient
                
                folium.Polygon(
                    locations=coords,
                    popup=f"{element_type.title()}: {subtype.replace('_', ' ').title()}",
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=1.0,
                    weight=0,
                    opacity=0
                ).add_to(map_obj)
            else:
                # Generative color variation based on position and style
                pos_hash = hash(str(coords[0])) % 1000 / 1000.0
                variation = 0.8 + (self.color_variance * pos_hash)
                
                if self.style_variation == 'organic':
                    variation *= random.uniform(0.6, 1.4)
                elif self.style_variation == 'geometric':
                    variation = 0.9 + (0.2 * (pos_hash > 0.5))
                
                # Apply spatial color variation for adjacent elements
                spatial_hash = hash(f"{coords[0][0]:.4f}{coords[0][1]:.4f}") % 1000 / 1000.0
                variation_factor = 1.0 + (spatial_hash - 0.5) * self.color_variation_intensity * 2.0
                varied_color = self._vary_color(color, variation_factor)
                
                # Style-based opacity - fixed values independent of seed
                base_opacity = {
                    'organic': 0.75,
                    'geometric': 0.8,
                    'flow': 0.75,
                    'structured': 0.7
                }[self.style_variation]
                
                # Palette-specific opacity boost for problematic palettes
                if self.palette_name in ['pastel_dream', 'sunset', 'forest', 'ocean', 'neon_city', 'cyberpunk']:
                    fill_opacity = min(0.9, base_opacity + 0.4)
                else:
                    fill_opacity = base_opacity
                
                # Force solid fill for all polygons
                final_fill_opacity = 0.9
                
                folium.Polygon(
                    locations=coords,
                    popup=f"{element_type}: {subtype}",
                    color=varied_color,
                    fill=True,
                    fillColor=varied_color,
                    fillOpacity=1.0,
                    weight=0,
                    opacity=0
                ).add_to(map_obj)
    
    def _add_buildings(self, map_obj, buildings):
        """
        Add buildings to map with simulated extrusion effects
        """
        import random
        
        for building in buildings:
            if len(building['coordinates']) < 3:
                continue
            
            building_type = building.get('subtype', 'yes')
            color = get_color_for_element(self.palette_name, 'building', building_type)
            
            # Use gradient only if enabled
            if self.use_gradients:
                gradient = get_gradient_for_element(self.palette_name, 'building', building_type)
            else:
                gradient = color
            
            # Calculate approximate building area to determine importance
            coords = building['coordinates']
            area = self._calculate_polygon_area(coords)
            
            # Generative building prominence
            pos_hash = hash(str(coords[0])) % 1000 / 1000.0
            random_prominence = random.random() < (self.noise_factor * 0.3)
            
            is_prominent = (
                area > (0.0005 * random.uniform(0.5, 2.0)) or
                building_type in ['cathedral', 'hospital', 'university', 'government'] or
                (self.style_variation in ['organic', 'flow'] and random_prominence)
            )
            
            if is_prominent:
                # Edificio destacado con gradiente
                style_dict = {
                    'fillColor': gradient,
                    'fillOpacity': 0.9,
                    'color': color,
                    'weight': 0.5,
                    'opacity': 0.8
                }
                
                folium.Polygon(
                    locations=coords,
                    popup=f"{building_type.replace('_', ' ').title()}",
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=1.0,
                    weight=0,
                    opacity=0
                ).add_to(map_obj)
            else:
                # Generative building clustering and variation
                pos_hash = hash(str(coords[0])) % 1000 / 1000.0
                cluster_factor = 1.0 + (pos_hash * self.color_variance)
                
                if self.style_variation == 'organic':
                    variation = 0.5 + (pos_hash * 1.0)
                elif self.style_variation == 'geometric': 
                    variation = 0.8 + (0.4 * (pos_hash > 0.6))
                elif self.style_variation == 'flow':
                    variation = 0.7 + (0.6 * abs(pos_hash - 0.5))
                else:  # structured
                    variation = 0.9 + (0.2 * random.random())
                
                # Apply spatial color variation for adjacent buildings
                spatial_hash = hash(f"{coords[0][0]:.4f}{coords[0][1]:.4f}") % 1000 / 1000.0
                variation_factor = 1.0 + (spatial_hash - 0.5) * self.color_variation_intensity * 2.0
                varied_color = self._vary_color(color, variation_factor * cluster_factor)
                
                # Style-based fill opacity - fixed values independent of seed
                base_fill_opacity = {
                    'organic': 0.75,
                    'geometric': 0.8,
                    'flow': 0.75,
                    'structured': 0.7
                }[self.style_variation]
                
                # Boost opacity for problematic palettes
                if self.palette_name in ['pastel_dream', 'sunset', 'forest', 'ocean', 'neon_city', 'cyberpunk']:
                    fill_opacity = min(0.9, base_fill_opacity + 0.4)
                else:
                    fill_opacity = base_fill_opacity
                
                # Force solid fill for all buildings
                final_fill_opacity = 0.9
                
                folium.Polygon(
                    locations=coords,
                    popup=f"Building: {building_type}",
                    color=varied_color,
                    fill=True,
                    fillColor=varied_color,
                    fillOpacity=1.0,
                    weight=0,
                    opacity=0
                ).add_to(map_obj)
    
    def _add_highways(self, map_obj, highways):
        """
        Add roads to map with variable thickness and visual effects
        """
        # Simplified widths for better visual hierarchy
        width_map = {
            'motorway': 4,
            'motorway_link': 3,
            'trunk': 3.5,
            'trunk_link': 2.5,
            'primary': 3,
            'primary_link': 2,
            'secondary': 2.5,
            'secondary_link': 2,
            'tertiary': 2,
            'tertiary_link': 1.5,
            'unclassified': 1.5,
            'residential': 1.5,
            'service': 1,
            'living_street': 1.5,
            'pedestrian': 1.5,
            'track': 0.8,
            'footway': 0.8,
            'bridleway': 0.8,
            'steps': 1,
            'path': 0.8,
            'cycleway': 1.2
        }
        
        # Define opacities according to importance
        opacity_map = {
            'motorway': 1.0,
            'trunk': 0.95,
            'primary': 0.9,
            'secondary': 0.85,
            'tertiary': 0.8,
            'residential': 0.75,
            'service': 0.6,
            'footway': 0.5,
            'path': 0.4
        }
        
        for highway in highways:
            if len(highway['coordinates']) < 2:
                continue
                
            highway_type = highway.get('subtype', 'residential')
            color = get_color_for_element(self.palette_name, 'highway', highway_type)
            
            # Use gradient only if enabled
            if self.use_gradients:
                gradient = get_gradient_for_element(self.palette_name, 'highway', highway_type)
            else:
                gradient = color
            
            # Generative road filtering based on style
            if self.style_variation == 'organic':
                # More organic, include some secondary roads randomly
                if highway_type not in ['motorway', 'trunk', 'primary', 'secondary'] or \
                   (highway_type == 'secondary' and random.random() > 0.6):
                    continue
            elif self.style_variation == 'flow':
                # Flowing style, include residential sometimes
                if highway_type not in ['motorway', 'trunk', 'primary'] and \
                   not (highway_type == 'residential' and random.random() < 0.2):
                    continue
            else:
                # Geometric/structured: only major roads
                if highway_type not in ['motorway', 'trunk', 'primary']:
                    continue
                
            width = width_map.get(highway_type, 1.5)
            
            opacity = opacity_map.get(highway_type, 0.7)
            
            # Generative road effects based on style
            if self.style_variation == 'organic' and random.random() < 0.4:
                # Organic glow effect
                glow_color = self._vary_color(color, 0.7)
                folium.PolyLine(
                    locations=highway['coordinates'],
                    color=glow_color,
                    weight=width + 1,
                    opacity=0.2
                ).add_to(map_obj)
            elif highway_type in ['motorway', 'trunk'] and width > 3:
                shadow_color = '#333333' if self.palette_name not in ['dark_mode'] else '#666666'
                folium.PolyLine(
                    locations=highway['coordinates'],
                    color=shadow_color,
                    weight=width + 0.5,
                    opacity=0.3
                ).add_to(map_obj)
            
            # Generative road styling with gradients
            final_color = gradient if (self.use_gradients and 'linear-gradient' in gradient) else color
            final_width = width
            final_opacity = opacity
            
            if self.style_variation == 'flow':
                # Flowing style with varied widths
                flow_factor = random.uniform(0.7, 1.3)
                final_width *= flow_factor
                final_color = self._vary_color(color, flow_factor)
            elif self.style_variation == 'organic':
                # Organic variation
                final_opacity *= random.uniform(0.6, 1.0)
                final_color = self._vary_color(color, random.uniform(0.8, 1.2))
            
            # Use gradient styling for roads if enabled
            if self.use_gradients and 'linear-gradient' in final_color:
                # Create custom CSS styling for gradient roads
                road_style = {
                    'color': color,  # fallback color
                    'weight': final_width,
                    'opacity': final_opacity,
                    'background': final_color
                }
                
                folium.PolyLine(
                    locations=highway['coordinates'],
                    popup=f"{highway_type.replace('_', ' ').title()}",
                    style_function=lambda x, style=road_style: style
                ).add_to(map_obj)
            else:
                folium.PolyLine(
                    locations=highway['coordinates'],
                    popup=f"{highway_type.replace('_', ' ').title()}",
                    color=final_color,
                    weight=final_width,
                    opacity=final_opacity
                ).add_to(map_obj)
    
    def _add_railways(self, map_obj, railways):
        """
        Add railways to map with enhanced visual effects
        """
        railway_styles = {
            'rail': {'weight': 3, 'dash': '8, 4', 'opacity': 0.9},
            'light_rail': {'weight': 2.5, 'dash': '6, 3', 'opacity': 0.85},
            'subway': {'weight': 4, 'dash': '10, 2', 'opacity': 0.95},
            'tram': {'weight': 2, 'dash': '4, 4', 'opacity': 0.8}
        }
        
        for railway in railways:
            if len(railway['coordinates']) < 2:
                continue
            
            railway_type = railway.get('subtype', 'rail')
            color = get_color_for_element(self.palette_name, 'railway', railway_type)
            style = railway_styles.get(railway_type, railway_styles['rail'])
            
            folium.PolyLine(
                locations=railway['coordinates'],
                popup=f"{railway_type.replace('_', ' ').title()}",
                color=color,
                weight=style['weight'],
                opacity=style['opacity'],
                dashArray=style['dash']
            ).add_to(map_obj)
    
    def generate_custom_map(self, location, radius_km, output_file="map.html"):
        """
        Generate a complete map with OSM data and custom colors
        """
        # Get coordinates if an address is provided
        if isinstance(location, str):
            lat, lon = self.osm_fetcher.get_coordinates_from_address(location)
        else:
            lat, lon = location
        
        print(f"Generating map for coordinates: {lat}, {lon}")
        print(f"Radius: {radius_km} km, Palette: {self.palette_name}")
        print(f"Seed: {self.seed}, Style: {self.style_variation}")
        
        # Obtener datos de OSM
        print("Fetching OpenStreetMap data...")
        osm_data = self.osm_fetcher.fetch_osm_data(lat, lon, radius_km)
        
        # Create base map
        map_obj = self.create_map(lat, lon, radius_km)
        
        # Add elements to map
        print("Adding elements to map...")
        self.add_elements_to_map(map_obj, osm_data)
        
        # Save map
        map_obj.save(output_file)
        print(f"Map saved as: {output_file}")
        
        return map_obj
    
    def _get_custom_css(self):
        """
        Generate custom CSS for advanced visual effects
        """
        neon_glow = ""
        if self.palette_name in ['neon_city', 'cyberpunk']:
            neon_glow = """
            .leaflet-interactive {
                filter: drop-shadow(0 0 2px currentColor) drop-shadow(0 0 5px currentColor);
            }
            """
        
        return f"""
        <style>
        .leaflet-container {{
            background: {self._get_background_color()};
            font-family: 'Courier New', monospace;
            clip-path: circle(50% at center);
        }}
        
        .leaflet-popup-content-wrapper {{
            background: rgba(0, 0, 0, 0.8);
            color: #fff;
            border-radius: 8px;
            backdrop-filter: blur(10px);
        }}
        
        .leaflet-popup-tip {{
            background: rgba(0, 0, 0, 0.8);
        }}
        
        {neon_glow}
        
        .custom-building {{
            transition: all 0.3s ease;
        }}
        
        .custom-building:hover {{
            transform: scale(1.05);
            filter: brightness(1.2);
        }}
        
        .gradient-line {{
            background: linear-gradient(90deg, var(--start-color), var(--end-color));
        }}
        
        /* Gradient support for polygons */
        .leaflet-interactive {{
            transition: all 0.2s ease;
        }}
        
        .gradient-fill {{
            background-image: var(--gradient-fill);
        }}
        
        /* Road gradient styling */
        .gradient-road {{
            background: var(--road-gradient);
            background-size: 100% 100%;
        }}
        
        /* Hide all map controls */
        .leaflet-control-container {{
            display: none !important;
        }}
        
        .leaflet-control {{
            display: none !important;
        }}
        
        /* Circular frame styling */        
        .circular-frame {{
            position: fixed;
            top: 50%;
            left: 50%;
            width: min(100vw, 100vh);
            height: min(100vw, 100vh);
            transform: translate(-50%, -50%);
            border: {self.frame_width}px solid {self.frame_color};
            border-radius: 50%;
            box-sizing: border-box;
            pointer-events: none;
            z-index: 10000;
            margin: 0;
        }}
        
        /* Ensure circular frame is visible during screenshot */
        @media screen {{
            .circular-frame {{
                display: block !important;
                visibility: visible !important;
                opacity: 1 !important;
            }}
        }}
        
        </style>
        """
    
    def _get_background_color(self):
        """
        Get background color according to palette
        """
        backgrounds = {
            'neon_city': '#0a0a0a',
            'cyberpunk': '#000011',
            'pastel_dream': '#fefefe',
            'dark_mode': '#121212',
            'classic': '#f8f8f8',
            'ocean': '#f0f8ff',
            'sunset': '#fff8f0',
            'forest': '#f0fff0'
        }
        return backgrounds.get(self.palette_name, '#ffffff')
    
    def _create_custom_icon(self, icon_type, color, size=20):
        """
        Create custom SVG icons for different elements
        """
        icons = {
            'hospital': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}"><path d="M19,3H5C3.9,3 3,3.9 3,5V19C3,20.1 3.9,21 5,21H19C20.1,21 21,20.1 21,19V5C21,3.9 20.1,3 19,3M18,14H13V19H11V14H6V12H11V7H13V12H18V14Z"/></svg>',
            'school': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}"><path d="M12,3L1,9L12,15L21,10.09V17H23V9M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z"/></svg>',
            'church': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}"><path d="M18,12.22V9L16,10V7H13V10.5L12,11L11,10.5V7H8V10L6,9V12.22L2,14.56L12,21L22,14.56L18,12.22M11,13H13V15H11V13Z"/></svg>',
            'commercial': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}"><path d="M12,18H6V14H12M21,14V12L20,7H4L3,12V14H4V20H14V14H18V20H20V14M12,10H6V8H12V10Z"/></svg>',
            'park': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}"><path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z"/></svg>',
            'water': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}"><path d="M12,2C13.1,7.48 18.5,9.89 18.5,14.5C18.5,18.64 15.64,21.5 12,21.5C8.36,21.5 5.5,18.64 5.5,14.5C5.5,9.89 10.9,7.48 12,2Z"/></svg>',
            'center': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}"><circle cx="12" cy="12" r="8" stroke="{color}" stroke-width="2" fill="none"/><circle cx="12" cy="12" r="3" fill="{color}"/><path d="M12 1v6m0 10v6m11-7h-6m-10 0H1" stroke="{color}" stroke-width="2"/></svg>'
        }
        
        svg_icon = icons.get(icon_type, icons['commercial'])
        encoded = base64.b64encode(svg_icon.encode()).decode()
        return f"data:image/svg+xml;base64,{encoded}"
    
    def _calculate_polygon_area(self, coordinates):
        """
        Calculate approximate polygon area using polygon area formula
        """
        if len(coordinates) < 3:
            return 0
        
        area = 0
        n = len(coordinates)
        for i in range(n):
            j = (i + 1) % n
            area += coordinates[i][0] * coordinates[j][1]
            area -= coordinates[j][0] * coordinates[i][1]
        return abs(area) / 2
    
    def _offset_coordinates(self, coordinates, offset_lat, offset_lon):
        """
        Offset coordinates to create shadow effect
        """
        return [[lat + offset_lat, lon + offset_lon] for lat, lon in coordinates]
    
    def _darken_color(self, color):
        """
        Darken a color to create depth effects
        """
        if color.startswith('#'):
            # Convert hex to RGB, darken, and return
            hex_color = color[1:]
            if len(hex_color) == 6:
                r = max(0, int(hex_color[0:2], 16) - 40)
                g = max(0, int(hex_color[2:4], 16) - 40)
                b = max(0, int(hex_color[4:6], 16) - 40)
                return f'#{r:02x}{g:02x}{b:02x}'
        return color  # Fallback to original color
    
    def _vary_color(self, color, factor):
        """
        Enhanced color variation with stronger effects
        """
        if not color.startswith('#'):
            return color
        
        try:
            hex_color = color[1:]
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16) 
            b = int(hex_color[4:6], 16)
            
            import colorsys
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            
            # Apply stronger variations based on factor
            hue_shift = (factor - 1.0) * 0.2  # More hue variation
            sat_factor = 0.5 + factor * 0.5    # Saturation variation
            val_factor = 0.3 + factor * 0.7    # Value variation
            
            # Apply variations
            h = (h + hue_shift) % 1.0
            s = min(1.0, max(0.0, s * sat_factor))
            v = min(1.0, max(0.2, v * val_factor))  # Keep minimum brightness
            
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            r, g, b = int(r*255), int(g*255), int(b*255)
            
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return color