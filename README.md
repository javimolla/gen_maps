# Generador de Mapas Personalizados

Una aplicación para generar mapas personalizados con datos de OpenStreetMap y paletas de colores predefinidas.

## Características

- **Búsqueda por dirección o coordenadas GPS**
- **Radio configurable** para el área del mapa
- **4 paletas de colores predefinidas**: classic, ocean, sunset, forest
- **Elementos de mapa soportados**: calles, parques, ríos, edificios, ferrocarriles
- **Salida en HTML** lista para abrir en navegador

## Instalación

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Comandos básicos

```bash
# Generar mapa por dirección
python3 main.py --address "Plaza Mayor, Madrid" --radius 1 --palette classic

# Generar mapa por coordenadas
python3 main.py --coords 40.4168 -3.7038 --radius 2 --palette ocean --output madrid_ocean.html

# Ver paletas disponibles
python3 main.py --list-palettes
```

### Parámetros

- `--address, -a`: Dirección a buscar
- `--coords, -c`: Coordenadas GPS (latitud longitud)
- `--radius, -r`: Radio en kilómetros (por defecto: 1.0 km)
- `--palette, -p`: Paleta de colores (classic, ocean, sunset, forest)
- `--output, -o`: Archivo de salida (por defecto: map.html)
- `--list-palettes`: Mostrar paletas disponibles

### Paletas de colores

- **classic**: Colores tradicionales de mapas
- **ocean**: Tonos azules y verdes marinos
- **sunset**: Colores cálidos naranjas y amarillos
- **forest**: Tonos verdes naturales

## Estructura del proyecto

```
gen_maps/
├── main.py              # Interfaz de línea de comandos
├── map_generator.py     # Generador principal de mapas
├── osm_data.py         # Obtención de datos de OpenStreetMap
├── color_palettes.py   # Definición de paletas de colores
├── requirements.txt    # Dependencias de Python
└── README.md          # Este archivo
```

## Desarrollo futuro

Esta versión CLI está diseñada para migrar fácilmente a una aplicación web con:
- Interfaz visual para seleccionar ubicaciones
- Preview en tiempo real de paletas de colores
- Exportación a diferentes formatos
- Editor de paletas personalizado