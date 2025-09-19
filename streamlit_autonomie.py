# Streamlit app pour autonomie des stocks EasyBeer
import os
import pandas as pd
import streamlit as st
from requests.auth import HTTPBasicAuth
import requests

# dotenv local (optionnel)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

BASE_URL = "https://api.easybeer.fr"

def get_credentials():
    user = None
    pwd = None
    if hasattr(st, "secrets"):
        user = st.secrets.get("EASYBEER_USER", None)
        pwd = st.secrets.get("EASYBEER_PASS", None)
    user = user or os.getenv("EASYBEER_USER")
    pwd = pwd or os.getenv("EASYBEER_PASS")
    return user, pwd

class EasyBeerClient:
    def __init__(self, base_url, username, password, timeout=30):
        self.base_url = base_url.rstrip("/")
        self.auth = HTTPBasicAuth(username, password)
        self.s = requests.Session()
        self.s.headers.update({"Accept": "application/json"})
        self.timeout = timeout

    def post(self, path, params=None, json_body=None):
        url = f"{self.base_url}{path}"
        r = self.s.post(url, params=params, json=json_body, auth=self.auth, timeout=self.timeout)
        if r.status_code < 200 or r.status_code >= 300:
            raise RuntimeError(f"HTTP {r.status_code} on {url}:\n{r.text[:500]}")
        try:
            return r.json()
        except:
            return r.text

st.set_page_config(page_title="Autonomie des stocks – EasyBeer", layout="wide")
st.title("Autonomie des stocks – EasyBeer")

username, password = get_credentials()
if not (username and password):
    st.error("Identifiants API manquants (EASYBEER_USER / EASYBEER_PASS).")
    st.stop()

api = EasyBeerClient(BASE_URL, username, password)

PERIODE_CALCUL = ["JOUR", "SEMAINE", "MOIS", "ANNEE"]
PERIODE_REFERENCE_TYPES = [
    "AUJOURDHUI", "SEMAINE_COURANTE", "MOIS_COURANT", "TRIMESTRE_COURANT",
    "SEMESTRE_COURANT", "PERIODE_COURANTE", "ANNEE_COURANTE",
    "EXERCICE_COMPTABLE_COURANT", "HIER", "SEMAINE_DERNIERE", "MOIS_DERNIER",
    "TRIMESTRE_DERNIER", "SEMESTRE_DERNIER", "ANNEE_DERNIERE",
    "EXERCICE_COMPTABLE_DERNIER", "MEME_JOUR_ANNEE_DERNIERE",
    "MEME_SEMAINE_ANNEE_DERNIERE", "MEME_MOIS_ANNEE_DERNIERE",
    "MEME_TRIMESTRE_ANNEE_DERNIERE", "MEME_SEMESTRE_ANNEE_DERNIERE",
    "MEME_PERIODE_ANNEE_DERNIERE", "DEMAIN", "SEMAINE_SUIVANTE", "MOIS_SUIVANT",
    "TRIMESTRE_SUIVANT", "SEMESTRE_SUIVANT", "ANNEE_SUIVANTE",
    "SEMAINE_GLISSANTE", "MOIS_GLISSANT", "TRIMESTRE_GLISSANT",
    "SEMESTRE_GLISSANT", "ANNEE_GLISSANTE"
]

with st.sidebar:
    st.header("Paramètres")
    periode_calcul = st.selectbox("Unité d'analyse", PERIODE_CALCUL, index=0)
    periode_ref_type = st.selectbox("Période de référence", PERIODE_REFERENCE_TYPES, index=28)  # TRIMESTRE_GLISSANT
    entrepot_id = st.number_input("ID Entrepôt", min_value=0, value=1, step=1)
    ids_text = st.text_area("IDs (séparés par virgules)", value="111377,111687,131955")
    ids = [int(x.strip()) for x in ids_text.split(",") if x.strip().isdigit()]
    force_refresh = st.checkbox("Force refresh", value=True)
    run = st.button("Calculer")

if run:
    body = {
        "periodeCalcul": periode_calcul,
        "periodeReference": {"type": periode_ref_type},
        "entrepotId": entrepot_id,
        "ids": ids
    }
    try:
        data = api.post("/indicateur/autonomie-stocks", params={"forceRefresh": str(force_refresh).lower()}, json_body=body)
        st.subheader("Réponse JSON")
        st.json(data)
        # Mise en table
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            for k in ["items", "lignes", "rows", "data", "contenu"]:
                if k in data and isinstance(data[k], list):
                    df = pd.DataFrame(data[k])
                    break
            else:
                df = pd.json_normalize(data)
        else:
            df = pd.DataFrame([{"valeur": data}])
        if not df.empty:
            st.subheader("Tableau")
            st.dataframe(df, use_container_width=True)
            st.download_button("⬇️ Export CSV", df.to_csv(index=False).encode("utf-8"),
                               file_name="autonomie_stocks.csv", mime="text/csv")
    except Exception as e:
        st.error(str(e))
