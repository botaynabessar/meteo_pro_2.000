"""
Module pour analyser les données météo et générer des insights
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from config import WEATHER_CODES


class WeatherAnalyzer:
    """Classe pour analyser les données météo"""
    
    @staticmethod
    def calculate_comfort_index(temp: float, humidity: float, units: str = "metric") -> float:
        """
        Calculer l'indice de confort thermique (Heat Index)
        
        Args:
            temp: Température
            humidity: Humidité relative (%)
            units: Système d'unités
            
        Returns:
            Indice de confort
        """
        if units == "imperial":
            # Formule pour Fahrenheit
            hi = 0.5 * (temp + 61.0 + ((temp - 68.0) * 1.2) + (humidity * 0.094))
        else:
            # Formule simplifiée pour Celsius
            hi = temp + 0.5 * (0.1 * temp) + (humidity - 50) * 0.1
        
        return round(hi, 1)
    
    @staticmethod
    def calculate_wind_chill(temp: float, wind_speed: float, units: str = "metric") -> float:
        """
        Calculer le refroidissement éolien
        
        Args:
            temp: Température
            wind_speed: Vitesse du vent
            units: Système d'unités
            
        Returns:
            Température ressentie avec le vent
        """
        if units == "metric":
            # Formule pour Celsius et km/h
            if temp <= 10 and wind_speed >= 4.8:
                wc = 13.12 + 0.6215 * temp - 11.37 * (wind_speed ** 0.16) + 0.3965 * temp * (wind_speed ** 0.16)
                return round(wc, 1)
        else:
            # Formule pour Fahrenheit et mph
            if temp <= 50 and wind_speed >= 3:
                wc = 35.74 + 0.6215 * temp - 35.75 * (wind_speed ** 0.16) + 0.4275 * temp * (wind_speed ** 0.16)
                return round(wc, 1)
        
        return temp
    
    @staticmethod
    def calculate_global_comfort_index(temp: float, humidity: float, wind_speed: float, aqi: float = 0) -> float:
        """
        Calculer un score global de confort (0-100)
        
        Args:
            temp: Température (°C)
            humidity: Humidité (%)
            wind_speed: Vent (km/h)
            aqi: Qualité de l'air
            
        Returns:
            Score sur 100 (100 = Parfait)
        """
        score = 100.0
        
        # Pénalité Température (Idéal entre 18 et 25)
        if temp < 18:
            score -= (18 - temp) * 2
        elif temp > 25:
            score -= (temp - 25) * 2.5
            
        # Pénalité Humidité (Idéal entre 40 et 60)
        if humidity < 40:
            score -= (40 - humidity) * 0.5
        elif humidity > 60:
            score -= (humidity - 60) * 0.5
            
        # Pénalité Vent
        if wind_speed > 20:
            score -= (wind_speed - 20) * 0.5
            
        # Pénalité AQI
        if aqi > 50:
            score -= (aqi - 50) * 0.5
            
        return max(0.0, min(100.0, round(score, 1)))

    @staticmethod
    def get_aqi_description(aqi_value: float) -> str:
        """
        Interpréter l'indice AQI (European)
        
        Args:
            aqi_value: Valeur de l'AQI
            
        Returns:
            Description textuelle
        """
        if aqi_value <= 20:
            return "Excellent 🟢"
        elif aqi_value <= 40:
            return "Bon 🟢"
        elif aqi_value <= 60:
            return "Moyen 🟡"
        elif aqi_value <= 80:
            return "Médiocre 🟠"
        elif aqi_value <= 100:
            return "Mauvais 🔴"
        else:
            return "Très Mauvais 🟣"
    
    @staticmethod
    def get_weather_description(code: int) -> str:
        """
        Traduire les codes météo
        
        Args:
            code: Code météo Open-Meteo
            
        Returns:
            Description textuelle
        """
        return WEATHER_CODES.get(code, {"desc": "🌡️ Conditions variables"})["desc"]
    
    @staticmethod
    def get_weather_category(code: int, is_day: int = 1) -> str:
        """
        Obtenir la catégorie météo détaillée
        
        Args:
            code: Code météo Open-Meteo
            is_day: 1 pour le jour, 0 pour la nuit
            
        Returns:
            Catégorie détaillée (ex: sunny_day, clear_night, rainy_night)
        """
        category = WEATHER_CODES.get(code, {"category": "cloudy"})["category"]
        
        if is_day == 1:
            return f"{category}_day"
        else:
            # Pour la nuit, sunny devient clear
            if category == "sunny":
                return "clear_night"
            return f"{category}_night"
    
    @staticmethod
    def get_recommendations(temp: float, code: int, units: str = "metric") -> List[str]:
        """
        Donner des conseils vestimentaires et d'activité
        
        Args:
            temp: Température
            code: Code météo
            units: Système d'unités
            
        Returns:
            Liste de recommandations
        """
        # Conversion en Celsius pour la logique interne
        temp_c = temp if units == "metric" else (temp - 32) * 5 / 9
        
        advice = []
        
        # Conseils vestimentaires
        if temp_c < 0:
            advice.append("🧥 Vêtements d'hiver indispensables ! Manteau épais, gants et bonnet.")
        elif temp_c < 10:
            advice.append("🧥 Manteau chaud et écharpe recommandés.")
        elif temp_c < 20:
            advice.append("🧥 Une veste ou un pull suffira.")
        elif temp_c < 30:
            advice.append("👕 Tenue légère et confortable.")
        else:
            advice.append("🩳 Vêtements très légers recommandés.")
        
        # Conseils selon la météo
        if code in [61, 63, 65, 80, 81, 82, 95, 96, 99]:
            advice.append("☂️ N'oubliez pas votre parapluie !")
        elif code in [71, 73, 75, 85, 86]:
            advice.append("❄️ Attention à la neige ! Conduisez prudemment.")
        elif code in [0, 1]:
            advice.append("🕶️ Lunettes de soleil conseillées.")
        
        # Conseils de santé
        if temp_c > 30:
            advice.append("💧 Pensez à bien vous hydrater !")
        if temp_c < 0:
            advice.append("🧊 Attention au risque de gelures.")
        
        return advice
    
    @staticmethod
    def analyze_daily_data(daily_data: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, float]]:
        """
        Analyser les données quotidiennes
        
        Args:
            daily_data: Données quotidiennes de l'API
            
        Returns:
            Tuple (DataFrame, statistiques)
        """
        df = pd.DataFrame({
            'Date': pd.to_datetime(daily_data['time']),
            'Temp_Max': daily_data['temperature_2m_max'],
            'Temp_Min': daily_data['temperature_2m_min'],
            'Précipitations': daily_data['precipitation_sum'],
            'Prob_Pluie': daily_data.get('precipitation_probability_max', [0] * len(daily_data['time'])),
            'Vent_Max': daily_data['wind_speed_10m_max'],
            'Code_Météo': daily_data['weather_code'],
            'UV_Max': daily_data.get('uv_index_max', [0] * len(daily_data['time']))
        })
        
        # Calculs statistiques
        stats = {
            'temp_moyenne': df['Temp_Max'].mean(),
            'temp_max_periode': df['Temp_Max'].max(),
            'temp_min_periode': df['Temp_Min'].min(),
            'total_precipitations': df['Précipitations'].sum(),
            'jours_pluie': (df['Précipitations'] > 0).sum(),
            'vent_moyen': df['Vent_Max'].mean(),
            'vent_max': df['Vent_Max'].max(),
            'uv_max': df['UV_Max'].max()
        }
        
        return df, stats
    

    
    @staticmethod
    def get_trend_analysis(df: pd.DataFrame) -> Dict[str, str]:
        """
        Analyser les tendances météo
        
        Args:
            df: DataFrame avec les données quotidiennes
            
        Returns:
            Dictionnaire de tendances
        """
        trends = {}
        
        # Tendance température
        temp_diff = df['Temp_Max'].iloc[-1] - df['Temp_Max'].iloc[0]
        if temp_diff > 3:
            trends['temperature'] = "📈 Tendance au réchauffement"
        elif temp_diff < -3:
            trends['temperature'] = "📉 Tendance au refroidissement"
        else:
            trends['temperature'] = "➡️ Température stable"
        
        # Tendance précipitations
        precip_first_half = df['Précipitations'].iloc[:len(df)//2].sum()
        precip_second_half = df['Précipitations'].iloc[len(df)//2:].sum()
        if precip_second_half > precip_first_half * 1.5:
            trends['precipitation'] = "🌧️ Augmentation des précipitations"
        elif precip_second_half < precip_first_half * 0.5:
            trends['precipitation'] = "☀️ Diminution des précipitations"
        else:
            trends['precipitation'] = "➡️ Précipitations stables"
        
        return trends
