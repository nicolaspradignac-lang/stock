# EasyBeer Stock Viewer

Une application **Streamlit** connectée à l'API EasyBeer pour suivre en temps réel le stock de bouteilles vides.

## 🚀 Installation

1. Clone le repo :
   ```bash
   git clone https://github.com/ton-compte/easybeer-stock.git
   cd easybeer-stock
   ```

2. Crée ton environnement virtuel et installe les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Copie `.env.example` en `.env` et renseigne tes identifiants API EasyBeer :
   ```bash
   cp .env.example .env
   ```

4. Lance l’application Streamlit :
   ```bash
   streamlit run streamlit_app.py
   ```

## 🛠 Fonctionnalités
- Recherche de bouteilles vides via `autocomplete`
- Affichage du stock disponible
- Détail par référence (quantité, seuils, entrepôt)
- Export DataFrame via Streamlit

## 🔒 Sécurité
Ne **jamais** commit ton fichier `.env` (identifiants API). Ils sont exclus par `.gitignore`.
