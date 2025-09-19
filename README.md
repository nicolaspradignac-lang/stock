# EasyBeer – Autonomie des stocks

Application **Streamlit** connectée à l'API EasyBeer pour suivre en temps réel l'autonomie des stocks.

## 🚀 Installation

```bash
git clone https://github.com/ton-compte/easybeer-autonomie.git
cd easybeer-autonomie
pip install -r requirements.txt
cp .env.example .env
```

Édite `.env` et mets tes identifiants API EasyBeer.

## ▶️ Lancer en local

```bash
streamlit run streamlit_autonomie.py
```

## ☁️ Déploiement Streamlit Cloud

Ajoute dans **Secrets** :

```toml
EASYBEER_USER = "ton_identifiant_api"
EASYBEER_PASS = "ton_mot_de_passe_api"
```
