import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URLs à scraper
URLS = [
    {
        'url': 'https://dakar-auto.com/senegal/voitures-4',
        'type': 'voitures',
        'fields': ['Marque et annee', 'Prix', 'Adresse', 'Kilometrage', 'Boite_vitesse', 'Carburant', 'Proprietaire'],
    },
    {
        'url': 'https://dakar-auto.com/senegal/motos-and-scooters-3',
        'type': 'motos',
        'fields': ['Marque et annee', 'Prix', 'Adresse', 'Kilometrage', 'Proprietaire'],
    },
    {
        'url': 'https://dakar-auto.com/senegal/location-de-voitures-19',
        'type': 'location',
        'fields': ['Marque et annee', 'Prix', 'Adresse', 'Proprietaire'],
    },
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def get_soup(url):
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, 'html.parser')


def parse_voiture_card(card):
    # À adapter selon la structure réelle du site
    marque_annee = card.find('h2').get_text(strip=True) if card.find('h2') else ''
    prix = card.find(class_='price').get_text(strip=True) if card.find(class_='price') else ''
    adresse = card.find(class_='location').get_text(strip=True) if card.find(class_='location') else ''
    kilometrage = ''
    boite = ''
    carburant = ''
    proprietaire = ''
    details = card.find_all('li')
    for li in details:
        txt = li.get_text(strip=True)
        if 'km' in txt:
            kilometrage = txt
        elif 'Manuelle' in txt or 'Automatique' in txt:
            boite = txt
        elif 'Essence' in txt or 'Diesel' in txt or 'Hybride' in txt:
            carburant = txt
        elif 'Propriétaire' in txt:
            proprietaire = txt.replace('Propriétaire:', '').strip()
    return [marque_annee, prix, adresse, kilometrage, boite, carburant, proprietaire]

def parse_moto_card(card):
    marque_annee = card.find('h2').get_text(strip=True) if card.find('h2') else ''
    prix = card.find(class_='price').get_text(strip=True) if card.find(class_='price') else ''
    adresse = card.find(class_='location').get_text(strip=True) if card.find(class_='location') else ''
    kilometrage = ''
    proprietaire = ''
    details = card.find_all('li')
    for li in details:
        txt = li.get_text(strip=True)
        if 'km' in txt:
            kilometrage = txt
        elif 'Propriétaire' in txt:
            proprietaire = txt.replace('Propriétaire:', '').strip()
    return [marque_annee, prix, adresse, kilometrage, proprietaire]

def parse_location_card(card):
    marque_annee = card.find('h2').get_text(strip=True) if card.find('h2') else ''
    prix = card.find(class_='price').get_text(strip=True) if card.find(class_='price') else ''
    adresse = card.find(class_='location').get_text(strip=True) if card.find(class_='location') else ''
    proprietaire = ''
    details = card.find_all('li')
    for li in details:
        txt = li.get_text(strip=True)
        if 'Propriétaire' in txt:
            proprietaire = txt.replace('Propriétaire:', '').strip()
    return [marque_annee, prix, adresse, proprietaire]


def scrape_category(url, type_, fields, max_pages=100):
    data = []
    for page in range(1, max_pages+1):
        page_url = f"{url}?page={page}"
        print(f"Scraping {type_} - page {page}")
        soup = get_soup(page_url)
        cards = soup.find_all('div', class_='listing-item')
        if not cards:
            break
        for card in cards:
            if type_ == 'voitures':
                row = parse_voiture_card(card)
            elif type_ == 'motos':
                row = parse_moto_card(card)
            elif type_ == 'location':
                row = parse_location_card(card)
            else:
                continue
            data.append([type_] + row)
        time.sleep(1)  # Pour éviter d'être bloqué
    return data


def main():
    all_data = []
    for cat in URLS:
        if cat['type'] == 'voitures':
            fields = ['categorie', 'Marque et annee', 'Prix', 'Adresse', 'Kilometrage', 'Boite_vitesse', 'Carburant', 'Proprietaire']
        elif cat['type'] == 'motos':
            fields = ['categorie', 'Marque et annee', 'Prix', 'Adresse', 'Kilometrage', 'Proprietaire']
        elif cat['type'] == 'location':
            fields = ['categorie', 'Marque et annee', 'Prix', 'Adresse', 'Proprietaire']
        else:
            continue
        data = scrape_category(cat['url'], cat['type'], fields)
        all_data.extend(data)
    # Harmonisation des colonnes (ajout de colonnes vides si besoin)
    max_cols = max(len(row) for row in all_data)
    for row in all_data:
        while len(row) < max_cols:
            row.append('')
    columns = ['categorie', 'Marque et annee', 'Prix', 'Adresse', 'Kilometrage', 'Boite_vitesse', 'Carburant', 'Proprietaire']
    df = pd.DataFrame(all_data, columns=columns)
    df.to_csv('scraped_data.csv', index=False)
    print('Scraping terminé. Données sauvegardées dans scraped_data.csv')

if __name__ == '__main__':
    main() 