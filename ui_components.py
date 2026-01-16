"""
Composants UI réutilisables pour l'application météo
"""

import streamlit as st
import base64
import os
from typing import Dict, Any
from config import THEME_COLORS, WEATHER_GRADIENTS
from weather_analyzer import WeatherAnalyzer

def get_base64_image(image_path):
    """Encoder une image en Base64 pour l'intégrer au CSS"""
    if not image_path or not os.path.exists(image_path):
        return None
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    except Exception:
        return None

# Mapping weather categories to local image paths for Base64 encoding
WEATHER_IMAGES = {
    "sunny_day": "image/sunny_weather_1767458011348.png",
    "cloudy_day": "image/cloudy_weather_1767458030393.png",
    "rainy_day": "image/rainy_weather_bg_1766842963940.png",
    "snowy_day": "image/snowy_day_background_1768336972914.png",
    "stormy_day": "image/stormy_weather_day_1768336242740.png",
    "misty_day": "image/misty_weather_day_1768336255667.png",
    "clear_night": "image/clear_night_weather_1768336272837.png",
    "cloudy_night": "image/cloudy_night_weather_1768336287659.png",
    "snowy_night": "image/snowy_night_background_1768336972914.png",
    "stormy_night": "image/stormy_weather_night_1768336242740.png",
    "misty_night": "image/misty_weather_night_1768336255667.png",
}



