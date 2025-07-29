"""
Predefined color palettes for OpenStreetMap elements
"""

# Available color palettes
COLOR_PALETTES = {
    "neon_city": {
        "highway": {
            "motorway": "#ff006e",
            "motorway_link": "#ff1a7a",
            "trunk": "#8338ec", 
            "trunk_link": "#9249f0",
            "primary": "#3a86ff",
            "primary_link": "#4d94ff",
            "secondary": "#06ffa5",
            "secondary_link": "#1affac",
            "tertiary": "#ffbe0b",
            "tertiary_link": "#ffc520",
            "unclassified": "#fb8500",
            "residential": "#666666",
            "service": "#555555",
            "living_street": "#777777",
            "pedestrian": "#888888",
            "track": "#444444",
            "footway": "#555555",
            "bridleway": "#666666",
            "steps": "#777777",
            "path": "#555555",
            "cycleway": "#00e676"
        },
        "landuse": {
            "forest": "#1b5e20",
            "grass": "#2e7d32",
            "residential": "#263238",
            "commercial": "#37474f",
            "industrial": "#455a64",
            "water": "#006064",
            "park": "#2e7d32"
        },
        "natural": {
            "water": "#00bcd4",
            "wood": "#388e3c",
            "grassland": "#66bb6a",
            "scrub": "#43a047"
        },
        "building": {
            "yes": "#424242",
            "residential": "#525252",
            "commercial": "#9c27b0",
            "office": "#673ab7",
            "industrial": "#607d8b",
            "retail": "#525252",
            "hotel": "#525252",
            "school": "#ff9800",
            "university": "#ffc107",
            "hospital": "#f44336",
            "church": "#795548",
            "cathedral": "#8d6e63",
            "mosque": "#795548",
            "synagogue": "#795548",
            "temple": "#795548"
        },
        "railway": {
            "rail": "#ff6b35",
            "light_rail": "#f7931e",
            "subway": "#c5299b",
            "tram": "#7209b7"
        }
    },
    
    "cyberpunk": {
        "highway": {
            "motorway": "#00ff41",
            "motorway_link": "#14ff55",
            "trunk": "#ff073a", 
            "trunk_link": "#ff1b4a",
            "primary": "#00d4aa",
            "primary_link": "#14ddb4",
            "secondary": "#ff9500",
            "secondary_link": "#ffa014",
            "tertiary": "#9d4edd",
            "tertiary_link": "#a663e1",
            "unclassified": "#7209b7",
            "residential": "#560bad",
            "service": "#480ca8",
            "living_street": "#3a0ca3",
            "pedestrian": "#3f37c9",
            "track": "#4361ee",
            "footway": "#4895ef",
            "bridleway": "#4cc9f0",
            "steps": "#7209b7",
            "path": "#f72585",
            "cycleway": "#b5179e"
        },
        "landuse": {
            "forest": "#0d1b2a",
            "grass": "#1b263b",
            "residential": "#0f0f23",
            "commercial": "#16213e",
            "industrial": "#1a1a2e",
            "water": "#16213e",
            "park": "#0f3460"
        },
        "natural": {
            "water": "#001d3d",
            "wood": "#003566",
            "grassland": "#0353a4",
            "scrub": "#023e7d"
        },
        "building": {
            "yes": "#0a0a0a",
            "residential": "#1a1a1a",
            "commercial": "#ff073a",
            "office": "#00d4aa",
            "industrial": "#240046",
            "retail": "#ff6d00",
            "hotel": "#f72585",
            "school": "#4361ee",
            "university": "#7209b7",
            "hospital": "#ff006e",
            "church": "#560bad",
            "cathedral": "#3a0ca3",
            "mosque": "#480ca8",
            "synagogue": "#3f37c9",
            "temple": "#4cc9f0"
        },
        "railway": {
            "rail": "#00ff41",
            "light_rail": "#ff073a",
            "subway": "#00d4aa",
            "tram": "#ff9500"
        }
    },
    
    "pastel_dream": {
        "highway": {
            "motorway": "#ff9a9e",
            "motorway_link": "#ffa8ac",
            "trunk": "#fecfef", 
            "trunk_link": "#fed7f0",
            "primary": "#c7ceea",
            "primary_link": "#d0d6ed",
            "secondary": "#b5ead7",
            "secondary_link": "#bfeddd",
            "tertiary": "#ffdac1",
            "tertiary_link": "#ffdfca",
            "unclassified": "#e2f0cb",
            "residential": "#f7f3e9",
            "service": "#f0f4c3",
            "living_street": "#fff9c4",
            "pedestrian": "#dcedc8",
            "track": "#c8e6c9",
            "footway": "#ffcdd2",
            "bridleway": "#d1c4e9",
            "steps": "#ffb3ba",
            "path": "#bae1ff",
            "cycleway": "#b5f2ea"
        },
        "landuse": {
            "forest": "#a8d8a8",
            "grass": "#c8e6c9",
            "residential": "#f3e5f5",
            "commercial": "#e1bee7",
            "industrial": "#d1c4e9",
            "water": "#b3e5fc",
            "park": "#dcedc8"
        },
        "natural": {
            "water": "#81d4fa",
            "wood": "#a5d6a7",
            "grassland": "#c5e1a5",
            "scrub": "#aed581"
        },
        "building": {
            "yes": "#f5f5f5",
            "residential": "#fce4ec",
            "commercial": "#e8eaf6",
            "office": "#e3f2fd",
            "industrial": "#f3e5f5",
            "retail": "#fff3e0",
            "hotel": "#fce4ec",
            "school": "#e0f2f1",
            "university": "#f1f8e9",
            "hospital": "#ffebee",
            "church": "#efebe9",
            "cathedral": "#f5f5f5",
            "mosque": "#e8f5e8",
            "synagogue": "#e1f5fe",
            "temple": "#fff8e1"
        },
        "railway": {
            "rail": "#9e9e9e",
            "light_rail": "#b39ddb",
            "subway": "#81c784",
            "tram": "#ffb74d"
        }
    },
    
    "classic": {
        "highway": {
            "motorway": "#e892a2",
            "motorway_link": "#eb9faa",
            "trunk": "#f9b29c", 
            "trunk_link": "#fabfa9",
            "primary": "#fcd6a4",
            "primary_link": "#fddbae",
            "secondary": "#f7fabf",
            "secondary_link": "#f9fcc7",
            "tertiary": "#c8facc",
            "tertiary_link": "#d2fbd4",
            "unclassified": "#e0e0e0",
            "residential": "#f0f0f0",
            "service": "#d0d0d0",
            "living_street": "#e8e8e8",
            "pedestrian": "#e8e8e8",
            "track": "#d4b896",
            "footway": "#cccccc",
            "bridleway": "#cccccc",
            "steps": "#cccccc",
            "path": "#cccccc",
            "cycleway": "#65c665"
        },
        "landuse": {
            "forest": "#8dc56c",
            "grass": "#cfeca8",
            "residential": "#e0dfdf",
            "commercial": "#efc8c8",
            "industrial": "#ebdbe8",
            "water": "#aad3df",
            "park": "#c8facc"
        },
        "natural": {
            "water": "#aad3df",
            "wood": "#8dc56c",
            "grassland": "#cfeca8",
            "scrub": "#b5d0a0"
        },
        "building": {
            "yes": "#d9d0c9",
            "residential": "#e8ddd6",
            "commercial": "#d4c4b8",
            "office": "#c9b8a8",
            "industrial": "#bfaea1",
            "retail": "#e0d1c4",
            "hotel": "#dccabe",
            "school": "#f2e8db",
            "university": "#ede0d3",
            "hospital": "#f7ede0",
            "church": "#e5d6c9",
            "cathedral": "#dcc8bb",
            "mosque": "#d7c2b5",
            "synagogue": "#d2bdaf",
            "temple": "#cdb8a9"
        },
        "railway": {
            "rail": "#444444",
            "light_rail": "#666666",
            "subway": "#222222",
            "tram": "#777777"
        }
    },
    
    "ocean": {
        "highway": {
            "motorway": "#1e3a8a",
            "trunk": "#1e40af",
            "primary": "#2563eb",
            "secondary": "#3b82f6",
            "tertiary": "#60a5fa",
            "residential": "#93c5fd",
            "service": "#bfdbfe",
            "footway": "#1e40af",
            "cycleway": "#2563eb"
        },
        "landuse": {
            "forest": "#065f46",
            "grass": "#10b981",
            "residential": "#d1fae5",
            "commercial": "#a7f3d0",
            "industrial": "#6ee7b7",
            "water": "#0891b2",
            "park": "#34d399"
        },
        "natural": {
            "water": "#0891b2",
            "wood": "#065f46",
            "grassland": "#10b981",
            "scrub": "#059669"
        },
        "building": "#e0f2fe",
        "railway": "#0f172a"
    },
    
    "sunset": {
        "highway": {
            "motorway": "#7c2d12",
            "trunk": "#ea580c",
            "primary": "#f97316",
            "secondary": "#fb923c",
            "tertiary": "#fdba74",
            "residential": "#fed7aa",
            "service": "#fef3c7",
            "footway": "#dc2626",
            "cycleway": "#f59e0b"
        },
        "landuse": {
            "forest": "#166534",
            "grass": "#22c55e",
            "residential": "#fef7cd",
            "commercial": "#fde047",
            "industrial": "#facc15",
            "water": "#0ea5e9",
            "park": "#4ade80"
        },
        "natural": {
            "water": "#0ea5e9",
            "wood": "#166534",
            "grassland": "#22c55e",
            "scrub": "#15803d"
        },
        "building": "#fef3c7",
        "railway": "#451a03"
    },
    
    "dark_mode": {
        "highway": {
            "motorway": "#bb86fc",
            "motorway_link": "#c499fd",
            "trunk": "#03dac6", 
            "trunk_link": "#1ce0d0",
            "primary": "#cf6679",
            "primary_link": "#d37383",
            "secondary": "#f48fb1",
            "secondary_link": "#f69bb5",
            "tertiary": "#80cbc4",
            "tertiary_link": "#8dd1ca",
            "unclassified": "#90a4ae",
            "residential": "#bcaaa4",
            "service": "#8d6e63",
            "living_street": "#a1887f",
            "pedestrian": "#b39ddb",
            "track": "#9fa8da",
            "footway": "#c5cae9",
            "bridleway": "#d1c4e9",
            "steps": "#e1bee7",
            "path": "#f8bbd9",
            "cycleway": "#f48fb1"
        },
        "landuse": {
            "forest": "#1b5e20",
            "grass": "#2e7d32",
            "residential": "#212121",
            "commercial": "#424242",
            "industrial": "#616161",
            "water": "#0d47a1",
            "park": "#388e3c"
        },
        "natural": {
            "water": "#1565c0",
            "wood": "#2e7d32",
            "grassland": "#388e3c",
            "scrub": "#43a047"
        },
        "building": {
            "yes": "#303030",
            "residential": "#424242",
            "commercial": "#512da8",
            "office": "#303f9f",
            "industrial": "#455a64",
            "retail": "#7b1fa2",
            "hotel": "#c2185b",
            "school": "#f57c00",
            "university": "#fbc02d",
            "hospital": "#d32f2f",
            "church": "#5d4037",
            "cathedral": "#6d4c41",
            "mosque": "#795548",
            "synagogue": "#8d6e63",
            "temple": "#a1887f"
        },
        "railway": {
            "rail": "#ff6f00",
            "light_rail": "#ff8f00",
            "subway": "#ffa000",
            "tram": "#ffb300"
        }
    },
    
    "forest": {
        "highway": {
            "motorway": "#365314",
            "trunk": "#4d7c0f",
            "primary": "#65a30d",
            "secondary": "#84cc16",
            "tertiary": "#a3e635",
            "residential": "#d9f99d",
            "service": "#ecfccb",
            "footway": "#166534",
            "cycleway": "#22c55e"
        },
        "landuse": {
            "forest": "#14532d",
            "grass": "#16a34a",
            "residential": "#f0fdf4",
            "commercial": "#dcfce7",
            "industrial": "#bbf7d0",
            "water": "#0891b2",
            "park": "#22c55e"
        },
        "natural": {
            "water": "#0891b2",
            "wood": "#14532d",
            "grassland": "#16a34a",
            "scrub": "#15803d"
        },
        "building": "#f0fdf4",
        "railway": "#052e16"
    }
}

