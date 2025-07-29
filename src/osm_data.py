"""
Module for fetching OpenStreetMap data
"""

import overpy
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import math

class OSMDataFetcher:
    def __init__(self):
        self.api = overpy.Overpass()
        self.geolocator = Nominatim(user_agent="map_generator")
    
    def get_coordinates_from_address(self, address):
        """
        Convierte una dirección en coordenadas GPS
        """
        try:
            location = self.geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude
            else:
                raise ValueError(f"No se pudo encontrar la dirección: {address}")
        except Exception as e:
            raise ValueError(f"Error al buscar la dirección: {str(e)}")
    
    def calculate_bbox(self, lat, lon, radius_km):
        """
        Calcula el bounding box basado en coordenadas centrales y radio
        """
        # Aproximación: 1 grado de latitud ≈ 111 km
        # 1 grado de longitud ≈ 111 km * cos(latitud)
        
        lat_offset = radius_km / 111.0
        lon_offset = radius_km / (111.0 * math.cos(math.radians(lat)))
        
        south = lat - lat_offset
        north = lat + lat_offset
        west = lon - lon_offset
        east = lon + lon_offset
        
        return south, west, north, east
    
    def fetch_osm_data(self, lat, lon, radius_km):
        """
        Obtiene datos de OpenStreetMap para la ubicación y radio especificados
        """
        south, west, north, east = self.calculate_bbox(lat, lon, radius_km)
        
        # Query para obtener diferentes tipos de elementos
        query = f"""
        [out:json][timeout:60];
        (
          way["highway"]({south},{west},{north},{east});
          way["landuse"]({south},{west},{north},{east});
          way["natural"]({south},{west},{north},{east});
          way["building"]({south},{west},{north},{east});
          way["railway"]({south},{west},{north},{east});
          relation["landuse"]({south},{west},{north},{east});
          relation["natural"]({south},{west},{north},{east});
        );
        (._;>;);
        out geom;
        """
        
        try:
            result = self.api.query(query)
            return self.process_osm_result(result)
        except Exception as e:
            raise Exception(f"Error al obtener datos de OSM: {str(e)}")
    
    def process_osm_result(self, result):
        """
        Procesa el resultado de la consulta OSM y lo organiza por tipos
        """
        processed_data = {
            'highways': [],
            'landuse': [],
            'natural': [],
            'buildings': [],
            'railways': []
        }
        
        # Procesar ways
        for way in result.ways:
            coords = [(float(node.lat), float(node.lon)) for node in way.nodes]
            
            element_data = {
                'coordinates': coords,
                'tags': way.tags
            }
            
            if 'highway' in way.tags:
                element_data['subtype'] = way.tags['highway']
                processed_data['highways'].append(element_data)
            elif 'landuse' in way.tags:
                element_data['subtype'] = way.tags['landuse']
                processed_data['landuse'].append(element_data)
            elif 'natural' in way.tags:
                element_data['subtype'] = way.tags['natural']
                processed_data['natural'].append(element_data)
            elif 'building' in way.tags:
                element_data['subtype'] = way.tags.get('building', 'yes')
                processed_data['buildings'].append(element_data)
            elif 'railway' in way.tags:
                element_data['subtype'] = way.tags['railway']
                processed_data['railways'].append(element_data)
        
        # Procesar relations (para áreas grandes)
        for relation in result.relations:
            if relation.members:
                # Simplificado: tomar solo el primer member que sea un way
                for member in relation.members:
                    if member.role == "outer":
                        try:
                            # Try to get coordinates from the member way directly
                            if hasattr(member, 'ref') and member.ref:
                                # Find the corresponding way in the result
                                way = None
                                for w in result.ways:
                                    if w.id == member.ref:
                                        way = w
                                        break
                                
                                if way and way.nodes:
                                    coords = [(float(node.lat), float(node.lon)) for node in way.nodes]
                                    
                                    element_data = {
                                        'coordinates': coords,
                                        'tags': relation.tags
                                    }
                                    
                                    if 'landuse' in relation.tags:
                                        element_data['subtype'] = relation.tags['landuse']
                                        processed_data['landuse'].append(element_data)
                                    elif 'natural' in relation.tags:
                                        element_data['subtype'] = relation.tags['natural']
                                        processed_data['natural'].append(element_data)
                                    break
                        except Exception:
                            # Skip problematic relations
                            continue
        
        return processed_data