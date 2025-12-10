# Streamlit - Exemple complet d'application dashboard
# Installation: pip install streamlit pandas plotly numpy

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# ============================================
# Configuration de la page
# ============================================

st.set_page_config(
    page_title="Dashboard Ventes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# Style CSS personnalisé
# ============================================

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# Session State (persistance)
# ============================================

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if 'sales_data' not in st.session_state:
    st.session_state.sales_data = None

# ============================================
# Fonctions de génération de données
# ============================================

@st.cache_data
def generate_sales_data(num_records=1000):
    """Générer des données de ventes simulées"""
    np.random.seed(42)

    dates = pd.date_range(
        start=datetime.now() - timedelta(days=365),
        end=datetime.now(),
        periods=num_records
    )

    products = ['Laptop', 'Smartphone', 'Tablette', 'Écouteurs', 'Montre']
    regions = ['Nord', 'Sud', 'Est', 'Ouest', 'Centre']
    categories = ['Électronique', 'Accessoires']

    data = {
        'Date': dates,
        'Produit': np.random.choice(products, num_records),
        'Région': np.random.choice(regions, num_records),
        'Catégorie': np.random.choice(categories, num_records),
        'Quantité': np.random.randint(1, 20, num_records),
        'Prix_Unitaire': np.random.uniform(50, 1500, num_records),
    }

    df = pd.DataFrame(data)
    df['Montant_Total'] = df['Quantité'] * df['Prix_Unitaire']
    df['Mois'] = df['Date'].dt.to_period('M').astype(str)
    df['Année'] = df['Date'].dt.year

    return df

# ============================================
# Sidebar - Filtres
# ============================================

st.sidebar.title("🎛️ Filtres")

# Charger les données
if st.sidebar.button("🔄 Charger/Recharger les données", type="primary"):
    with st.spinner("Chargement des données..."):
        st.session_state.sales_data = generate_sales_data()
        st.session_state.data_loaded = True
    st.sidebar.success("✅ Données chargées avec succès!")

# Si les données ne sont pas chargées, afficher un message
if not st.session_state.data_loaded:
    st.info("👈 Cliquez sur 'Charger les données' dans la sidebar pour commencer")
    st.stop()

# Récupérer les données
df = st.session_state.sales_data

# Filtres
st.sidebar.subheader("📅 Période")
date_min = df['Date'].min().date()
date_max = df['Date'].max().date()

date_range = st.sidebar.date_input(
    "Sélectionner la période",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max
)

if len(date_range) == 2:
    mask = (df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])
    df_filtered = df[mask]
else:
    df_filtered = df

st.sidebar.subheader("🏷️ Produits")
products = st.sidebar.multiselect(
    "Sélectionner les produits",
    options=df['Produit'].unique(),
    default=df['Produit'].unique()
)

st.sidebar.subheader("🗺️ Régions")
regions = st.sidebar.multiselect(
    "Sélectionner les régions",
    options=df['Région'].unique(),
    default=df['Région'].unique()
)

# Appliquer les filtres
df_filtered = df_filtered[
    (df_filtered['Produit'].isin(products)) &
    (df_filtered['Région'].isin(regions))
]

# ============================================
# Header
# ============================================

st.title("📊 Dashboard de Ventes")
st.markdown("---")

# ============================================
# Métriques principales (KPIs)
# ============================================

col1, col2, col3, col4 = st.columns(4)

total_sales = df_filtered['Montant_Total'].sum()
total_quantity = df_filtered['Quantité'].sum()
avg_price = df_filtered['Prix_Unitaire'].mean()
num_transactions = len(df_filtered)

with col1:
    st.metric(
        label="💰 Ventes Totales",
        value=f"{total_sales:,.0f} €",
        delta=f"{(total_sales / len(df_filtered)):.0f} € par transaction"
    )

with col2:
    st.metric(
        label="📦 Quantité Vendue",
        value=f"{total_quantity:,}",
        delta=f"{(total_quantity / len(df_filtered)):.1f} par transaction"
    )

with col3:
    st.metric(
        label="💵 Prix Moyen",
        value=f"{avg_price:.2f} €",
        delta=None
    )

with col4:
    st.metric(
        label="🛒 Transactions",
        value=f"{num_transactions:,}",
        delta=None
    )

st.markdown("---")

# ============================================
# Graphiques
# ============================================

