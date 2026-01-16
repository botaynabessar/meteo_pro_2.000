"""
Module pour gérer les appels API météo avec gestion d'erreurs robuste
"""

import streamlit as st
import requests
from typing import Optional, Dict, Any
import time
from config import (
    API_BASE_URL, GEOCODING_URL, AIR_QUALITY_URL,
    CACHE_TTL_WEATHER, CACHE_TTL_GEOCODING, CACHE_TTL_AIR_QUALITY
)


class WeatherAPI:
    """Classe pour gérer les appels API météo avec retry et cache"""
    
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        self.base_url = API_BASE_URL
        self.geocoding_url = GEOCODING_URL
        self.air_quality_url = AIR_QUALITY_URL
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def _make_request(self, url: str, params: Dict[str, Any]) -> Optional[Dict]:
        """
        Effectue une requête HTTP avec retry automatique
        
        Args:
            url: URL de l'API
            params: Paramètres de la requête
            
        Returns:
            Données JSON ou None en cas d'erreur
        """
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                st.error("⏱️ Délai d'attente dépassé. Veuillez réessayer.")
                return None
            except requests.exceptions.ConnectionError:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                st.error("🌐 Erreur de connexion. Vérifiez votre connexion Internet.")
                return None
            except requests.exceptions.HTTPError as e:
                st.error(f"❌ Erreur HTTP: {e}")
                return None
            except Exception as e:
                st.error(f"❌ Erreur inattendue: {e}")
                return None
        return None
    
    @st.cache_data(ttl=CACHE_TTL_GEOCODING, show_spinner=False)
    def get_coordinates(_self, city_name: str) -> Optional[Dict[str, Any]]:
        """
        Obtenir les coordonnées d'une ville (avec cache)
        
        Args:
            city_name: Nom de la ville
            
        Returns:
            Dictionnaire avec lat, lon, name, country, timezone
        """
        params = {
            'name': city_name,
            'count': 1,
            'language': 'fr',
            'format': 'json'
        }
        
        data = _self._make_request(_self.geocoding_url, params)
        
        if data and 'results' in data and len(data['results']) > 0:
            result = data['results'][0]
            return {
                'lat': result['latitude'],
                'lon': result['longitude'],
                'name': result['name'],
                'country': result.get('country', 'N/A'),
                'timezone': result.get('timezone', 'auto')
            }
        
        st.warning(f"🔍 Ville '{city_name}' non trouvée.")
        return None
    
    @st.cache_data(ttl=CACHE_TTL_WEATHER, show_spinner=False)
    def get_weather_data(
        _self,
        lat: float,
        lon: float,
        days: int = 7,
        units: str = "metric"
    ) -> Optional[Dict[str, Any]]:
        """
        Récupérer les données météo (avec cache)
        
        Args:
            lat: Latitude
            lon: Longitude
            days: Nombre de jours de prévisions (1-16)
            units: Système d'unités ("metric" ou "imperial")
            
        Returns:
            Données météo complètes
        """
        temp_unit = "celsius" if units == "metric" else "fahrenheit"
        wind_unit = "kmh" if units == "metric" else "mph"
        
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,pressure_msl,cloud_cover,is_day',
            'hourly': 'temperature_2m,precipitation_probability,precipitation,weather_code,wind_speed_10m,relative_humidity_2m,cloud_cover',
            'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,sunrise,sunset,uv_index_max',
            'timezone': 'auto',
            'forecast_days': min(days, 16),  # Max 16 jours
            'temperature_unit': temp_unit,
            'wind_speed_unit': wind_unit
        }
        
        data = _self._make_request(_self.base_url, params)
        
        if data and _self._validate_weather_data(data):
            return data
        
        st.error("❌ Données météo invalides ou incomplètes.")
        return None
    
    @st.cache_data(ttl=CACHE_TTL_AIR_QUALITY, show_spinner=False)
    def get_air_quality(_self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Récupérer l'indice de qualité de l'air
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Données de qualité de l'air
        """
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'european_aqi,us_aqi,uv_index,dust,carbon_monoxide,pm10,pm2_5',
            'timezone': 'auto'
        }
        
        data = _self._make_request(_self.air_quality_url, params)
        return data if data else {'current': {}}
    
    @staticmethod
    def _validate_weather_data(data: Dict[str, Any]) -> bool:
        """
        Valider la structure des données météo
        
        Args:
            data: Données à valider
            
        Returns:
            True si valide, False sinon
        """
        required_keys = ['current', 'daily', 'hourly']
        if not all(key in data for key in required_keys):
            return False
        
        # Vérifier que les données actuelles contiennent les champs essentiels
        current_required = ['temperature_2m', 'weather_code']
        if not all(key in data['current'] for key in current_required):
            return False
        
        return True
    
    def get_multiple_cities_data(
        self,
        city_names: list,
        days: int = 7,
        units: str = "metric"
    ) -> Dict[str, Optional[Dict]]:
        """
        Récupérer les données pour plusieurs villes
        
        Args:
            city_names: Liste des noms de villes
            days: Nombre de jours de prévisions
            units: Système d'unités
            
        Returns:
            Dictionnaire {ville: données_météo}
        """
        results = {}
        
        for city in city_names:
            coords = self.get_coordinates(city)
            if coords:
                weather = self.get_weather_data(
                    coords['lat'],
                    coords['lon'],
                    days,
                    units
                )
                results[city] = {
                    'coords': coords,
                    'weather': weather,
                    'aqi': self.get_air_quality(coords['lat'], coords['lon'])
                }
            else:
                results[city] = None
        
        return results
