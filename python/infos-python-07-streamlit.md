# 🎨 Streamlit

[← Fichiers](./infos-python-06-fichiers-io.md) | [Index](./infos-python-00-index.md) | [Flask →](./infos-python-08-flask.md)

## Installation

```bash
pip install streamlit
```

## Premier app

```python
# app.py
import streamlit as st

st.title("Mon App Streamlit")
st.write("Hello World!")
```

```bash
streamlit run app.py
```

Ouvre `http://localhost:8501`

## Texte et markdown

```python
import streamlit as st

# Titre
st.title("Titre principal")
st.header("Header")
st.subheader("Subheader")

# Texte
st.text("Texte simple")
st.write("Write peut afficher n'importe quoi")

# Markdown
st.markdown("**Gras** et *italique*")
st.markdown("""
## Liste
- Item 1
- Item 2
""")

# Code
st.code("""
def hello():
    print("Hello")
""", language="python")

# LaTeX
st.latex(r"e^{i\pi} + 1 = 0")
```

## Widgets d'entrée

### Boutons

```python
if st.button("Cliquez-moi"):
    st.write("Bouton cliqué !")

# Download button
data = "Hello World"
st.download_button(
    label="Télécharger",
    data=data,
    file_name="hello.txt"
)
```

### Input texte

```python
# Text input
name = st.text_input("Votre nom:", "Alice")
st.write(f"Bonjour {name}")

# Text area
text = st.text_area("Votre message:", "")

# Number input
age = st.number_input("Âge:", min_value=0, max_value=150, value=25)

# Password
password = st.text_input("Mot de passe:", type="password")
```

### Sélection

```python
# Select box
option = st.selectbox(
    "Choisissez:",
    ["Option 1", "Option 2", "Option 3"]
)

# Multi-select
options = st.multiselect(
    "Sélectionnez plusieurs:",
    ["A", "B", "C", "D"]
)

# Radio
choice = st.radio(
    "Choisissez:",
    ["Oui", "Non"]
)

# Checkbox
agree = st.checkbox("J'accepte les conditions")
if agree:
    st.write("Merci !")
```

### Sliders

```python
# Slider simple
value = st.slider("Choisissez une valeur:", 0, 100, 50)

# Range slider
values = st.slider("Range:", 0.0, 100.0, (25.0, 75.0))

# Date
from datetime import date
d = st.date_input("Date:", date.today())

# Time
t = st.time_input("Heure:")
```

### Upload fichiers

```python
uploaded_file = st.file_uploader("Choisir un fichier", type=["csv", "txt"])
if uploaded_file is not None:
    # Lire CSV
    import pandas as pd
    df = pd.read_csv(uploaded_file)
    st.write(df)

    # Lire texte
    content = uploaded_file.getvalue().decode("utf-8")
    st.write(content)
```

## Affichage de données

### DataFrames

```python
import pandas as pd
import streamlit as st

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["Paris", "Lyon", "Marseille"]
})

# Table simple
st.write(df)

# DataFrame interactif
st.dataframe(df)

# Table statique
st.table(df)

# Métriques
st.metric(label="Temperature", value="25°C", delta="1.2°C")
```

### JSON

```python
data = {
    "name": "Alice",
    "age": 25,
    "skills": ["Python", "SQL"]
}
st.json(data)
```

## Graphiques

### Plotly

```bash
pip install plotly
```

```python
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 20, 15, 25, 30]
})

fig = px.line(df, x="x", y="y", title="Mon graphique")
st.plotly_chart(fig)

# Bar chart
fig = px.bar(df, x="x", y="y")
st.plotly_chart(fig)

# Scatter
fig = px.scatter(df, x="x", y="y")
st.plotly_chart(fig)
```

### Matplotlib

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("Sinus")
st.pyplot(fig)
```

### Charts Streamlit

```python
import pandas as pd

df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 20, 15, 25, 30]
})

# Line chart
st.line_chart(df)

# Bar chart
st.bar_chart(df)

# Area chart
st.area_chart(df)
```

## Layout

### Colonnes

```python
col1, col2 = st.columns(2)

with col1:
    st.header("Colonne 1")
    st.write("Contenu gauche")

with col2:
    st.header("Colonne 2")
    st.write("Contenu droite")

# Colonnes inégales
col1, col2, col3 = st.columns([2, 1, 1])
```

### Expander

```python
with st.expander("Voir détails"):
    st.write("Contenu caché par défaut")
    st.image("image.jpg")
```

### Tabs

```python
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

with tab1:
    st.write("Contenu tab 1")

with tab2:
    st.write("Contenu tab 2")

