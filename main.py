#!/usr/bin/env python3
"""
Aplicación de línea de comandos para generar mapas personalizados
"""

import argparse
import sys
from map_generator import MapGenerator
from color_palettes import list_palettes

def main():
    parser = argparse.ArgumentParser(
        description="Genera mapas personalizados con datos de OpenStreetMap",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py --address "Plaza Mayor, Madrid" --radius 1 --palette classic
  python main.py --coords 40.4168 -3.7038 --radius 2 --palette ocean --output madrid_ocean.html
  python main.py --list-palettes
        """
    )
    
    # Grupo para ubicación
    location_group = parser.add_mutually_exclusive_group(required=False)
    location_group.add_argument(
        '--address', '-a',
        type=str,
        help='Dirección a buscar (ej: "Plaza Mayor, Madrid")'
    )
    location_group.add_argument(
        '--coords', '-c',
        nargs=2,
        type=float,
        metavar=('LAT', 'LON'),
        help='Coordenadas GPS (latitud longitud)'
    )
    
    # Parámetros del mapa
    parser.add_argument(
        '--radius', '-r',
        type=float,
        default=1.0,
        help='Radio en kilómetros (por defecto: 1.0 km)'
    )
    
    parser.add_argument(
        '--palette', '-p',
        type=str,
        default='classic',
        choices=list_palettes(),
        help=f'Paleta de colores a usar (opciones: {", ".join(list_palettes())})'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='map.html',
        help='Archivo de salida (por defecto: map.html)'
    )
    
    # Opciones informativas
    parser.add_argument(
        '--list-palettes',
        action='store_true',
        help='Muestra las paletas de colores disponibles'
    )
    
    args = parser.parse_args()
    
    # Mostrar paletas disponibles
    if args.list_palettes:
        print("Paletas de colores disponibles:")
        for palette in list_palettes():
            print(f"  - {palette}")
        return
    
    # Validar que se proporcione una ubicación
    if not args.address and not args.coords:
        print("Error: Debes proporcionar una dirección (--address) o coordenadas (--coords)")
        parser.print_help()
        sys.exit(1)
    
    # Validar radio
    if args.radius <= 0:
        print("Error: El radio debe ser mayor que 0")
        sys.exit(1)
    
    try:
        # Crear generador de mapas
        generator = MapGenerator(palette_name=args.palette)
        
        # Determinar ubicación
        if args.address:
            location = args.address
            print(f"Buscando dirección: {args.address}")
        else:
            location = tuple(args.coords)
            print(f"Usando coordenadas: {args.coords[0]}, {args.coords[1]}")
        
        # Generar mapa
        generator.generate_custom_map(
            location=location,
            radius_km=args.radius,
            output_file=args.output
        )
        
        print(f"\n✓ Mapa generado exitosamente: {args.output}")
        print(f"Abre el archivo en tu navegador para ver el resultado.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()