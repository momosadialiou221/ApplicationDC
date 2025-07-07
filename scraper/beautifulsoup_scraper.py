import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import streamlit as st


def scraper_multi_pages(nb_pages=10, categorie="voitures"):
    urls = {
        "voitures": "https://dakar-auto.com/senegal/voitures-4?page=",
        "motos": "https://dakar-auto.com/senegal/motos-and-scooters-3?page=",
        "location": "https://dakar-auto.com/senegal/location-de-voitures-19?page="
    }

    url_base = urls.get(categorie)
    if not url_base:
        raise ValueError(f"Catégorie inconnue : {categorie}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    data = []
    total_containers_found = 0

    for page in range(1, nb_pages + 1):
        url = f"{url_base}{page}"
        
        try:
            # Afficher le progrès
            if 'st' in globals():
                st.write(f"Scraping page {page}/{nb_pages}...")
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Chercher les cartes d'annonces avec le bon sélecteur
            containers = soup.select("div.listing-card")
            
            if 'st' in globals():
                st.write(f"Trouvé {len(containers)} annonces sur la page {page}")
            
            page_containers_found = 0
            
            for container in containers:
                try:
                    # Extraire le titre (marque et année)
                    title_element = container.select_one("h2.listing-card__header__title a")
                    marque_annee = title_element.get_text(strip=True) if title_element else "Non spécifié"
                    
                    # Extraire le prix
                    price_element = container.select_one("h3.listing-card__header__price")
                    prix = price_element.get_text(strip=True) if price_element else "Non spécifié"
                    
                    # Extraire l'adresse
                    address_element = container.select_one("div.entry-zone-address")
                    adresse = address_element.get_text(strip=True) if address_element else "Non spécifié"
                    
                    # Extraire les attributs (kilométrage, boîte, carburant)
                    attributes = container.select("li.listing-card__attribute.list-inline-item")
                    km = boite = carburant = "Non spécifié"
                    
                    for attr in attributes:
                        text = attr.get_text(strip=True)
                        if "km" in text.lower():
                            km = text
                        elif any(k in text.lower() for k in ["manuelle", "auto", "automatique"]):
                            boite = text
                        elif any(f in text.lower() for f in ["essence", "diesel", "électrique", "hybride"]):
                            carburant = text
                    
                    # Extraire la référence
                    ref_element = container.select_one("li.listing-card__attribute.list-inline-item b")
                    reference = ""
                    if ref_element and ref_element.next_sibling:
                        reference = ref_element.next_sibling.strip()
                    
                    # Extraire le propriétaire
                    owner_element = container.select_one("p.time-author a")
                    proprietaire = owner_element.get_text(strip=True) if owner_element else "Non spécifié"
                    
                    # Sauvegarder les données seulement si on a au moins un titre ou prix
                    if marque_annee != "Non spécifié" or prix != "Non spécifié":
                        data.append({
                            "categorie": categorie,
                            "Marque et annee": marque_annee,
                            "Prix": prix,
                            "Adresse": adresse,
                            "Kilometrage": km,
                            "Boite_vitesse": boite,
                            "Carburant": carburant,
                            "Reference": reference,
                            "Proprietaire": proprietaire,
                        })
                        page_containers_found += 1

                except Exception as e:
                    if 'st' in globals():
                        st.warning(f"Erreur lors de l'extraction d'une annonce: {str(e)}")
                    continue
            
            total_containers_found += page_containers_found
            
            if 'st' in globals():
                st.write(f"Page {page}: {page_containers_found} annonces extraites")
            
            # Pause entre les requêtes
            time.sleep(2)
            
        except requests.exceptions.RequestException as e:
            if 'st' in globals():
                st.error(f"Erreur lors de la requête page {page}: {str(e)}")
            continue
        except Exception as e:
            if 'st' in globals():
                st.error(f"Erreur inattendue page {page}: {str(e)}")
            continue

    # Convertir en DataFrame
    df = pd.DataFrame(data)
    
    if 'st' in globals():
        st.write(f"Scraping terminé. Total: {len(df)} annonces trouvées sur {total_containers_found} conteneurs analysés")
    
    return df 