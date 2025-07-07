import streamlit as st
import pandas as pd
from scraper.beautifulsoup_scraper import scraper_multi_pages
from dashboard.visualisations import afficher_dashboard
from form.evaluation import afficher_formulaire

# --- Configuration de la page ---
st.set_page_config(page_title="Dakar auto scrapper", layout="wide")
st.title("Bienvenue dans Dakar auto scrapper")
st.markdown("Explorez, téléchargez, visualisez et évaluez.")

# --- Chargement du style CSS ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

menu = st.sidebar.radio("Navigation", [
    "Scraper les données (nettoyées)",
    "Télécharger les données brutes",
    "Visualiser le dashboard",
    "Donner votre avis"
])

# --- Fichiers de données ---
fichiers_bruts = {
    "Les Voitures à vendre": "data/dakar-auto_datacolection_100page.xlsx",
    "Les motos à vendre": "data/dakar-auto_Motos_54page.xlsx",
    "Les voitures d'occasion à vendre": "data/dakar-auto_Occasion_8page.xlsx"
}

fichiers_nettoyes = {
    "Les voitures à vendre": "data/dakar-auto_datacolection_100page.csv",
    "Les motos à vendre": "data/dakar-auto_Motos_54page.csv",
    "Les voitures d'occasion à vendre": "data/dakar-auto_Occasion_8page.csv"
}

# --- Scraping ---
if menu == "Scraper les données (nettoyées)":
    st.header("Scraping des données automobilières")
    
    # Mapping des catégories d'affichage vers les catégories du scraper
    categorie_mapping = {
        "Les voitures à vendre": "voitures",
        "Les motos à vendre": "motos",
        "Les voitures d'occasion à vendre": "location"
    }
    
    # Choix de la catégorie
    categorie_display = st.selectbox("Choisissez une catégorie à scraper :", [
        "Les voitures à vendre",
        "Les motos à vendre",
        "Les voitures d'occasion à vendre"
    ])

    # Choix du nombre de pages
    votre_choix = 100 
    nb_pages = st.slider("Nombre de pages à scraper :", min_value=1, max_value=votre_choix, value=10)

    # Scraper les données
    if st.button("Lancer le scraping"):
        with st.spinner(f"Scraping {categorie_display} sur {nb_pages} page(s)..."):
            # Utiliser la catégorie mappée pour le scraper
            categorie_scraper = categorie_mapping[categorie_display]
            df = scraper_multi_pages(nb_pages, categorie_scraper)  
           
            nom_fichier = {
                "Les voitures à vendre": "data/dakar-auto_datacolection_100page.csv",
                "Les motos à vendre": "data/dakar-auto_Motos_54page.csv",
                "Les voitures d'occasion à vendre": "data/dakar-auto_Occasion_8page.csv"
            }[categorie_display]
            df.to_csv(nom_fichier, index=False)
            st.success(f"Scraping terminé : {len(df)} annonces récupérées.")
            st.dataframe(df.head())

# --- Téléchargement des données brutes ---
elif menu == "Télécharger les données brutes":
    st.header("Téléchargement des données brutes")
    st.markdown("Téléchargez les fichiers originaux au format `.csv` extraits avec Web Scraper.")

    for titre, chemin in fichiers_bruts.items():
        try:
            df = pd.read_excel(chemin)
            st.download_button(
                label=f"Télécharger : {titre}",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=chemin.replace("data/", "").replace(".xlsx", ".csv"),
                mime="text/csv"
            )
        except FileNotFoundError:
            st.error(f"Fichier non trouvé : {chemin}")
        except Exception as e:
            st.error(f"Erreur lors du chargement de {chemin}: {str(e)}")

# --- Visualisation Dashboard ---
elif menu == "Visualiser le dashboard":
    st.header("Dashboard des données nettoyées")
    choix = st.selectbox("Sélectionnez une catégorie :", list(fichiers_nettoyes.keys()))
    try:
        df = pd.read_csv(fichiers_nettoyes[choix])
        afficher_dashboard(df, choix)
    except FileNotFoundError:
        st.error(f"Fichier non trouvé : {fichiers_nettoyes[choix]}")
        st.info("Veuillez d'abord scraper les données pour cette catégorie.")
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {str(e)}")

# --- Évaluation de l'application ---
elif menu == "Donner votre avis":
    st.header("Donnez votre avis")
    afficher_formulaire()