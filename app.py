"""
🌦️ APPLICATION MÉTÉO PROFESSIONNELLE
Reconstruction complète avec interface moderne et fonctionnalités avancées

Date: 2026-01-02
Version: 2.0
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import importlib

# Import des modules personnalisés
from config import PREDEFINED_CITIES
from weather_api import WeatherAPI
from weather_analyzer import WeatherAnalyzer
import weather_analyzer
importlib.reload(weather_analyzer)
from session_manager import SessionManager
from ui_components import (
    inject_custom_css, create_hero_section, create_metric_card,
    create_forecast_card
)
from charts import (
    create_temperature_chart, create_precipitation_chart, create_wind_chart,
    create_hourly_forecast, create_correlation_matrix,
    create_uv_gauge
)
from export_utils import export_to_csv, export_to_json, export_to_pdf

# Configuration de la page
st.set_page_config(
    page_title="🌦️ Météo",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Fonction principale de l'application"""
    
    # Initialisation de la session
    SessionManager.initialize()
    
    # Récupération du thème
    theme = 'premium'  # Theme unique premium
    
    # ==================== SIDEBAR ====================
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>🌐 NAVIGATION</h2>", unsafe_allow_html=True)
        st.divider()
        
        # Sélection de ville
        st.markdown("### 🏙️ Recherche")
        city_name = st.selectbox(
            "Choisir une ville:",
            PREDEFINED_CITIES,
            index=0
        )
        
        # Configuration
        st.markdown("### ⚙️ Configuration")
        
        units = st.segmented_control(
            "Unités:",
            options=["metric", "imperial"],
            format_func=lambda x: "Métrique (°C)" if x == "metric" else "Impérial (°F)",
            default="metric"
        )
        
        periode = st.select_slider(
            "Prévisions:",
            options=[1, 3, 5, 7, 10, 14],
            value=7,
            format_func=lambda x: f"{x} jours"
        )
        
        st.divider()
        
        # Mode Test (Debug)
        st.markdown("### 🔧 Mode Test")
        test_mode = st.checkbox("Activer test visuel", value=False, help="Permet de tester manuellement chaque arrière-plan")
        selected_test_category = "sunny_day"
        if test_mode:
            from config import WEATHER_GRADIENTS
            selected_test_category = st.selectbox(
                "Choisir un scénario:",
                options=list(WEATHER_GRADIENTS.keys())
            )
        
        rechercher = st.button("🔍 RECHERCHER", type="primary", use_container_width=True)

    # Déterminer la catégorie météo pour le fond
    weather_category = 'sunny_day'
    if st.session_state.weather_data:
        current = st.session_state.weather_data['current']
        code = current['weather_code']
        is_day = current.get('is_day', 1)
        analyzer = WeatherAnalyzer()
        weather_category = analyzer.get_weather_category(code, is_day)
    
    # Override weather category if test mode is enabled
    if test_mode:
        weather_category = selected_test_category
    
    # Injection du CSS
    inject_custom_css(theme, weather_category)
    
    # ==================== RÉCUPÉRATION DES DONNÉES ====================
    if rechercher or st.session_state.weather_data is None:
        with st.spinner(f"🔍 Recherche des données pour {city_name}..."):
            api = WeatherAPI()
            coords = api.get_coordinates(city_name)
            
            if coords:
                weather_data = api.get_weather_data(coords['lat'], coords['lon'], periode, units)
                aqi_data = api.get_air_quality(coords['lat'], coords['lon'])
                
                if weather_data:
                    st.session_state.weather_data = weather_data
                    st.session_state.aqi_data = aqi_data
                    st.session_state.city_info = coords
                    st.session_state.current_units = units
                    
                    
                    st.rerun()
    
    # ==================== AFFICHAGE DES DONNÉES ====================
    if st.session_state.weather_data:
        weather_data = st.session_state.weather_data
        city_info = st.session_state.city_info
        aqi_data = st.session_state.aqi_data
        analyzer = WeatherAnalyzer()
        current = weather_data['current']
        daily = weather_data['daily']
        hourly = weather_data['hourly']
        
        u_temp = "°C" if units == "metric" else "°F"
        u_wind = "km/h" if units == "metric" else "mph"
        
        # HERO SECTION
        create_hero_section(
            city_info['name'],
            current['temperature_2m'],
            analyzer.get_weather_description(current['weather_code']),
            u_temp,
            current.get('precipitation', 0.0)
        )
        
        # ONGLETS
        # ONGLETS
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Tableau de Bord",
            "🕒 Prévisions Horaires",
            "📈 Analyses",
            "📋 Données",
            "🏙️ Comparateur",
            "💾 Export"
        ])

        
        # ==================== TAB 1: TABLEAU DE BORD ====================
        with tab1:
            st.markdown("<div class='animate-fadeIn'>", unsafe_allow_html=True)
            
            # Métriques principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                create_metric_card(
                    "🌡️",
                    "Température",
                    f"{round(current['temperature_2m'])}{u_temp}",
                    f"Ressenti: {round(current['apparent_temperature'])}{u_temp}"
                )
            
            with col2:
                create_metric_card(
                    "💧",
                    "Humidité",
                    f"{current['relative_humidity_2m']}%",
                    f"Pluie: {current.get('precipitation', 0.0)} mm"
                )
            
            with col3:
                create_metric_card(
                    "💨",
                    "Vent",
                    f"{round(current['wind_speed_10m'])} {u_wind}"
                )
            
            with col4:
                create_metric_card(
                    "🔽",
                    "Pression",
                    f"{round(current['pressure_msl'])} hPa"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Qualité de l'air et cycles solaires
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h4 style='color: white; font-weight: 500;'>🍃 Qualité de l'Air</h4>", unsafe_allow_html=True)
                aqi_val = aqi_data.get('current', {}).get('european_aqi', 0)
                st.markdown(f"""
                <div class="glass-card" style="height: 200px; display: flex; flex-direction: column; justify-content: center;">
                    <p style="margin:0; opacity:0.8;">Indice AQI Européen</p>
                    <h3 style="margin: 10px 0;">{aqi_val} - {analyzer.get_aqi_description(aqi_val)}</h3>
                    <p style="margin:0; opacity:0.7;">☀️ Indice UV: {aqi_data.get('current', {}).get('uv_index', 0)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("<h4 style='color: white; font-weight: 500;'>🌅 Cycles Solaires</h4>", unsafe_allow_html=True)
                sunrise = daily['sunrise'][0].split('T')[1]
                sunset = daily['sunset'][0].split('T')[1]
                st.markdown(f"""
                <div class="glass-card" style="height: 200px; display: flex; align-items: center; justify-content: space-around;">
                    <div style="text-align: center;">
                        <p style="font-size: 2.5rem; margin:0;">🌅</p>
                        <p style="margin:0; font-weight: 600; font-size: 1.3rem;">{sunrise}</p>
                        <p style="font-size: 0.9rem; margin:0; opacity:0.7;">Lever</p>
                    </div>
                    <div style="text-align: center;">
                        <p style="font-size: 2.5rem; margin:0;">🌇</p>
                        <p style="margin:0; font-weight: 600; font-size: 1.3rem;">{sunset}</p>
                        <p style="font-size: 0.9rem; margin:0; opacity:0.7;">Coucher</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Recommandations
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: white; font-weight: 500;'>💡 Conseils du jour</h4>", unsafe_allow_html=True)
            recommendations = analyzer.get_recommendations(
                current['temperature_2m'],
                current['weather_code'],
                units
            )
            for rec in recommendations:
                st.markdown(f'<div class="recommendation-card">💡 {rec}</div>', unsafe_allow_html=True)
            
            # Prévisions quotidiennes
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: white; font-weight: 500; text-align: center;'>📅 Prévisions Quotidiennes</h3>", unsafe_allow_html=True)
            
            df, stats = analyzer.analyze_daily_data(daily)
            
            cols = st.columns(min(7, len(df)))
            for idx, (_, row) in enumerate(df.iterrows()):
                if idx < len(cols):
                    with cols[idx]:
                        create_forecast_card(
                            row['Date'].strftime('%d/%m'),
                            row['Date'].strftime('%a'),
                            row['Temp_Max'],
                            row['Temp_Min'],
                            row['Précipitations']
                        )
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # ==================== TAB 2: PRÉVISIONS HORAIRES ====================
        with tab2:
            st.markdown("<h3 style='text-align: center;'>🕒 Prévisions sur 24 heures</h3>", unsafe_allow_html=True)
            
            fig_hourly = create_hourly_forecast(hourly, 24, theme)
            st.plotly_chart(fig_hourly, use_container_width=True)
            
            # Tableau détaillé
            with st.expander("📋 Voir les détails horaires"):
                hourly_df = pd.DataFrame({
                    'Heure': pd.to_datetime(hourly['time'][:24]).strftime('%H:%M'),
                    'Temp (°C)': hourly['temperature_2m'][:24],
                    'Pluie (mm)': hourly['precipitation'][:24],
                    'Prob. Pluie (%)': hourly['precipitation_probability'][:24],
                    'Vent (km/h)': hourly['wind_speed_10m'][:24],
                    'Humidité (%)': hourly['relative_humidity_2m'][:24]
                })
                st.dataframe(hourly_df, use_container_width=True, hide_index=True)
        
        # ==================== TAB 3: ANALYSES ====================
        with tab3:
            st.markdown("<h3 style='text-align: center;'>📈 Analyses Détaillées</h3>", unsafe_allow_html=True)
            
            # Statistiques
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="margin:0 0 15px 0;">📈 Période</h4>
                    <p style="margin:5px 0;">🌡️ Moyenne: <b>{stats['temp_moyenne']:.1f}°C</b></p>
                    <p style="margin:5px 0;">🔥 Maximum: <b>{stats['temp_max_periode']:.1f}°C</b></p>
                    <p style="margin:5px 0;">❄️ Minimum: <b>{stats['temp_min_periode']:.1f}°C</b></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="margin:0 0 15px 0;">🌧️ Précipitations & Vent</h4>
                    <p style="margin:5px 0;">💧 Total: <b>{stats['total_precipitations']:.1f} mm</b></p>
                    <p style="margin:5px 0;">☔ Jours: <b>{stats['jours_pluie']}</b></p>
                    <p style="margin:5px 0;">💨 Vent moy.: <b>{stats['vent_moyen']:.1f} km/h</b></p>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # Graphiques
            st.plotly_chart(create_temperature_chart(df, theme), use_container_width=True)
            st.plotly_chart(create_precipitation_chart(df, theme), use_container_width=True)
            st.plotly_chart(create_wind_chart(df, theme), use_container_width=True)
            
            # Matrice de corrélation
            st.plotly_chart(create_correlation_matrix(df, theme), use_container_width=True)
        
        # ==================== TAB 4: DONNÉES ====================
        with tab4:
            st.markdown("<h3 style='text-align: center;'>📋 Données de la Période</h3>", unsafe_allow_html=True)
            
            df_display = df.copy()
            df_display['Date'] = df_display['Date'].dt.strftime('%d/%m/%Y')
            df_display['Météo'] = df_display['Code_Météo'].apply(analyzer.get_weather_description)
            df_display = df_display.drop('Code_Météo', axis=1)
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # ==================== TAB 5: COMPARATEUR ====================
        with tab5:
            st.markdown("<h3 style='text-align: center;'>🏙️ Comparateur Multi-Villes</h3>", unsafe_allow_html=True)
            
            # Sélection des villes (Toutes les villes disponibles)
            comp_options = PREDEFINED_CITIES
            
            # Filtre les valeurs par défaut pour s'assurer qu'elles sont dans les options
            default_comp = [c for c in ["Casablanca", "Mohammedia"] if c in comp_options]
            
            cities_to_compare = st.multiselect(
                "Sélectionnez les villes à comparer (Max 4):",
                options=comp_options,
                default=default_comp[:2],
                max_selections=4
            )
            
            if st.button("🚀 Lancer la comparaison", type="primary", use_container_width=True):
                if cities_to_compare:
                    cols = st.columns(len(cities_to_compare))
                    
                    scores = []
                    
                    for idx, city in enumerate(cities_to_compare):
                        with cols[idx]:
                                    # Récupération données pour chaque ville
                            comp_api = WeatherAPI()
                            comp_coords = comp_api.get_coordinates(city)
                            if comp_coords:
                                comp_data = comp_api.get_weather_data(comp_coords['lat'], comp_coords['lon'], 1, units)
                                comp_aqi = comp_api.get_air_quality(comp_coords['lat'], comp_coords['lon'])
                                
                                if comp_data:
                                    c_current = comp_data['current']
                                    c_aqi_val = comp_aqi.get('current', {}).get('european_aqi', 0)
                                    
                                    # Calcul Score Confort
                                    c_temp = c_current['temperature_2m']
                                    c_hum = c_current['relative_humidity_2m']
                                    c_wind = c_current['wind_speed_10m']
                                    c_precip = c_current.get('precipitation', 0.0)
                                    
                                    comfort_score = analyzer.calculate_global_comfort_index(c_temp, c_hum, c_wind, c_aqi_val)
                                    scores.append((city, comfort_score))
                                    
                                    # Gestion affichage pluie
                                    weather_cat = analyzer.get_weather_category(c_current['weather_code'])
                                    is_rainy = "rainy" in weather_cat or "stormy" in weather_cat or c_precip > 0

                                    if is_rainy:
                                        label = "🌧️ Pluie" if "rainy" in weather_cat else "⛈️ Orage" if "stormy" in weather_cat else "💧 Précip."
                                        precip_html = f"<p style='color: #4fc3f7; font-weight: bold;'>{label}: {c_precip} mm</p>"
                                    else:
                                        precip_html = "<p style='opacity: 0.6;'>☀️ Pas de pluie</p>"

                                    # Affichage Carte
                                    st.markdown(f"""
                                    <div class="glass-card" style="text-align: center;">
                                        <h4>{city}</h4>
                                        <div style="font-size: 2rem; margin: 10px 0;">{analyzer.get_weather_description(c_current['weather_code']).split(' ')[0]}</div>
                                        <p style="font-size: 1.5rem; font-weight: bold;">{c_temp} {u_temp}</p>
                                        <hr style="opacity: 0.2;">
                                        <div style="text-align: left; font-size: 0.9rem;">
                                            <p>💧 Humidité: <b>{c_hum}%</b></p>
                                            <p>💨 Vent: <b>{c_wind} {u_wind}</b></p>
                                            <p>🍃 AQI: <b>{c_aqi_val}</b></p>
                                            {precip_html}
                                        </div>
                                        <div style="margin-top: 10px; padding: 5px; background: rgba(255,255,255,0.1); border-radius: 10px;">
                                            <small>Score Confort</small><br>
                                            <b style="font-size: 1.2rem; color: {'#4caf50' if comfort_score > 80 else '#ff9800' if comfort_score > 50 else '#f44336'};">{comfort_score}/100</b>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)

                    # Gagnant avec Style "Recommendation Card"
                    if scores:
                        best_city = max(scores, key=lambda x: x[1])
                        st.markdown(f"""
                        <div>
                        <h3 style="margin: 0 0 10px 0;">🏆 Verdict</h3>
                        <div class="recommendation-card" style="margin-top: 2rem; background: rgba(30, 136, 229, 0.2); border-left: 5px solid #2196f3;">
                            <p style="font-size: 1rem; margin: 0;">
                                La ville la plus agréable actuellement est <b>{best_city[0]}</b> avec un score de confort de <b>{best_city[1]}/100</b>.
                            </p>
                        </div>
                        </div>
                        """, unsafe_allow_html=True)

        
        # ==================== TAB 6: EXPORT ====================
        with tab6:
            st.markdown("<h3 style='text-align: center;'>💾 Exportation des Données</h3>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("<h4 style='text-align: center;'>📄 CSV</h4>", unsafe_allow_html=True)
                st.write("<p style='text-align: center;'>Tableau de données complet</p>", unsafe_allow_html=True)
                
                csv_data, csv_filename = export_to_csv(df, city_info['name'])
                st.download_button(
                    label="⬇️ Télécharger CSV",
                    data=csv_data,
                    file_name=csv_filename,
                    mime="text/csv",
                    type="primary",
                    use_container_width=True
                )
            
            with col2:
                st.markdown("<h4 style='text-align: center;'>📦 JSON</h4>", unsafe_allow_html=True)
                st.write("<p style='text-align: center;'>Données complètes + stats</p>", unsafe_allow_html=True)
                
                json_data, json_filename = export_to_json(weather_data, city_info, stats)
                st.download_button(
                    label="⬇️ Télécharger JSON",
                    data=json_data,
                    file_name=json_filename,
                    mime="application/json",
                    type="primary",
                    use_container_width=True
                )
            
            with col3:
                st.markdown("<h4 style='text-align: center;'>📄 PDF</h4>", unsafe_allow_html=True)
                st.write("<p style='text-align: center;'>Rapport complet</p>", unsafe_allow_html=True)
                
                pdf_buffer, result = export_to_pdf(city_info, current, df, stats)
                
                if pdf_buffer:
                    st.download_button(
                        label="⬇️ Télécharger PDF",
                        data=pdf_buffer,
                        file_name=result,
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
                else:
                    if result and "manquant" in result:
                        st.warning("📦 Installez `reportlab` pour l'export PDF:\n```pip install reportlab```")
                    else:
                        st.error(f"❌ {result}")
    
    else:
        # Message d'accueil
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem;">
            <h1 style="font-size: 4rem; margin-bottom: 1rem;">🌦️</h1>
            <h2>Bienvenue sur Météo Pro 2.0</h2>
            <p style="font-size: 1.2rem; opacity: 0.8; margin-top: 1rem;">
                Sélectionnez une ville dans la barre latérale pour commencer
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.divider()



if __name__ == "__main__":
    main()