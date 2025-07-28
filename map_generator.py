"""
Generador de mapas personalizados con datos de OpenStreetMap
"""

import folium
from folium import plugins
from color_palettes import get_color_for_element
from osm_data import OSMDataFetcher

class MapGenerator:
    def __init__(self, palette_name="classic"):
        self.palette_name = palette_name
        self.osm_fetcher = OSMDataFetcher()
    
    def create_map(self, lat, lon, radius_km, zoom_start=15):
        """
        Crea un mapa base centrado en las coordenadas especificadas
        """
        # Crear mapa base con estilo limpio
        m = folium.Map(
            location=[lat, lon],
            zoom_start=zoom_start,
            tiles=None  # No usar tiles por defecto
        )
        
        # Añadir un tile layer personalizado o blanco
        folium.TileLayer(
            tiles='OpenStreetMap',
            attr='OpenStreetMap',
            name='Base',
            overlay=False,
            control=True,
            opacity=0.1  # Muy transparente para que no interfiera
        ).add_to(m)
        
        return m
    
    def add_elements_to_map(self, map_obj, osm_data):
        """
        Añade elementos de OSM al mapa con colores personalizados
        """
        # Añadir landuse y natural primero (fondo)
        self._add_polygons(map_obj, osm_data['landuse'], 'landuse')
        self._add_polygons(map_obj, osm_data['natural'], 'natural')
        
        # Añadir edificios
        self._add_buildings(map_obj, osm_data['buildings'])
        
        # Añadir vías (encima)
        self._add_highways(map_obj, osm_data['highways'])
        self._add_railways(map_obj, osm_data['railways'])
    
    def _add_polygons(self, map_obj, elements, element_type):
        """
        Añade polígonos (áreas) al mapa
        """
        for element in elements:
            if len(element['coordinates']) < 3:
                continue
                
            color = get_color_for_element(
                self.palette_name, 
                element_type, 
                element.get('subtype', 'unknown')
            )
            
            folium.Polygon(
                locations=element['coordinates'],
                popup=f"{element_type}: {element.get('subtype', 'unknown')}",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=1,
                opacity=0.8
            ).add_to(map_obj)
    
    def _add_buildings(self, map_obj, buildings):
        """
        Añade edificios al mapa
        """
        color = get_color_for_element(self.palette_name, 'building')
        
        for building in buildings:
            if len(building['coordinates']) < 3:
                continue
                
            folium.Polygon(
                locations=building['coordinates'],
                popup=f"Edificio",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.8,
                weight=1,
                opacity=0.9
            ).add_to(map_obj)
    
    def _add_highways(self, map_obj, highways):
        """
        Añade carreteras al mapa
        """
        # Definir anchos de línea según tipo de carretera
        width_map = {
            'motorway': 4,
            'trunk': 3.5,
            'primary': 3,
            'secondary': 2.5,
            'tertiary': 2,
            'residential': 1.5,
            'service': 1,
            'footway': 1,
            'cycleway': 1.5
        }
        
        for highway in highways:
            if len(highway['coordinates']) < 2:
                continue
                
            highway_type = highway.get('subtype', 'residential')
            color = get_color_for_element(self.palette_name, 'highway', highway_type)
            width = width_map.get(highway_type, 1.5)
            
            folium.PolyLine(
                locations=highway['coordinates'],
                popup=f"Carretera: {highway_type}",
                color=color,
                weight=width,
                opacity=0.9
            ).add_to(map_obj)
    
    def _add_railways(self, map_obj, railways):
        """
        Añade ferrocarriles al mapa
        """
        color = get_color_for_element(self.palette_name, 'railway')
        
        for railway in railways:
            if len(railway['coordinates']) < 2:
                continue
                
            folium.PolyLine(
                locations=railway['coordinates'],
                popup=f"Ferrocarril: {railway.get('subtype', 'rail')}",
                color=color,
                weight=2,
                opacity=0.9,
                dashArray='5, 5'  # Línea discontinua
            ).add_to(map_obj)
    
    def generate_custom_map(self, location, radius_km, output_file="map.html"):
        """
        Genera un mapa completo con datos de OSM y colores personalizados
        """
        # Obtener coordenadas si se proporciona una dirección
        if isinstance(location, str):
            lat, lon = self.osm_fetcher.get_coordinates_from_address(location)
        else:
            lat, lon = location
        
        print(f"Generando mapa para coordenadas: {lat}, {lon}")
        print(f"Radio: {radius_km} km")
        print(f"Paleta de colores: {self.palette_name}")
        
        # Obtener datos de OSM
        print("Obteniendo datos de OpenStreetMap...")
        osm_data = self.osm_fetcher.fetch_osm_data(lat, lon, radius_km)
        
        # Crear mapa base
        map_obj = self.create_map(lat, lon, radius_km)
        
        # Añadir elementos al mapa
        print("Añadiendo elementos al mapa...")
        self.add_elements_to_map(map_obj, osm_data)
        
        # Añadir marcador central
        folium.Marker(
            [lat, lon], 
            popup="Centro del mapa",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(map_obj)
        
        # Guardar mapa
        map_obj.save(output_file)
        print(f"Mapa guardado como: {output_file}")
        
        return map_obj