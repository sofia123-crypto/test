import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="🧪 Test Gantt", layout="wide")
st.title("✅ Test Gantt - Ajout immédiat")

# Initialisation
if "planning" not in st.session_state:
    st.session_state.planning = []

# --- Formulaire ---
with st.form("ajout_form"):
    st.subheader("➕ Ajouter une tâche")

    now = datetime.now()
    col1, col2 = st.columns(2)
    heure_debut = col1.time_input("Heure de début", now.time())
    heure_fin = col2.time_input("Heure de fin", (now + timedelta(minutes=30)).time())
    nom_tache = st.text_input("Nom de la tâche", "Tâche test")

    submitted = st.form_submit_button("📌 Ajouter au planning")
    if submitted:
        date_str = now.strftime("%Y-%m-%d")
        st.session_state.planning.append((
            date_str,
            heure_debut.strftime("%H:%M"),
            heure_fin.strftime("%H:%M"),
            nom_tache
        ))
        st.rerun()

# --- Affichage Gantt ---
if st.session_state.planning:
    df = pd.DataFrame(st.session_state.planning, columns=["date", "heure_debut", "heure_fin", "nom"])
    df["Début"] = pd.to_datetime(df["date"] + " " + df["heure_debut"])
    df["Fin"] = pd.to_datetime(df["date"] + " " + df["heure_fin"])
    df["Jour"] = pd.to_datetime(df["date"]).dt.strftime("%A %d/%m")
    df["Tâche"] = df["nom"]

    st.subheader("📅 Gantt")
    fig = px.timeline(df, x_start="Début", x_end="Fin", y="Jour", color="Tâche", title="Planning Gantt")
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Aucune tâche planifiée pour l’instant.")