# Row 1: Ventes par mois et par produit
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Ventes par Mois")

    sales_by_month = df_filtered.groupby('Mois')['Montant_Total'].sum().reset_index()

    fig = px.line(
        sales_by_month,
        x='Mois',
        y='Montant_Total',
        title='Évolution des ventes mensuelles',
        labels={'Montant_Total': 'Ventes (€)', 'Mois': 'Mois'}
    )
    fig.update_traces(line_color='#1f77b4', line_width=3)
    fig.update_layout(hovermode='x unified')

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏆 Top Produits")

    sales_by_product = df_filtered.groupby('Produit')['Montant_Total'].sum().reset_index()
    sales_by_product = sales_by_product.sort_values('Montant_Total', ascending=True)

    fig = px.bar(
        sales_by_product,
        x='Montant_Total',
        y='Produit',
        orientation='h',
        title='Ventes par produit',
        labels={'Montant_Total': 'Ventes (€)', 'Produit': 'Produit'},
        color='Montant_Total',
        color_continuous_scale='Blues'
    )

    st.plotly_chart(fig, use_container_width=True)

# Row 2: Ventes par région et distribution des prix
col1, col2 = st.columns(2)

with col1:
    st.subheader("🗺️ Ventes par Région")

    sales_by_region = df_filtered.groupby('Région')['Montant_Total'].sum().reset_index()

    fig = px.pie(
        sales_by_region,
        values='Montant_Total',
        names='Région',
        title='Répartition des ventes par région',
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💰 Distribution des Prix")

    fig = px.histogram(
        df_filtered,
        x='Prix_Unitaire',
        nbins=50,
        title='Distribution des prix unitaires',
        labels={'Prix_Unitaire': 'Prix (€)', 'count': 'Fréquence'},
        color_discrete_sequence=['#2ecc71']
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# Heatmap
# ============================================

st.subheader("🔥 Heatmap: Ventes par Produit et Région")

heatmap_data = df_filtered.pivot_table(
    values='Montant_Total',
    index='Produit',
    columns='Région',
    aggfunc='sum',
    fill_value=0
)

fig = px.imshow(
    heatmap_data,
    labels=dict(x="Région", y="Produit", color="Ventes (€)"),
    title="Ventes par produit et région",
    color_continuous_scale='RdYlGn',
    aspect="auto"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# Tableau de données
# ============================================

st.subheader("📋 Données Détaillées")

# Options d'affichage
col1, col2, col3 = st.columns(3)

with col1:
    show_columns = st.multiselect(
        "Colonnes à afficher",
        options=df_filtered.columns.tolist(),
        default=['Date', 'Produit', 'Région', 'Quantité', 'Montant_Total']
    )

with col2:
    sort_by = st.selectbox(
        "Trier par",
        options=df_filtered.columns.tolist(),
        index=0
    )

with col3:
    sort_order = st.radio(
        "Ordre",
        options=['Croissant', 'Décroissant'],
        horizontal=True
    )

# Afficher le tableau
df_display = df_filtered[show_columns].sort_values(
    by=sort_by,
    ascending=(sort_order == 'Croissant')
)

st.dataframe(
    df_display.head(100),
    use_container_width=True,
    height=400
)

# Téléchargement CSV
csv = df_display.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Télécharger les données (CSV)",
    data=csv,
    file_name=f"ventes_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)

# ============================================
# Formulaire d'ajout (exemple interactif)
# ============================================

st.markdown("---")
st.subheader("➕ Ajouter une Vente (Simulation)")

with st.expander("Formulaire d'ajout", expanded=False):
    with st.form("add_sale_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            new_date = st.date_input("Date", value=datetime.now())
            new_product = st.selectbox("Produit", df['Produit'].unique())

        with col2:
            new_region = st.selectbox("Région", df['Région'].unique())
            new_quantity = st.number_input("Quantité", min_value=1, value=1)

        with col3:
            new_price = st.number_input("Prix Unitaire (€)", min_value=0.0, value=100.0)

        submitted = st.form_submit_button("Ajouter", type="primary")

        if submitted:
            st.success(f"✅ Vente ajoutée: {new_quantity}x {new_product} à {new_price}€")
            st.info("📝 Note: Ceci est une simulation. En production, les données seraient enregistrées dans une base de données.")

# ============================================
# Footer
# ============================================

st.markdown("---")
st.caption(f"Dashboard généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")

# ============================================
# Sidebar - Informations
# ============================================

st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ Informations")
st.sidebar.info(f"""
**Période**: {date_range[0]} au {date_range[1]}

**Filtres actifs**:
- {len(products)} produit(s)
- {len(regions)} région(s)

**Données**:
- {len(df_filtered):,} transactions filtrées
- {len(df):,} transactions totales
""")

# ============================================
# Point d'entrée
# ============================================

"""
Pour démarrer l'application:
    streamlit run app.py

L'application sera accessible sur:
    http://localhost:8501

Fonctionnalités:
✅ Dashboard interactif
✅ Filtres dynamiques
✅ Graphiques avec Plotly
✅ Métriques KPI
✅ Tableau de données
✅ Export CSV
✅ Formulaire interactif
✅ Session state
✅ Cache de données
"""
