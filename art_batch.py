#!/usr/bin/env python3
"""
Generación en lote de arte generativo de mapas
"""

import subprocess
import random
from color_palettes import list_palettes

def generate_art_batch():
    """
    Genera múltiples obras de arte generativo
    """
    # Coordenadas interesantes para arte
    locations = [
        ([40.4168, -3.7038], "madrid"),
        ([51.5074, -0.1278], "london"), 
        ([48.8566, 2.3522], "paris"),
        ([35.6762, 139.6503], "tokyo"),
        ([40.7128, -74.0060], "nyc")
    ]
    
    palettes = list_palettes()
    
    print("🎨 Generando colección de arte generativo...")
    
    for coords, city in locations:
        for palette in palettes[:3]:  # Solo primeras 3 paletas
            seed = random.randint(1, 9999)
            
            output_html = f"art_collection/{city}_{palette}_{seed}.html"
            output_image = f"art_collection/{city}_{palette}_{seed}.png"
            
            cmd = [
                "python3", "main.py",
                "--coords", str(coords[0]), str(coords[1]),
                "--radius", "1.5",
                "--palette", palette,
                "--seed", str(seed),
                "--output", output_html,
                "--export-image", output_image
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✓ {city}_{palette}_{seed}")
                else:
                    print(f"✗ Error: {city}_{palette}_{seed}")
            except Exception as e:
                print(f"✗ Exception: {e}")

if __name__ == "__main__":
    import os
    os.makedirs("art_collection", exist_ok=True)
    generate_art_batch()