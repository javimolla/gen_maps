#!/usr/bin/env python3
"""
Script para generar y visualizar mapas mejorados usando Playwright
"""

import os
import time
from playwright.sync_api import sync_playwright
from map_generator import MapGenerator
from color_palettes import list_palettes

def generate_and_screenshot_map(location, radius_km=1.5, palette="classic"):
    """
    Genera un mapa y toma una captura de pantalla
    """
    print(f"Generando mapa con paleta: {palette}")
    
    # Generar el mapa
    generator = MapGenerator(palette_name=palette)
    map_obj = generator.generate_custom_map(location, radius_km, f"test_maps/map_{palette}.html")
    
    # Tomar captura de pantalla con Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False para ver el proceso
        page = browser.new_page()
        
        # Cargar el mapa
        map_path = os.path.abspath(f"test_maps/map_{palette}.html")
        page.goto(f"file://{map_path}")
        
        # Esperar a que el mapa cargue completamente
        page.wait_for_load_state("networkidle")
        time.sleep(3)  # Tiempo extra para asegurar carga completa
        
        # Configurar viewport y tomar captura
        page.set_viewport_size({"width": 1200, "height": 800})
        screenshot_path = f"test_maps/screenshot_{palette}.png"
        page.screenshot(path=screenshot_path)
        
        print(f"Captura guardada: {screenshot_path}")
        
        browser.close()
    
    return screenshot_path

def test_improved_maps():
    """
    Función principal para probar las mejoras
    """
    # Crear directorio para resultados
    os.makedirs("test_maps", exist_ok=True)
    
    # Coordenadas de prueba (Madrid, España)
    test_location = [40.4168, -3.7038]
    
    # Probar diferentes paletas
    palettes_to_test = ["classic", "neon_city", "pastel_dream"]
    
    print("Iniciando generación de mapas de prueba...")
    
    for palette in palettes_to_test:
        try:
            screenshot_path = generate_and_screenshot_map(test_location, 1.0, palette)
            print(f"✓ Mapa con paleta '{palette}' generado exitosamente")
        except Exception as e:
            print(f"✗ Error con paleta '{palette}': {e}")
        
        time.sleep(2)  # Pausa entre generaciones
    
    print("\n¡Pruebas completadas!")
    print("Revisa la carpeta 'test_maps' para ver los resultados.")

if __name__ == "__main__":
    test_improved_maps()