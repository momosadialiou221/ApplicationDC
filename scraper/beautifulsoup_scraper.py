import pandas as pd

def scraper_multi_pages(nb_pages, categorie_scraper):
    # Dummy data for demonstration
    data = [{
        'Marque et annee': 'Test 2020',
        'Prix': '1 000 000 FCFA',
        'Adresse': 'Dakar',
        'Kilometrage': '10000 km',
        'Boite_vitesse': 'Manuelle',
        'Carburant': 'Essence',
        'Proprietaire': 'Testeur'
    } for _ in range(nb_pages)]
    return pd.DataFrame(data) 