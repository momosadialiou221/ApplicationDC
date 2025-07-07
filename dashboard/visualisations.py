import streamlit as st

def afficher_dashboard(df, choix):
    st.write(f"Dashboard pour : {choix}")
    st.dataframe(df) 