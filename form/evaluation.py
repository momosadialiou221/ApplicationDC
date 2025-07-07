import streamlit as st

def afficher_formulaire():
    note = st.slider("Notez l'application", 1, 5, 3)
    commentaire = st.text_area("Votre commentaire")
    if st.button("Envoyer l'évaluation"):
        with open("evaluations.csv", "a", encoding="utf-8") as f:
            f.write(f"{note};{commentaire}\n")
        st.success("Merci pour votre retour !") 