"""
Configuration centralisée pour l'application météo
"""

# URLs des APIs
API_BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# Configuration du cache (en secondes)
CACHE_TTL_WEATHER = 900  # 15 minutes
CACHE_TTL_GEOCODING = 3600  # 1 heure
CACHE_TTL_AIR_QUALITY = 3600  # 1 heure

# Villes prédéfinies
PREDEFINED_CITIES = [
    "Casablanca", "Rabat", "Marrakech", "Fès", "Tanger", "Agadir", "Mohammedia",
    "Paris", "London", "New York", "Tokyo", "Dubai", "Berlin",
    "Madrid", "Rome", "Cairo", "Istanbul", "Moscow", "Sydney",
    "Toronto", "Los Angeles", "Singapore", "Mumbai", "Beijing"
]

# Codes météo Open-Meteo
WEATHER_CODES = {
    0: {"desc": "☀️ Ciel dégagé", "category": "sunny"},
    1: {"desc": "🌤️ Principalement dégagé", "category": "sunny"},
    2: {"desc": "⛅ Partiellement nuageux", "category": "cloudy"},
    3: {"desc": "☁️ Couvert", "category": "cloudy"},
    29: {"desc": "🌫️ Brouillard", "category": "misty"},
    30: {"desc": "🌫️ Brouillard givrant", "category": "misty"},
    31: {"desc": "🌦️ Bruine légère", "category": "rainy"},
    32: {"desc": "🌦️ Bruine modérée", "category": "rainy"},
    33: {"desc": "🌦️ Bruine dense", "category": "rainy"},
    34: {"desc": "🌧️ Pluie légère", "category": "rainy"},
    35: {"desc": "🌧️ Pluie modérée", "category": "rainy"},
    36: {"desc": "🌧️ Pluie forte", "category": "rainy"},
    37: {"desc": "🌨️ Neige légère", "category": "snowy"},
    38: {"desc": "🌨️ Neige modérée", "category": "snowy"},
    39: {"desc": "❄️ Neige forte", "category": "snowy"},
    40: {"desc": "🌨️ Grêle", "category": "snowy"},
    41: {"desc": "🌦️ Averses légères", "category": "rainy"},
    42: {"desc": "⛈️ Averses modérées", "category": "rainy"},
    43: {"desc": "⛈️ Averses violentes", "category": "rainy"},
    45: {"desc": "🌫️ Brouillard", "category": "misty"},
    48: {"desc": "🌫️ Brouillard givrant", "category": "misty"},
    51: {"desc": "🌦️ Bruine légère", "category": "rainy"},
    53: {"desc": "🌦️ Bruine modérée", "category": "rainy"},
    55: {"desc": "🌦️ Bruine dense", "category": "rainy"},
    61: {"desc": "🌧️ Pluie légère", "category": "rainy"},
    63: {"desc": "🌧️ Pluie modérée", "category": "rainy"},
    65: {"desc": "🌧️ Pluie forte", "category": "rainy"},
    71: {"desc": "🌨️ Neige légère", "category": "snowy"},
    73: {"desc": "🌨️ Neige modérée", "category": "snowy"},
    75: {"desc": "❄️ Neige forte", "category": "snowy"},
    77: {"desc": "🌨️ Grêle", "category": "snowy"},
    80: {"desc": "🌦️ Averses légères", "category": "rainy"},
    81: {"desc": "⛈️ Averses modérées", "category": "rainy"},
    82: {"desc": "⛈️ Averses violentes", "category": "rainy"},
    85: {"desc": "🌨️ Averses de neige légères", "category": "snowy"},
    86: {"desc": "❄️ Averses de neige fortes", "category": "snowy"},
    95: {"desc": "⚡ Orage", "category": "stormy"},
    96: {"desc": "⚡ Orage avec grêle", "category": "stormy"},
    99: {"desc": "⚡ Orage violent avec grêle", "category": "stormy"}
}

# Thème Premium Unifié
THEME_COLORS = {
    "premium": {
        "primary": "#4facfe", # Bleu ciel vibrant
        "secondary": "#00f2fe", # Cyan vibrant
        "background": "rgba(20, 30, 48, 0.9)", # Bleu nuit profond
        "card": "rgba(255, 255, 255, 0.1)", # Blanc translucide
        "text": "#FFFFFF",
        "text_secondary": "rgba(255, 255, 255, 0.85)"
    }
}

# Gradients pour les backgrounds dynamiques (Plus subtils et élégants)
WEATHER_GRADIENTS = {
    "sunny_day": "linear-gradient(135deg, #fce38a 0%, #f38181 100%)",
    "cloudy_day": "linear-gradient(135deg, #5f72bd 0%, #9b23ea 100%)",
    "rainy_day": "linear-gradient(135deg, #3a6186 0%, #89253e 100%)",
    "snowy_day": "linear-gradient(135deg, #E0EAFC 0%, #CFDEF3 100%)",
    "stormy_day": "linear-gradient(135deg, #232526 0%, #414345 100%)",
    "misty_day": "linear-gradient(135deg, #757f9a 0%, #d7dde8 100%)",
    "clear_night": "linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)",
    "cloudy_night": "linear-gradient(135deg, #141e30 0%, #243b55 100%)",
    "rainy_night": "linear-gradient(135deg, #16222a 0%, #3a6073 100%)",
    "snowy_night": "linear-gradient(135deg, #83a4d4 0%, #b6fbff 100%)",
    "stormy_night": "linear-gradient(135deg, #000000 0%, #434343 100%)",
    "misty_night": "linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%)"
}



# Configuration de l'export PDF
PDF_CONFIG = {
    "page_size": "A4",
    "margin": 50,
    "title_font_size": 24,
    "heading_font_size": 16,
    "body_font_size": 12
}
