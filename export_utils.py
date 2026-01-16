"""
Utilitaires pour exporter les données météo
"""

import pandas as pd
import json
import numpy as np
from datetime import datetime
from typing import Dict, Any
from io import BytesIO


def convert_numpy(obj: Any) -> Any:
    """
    Convertir les types numpy en types Python natifs
    
    Args:
        obj: Objet à convertir
        
    Returns:
        Objet converti
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        if np.isnan(obj) or np.isinf(obj):
            return None
        return float(obj)
    elif isinstance(obj, float):
        if np.isnan(obj) or np.isinf(obj):
            return None
        return obj
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(item) for item in obj]
    return obj


def export_to_csv(df: pd.DataFrame, city_name: str) -> tuple:
    """
    Exporter les données en CSV
    
    Args:
        df: DataFrame à exporter
        city_name: Nom de la ville
        
    Returns:
        Tuple (données CSV, nom de fichier)
    """
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    filename = f"meteo_{city_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    return csv, filename


def export_to_json(
    weather_data: Dict[str, Any],
    city_info: Dict[str, Any],
    stats: Dict[str, float]
) -> tuple:
    """
    Exporter en JSON
    
    Args:
        weather_data: Données météo complètes
        city_info: Informations sur la ville
        stats: Statistiques calculées
        
    Returns:
        Tuple (données JSON, nom de fichier)
    """
    # Convertir les statistiques
    stats_converted = convert_numpy(stats)
    
    # Convertir les données météo
    current_converted = convert_numpy(weather_data.get('current', {}))
    daily_converted = convert_numpy(weather_data.get('daily', {}))
    
    export_data = {
        'ville': city_info,
        'date_export': datetime.now().isoformat(),
        'statistiques': stats_converted,
        'donnees_actuelles': current_converted,
        'previsions_quotidiennes': daily_converted
    }
    
    json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
    filename = f"meteo_{city_info['name']}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    return json_str, filename


def export_to_pdf(
    city_info: Dict[str, Any],
    current_data: Dict[str, Any],
    df: pd.DataFrame,
    stats: Dict[str, float]
) -> tuple:
    """
    Exporter en PDF avec graphiques
    
    Args:
        city_info: Informations sur la ville
        current_data: Données actuelles
        df: DataFrame avec prévisions
        stats: Statistiques
        
    Returns:
        Tuple (buffer PDF, nom de fichier) ou (None, message d'erreur)
    """
    try:
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import cm
            from reportlab.pdfgen import canvas
            from reportlab.lib import colors
            from reportlab.platypus import Table, TableStyle
        except ImportError:
            return None, "Module 'reportlab' manquant"

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # Titre
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2, height - 2 * cm, f"Rapport Météo - {city_info['name']}")
        
        # Date
        c.setFont("Helvetica", 12)
        c.drawCentredString(width / 2, height - 3 * cm, f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
        
        # Ligne de séparation
        c.line(2 * cm, height - 3.5 * cm, width - 2 * cm, height - 3.5 * cm)
        
        # Données actuelles
        y_position = height - 5 * cm
        c.setFont("Helvetica-Bold", 16)
        c.drawString(2 * cm, y_position, "Conditions Actuelles")
        
        y_position -= 1 * cm
        c.setFont("Helvetica", 12)
        
        current_info = [
            f"Température: {current_data.get('temperature_2m', 'N/A')}°C",
            f"Ressenti: {current_data.get('apparent_temperature', 'N/A')}°C",
            f"Humidité: {current_data.get('relative_humidity_2m', 'N/A')}%",
            f"Vent: {current_data.get('wind_speed_10m', 'N/A')} km/h",
            f"Pression: {current_data.get('pressure_msl', 'N/A')} hPa"
        ]
        
        for info in current_info:
            c.drawString(2 * cm, y_position, info)
            y_position -= 0.7 * cm
        
        # Statistiques
        y_position -= 1 * cm
        c.setFont("Helvetica-Bold", 16)
        c.drawString(2 * cm, y_position, "Statistiques de la Période")
        
        y_position -= 1 * cm
        c.setFont("Helvetica", 12)
        
        stats_info = [
            f"Température moyenne: {stats.get('temp_moyenne', 0):.1f}°C",
            f"Température max: {stats.get('temp_max_periode', 0):.1f}°C",
            f"Température min: {stats.get('temp_min_periode', 0):.1f}°C",
            f"Total précipitations: {stats.get('total_precipitations', 0):.1f} mm",
            f"Jours de pluie: {stats.get('jours_pluie', 0)}",
            f"Vent moyen: {stats.get('vent_moyen', 0):.1f} km/h"
        ]
        
        for info in stats_info:
            c.drawString(2 * cm, y_position, info)
            y_position -= 0.7 * cm
        
        # Tableau des prévisions (première page)
        y_position -= 1 * cm
        c.setFont("Helvetica-Bold", 16)
        c.drawString(2 * cm, y_position, "Prévisions Quotidiennes")
        
        # Créer le tableau
        y_position -= 0.5 * cm
        table_data = [['Date', 'T° Max', 'T° Min', 'Pluie (mm)']]
        
        for _, row in df.head(7).iterrows():
            table_data.append([
                row['Date'].strftime('%d/%m'),
                f"{row['Temp_Max']:.1f}°",
                f"{row['Temp_Min']:.1f}°",
                f"{row['Précipitations']:.1f}"
            ])
        
        table = Table(table_data, colWidths=[3 * cm, 3 * cm, 3 * cm, 3 * cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        table.wrapOn(c, width, height)
        table.drawOn(c, 2 * cm, y_position - 6 * cm)
        
        # Footer
        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(width / 2, 1 * cm, "Données fournies par Open-Meteo API")
        
        c.save()
        buffer.seek(0)
        
        filename = f"rapport_meteo_{city_info['name']}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        return buffer, filename
        
    except Exception as e:
        return None, f"Erreur lors de la génération PDF: {str(e)}"


def generate_report(
    city_info: Dict[str, Any],
    weather_data: Dict[str, Any],
    df: pd.DataFrame,
    stats: Dict[str, float],
    format: str = 'json'
) -> tuple:
    """
    Générer un rapport dans le format spécifié
    
    Args:
        city_info: Informations sur la ville
        weather_data: Données météo complètes
        df: DataFrame avec prévisions
        stats: Statistiques
        format: Format de sortie ('csv', 'json', 'pdf')
        
    Returns:
        Tuple (données, nom de fichier)
    """
    if format == 'csv':
        return export_to_csv(df, city_info['name'])
    elif format == 'json':
        return export_to_json(weather_data, city_info, stats)
    elif format == 'pdf':
        return export_to_pdf(city_info, weather_data['current'], df, stats)
    else:
        raise ValueError(f"Format non supporté: {format}")
