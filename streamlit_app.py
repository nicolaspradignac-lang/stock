import os
import pandas as pd
import streamlit as st
from easybeer_client import EasyBeerClient

st.set_page_config(page_title="Stock bouteilles vides", layout="wide")
st.title("Stock bouteilles vides – EasyBeer")

api = EasyBeerClient(
    base_url="https://api.easybeer.fr",
    username=os.getenv("EASYBEER_USER", "demo_user"),
    password=os.getenv("EASYBEER_PASS", "demo_pass")
)

query = st.text_input("Recherche (ex: 33, 75, 'bouteille')", "33")

try:
    results = api.search_empty_bottles(query)
    if not results:
        st.info("Aucune référence trouvée.")
    else:
        df = pd.DataFrame(results)[["idStockBouteille", "libelle", "entrepot", "quantiteDisponible", "seuilBas", "seuilHaut"]]
        st.dataframe(df, use_container_width=True)

        selected = st.selectbox("Choisir une référence pour le détail", options=df["idStockBouteille"], format_func=lambda _id: df.loc[df["idStockBouteille"]==_id, "libelle"].iloc[0])
        if selected:
            detail = api.get_empty_bottle_stock(int(selected))
            st.subheader("Détail de la référence")
            st.json(detail)
except Exception as e:
    st.error(f"Erreur API: {e}")
