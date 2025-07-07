# Dakar Auto Data App

Cette application permet de scraper, explorer, télécharger et évaluer des données d'annonces automobiles du site dakar-auto.com.

## Fonctionnalités
- **Scraping** de données sur plusieurs pages (voitures, motos, location)
- **Dashboard** interactif (tableau, stats, graphiques)
- **Téléchargement** des fichiers CSV (données scrapées et importées)
- **Formulaire d'évaluation** de l'application

## Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/momosadialiou221/ApplicationDC.git
   cd ApplicationDC
   ```
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation
1. **Lancer l'application Streamlit** :
   ```bash
   streamlit run app.py
   ```
2. **Scraper les données** :
   - Allez dans l'onglet "Scraper" et cliquez sur le bouton pour lancer le scraping (jusqu'à 100 pages par catégorie).
   - Les données sont sauvegardées dans `scraped_data.csv`.
3. **Explorer les données** :
   - Onglet "Dashboard" pour visualiser les annonces, stats, graphiques.
4. **Télécharger les fichiers** :
   - Onglet "Téléchargement" pour récupérer les CSV.
5. **Évaluer l'application** :
   - Onglet "Évaluation" pour donner une note/commentaire (stockés dans `evaluations.csv`).

## Structure du projet
```
.
├── app.py                        # Application Streamlit
├── scraper.py                    # Script de scraping
├── requirements.txt              # Dépendances Python
├── dakar-auto_datacolection_100page.csv   # Données importées
├── dakar-auto_Occasion_8page.csv          # Données importées
├── dakar-auto_Motos_54page.csv            # Données importées
├── scraped_data.csv              # Données scrapées (générées)
├── evaluations.csv               # Évaluations utilisateurs (généré)
└── README.md
```

## Remarques
- Le scraping peut prendre plusieurs minutes.
- Les fichiers CSV importés doivent être placés à la racine du projet.
- Pour toute question, ouvrez une issue sur le dépôt GitHub. 