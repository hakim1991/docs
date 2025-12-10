# Frontend Streamlit - Application de gestion de tâches (TODO)
# Installation: pip install streamlit requests plotly pandas

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# ============================================
# Configuration
# ============================================

st.set_page_config(
    page_title="Gestionnaire de Tâches",
    page_icon="✅",
    layout="wide"
)

# URL de l'API
API_URL = "http://localhost:8000"

# ============================================
# Fonctions API
# ============================================

def get_tasks(status=None, priority=None):
    """Récupérer les tâches depuis l'API"""
    params = {}
    if status:
        params['status'] = status
    if priority:
        params['priority'] = priority

    try:
        response = requests.get(f"{API_URL}/tasks", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erreur de connexion à l'API: {e}")
        return []

def create_task(title, description, priority, status):
    """Créer une nouvelle tâche"""
    try:
        data = {
            "title": title,
            "description": description,
            "priority": priority,
            "status": status
        }
        response = requests.post(f"{API_URL}/tasks", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erreur lors de la création: {e}")
        return None

def update_task(task_id, **kwargs):
    """Mettre à jour une tâche"""
    try:
        data = {k: v for k, v in kwargs.items() if v is not None}
        response = requests.put(f"{API_URL}/tasks/{task_id}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erreur lors de la mise à jour: {e}")
        return None

def delete_task(task_id):
    """Supprimer une tâche"""
    try:
        response = requests.delete(f"{API_URL}/tasks/{task_id}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erreur lors de la suppression: {e}")
        return False

def get_statistics():
    """Récupérer les statistiques"""
    try:
        response = requests.get(f"{API_URL}/stats")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erreur de connexion aux statistiques: {e}")
        return None

# ============================================
# Vérification de connexion API
# ============================================

def check_api_connection():
    """Vérifier si l'API est accessible"""
    try:
        response = requests.get(API_URL, timeout=2)
        return response.status_code == 200
    except:
        return False

if not check_api_connection():
    st.error("⚠️ L'API n'est pas accessible. Assurez-vous que le backend FastAPI est démarré sur http://localhost:8000")
    st.code("python backend/api.py", language="bash")
    st.stop()

# ============================================
# Header
# ============================================

st.title("✅ Gestionnaire de Tâches")
st.markdown("Application complète avec **FastAPI** (backend) et **Streamlit** (frontend)")
st.markdown("---")

# ============================================
# Sidebar - Statistiques
# ============================================

st.sidebar.title("📊 Statistiques")

stats = get_statistics()

if stats:
    st.sidebar.metric("Total des tâches", stats['total'])

    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("À faire", stats['by_status']['todo'])
        st.metric("En cours", stats['by_status']['in_progress'])
    with col2:
        st.metric("Terminées", stats['by_status']['done'])
        st.metric("Taux", f"{stats['completion_rate']:.0f}%")

    # Graphique priorités
    st.sidebar.markdown("### Priorités")
    priority_data = pd.DataFrame({
        'Priorité': ['Haute', 'Moyenne', 'Basse'],
        'Nombre': [
            stats['by_priority']['high'],
            stats['by_priority']['medium'],
            stats['by_priority']['low']
        ]
    })

    fig = px.pie(
        priority_data,
        values='Nombre',
        names='Priorité',
        color='Priorité',
        color_discrete_map={
            'Haute': '#e74c3c',
            'Moyenne': '#f39c12',
            'Basse': '#3498db'
        }
    )
    fig.update_layout(height=250, margin=dict(l=0, r=0, t=30, b=0))
    st.sidebar.plotly_chart(fig, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("🔄 Les données sont automatiquement rechargées")

# ============================================
# Onglets principaux
# ============================================

tab1, tab2, tab3 = st.tabs(["📋 Tâches", "➕ Ajouter", "📈 Analyse"])

# ============================================
# Tab 1: Liste des tâches
# ============================================

with tab1:
    st.subheader("📋 Liste des Tâches")

    # Filtres
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        status_filter = st.selectbox(
            "Statut",
            options=[None, "todo", "in_progress", "done"],
            format_func=lambda x: {
                None: "Tous",
                "todo": "À faire",
                "in_progress": "En cours",
                "done": "Terminé"
            }.get(x)
        )

    with col2:
        priority_filter = st.selectbox(
            "Priorité",
            options=[None, "high", "medium", "low"],
            format_func=lambda x: {
                None: "Toutes",
                "high": "Haute",
                "medium": "Moyenne",
                "low": "Basse"
            }.get(x)
        )

    with col3:
        if st.button("🔄 Actualiser", type="primary"):
            st.rerun()

    # Récupérer et afficher les tâches
    tasks = get_tasks(status=status_filter, priority=priority_filter)

    if not tasks:
        st.info("📝 Aucune tâche trouvée. Créez-en une dans l'onglet 'Ajouter'!")
    else:
        # Grouper par statut
        for status in ["todo", "in_progress", "done"]:
            status_tasks = [t for t in tasks if t['status'] == status]

            if status_tasks:
                status_labels = {
                    "todo": "📝 À faire",
                    "in_progress": "⏳ En cours",
                    "done": "✅ Terminé"
                }

                with st.expander(f"{status_labels[status]} ({len(status_tasks)})", expanded=(status != "done")):
                    for task in status_tasks:
                        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                        with col1:
                            priority_emoji = {
                                "high": "🔴",
                                "medium": "🟡",
                                "low": "🔵"
                            }
                            st.markdown(f"**{priority_emoji[task['priority']]} {task['title']}**")
                            if task['description']:
                                st.caption(task['description'])

                        with col2:
                            new_status = st.selectbox(
                                "Statut",
                                options=["todo", "in_progress", "done"],
                                index=["todo", "in_progress", "done"].index(task['status']),
                                key=f"status_{task['id']}",
                                label_visibility="collapsed"
                            )
                            if new_status != task['status']:
                                if update_task(task['id'], status=new_status):
                                    st.success("✅ Mis à jour!")
                                    st.rerun()

                        with col3:
                            new_priority = st.selectbox(
                                "Priorité",
                                options=["high", "medium", "low"],
                                index=["high", "medium", "low"].index(task['priority']),
                                key=f"priority_{task['id']}",
                                label_visibility="collapsed",
                                format_func=lambda x: {"high": "Haute", "medium": "Moyenne", "low": "Basse"}[x]
                            )
                            if new_priority != task['priority']:
                                if update_task(task['id'], priority=new_priority):
                                    st.success("✅ Mis à jour!")
                                    st.rerun()

                        with col4:
                            if st.button("🗑️", key=f"delete_{task['id']}", help="Supprimer"):
                                if delete_task(task['id']):
                                    st.success("✅ Supprimé!")
                                    st.rerun()

                        st.markdown("---")

# ============================================
# Tab 2: Ajouter une tâche
# ============================================

with tab2:
    st.subheader("➕ Créer une Nouvelle Tâche")

    with st.form("create_task_form"):
        title = st.text_input("Titre *", placeholder="Ex: Finir le rapport")

        description = st.text_area(
            "Description",
            placeholder="Description détaillée de la tâche (optionnel)"
        )

        col1, col2 = st.columns(2)

        with col1:
            priority = st.selectbox(
                "Priorité",
                options=["low", "medium", "high"],
                index=1,
                format_func=lambda x: {"low": "Basse", "medium": "Moyenne", "high": "Haute"}[x]
            )

        with col2:
            status = st.selectbox(
                "Statut",
                options=["todo", "in_progress", "done"],
                index=0,
                format_func=lambda x: {"todo": "À faire", "in_progress": "En cours", "done": "Terminé"}[x]
            )

        submitted = st.form_submit_button("✅ Créer la tâche", type="primary", use_container_width=True)

        if submitted:
            if not title:
                st.error("❌ Le titre est obligatoire!")
            else:
                task = create_task(title, description, priority, status)
                if task:
                    st.success(f"✅ Tâche '{title}' créée avec succès!")
                    st.balloons()
                    st.rerun()

# ============================================
# Tab 3: Analyse
# ============================================

with tab3:
    st.subheader("📈 Analyse des Tâches")

    if stats:
        # Graphique statuts
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Répartition par Statut")
            status_data = pd.DataFrame({
                'Statut': ['À faire', 'En cours', 'Terminé'],
                'Nombre': [
                    stats['by_status']['todo'],
                    stats['by_status']['in_progress'],
                    stats['by_status']['done']
                ]
            })

            fig = px.bar(
                status_data,
                x='Statut',
                y='Nombre',
                color='Statut',
                color_discrete_map={
                    'À faire': '#3498db',
                    'En cours': '#f39c12',
                    'Terminé': '#2ecc71'
                }
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Répartition par Priorité")
            fig = px.pie(
                priority_data,
                values='Nombre',
                names='Priorité',
                hole=0.4,
                color='Priorité',
                color_discrete_map={
                    'Haute': '#e74c3c',
                    'Moyenne': '#f39c12',
                    'Basse': '#3498db'
                }
            )
            st.plotly_chart(fig, use_container_width=True)

        # Timeline
        st.markdown("### Détails des Tâches")
        all_tasks = get_tasks()
        if all_tasks:
            df = pd.DataFrame(all_tasks)
            df['created_at'] = pd.to_datetime(df['created_at'])

            # Ajouter traductions
            df['status_fr'] = df['status'].map({
                'todo': 'À faire',
                'in_progress': 'En cours',
                'done': 'Terminé'
            })

            df['priority_fr'] = df['priority'].map({
                'high': 'Haute',
                'medium': 'Moyenne',
                'low': 'Basse'
            })

            st.dataframe(
                df[['title', 'status_fr', 'priority_fr', 'created_at']].rename(columns={
                    'title': 'Titre',
                    'status_fr': 'Statut',
                    'priority_fr': 'Priorité',
                    'created_at': 'Créée le'
                }),
                use_container_width=True,
                height=400
            )

# ============================================
# Footer
# ============================================

st.markdown("---")
st.caption("💻 Application créée avec FastAPI et Streamlit")

# ============================================
# Documentation
# ============================================

"""
Pour démarrer l'application complète:

1. Démarrer le backend FastAPI:
   cd backend
   python api.py

   L'API sera accessible sur http://localhost:8000
   Documentation: http://localhost:8000/docs

2. Démarrer le frontend Streamlit:
   cd frontend
   streamlit run app.py

   L'interface sera accessible sur http://localhost:8501

Fonctionnalités:
✅ CRUD complet (Create, Read, Update, Delete)
✅ Filtres par statut et priorité
✅ Statistiques en temps réel
✅ Graphiques interactifs
✅ Interface responsive
✅ Communication API REST
"""
