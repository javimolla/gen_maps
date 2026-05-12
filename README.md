# Generative Map Art Generator

A generative art tool that transforms real OpenStreetMap data into unique artworks. Runs entirely in the browser — no installation required.

**[Try it live →](https://javimolla.github.io/gen_maps/)**

## ✨ Features

- **8 color palettes**: `classic`, `neon_city`, `cyberpunk`, `pastel_dream`, `ocean`, `sunset`, `forest`, `dark_mode`
- **4 generative styles**: `organic`, `geometric`, `flow`, `structured`
- **Seed system**: reproduce any artwork with its numerical seed
- **Flexible search**: by address or GPS coordinates
- **Circular frame**: optional frame with configurable color and width
- **Color variation**: adjustable diversity for adjacent elements (0.0–1.0)
- **Export**: download a standalone HTML file ready to share or print to PDF

## 🚀 Usage

Open [https://javimolla.github.io/gen_maps/](https://javimolla.github.io/gen_maps/) and follow the 5-step wizard:

1. **Palette** — choose a color palette
2. **Parameters** — set radius, seed, style, and color variation
3. **Frame** — optionally add a circular frame
4. **Preview** — generate a live preview from OpenStreetMap data
5. **Download** — export a standalone HTML artwork

No sign-up, no server, no dependencies. Everything runs in your browser using the public [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API) and [Nominatim](https://nominatim.org/) for geocoding.

## 🎨 Palettes

| Palette | Description |
|---------|-------------|
| `classic` | Traditional cartographic colors |
| `neon_city` | Vibrant neons on dark background |
| `cyberpunk` | Futuristic colors, high saturation |
| `pastel_dream` | Soft and relaxing tones |
| `ocean` | Marine blues and greens |
| `sunset` | Warm oranges and yellows |
| `forest` | Natural greens |
| `dark_mode` | Dark tones with bright accents |

## 🎭 Generative Styles

| Style | Character |
|-------|-----------|
| `organic` | Fluid forms, hue variation, random elements |
| `geometric` | Mathematical precision, binary colors, rigid structure |
| `flow` | Dynamic movement, variable saturation, fluctuating widths |
| `structured` | Architectural order, clear hierarchy, balanced composition |

## 🛠️ Project Structure

```
gen_maps/
├── index.html          # Full static web app (single file)
├── src/
│   ├── main.py         # Python CLI (local use)
│   ├── map_generator.py
│   ├── osm_data.py
│   └── color_palettes.py
├── .github/workflows/
│   └── pages.yml       # GitHub Pages deployment
└── requirements.txt    # Python dependencies (CLI only)
```

## 🔧 Local Python CLI

The original Python CLI is still available for local use:

```bash
pip install -r requirements.txt

# Generate art by coordinates
python3 src/main.py --coords 39.4699 -0.3763 --palette neon_city --seed 42

# Generate art by address
python3 src/main.py --address "Times Square, New York" --palette pastel_dream --seed 777

# See all options
python3 src/main.py --help
```

## 🔮 How It Works

The generative engine uses:

- **Positional hashing** — colors vary by geographic coordinates
- **Seeded PRNG** (mulberry32) — fully reproducible outputs
- **HSV color transformations** — dynamic saturation and hue variation
- **Adaptive density** — elements weighted by generative importance

Data is fetched live from OpenStreetMap via the Overpass API and rendered client-side with [Leaflet.js](https://leafletjs.com/).
