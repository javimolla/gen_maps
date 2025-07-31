# Generative Map Art - Web Application 🎨

A modern web application that transforms real OpenStreetMap data into unique and unrepeatable generative artworks.

## ✨ Web Features

- **🗺️ Interactive Map**: Smooth navigation with Leaflet.js
- **🔍 Smart Search**: Find any place in the world like OpenStreetMap
- **🎨 Visual Configuration**: Intuitive interface to customize artistic appearance
- **📸 Advanced Export**: Multiple formats and resolutions
- **💫 Modern Design**: Clean interface inspired by Dribbble/Behance
- **📱 Responsive**: Optimized for all devices

## 🚀 Quick Setup

```bash
# 1. Clone or navigate to project directory
cd gen_maps

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browser (for export)
playwright install chromium

# 4. Start web application
python start_web.py
```

## 🌐 Using the Web Application

### Access
Open your browser at: **http://localhost:5000**

### Main Features

#### 1. **Place Search** 🔍
- Type any address or location in the search box
- Select from automatic results
- Map will automatically position

#### 2. **Aspect Configuration** 🎨
**"Aspect" Button** opens a modal with:
- **8 Predefined Palettes**: Classic, Neon City, Cyberpunk, Pastel Dream, Ocean, Sunset, Forest, Dark Mode
- **Artistic Parameters**:
  - Seed (for reproducibility)
  - Search radius (0.1-10 km)
  - Circular frame color and width
  - Color variation (0.0-1.0)
  - Enable/disable gradients
- **Import/Export Palettes**: Load temporary custom palettes

#### 3. **Art Generation** ✨
**"Generate Art" Button** creates the artistic map:
- Uses current configuration
- Opens result in new tab
- Enables image export

#### 4. **Image Export** 📸
**"Export" Button** (available after generation):
- **Formats**: PNG, JPEG, WebP, SVG
- **Predefined Resolutions**: 800px to 4000px
- **Custom Resolution**: Up to 8000x8000px
- **Quality Control**: For compressed formats

## 🎭 Paletas Artísticas

| Paleta | Descripción | Mejor Para |
|--------|-------------|------------|
| **Classic** | Colores cartográficos tradicionales | Arte minimalista, impresión |
| **Neon City** | Neones vibrantes sobre fondo oscuro | Arte urbano, cyberpunk |
| **Cyberpunk** | Colores futuristas, alta saturación | Sci-fi, gaming |
| **Pastel Dream** | Tonos suaves y relajantes | Arte decorativo, wellness |
| **Ocean** | Azules y verdes marinos | Paisajes costeros, calma |
| **Sunset** | Naranjas y amarillos cálidos | Arte emocional, energía |
| **Forest** | Verdes naturales | Sostenibilidad, naturaleza |
| **Dark Mode** | Tonos oscuros con acentos brillantes | Interfaces modernas, elegancia |

## 🛠️ Arquitectura Técnica

### Frontend
- **Leaflet.js**: Mapa interactivo
- **CSS3**: Diseño moderno con gradientes y blur effects
- **JavaScript ES6+**: Funcionalidad asíncrona y modular
- **Responsive Design**: Mobile-first approach

### Backend
- **Flask**: Servidor web ligero
- **Flask-CORS**: Habilitación de cross-origin requests
- **Playwright**: Generación de imágenes de alta calidad
- **Nominatim API**: Búsqueda de lugares

### Integración
- **API RESTful**: Comunicación frontend-backend
- **Sistema de archivos temporales**: Gestión de mapas generados
- **Procesamiento asíncrono**: Generación no bloqueante

## 📁 Estructura de Archivos Web

```
gen_maps/
├── index.html              # Página principal de la web
├── app.py                 # Servidor Flask con API
├── start_web.py           # Script de inicio rápido
├── WEB_README.md          # Documentación web
├── src/                   # Código Python existente
│   ├── map_generator.py   # Motor de generación artística
│   ├── color_palettes.py  # Sistema de paletas
│   └── osm_data.py       # Interface OpenStreetMap
└── output/web/           # Mapas y imágenes generadas
```

## 🎨 Casos de Uso

### Arte Digital
- Creación de piezas únicas para exposiciones
- NFTs basados en geografía
- Ilustraciones para publicaciones urbanas

### Diseño Gráfico
- Fondos abstractos para interfaces
- Patrones decorativos únicos
- Identidad visual basada en ubicación

### Investigación Urbana
- Visualización alternativa de datos geográficos
- Análisis estético de estructuras urbanas
- Comparación artística entre ciudades

## 🔧 Solución de Problemas

### Error: "Dependencies missing"
```bash
pip install -r requirements.txt
```

### Error: "Playwright browser not installed"
```bash
playwright install chromium
```

### Error: "Map generation failed"
- Verifica conexión a internet
- Comprueba que las coordenadas sean válidas
- Revisa que el radio no sea excesivo (max 10km)

### Error: "Export failed"
- Asegúrate de haber generado un mapa primero
- Verifica que Playwright esté instalado correctamente
- Reduce la resolución si la exportación es muy lenta

## 🎯 Próximas Características

- **Animaciones Generativas**: Mapas que evolucionan en tiempo real
- **Editor de Paletas Visual**: Creación de paletas personalizada en la web
- **Estilos Híbridos**: Combinación de múltiples algoritmos
- **Exportación Vectorial**: SVG para impresión de alta calidad
- **API Pública**: Generación de arte desde cualquier aplicación
- **Galería Comunitaria**: Compartir y descubrir creaciones

## 🌟 Contribuir

¿Ideas para mejoras? ¡Contribuye al proyecto!

1. Fork del repositorio
2. Crea una rama para tu feature
3. Implementa y prueba tus cambios
4. Envía un pull request

## 📄 Licencia

Este proyecto mantiene la misma licencia que el proyecto original.

---

**¡Explora el mundo a través del arte generativo!** 🎨🗺️