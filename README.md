# 🌦️ Météo Pro 2.0 - Documentation Technique

## 📋 Résumé Exécutif

**Météo Pro 2.0** est une application de tableau de bord météorologique avancée, conçue en Python avec le framework Streamlit. Elle délivre des prévisions météorologiques de haute précision intégrées dans une interface utilisateur réactive et immersive, basée sur les principes du Glassmorphism.

Les différenciateurs techniques clés incluent un moteur de rendu atmosphérique contextuel (arrière-plans dynamiques basés sur les codes WMO et les cycles diurnes) et une architecture robuste de repli pour la disponibilité des ressources graphiques.

---

## 🏗️ Architecture du Système

L'application suit une **Architecture Basée sur les Composants**, assurant une séparation des préoccupations entre l'acquisition des données, la logique de traitement et le rendu de l'interface utilisateur.

### Modules Clés

| Module                | Classification                       | Responsabilité                                                                                                                                                                                 |
| :-------------------- | :----------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `app.py`              | **Contrôleur / Point d'Entrée**      | Orchestre le cycle de vie de l'application, la gestion de l'état de session (`st.session_state`) et l'injection des composants.                                                                |
| `weather_analyzer.py` | **Couche Logique Métier**            | Implémente les algorithmes d'interprétation des codes WMO, la génération des indices de confort (Heat Index/Wind Chill) et l'analyse des tendances de données.                                 |
| `weather_api.py`      | **Couche d'Accès aux Données (DAL)** | Gère la communication synchrone avec les endpoints REST d'Open-Meteo. Implémente des stratégies de mise en cache (`@st.cache_data`) pour optimiser l'utilisation des quotas API et la latence. |
| `ui_components.py`    | **Vue / Couche de Présentation**     | Gère l'injection CSS, l'encodage des actifs en Base64 et le rendu des éléments UI atomiques (Cartes, Métriques). Implémente la logique d'arrière-plan dynamique.                               |
| `config.py`           | **Configuration**                    | Centralise la configuration statique, le proxy des variables d'environnement (si applicable) et les constantes mappées (Codes Météo, Palettes de Couleurs).                                    |

---

## 💻 Stack Technique

- **Environnement d'Exécution** : Python 3.8+
- **Framework Frontend** : [Streamlit](https://streamlit.io/) (Reactive Web Framework)
- **Traitement de Données** :
  - **Pandas** : Manipulation de séries temporelles et structuration de dataframes.
  - **NumPy** : Opérations vectorisées pour l'analyse statistique.
  - **Plotly Express** : Moteur de visualisation de données interactif.
- **APIs Externes** :
  - [Open-Meteo](https://open-meteo.com/) : API de Prévisions Météo (Sans Auth, Haute Disponibilité).
  - Geocoding API : Résolution de coordonnées spatiales.
  - Air Quality API : Données AQI et concentration de polluants.

---

## ⚙️ Implémentations Techniques Clés

### 1. Moteur de Rendu d'Arrière-plan Contextuel

L'interface s'adapte dynamiquement aux conditions environnementales via un pipeline logique personnalisé :

1.  **Extraction d'État** : Récupère le `weather_code` (standards WMO) et le booléen `is_day` depuis la payload API.
2.  **Mappage de Catégorie** : `WeatherAnalyzer.get_weather_category(code, is_day)` résout les états internes précis (ex: `misty_night` vs `misty_day`).
3.  **Résolution d'Actifs** :
    - **Primaire** : Vérifie le chemin de l'actif haute résolution mappé.
    - **Stratégie de Repli (Heuristique)** : Si un actif nocturne spécifique est manquant (ex: `misty_night`), le système charge l'actif diurne correspondant (`misty_day`) et applique un **filtre de luminosité CSS** (overlay sombre) pour simuler les conditions nocturnes, assurant la continuité visuelle.
    - **Sécurité** : Retourne aux gradients linéaires CSS si aucun actif n'est résoluble.

### 2. Stylisation Isomorphique (Glassmorphism)

L'application surcharge les classes CSS standard de Streamlit via `st.markdown(unsafe_allow_html=True)` pour implémenter un langage de design Glassmorphism cohérent :

- **Backdrop Filter** : `blur(10px)`
- **Translucidité** : `rgba(255, 255, 255, 0.1)`
- **Bordure** : `1px solid rgba(255, 255, 255, 0.2)`

### 3. Outillage Développeur (Mode Test Visuel)

Pour faciliter le débogage de l'interface sans dépendre des variations API en temps réel, un **Harnais de Test Visuel** est intégré dans `app.py`.

- **Mécanisme** : Permet l'injection d'états météo simulés directement dans le pipeline de rendu, contournant la réponse API.
- **Utilisation** : Accessible via Sidebar -> "Mode Test". L'activation surcharge la `weather_category` dérivée des données réelles.

---

## 🚀 Déploiement & Installation

### Prérequis

- Environnement Python (Virtualenv/Conda recommandé)
- Git

### Routine d'Installation

```bash
# 1. Cloner le Dépôt
git clone <url_du_depot>
cd meteo-py

# 2. Résolution des Dépendances
pip install -r requirements.txt

# 3. Exécution
streamlit run app.py
```

### Configuration

Les paramètres du projet peuvent être ajustés dans `config.py`.

- `CACHE_TTL_WEATHER` : Ajuste la fréquence de polling API (Défaut : 900s).
- `THEME_COLORS` : Définition du schéma de couleurs de l'application.

---

## 📄 Licence & Crédits

Développé dans le cadre du cursus **"Compétences numériques et informatique (Python)"**.
**Version** : 2.0.0-stable
**Date de Build** : Janvier 2026
