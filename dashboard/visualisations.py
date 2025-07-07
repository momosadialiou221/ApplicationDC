import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def afficher_dashboard(df, choix):
    st.write(f"## Dashboard pour : {choix}")
    
    # Statistiques générales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Nombre total d'annonces", len(df))
    with col2:
        if 'Prix' in df.columns:
            prix_clean = pd.to_numeric(df['Prix'].str.replace(r'[^\d]', '', regex=True), errors='coerce')
            st.metric("Prix moyen", f"{prix_clean.mean():,.0f} FCFA")
    with col3:
        if 'Marque et annee' in df.columns:
            marques = df['Marque et annee'].str.split().str[0].value_counts()
            st.metric("Marques différentes", len(marques))
    with col4:
        if 'Adresse' in df.columns:
            villes = df['Adresse'].str.split(',').str[0].value_counts()
            st.metric("Villes différentes", len(villes))
    
    # Tableau des données
    st.subheader("📊 Données complètes")
    st.dataframe(df, use_container_width=True)
    
    # Graphiques
    if len(df) > 0:
        st.subheader("📈 Visualisations")
        
        # 1. Répartition des marques
        if 'Marque et annee' in df.columns:
            st.write("### Répartition des marques")
            marques = df['Marque et annee'].str.split().str[0].value_counts().head(10)
            fig_marques = px.bar(
                x=marques.index, 
                y=marques.values,
                title="Top 10 des marques les plus fréquentes",
                labels={'x': 'Marque', 'y': 'Nombre d\'annonces'}
            )
            st.plotly_chart(fig_marques, use_container_width=True)
        
        # 2. Distribution des prix
        if 'Prix' in df.columns:
            st.write("### Distribution des prix")
            prix_clean = pd.to_numeric(df['Prix'].str.replace(r'[^\d]', '', regex=True), errors='coerce')
            prix_clean = prix_clean.dropna()
            
            if len(prix_clean) > 0:
                fig_prix = px.histogram(
                    x=prix_clean,
                    nbins=20,
                    title="Distribution des prix",
                    labels={'x': 'Prix (FCFA)', 'y': 'Nombre d\'annonces'}
                )
                st.plotly_chart(fig_prix, use_container_width=True)
        
        # 3. Répartition géographique
        if 'Adresse' in df.columns:
            st.write("### Répartition géographique")
            villes = df['Adresse'].str.split(',').str[0].value_counts().head(10)
            fig_villes = px.pie(
                values=villes.values,
                names=villes.index,
                title="Top 10 des villes"
            )
            st.plotly_chart(fig_villes, use_container_width=True)
        
        # 4. Types de boîtes de vitesse
        if 'Boite_vitesse' in df.columns:
            st.write("### Types de boîtes de vitesse")
            boites = df['Boite_vitesse'].value_counts()
            fig_boites = px.bar(
                x=boites.index,
                y=boites.values,
                title="Répartition des boîtes de vitesse",
                labels={'x': 'Type de boîte', 'y': 'Nombre d\'annonces'}
            )
            st.plotly_chart(fig_boites, use_container_width=True)
        
        # 5. Types de carburant
        if 'Carburant' in df.columns:
            st.write("### Types de carburant")
            carburants = df['Carburant'].value_counts()
            fig_carburants = px.pie(
                values=carburants.values,
                names=carburants.index,
                title="Répartition des types de carburant"
            )
            st.plotly_chart(fig_carburants, use_container_width=True)
        
        # 6. Distribution des kilométrages
        if 'Kilometrage' in df.columns:
            st.write("### Distribution des kilométrages")
            km_clean = pd.to_numeric(df['Kilometrage'].str.replace(r'[^\d]', '', regex=True), errors='coerce')
            km_clean = km_clean.dropna()
            
            if len(km_clean) > 0:
                fig_km = px.histogram(
                    x=km_clean,
                    nbins=15,
                    title="Distribution des kilométrages",
                    labels={'x': 'Kilométrage (km)', 'y': 'Nombre d\'annonces'}
                )
                st.plotly_chart(fig_km, use_container_width=True)
        
        # 7. Évolution des prix par marque (si année disponible)
        if 'Marque et annee' in df.columns and 'Prix' in df.columns:
            st.write("### Prix moyen par marque")
            df_copy = df.copy()
            df_copy['Marque'] = df_copy['Marque et annee'].str.split().str[0]
            df_copy['Prix_num'] = pd.to_numeric(df_copy['Prix'].str.replace(r'[^\d]', '', regex=True), errors='coerce')
            
            prix_par_marque = df_copy.groupby('Marque')['Prix_num'].mean().sort_values(ascending=False).head(10)
            
            fig_prix_marque = px.bar(
                x=prix_par_marque.index,
                y=prix_par_marque.values,
                title="Prix moyen par marque (Top 10)",
                labels={'x': 'Marque', 'y': 'Prix moyen (FCFA)'}
            )
            st.plotly_chart(fig_prix_marque, use_container_width=True)
    
    else:
        st.warning("Aucune donnée à visualiser. Veuillez d'abord scraper des données.") 