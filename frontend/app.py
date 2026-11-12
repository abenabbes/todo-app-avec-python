import os
import streamlit as st
import pandas as pd
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Gestionnaire de Tâches", page_icon="✅")
st.title("✅ Gestionnaire de Tâches")

# --- Formulaire de création ---
with st.form("nouvelle_tache"):
    title = st.text_input("Titre de la tâche")
    description = st.text_area("Description (optionnel)")
    submitted = st.form_submit_button("Ajouter")
    if submitted and title:
        r = requests.post(f"{API_URL}/tasks/", json={"title": title, "description": description})
        if r.status_code == 201:
            st.success("Tâche ajoutée !")
        else:
            st.error(f"Erreur : {r.status_code}")

# --- Liste des tâches ---
try:
    r = requests.get(f"{API_URL}/tasks/", timeout=5)
    r.raise_for_status()
    tasks = r.json()
except requests.RequestException:
    st.error("⚠️ API inaccessible. Vérifie que FastAPI tourne.")
    st.stop()

if not tasks:
    st.info("Aucune tâche. Ajoute-en une !")
    st.stop()

df = pd.DataFrame(tasks)

# --- Filtre ---
filtre = st.radio("Filtrer", ["Toutes", "À faire", "Terminées"], horizontal=True)
if filtre == "À faire":
    df = df[~df["done"]]
elif filtre == "Terminées":
    df = df[df["done"]]

# --- Affichage + actions ---
for _, task in df.iterrows():
    col1, col2, col3 = st.columns([6, 1, 1])
    col1.markdown(f"{'~~'+task['title']+'~~' if task['done'] else '**'+task['title']+'**'}")
    col1.caption(task["description"] or "")
    if col2.button("✓", key=f"done{task['id']}"):
        requests.patch(f"{API_URL}/tasks/{task['id']}", json={"done": not task["done"]})
        st.rerun()
    if col3.button("🗑", key=f"del{task['id']}"):
        requests.delete(f"{API_URL}/tasks/{task['id']}")
        st.rerun()

st.metric("Total tâches", len(tasks))