def inject_custom_css(theme: str = 'premium', weather_category: str = 'sunny_day'):
    """
    Injecter le CSS personnalisé avec glassmorphism et animations
    
    Args:
        theme: 'premium' (unifié)
        weather_category: Catégorie météo pour le fond
    """
    # Force premium theme
    theme = 'premium'
    colors = THEME_COLORS[theme]
    gradient = WEATHER_GRADIENTS.get(weather_category, WEATHER_GRADIENTS['sunny_day'])
    
    # Récupérer l'image en Base64
    image_path = WEATHER_IMAGES.get(weather_category)
    
    # Fallback pour les images de nuit manquantes : réutilisation des images de jour
    is_night_fallback = False
    if not image_path and weather_category.endswith('_night'):
        day_category = weather_category.replace('_night', '_day')
        image_path = WEATHER_IMAGES.get(day_category)
        if image_path:
            is_night_fallback = True
            
    base64_image = get_base64_image(image_path) if image_path else None
    
    # Construction du style de fond
    if base64_image:
        # Si c'est un fallback nuit, on assombrit l'image
        if is_night_fallback:
            bg_style = f"linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{base64_image}') no-repeat center center fixed"
        else:
            bg_style = f"url('{base64_image}') no-repeat center center fixed"
    else:
        bg_style = gradient

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {{
            font-family: 'Poppins', sans-serif;
        }}

        .stApp {{
            background: {bg_style};
            background-size: cover;
        }}

        /* Overlay principal subtil pour unifier le contraste */
        .main {{
            background: linear-gradient(to bottom, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.6) 100%);
            min-height: 100vh;
        }}

        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .animate-fadeIn {{
            animation: fadeIn 0.8s ease-out forwards;
        }}

        /* Glassmorphism Premium Unifié */
        .glass-card {{
            background: {colors['card']};
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 24px;
            padding: 2rem;
            color: {colors['text']};
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            margin-bottom: 2.5rem;
        }}

        .glass-card:hover {{
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-5px);
            border-color: rgba(255, 255, 255, 0.4);
            box-shadow: 0 15px 40px 0 rgba(0, 0, 0, 0.3);
        }}

        /* Hero Section */
        .hero-container {{
            text-align: center;
            padding: 3.5rem 1rem;
            margin-bottom: 6rem;
            border-radius: 40px;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            animation: fadeIn 1.2s ease-out;
        }}

        .hero-title {{
            font-size: 4.5rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: -1px;
            color: {colors['text']} !important;
            text-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}

        .hero-temp {{
            color: {colors['text']} !important;
            font-size: 7rem;
            font-weight: 200;
            margin: -15px 0;
            text-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}

        /* Tabs Stylisés */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(40px);
            -webkit-backdrop-filter: blur(40px);
            padding: 10px 15px;
            border-radius: 50px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin-bottom: 6rem;
            justify-content: center;
            flex-wrap: wrap;
        }}

        .stTabs [data-baseweb="tab"] {{
            height: 45px;
            padding: 0 15px !important;
            background-color: transparent !important;
            border: none !important;
            color: rgba(255, 255, 255, 0.8) !important;
            font-weight: 500 !important;
            border-radius: 25px !important;
            font-size: 0.9rem;
            flex-grow: 1;
            max-width: fit-content;
        }}

        .stTabs [aria-selected="true"] {{
            background-color: rgba(255, 255, 255, 0.4) !important;
            color: white !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}

        .recommendation-card {{
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border-radius: 15px;
            padding: 15px;
            border-left: 5px solid {colors['primary']};
            margin-bottom: 10px;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}

        /* Sidebar Glass */
        [data-testid="stSidebar"] {{
            background-color: rgba(10, 20, 35, 0.85);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
        }}
        
        [data-testid="stSidebar"] * {{
            color: rgba(255, 255, 255, 0.9) !important;
        }}

        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 6px;
        }}
        ::-webkit-scrollbar-thumb {{
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
        }}

        /* Text shadows defaults */
        div.stMarkdown p, div.stMarkdown h1, div.stMarkdown h2, div.stMarkdown h3, 
        .stMetricValue, .stMetricLabel {{
            color: {colors['text']} !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.4);
        }}
    </style>
    """, unsafe_allow_html=True)


def create_hero_section(city_name: str, temp: float, weather_desc: str, unit: str = "°C", precipitation: float = 0.0):
    """
    Créer la section hero avec la température et les précipitations
    
    Args:
        city_name: Nom de la ville
        temp: Température
        weather_desc: Description météo
        unit: Unité de température
        precipitation: Précipitations actuelles (mm)
    """
    precip_html = f'<p style="font-size: 1.2rem; margin-top: 10px; opacity: 0.9;">💧 Précipitations: {precipitation} mm</p>' if precipitation > 0 else ""
    
    st.markdown(f"""
    <div class="hero-container animate-fadeIn">
        <p style="font-size: 1rem; opacity: 0.8; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 10px;">MÉTÉO ACTUELLE</p>
        <h1 class="hero-title">{city_name}</h1>
        <p class="hero-temp">{round(temp)}{unit}</p>
        <p style="font-size: 1.5rem; font-weight: 400; opacity: 0.9; margin-top: 5px;">{weather_desc}</p>
        {precip_html}
    </div>
    """, unsafe_allow_html=True)


def create_metric_card(icon: str, label: str, value: str, extra: str = ""):
    """
    Créer une carte de métrique glassmorphism avec hauteur fixe pour alignement parfait
    """
    extra_html = f"<p style='margin: 5px 0; font-size: 0.85em; opacity: 0.7;'>{extra}</p>" if extra else "<div style='height:20px;'></div>"
    
    st.markdown(f"""
    <div class="glass-card" style="height: 180px; display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 20px; text-align: center; padding: 1rem;">
        <p style="margin:0; opacity:0.8; font-size: 0.9rem; letter-spacing: 1px; text-transform: uppercase;">{icon} {label}</p>
        <h2 style="margin: 10px 0; font-weight: 600;">{value}</h2>
        {extra_html}
    </div>
    """, unsafe_allow_html=True)


def create_forecast_card(date_str: str, day_str: str, temp_max: float, temp_min: float, precip: float, temp_color: str = "blue"):
    """
    Créer une carte de prévision quotidienne
    """
    # Gradient subtil pour les cartes de prévision
    bg_style = "background: rgba(255, 255, 255, 0.08);"
    if temp_max > 30:
        bg_style = "background: linear-gradient(135deg, rgba(255, 100, 100, 0.15), rgba(255, 255, 255, 0.05));"
    elif precip > 5:
        bg_style = "background: linear-gradient(135deg, rgba(100, 150, 255, 0.15), rgba(255, 255, 255, 0.05));"
    
    st.markdown(f"""
    <div class="glass-card" style='{bg_style} text-align: center; padding: 15px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.15);'>
        <h4 style='margin:0; font-size: 1.1rem;'>{date_str}</h4>
        <p style='font-size: 0.85em; opacity: 0.7; text-transform: uppercase; letter-spacing: 1px;'>{day_str}</p>
        <div style="margin: 10px 0;">
            <span style="font-size: 1.4rem; font-weight: 600;">{round(temp_max)}°</span>
            <span style="font-size: 1rem; opacity: 0.6; margin-left: 5px;">{round(temp_min)}°</span>
        </div>
        <p style='font-size: 0.8em; margin-top: 5px; opacity: 0.8;'>💧 {precip}mm</p>
    </div>
    """, unsafe_allow_html=True)



