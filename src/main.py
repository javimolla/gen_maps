#!/usr/bin/env python3
"""
Command line application for generating custom maps
"""

import argparse
import sys
from map_generator import MapGenerator
from color_palettes import list_palettes

def main():
    parser = argparse.ArgumentParser(
        description="Generate custom maps with OpenStreetMap data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  python main.py --address "Plaza Mayor, Madrid" --radius 1 --palette classic
  python main.py --coords 40.4168 -3.7038 --radius 2 --palette ocean --output madrid_ocean.html
  python main.py --list-palettes
        """
    )
    
    # Location group
    location_group = parser.add_mutually_exclusive_group(required=False)
    location_group.add_argument(
        '--address', '-a',
        type=str,
        help='Address to search (e.g.: "Plaza Mayor, Madrid")'
    )
    location_group.add_argument(
        '--coords', '-c',
        nargs=2,
        type=float,
        metavar=('LAT', 'LON'),
        help='GPS coordinates (latitude longitude)'
    )
    
    # Map parameters
    parser.add_argument(
        '--radius', '-r',
        type=float,
        default=0.5,
        help='Radius in kilometers (default: 0.5 km)'
    )
    
    parser.add_argument(
        '--palette', '-p',
        type=str,
        default='classic',
        choices=list_palettes(),
        help=f'Color palette to use (options: {", ".join(list_palettes())})'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='map.html',
        help='Output file (default: map.html)'
    )
    
    parser.add_argument(
        '--seed', '-s',
        type=int,
        help='Seed for reproducible generative art'
    )
    
    parser.add_argument(
        '--gradients', '-g',
        action='store_true',
        help='Enable gradient styling for elements'
    )
    
    parser.add_argument(
        '--export-image', '-i',
        type=str,
        help='Export as PNG image (e.g.: map.png)'
    )
    
    # Informational options
    parser.add_argument(
        '--list-palettes',
        action='store_true',
        help='Show available color palettes'
    )
    
    args = parser.parse_args()
    
    # Show available palettes
    if args.list_palettes:
        print("Available color palettes:")
        for palette in list_palettes():
            print(f"  - {palette}")
        return
    
    # Validate that a location is provided
    if not args.address and not args.coords:
        print("Error: You must provide an address (--address) or coordinates (--coords)")
        parser.print_help()
        sys.exit(1)
    
    # Validate radius
    if args.radius <= 0:
        print("Error: Radius must be greater than 0")
        sys.exit(1)
    
    try:
        # Create map generator
        generator = MapGenerator(
            palette_name=args.palette, 
            seed=args.seed,
            use_gradients=args.gradients
        )
        
        # Determine location
        if args.address:
            location = args.address
            print(f"Searching address: {args.address}")
        else:
            location = tuple(args.coords)
            print(f"Using coordinates: {args.coords[0]}, {args.coords[1]}")
        
        # Generate map
        generator.generate_custom_map(
            location=location,
            radius_km=args.radius,
            output_file=args.output
        )
        
        print(f"\n✓ Map generated successfully: {args.output}")
        
        # Export as image if requested
        if args.export_image:
            try:
                from playwright.sync_api import sync_playwright
                import os
                import time
                
                print(f"Exporting to image: {args.export_image}")
                
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    
                    # Load HTML map
                    map_path = os.path.abspath(args.output)
                    page.goto(f"file://{map_path}")
                    
                    # Wait for complete load
                    page.wait_for_load_state("networkidle")
                    time.sleep(3)
                    
                    # Configure viewport for generative art
                    page.set_viewport_size({"width": 1200, "height": 1200})
                    
                    # Take screenshot without controls
                    page.screenshot(
                        path=args.export_image,
                        full_page=False,
                        clip={"x": 0, "y": 0, "width": 1200, "height": 1200}
                    )
                    
                    browser.close()
                
                print(f"✓ Image exported: {args.export_image}")
                
            except ImportError:
                print("Error: Playwright is not installed. Install it with 'pip install playwright'")
            except Exception as e:
                print(f"Error exporting image: {e}")
        else:
            print(f"Open the file in your browser to see the result.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()