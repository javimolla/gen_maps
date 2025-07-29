#!/usr/bin/env python3
"""
Script para probar el arte generativo de mapas
"""

import os
from map_generator import MapGenerator
from color_palettes import list_palettes

def test_generative_variations():
    """
    Genera múltiples variaciones del mismo mapa con diferentes seeds
    """
    # Crear directorio para resultados
    os.makedirs("generative_tests", exist_ok=True)
    
    # Coordenadas de prueba (Madrid, España)
    test_location = [40.4168, -3.7038]
    
    # Probar diferentes combinaciones
    palettes = ["classic", "neon_city", "ocean", "sunset"]
    seeds = [42, 123, 777, 999, 2024]
    
    print("Generando arte generativo de mapas...")
    
    for palette in palettes:
        print(f"\n--- Paleta: {palette} ---")
        
        for i, seed in enumerate(seeds):
            try:
                generator = MapGenerator(palette_name=palette, seed=seed)
                output_file = f"generative_tests/{palette}_seed{seed}.html"
                
                generator.generate_custom_map(
                    location=test_location,
                    radius_km=1.0,
                    output_file=output_file
                )
                
                print(f"✓ {palette} - seed {seed}: {generator.style_variation}")
                
            except Exception as e:
                print(f"✗ Error con {palette} seed {seed}: {e}")
    
    print(f"\n¡Generación completada!")
    print("Revisa la carpeta 'generative_tests' para comparar variaciones.")
    print("Cada mapa será único incluso con la misma ubicación y paleta.")

if __name__ == "__main__":
    test_generative_variations()