with tab3:
    st.write("Contenu tab 3")
```

### Sidebar

```python
st.sidebar.title("Menu")
option = st.sidebar.selectbox(
    "Choisissez:",
    ["Accueil", "À propos", "Contact"]
)

st.sidebar.slider("Valeur:", 0, 100, 50)
```

### Container

```python
with st.container():
    st.write("Dans un container")
    st.write("Autre contenu")
```

## État et cache

### Session State

```python
# Initialiser
if "count" not in st.session_state:
    st.session_state.count = 0

# Utiliser
if st.button("Incrémenter"):
    st.session_state.count += 1

st.write(f"Count: {st.session_state.count}")

# Avec callback
def increment():
    st.session_state.count += 1

st.button("Click", on_click=increment)
```

### Cache

```python
@st.cache_data
def load_data():
    # Fonction coûteuse
    return pd.read_csv("large_file.csv")

df = load_data()  # Mis en cache

# Cache avec TTL
@st.cache_data(ttl=3600)  # 1 heure
def get_data():
    return fetch_from_api()

# Cache ressources (connexions)
@st.cache_resource
def get_database_connection():
    return create_connection()
```

## Forms

```python
with st.form("my_form"):
    st.write("Formulaire")
    name = st.text_input("Nom:")
    age = st.number_input("Âge:", min_value=0)

    submitted = st.form_submit_button("Envoyer")
    if submitted:
        st.write(f"Nom: {name}, Âge: {age}")
```

## Messages

```python
# Success
st.success("Opération réussie !")

# Info
st.info("Information")

# Warning
st.warning("Attention !")

# Error
st.error("Erreur !")

# Exception
try:
    1 / 0
except Exception as e:
    st.exception(e)
```

## Progress et spinner

```python
import time

# Progress bar
progress = st.progress(0)
for i in range(100):
    progress.progress(i + 1)
    time.sleep(0.01)

# Spinner
with st.spinner("Chargement..."):
    time.sleep(2)
st.success("Terminé !")
```

## Media

```python
# Image
st.image("image.jpg", caption="Ma photo")

# Audio
st.audio("audio.mp3")

# Video
st.video("video.mp4")
```

## Maps

```python
import pandas as pd

df = pd.DataFrame({
    "lat": [48.8566, 45.7640],
    "lon": [2.3522, 4.8357]
})

st.map(df)
```

## App multi-pages

```
app/
├── Home.py
└── pages/
    ├── 1_📊_Dashboard.py
    ├── 2_📈_Analytics.py
    └── 3_⚙️_Settings.py
```

```python
# Home.py
import streamlit as st

st.set_page_config(page_title="Mon App", page_icon="🏠")
st.title("Accueil")
```

```python
# pages/1_📊_Dashboard.py
import streamlit as st

st.title("Dashboard")
st.write("Contenu du dashboard")
```

## Configuration

```python
# Au début de l'app
st.set_page_config(
    page_title="Mon App",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://example.com/help",
        "Report a bug": "https://example.com/bug",
        "About": "Mon application Streamlit"
    }
)
```

## Exemple complet

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Dashboard de Ventes")

# Sidebar
with st.sidebar:
    st.header("Filtres")
    year = st.selectbox("Année:", [2021, 2022, 2023, 2024])
    region = st.multiselect("Région:", ["Nord", "Sud", "Est", "Ouest"])

# Cache data
@st.cache_data
def load_data():
    return pd.DataFrame({
        "month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "sales": [100, 150, 120, 200, 180],
        "profit": [20, 30, 25, 40, 35]
    })

df = load_data()

# Métriques
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Ventes totales", f"{df['sales'].sum()}€")
with col2:
    st.metric("Profit total", f"{df['profit'].sum()}€")
with col3:
    st.metric("Moyenne", f"{df['sales'].mean():.0f}€")

# Graphiques
col1, col2 = st.columns(2)

with col1:
    fig = px.line(df, x="month", y="sales", title="Ventes par mois")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(df, x="month", y="profit", title="Profit par mois")
    st.plotly_chart(fig, use_container_width=True)

# Table
with st.expander("Voir les données"):
    st.dataframe(df, use_container_width=True)
```

## Déploiement

### Streamlit Cloud

1. Push sur GitHub
2. Aller sur https://share.streamlit.io
3. Connecter le repo
4. Déployer !

### requirements.txt

```txt
streamlit==1.28.0
pandas==2.1.0
plotly==5.17.0
```

[← Fichiers](./infos-python-06-fichiers-io.md) | [Index](./infos-python-00-index.md) | [Flask →](./infos-python-08-flask.md)
