# Generative Map Art Generator (VIBE CODING)

A generative art system that transforms real OpenStreetMap data into unique and unrepeatable artworks.

## ✨ Features

- **🎨 Generative Art**: Each map is a unique artwork based on creative algorithms
- **🌱 Seed System**: Generate reproducible art with numerical seeds
- **🎭 4 Generative Styles**: `organic`, `geometric`, `flow`, `structured`
- **🎨 8 Color Palettes**: `classic`, `neon_city`, `cyberpunk`, `pastel_dream`, `ocean`, `sunset`, `forest`, `dark_mode`
- **📍 Flexible Search**: By address or GPS coordinates
- **🖼️ Direct Export**: Interactive HTML or high-quality PNG
- **🔄 Infinite Variation**: Same location generates completely different art
- **⭕ Circular Frame**: Configurable circular frame with custom color and width
- **🎨 Color Variation**: Adjustable color diversity for adjacent elements (0.0-1.0)

## 🎯 Generative Art

This system is not just a map generator, but an **urban generative art** tool that:

- **Interprets geographic data** as artistic elements
- **Applies algorithmic variations** based on position, seed and style
- **Generates dynamic palettes** with color, saturation and hue variations
- **Creates unique compositions** where each execution produces different artwork

### Generative Styles

- **`organic`**: Fluid forms, hue variations, random elements
- **`geometric`**: Mathematical precision, binary colors, rigid structure  
- **`flow`**: Dynamic movement, variable saturation, fluctuating widths
- **`structured`**: Architectural order, clear hierarchy, balanced composition

## 🚀 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright for image export
playwright install chromium
```

## 🎨 Usage

### Generate Generative Art

```bash
# Art with specific seed for reproducibility
python3 main.py --coords 39.4699 -0.3763 --palette neon_city --seed 42 --export-image valencia_neon.png

# Explore different styles with gradients
python3 main.py --coords 51.5074 -0.1278 --palette cyberpunk --seed 999 --gradients --export-image london_cyber.png

# Organic art with pastel palette, custom frame and high color variation
python3 main.py --address "Times Square, New York" --palette pastel_dream --seed 777 --gradients --frame-color "#ff6b6b" --frame-width 20 --color-variation 0.8 --export-image nyc_pastel.png
```

### Complete Parameters

```bash
python3 main.py [LOCATION] [OPTIONS]

# Location (one required)
--address, -a TEXT          Address to search
--coords, -c LAT LON        GPS coordinates

# Artistic configuration  
--palette, -p PALETTE       Color palette (see --list-palettes)
--seed, -s INT             Seed for reproducible art
--gradients, -g            Enable gradient styling for elements
--radius, -r FLOAT         Radius in kilometers (default: 1.0)
--frame-color COLOR        Color of circular frame (default: #333)
--frame-width INT          Width of circular frame in pixels (default: 10)
--color-variation FLOAT    Color diversity for adjacent elements (0.0-1.0, default: 0.3)

# Export
--output, -o FILE          HTML file (default: map.html)
--export-image, -i FILE    Export as high-quality PNG
--image-size, -size INT    Image size in pixels (default: 1200)

# Utilities
--list-palettes            Show available palettes
```

### Artistic Palettes

| Palette | Description | Best for |
|---------|-------------|----------|
| `classic` | Traditional cartographic colors | Minimal art, printing |
| `neon_city` | Vibrant neons on dark background | Urban art, cyberpunk |
| `cyberpunk` | Futuristic colors, high saturation | Sci-fi, gaming |
| `pastel_dream` | Soft and relaxing tones | Decorative art, wellness |
| `ocean` | Marine blues and greens | Coastal landscapes, calm |
| `sunset` | Warm oranges and yellows | Emotional art, energy |
| `forest` | Natural greens | Sustainability, nature |
| `dark_mode` | Dark tones with bright accents | Modern interfaces, elegance |

## 🎭 Generative Art Examples

```bash
# Valencia art collection with different seeds
python3 main.py --coords 39.4699 -0.3763 --palette sunset --seed 123 --export-image valencia_1.png
python3 main.py --coords 39.4699 -0.3763 --palette sunset --seed 456 --export-image valencia_2.png
python3 main.py --coords 39.4699 -0.3763 --palette sunset --seed 789 --export-image valencia_3.png

# Same place, different palettes
python3 main.py --coords 48.8566 2.3522 --palette neon_city --seed 2024 --export-image paris_neon.png
python3 main.py --coords 48.8566 2.3522 --palette pastel_dream --seed 2024 --export-image paris_pastel.png
```

## 🛠️ Project Structure

```
gen_maps/
├── main.py                 # Main CLI with image export
├── map_generator.py        # Generative art engine
├── osm_data.py            # OpenStreetMap interface
├── color_palettes.py      # Advanced palette system
├── screenshot_map.py      # Screenshot utility
├── generative_test.py     # Generative variation tests
├── art_batch.py          # Batch art generation
└── requirements.txt       # Dependencies
```

## 🎨 Use Cases

### Digital Art
- Creating unique pieces for exhibitions
- Geography-based NFTs
- Urban publication illustrations

### Graphic Design
- Abstract backgrounds for interfaces
- Unique decorative patterns
- Location-based visual identity

### Urban Research
- Alternative geographic data visualization
- Aesthetic analysis of urban structures
- Artistic comparison between cities

## 🔮 Generative Algorithms

The system implements multiple generative art techniques:

- **Positional hashing**: Colors vary by geographic coordinates
- **Spatial color variation**: Configurable diversity for adjacent elements
- **Emergent clustering**: Similar elements group naturally  
- **Stochastic variation**: Seed-controlled randomization
- **Color transformations**: HSV, dynamic saturation, complementaries
- **Adaptive density**: Elements shown by generative importance
- **Procedural effects**: Glow, shadows, variable transparencies

## 📊 Reproducibility

Each generated artwork includes:
- **Unique seed**: To regenerate the exact same piece
- **Identified style**: Specific algorithm applied
- **Technical parameters**: Complete configuration for reproduction

## 🌟 Upcoming Features

- **Generative animations**: Maps that evolve in real time
- **Custom palettes**: Visual color editor
- **Hybrid styles**: Combination of multiple algorithms
- **Vector export**: SVG for high-quality printing
- **Web API**: Art generation from any application