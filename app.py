import streamlit as st
import pandas as pd
import os
import subprocess

st.set_page_config(page_title="Dakar Auto Data App", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à :", ["Dashboard", "Téléchargement", "Scraper", "Évaluation"])

# Chargement des fichiers CSV
@st.cache_data
def load_csv(file):
    if os.path.exists(file):
        return pd.read_csv(file)
    return pd.DataFrame()

files = {
    "Données Scrappées": "scraped_data.csv",
    "Collection 100 pages": "dakar-auto_datacolection_100page.csv",
    "Occasion 8 pages": "dakar-auto_Occasion_8page.csv",
    "Motos 54 pages": "dakar-auto_Motos_54page.csv",
}

dataframes = {name: load_csv(path) for name, path in files.items()}

if page == "Dashboard":
    st.title("Dashboard des Données Dakar Auto")
    tab = st.selectbox("Choisissez le jeu de données à explorer", list(dataframes.keys()))
    df = dataframes[tab]
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.write(f"**Nombre d'annonces :** {len(df)}")
        if 'Prix' in df.columns:
            prix_clean = pd.to_numeric(df['Prix'].str.replace(r'[^\d]', '', regex=True), errors='coerce')
            st.write(f"**Prix moyen :** {prix_clean.mean():,.0f} FCFA")
        if 'Marque et annee' in df.columns:
            marques = df['Marque et annee'].str.split().str[0].value_counts().head(10)
            st.bar_chart(marques)
    else:
        st.warning("Aucune donnée à afficher.")

elif page == "Téléchargement":
    st.title("Télécharger les fichiers de données")
    for name, path in files.items():
        if os.path.exists(path):
            with open(path, "rb") as f:
                st.download_button(f"Télécharger {name}", f, file_name=os.path.basename(path))
        else:
            st.info(f"Fichier {name} non trouvé.")

elif page == "Scraper":
    st.title("Scraper les données (100 pages max)")
    st.write("Cliquez sur le bouton pour lancer le scraping. Cela peut prendre plusieurs minutes.")
    if st.button("Lancer le scraping"):
        with st.spinner("Scraping en cours..."):
            result = subprocess.run(["python", "scraper.py"], capture_output=True, text=True)
            if result.returncode == 0:
                st.success("Scraping terminé. Les données sont à jour.")
            else:
                st.error(f"Erreur lors du scraping : {result.stderr}")

elif page == "Évaluation":
    st.title("Évaluation de l'application")
    note = st.slider("Notez l'application", 1, 5, 3)
    commentaire = st.text_area("Votre commentaire")
    if st.button("Envoyer l'évaluation"):
        with open("evaluations.csv", "a", encoding="utf-8") as f:
            f.write(f"{note};{commentaire}\n")
        st.success("Merci pour votre retour !") 