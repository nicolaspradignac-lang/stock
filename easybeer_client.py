import os
import time
import requests
from requests.auth import HTTPBasicAuth

class EasyBeerClient:
    def __init__(self, base_url: str, username: str, password: str, timeout=20):
        self.base_url = base_url.rstrip("/")
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        self.timeout = timeout

    def _get(self, path: str, **kwargs):
        url = f"{self.base_url}{path}"
        for attempt in range(3):  # retry simple
            try:
                r = self.session.get(url, auth=self.auth, timeout=self.timeout, **kwargs)
                if r.status_code >= 200 and r.status_code < 300:
                    return r.json()
                msg = f"HTTP {r.status_code} on {url}: {r.text[:300]}"
                if r.status_code in (500, 502, 503) and attempt < 2:
                    time.sleep(0.8 * (attempt + 1))
                    continue
                raise RuntimeError(msg)
            except requests.RequestException as e:
                if attempt == 2:
                    raise
                time.sleep(0.8 * (attempt + 1))
        raise RuntimeError("Unreachable")

    # --- Bouteilles vides ---
    def search_empty_bottles(self, query: str):
        return self._get("/stock/bouteilles-vides/autocomplete", params={"query": query})

    def get_empty_bottle_stock(self, id_stock_bouteille: int):
        return self._get(f"/stock/bouteilles-vides/edition/{id_stock_bouteille}")

    def get_empty_bottles_lots(self):
        return self._get("/stock/bouteilles-vides/numeros-lots")

    def get_available_containers(self):
        return self._get("/stock/bouteilles/contenants-disponibles")
