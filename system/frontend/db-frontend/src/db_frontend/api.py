import os
import requests

BASE_URL = os.environ.get("DB_API_URL", "http://localhost:8000")
HEADERS = {}

def alle_spender() -> list[dict]:
    r = requests.get(f"{BASE_URL}/spender", timeout=5)
    r.raise_for_status()
    return r.json()

def spender_create(vorname: str, nachname: str, geburtsdatum: str,
                    blutgruppe: str, email: str) -> dict:
    payload = {
        "vorname": vorname,
        "nachname": nachname,
        "geburtsdatum": geburtsdatum,
        "blutgruppe": blutgruppe,
        "email": email,
    }
    r = requests.post(f"{BASE_URL}/spender", json=payload,
                       headers=HEADERS, timeout=5)
    r.raise_for_status()
    return r.json()

def alle_zentren() -> list[dict]:
    r = requests.get(f"{BASE_URL}/spendezentrum", timeout=5)
    r.raise_for_status()
    return r.json()

def zentrum_create(name: str, adresse: str, stadt: str) -> dict:
    payload = {"name": name, "adresse": adresse, "stadt": stadt}
    r = requests.post(f"{BASE_URL}/spendezentrum", json=payload,
                       headers=HEADERS, timeout=5)
    r.raise_for_status()
    return r.json()

def alle_spenden() -> list[dict]:
    r = requests.get(f"{BASE_URL}/spende", timeout=5)
    r.raise_for_status()
    return r.json()

def spende_create(spender_id: int, zentrum_id: int,
                   spende_datum: str, menge_ml: int) -> dict:
    payload = {
        "spender_id": spender_id,
        "zentrum_id": zentrum_id,
        "spende_datum": spende_datum,
        "menge_ml": menge_ml,
    }
    r = requests.post(f"{BASE_URL}/spende", json=payload,
                       headers=HEADERS, timeout=5)
    r.raise_for_status()
    return r.json()
