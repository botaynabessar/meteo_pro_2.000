"""
Fonctions pour créer des graphiques Plotly interactifs
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any, List


def get_chart_template(theme: str = 'dark') -> str:
    """
    Obtenir le template Plotly selon le thème
    
    Args:
        theme: 'dark' ou 'light'
        
    Returns:
        Nom du template
    """
    return 'plotly_dark' if theme == 'dark' else 'plotly_white'


def create_temperature_chart(df: pd.DataFrame, theme: str = 'dark') -> go.Figure:
    """
    Créer un graphique de température
    
    Args:
        df: DataFrame avec colonnes Date, Temp_Max, Temp_Min
        theme: Thème du graphique
        
    Returns:
        Figure Plotly
    """
    fig = go.Figure()
    
    # Ligne température max
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Temp_Max'],
        name='Température Max',
        mode='lines+markers',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=8),
        fill='tonexty'
    ))
    
    # Ligne température min
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Temp_Min'],
        name='Température Min',
        mode='lines+markers',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='🌡️ Évolution des Températures',
        xaxis_title='Date',
        yaxis_title='Température (°C)',
        template=get_chart_template(theme),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white' if theme == 'dark' else 'black'),
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )
    
    return fig


def create_precipitation_chart(df: pd.DataFrame, theme: str = 'dark') -> go.Figure:
    """
    Créer un graphique de précipitations
    
    Args:
        df: DataFrame avec colonnes Date, Précipitations
        theme: Thème du graphique
        
    Returns:
        Figure Plotly
    """
    fig = px.bar(
        df,
        x='Date',
        y='Précipitations',
        title='💧 Précipitations Quotidiennes',
        template=get_chart_template(theme)
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white' if theme == 'dark' else 'black'),
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis_title='Précipitations (mm)'
    )
    
    fig.update_traces(marker_color='#1E88E5')
    
    return fig


def create_wind_chart(df: pd.DataFrame, theme: str = 'dark') -> go.Figure:
    """
    Créer un graphique de vent
    
    Args:
        df: DataFrame avec colonnes Date, Vent_Max
        theme: Thème du graphique
        
    Returns:
        Figure Plotly
    """
    fig = px.area(
        df,
        x='Date',
        y='Vent_Max',
        title='💨 Vitesse du Vent',
        template=get_chart_template(theme)
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white' if theme == 'dark' else 'black'),
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis_title='Vitesse (km/h)'
    )
    
    fig.update_traces(line_color='#00C853', fillcolor='rgba(0, 200, 83, 0.2)')
    
    return fig


def create_hourly_forecast(hourly_data: Dict[str, Any], hours: int = 24, theme: str = 'dark') -> go.Figure:
    """
    Créer un graphique des prévisions horaires
    
    Args:
        hourly_data: Données horaires de l'API
        hours: Nombre d'heures à afficher
        theme: Thème du graphique
        
    Returns:
        Figure Plotly
    """
    df = pd.DataFrame({
        'Heure': pd.to_datetime(hourly_data['time'][:hours]),
        'Température': hourly_data['temperature_2m'][:hours],
        'Précipitations': hourly_data['precipitation'][:hours],
        'Prob_Pluie': hourly_data['precipitation_probability'][:hours]
    })
    
    df['Heure_Format'] = df['Heure'].dt.strftime('%H:%M')
    
    fig = go.Figure()
    
    # Température
    fig.add_trace(go.Scatter(
        x=df['Heure_Format'],
        y=df['Température'],
        name='Température',
        mode='lines+markers',
        line=dict(color='#FF6B6B', width=2),
        yaxis='y'
    ))
    
    # Probabilité de pluie
    fig.add_trace(go.Bar(
        x=df['Heure_Format'],
        y=df['Prob_Pluie'],
        name='Probabilité de pluie (%)',
        marker_color='#1E88E5',
        opacity=0.6,
        yaxis='y2'
    ))
    
    # Volume de pluie
    fig.add_trace(go.Bar(
        x=df['Heure_Format'],
        y=df['Précipitations'],
        name='Précipitations (mm)',
        marker_color='#00D4FF',
        yaxis='y3'
    ))
    
    fig.update_layout(
        title='🕒 Prévisions Horaires (24h)',
        xaxis_title='Heure',
        yaxis=dict(title='Température (°C)', side='left'),
        yaxis2=dict(title='Probabilité (%)', side='right', overlaying='y', range=[0, 100], showgrid=False),
        yaxis3=dict(title='Précipitations (mm)', side='right', overlaying='y', anchor='free', position=0.95, showgrid=False),
        template=get_chart_template(theme),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white' if theme == 'dark' else 'black'),
        margin=dict(l=20, r=80, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )
    
    return fig




def create_correlation_matrix(df: pd.DataFrame, theme: str = 'dark') -> go.Figure:
    """
    Créer une matrice de corrélation
    
    Args:
        df: DataFrame avec les données météo
        theme: Thème du graphique
        
    Returns:
        Figure Plotly
    """
    corr_data = df[['Temp_Max', 'Temp_Min', 'Précipitations', 'Vent_Max']].corr()
    
    fig = px.imshow(
        corr_data,
        text_auto='.2f',
        aspect='auto',
        color_continuous_scale='RdBu_r',
        template=get_chart_template(theme),
        title='🔗 Matrice de Corrélation'
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white' if theme == 'dark' else 'black'),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig


def create_uv_gauge(uv_index: float, theme: str = 'dark') -> go.Figure:
    """
    Créer une jauge pour l'indice UV
    
    Args:
        uv_index: Valeur de l'indice UV
        theme: Thème du graphique
        
    Returns:
        Figure Plotly
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=uv_index,
        title={'text': "☀️ Indice UV"},
        gauge={
            'axis': {'range': [None, 11]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 2], 'color': "#00E400"},
                {'range': [2, 5], 'color': "#FFFF00"},
                {'range': [5, 7], 'color': "#FF7E00"},
                {'range': [7, 10], 'color': "#FF0000"},
                {'range': [10, 11], 'color': "#8B00FF"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': uv_index
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white' if theme == 'dark' else 'black'),
        height=300
    )
    
    return fig
