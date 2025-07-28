"""
Paletas de colores predefinidas para elementos de OpenStreetMap
"""

# Paletas de colores disponibles
COLOR_PALETTES = {
    "classic": {
        "highway": {
            "motorway": "#e892a2",
            "trunk": "#f9b29c", 
            "primary": "#fcd6a4",
            "secondary": "#f7fabf",
            "tertiary": "#c8facc",
            "residential": "#ffffff",
            "service": "#cccccc",
            "footway": "#fa8072",
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
        "building": "#d9d0c9",
        "railway": "#444444"
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

def get_color_for_element(palette_name, element_type, element_subtype=None):
    """
    Obtiene el color para un elemento específico según la paleta seleccionada
    """
    if palette_name not in COLOR_PALETTES:
        palette_name = "classic"
    
    palette = COLOR_PALETTES[palette_name]
    
    if element_type in palette:
        if isinstance(palette[element_type], dict) and element_subtype:
            return palette[element_type].get(element_subtype, palette[element_type].get("residential", "#ffffff"))
        elif isinstance(palette[element_type], str):
            return palette[element_type]
    
    return "#ffffff"  # Color por defecto

def list_palettes():
    """
    Devuelve la lista de paletas disponibles
    """
    return list(COLOR_PALETTES.keys())