def get_gradient_colors(base_color, steps=3):
    """
    Generates a series of colors to create more subtle gradient effects
    """
    if not base_color.startswith('#'):
        return [base_color] * steps
    
    try:
        # Convert hex to RGB
        hex_color = base_color[1:]
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        colors = []
        for i in range(steps):
            # More subtle variations for less visual noise
            factor = 0.9 + (i * 0.2 / steps)  # Between 0.9 and 1.1
            new_r = min(255, max(0, int(r * factor)))
            new_g = min(255, max(0, int(g * factor)))
            new_b = min(255, max(0, int(b * factor)))
            colors.append(f'#{new_r:02x}{new_g:02x}{new_b:02x}')
        
        return colors
    except:
        return [base_color] * steps

def get_complementary_color(color):
    """
    Gets complementary color for contrast effects
    """
    if not color.startswith('#'):
        return color
    
    try:
        hex_color = color[1:]
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Calculate complementary
        comp_r = 255 - r
        comp_g = 255 - g
        comp_b = 255 - b
        
        return f'#{comp_r:02x}{comp_g:02x}{comp_b:02x}'
    except:
        return color

def get_color_for_element(palette_name, element_type, element_subtype=None):
    """
    Gets color for specific element according to selected palette
    """
    if palette_name not in COLOR_PALETTES:
        palette_name = "classic"
    
    palette = COLOR_PALETTES[palette_name]
    
    if element_type in palette:
        if isinstance(palette[element_type], dict) and element_subtype:
            # Search for specific subtype, or use appropriate fallback
            if element_subtype in palette[element_type]:
                return palette[element_type][element_subtype]
            elif element_type == "highway":
                return palette[element_type].get("residential", "#ffffff")
            elif element_type == "building":
                return palette[element_type].get("yes", "#d9d0c9")
            elif element_type == "railway":
                return palette[element_type].get("rail", "#444444")
            else:
                # For landuse and natural, use first available value
                return list(palette[element_type].values())[0] if palette[element_type] else "#ffffff"
        elif isinstance(palette[element_type], str):
            return palette[element_type]
    
    return "#ffffff"  # Default color

def list_palettes():
    """
    Returns list of available palettes
    """
    return list(COLOR_PALETTES.keys())