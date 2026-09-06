#!/usr/bin/env python3
import requests
import sys

API_URL = "http://localhost:8000"
API_KEY = "geheimschluessel123"

def menu():
    print("\n=== Blutspende-Verwaltung ===")
    print("1) Spender anzeigen")
    print("2) Spender anlegen")
    print("3) Spendezentren anzeigen")
    print("4) Spendezentrum anlegen")
    print("5) Spenden anzeigen")
    print("6) Spende anlegen")
    print("0) Beenden")

def list_spender():
    r = requests.get(f"{API_URL}/spender")
    print(r.json())

def create_spender():
    vorname = input("Vorname: ")
    nachname = input("Nachname: ")
    geburtsdatum = input("Geburtsdatum (YYYY-MM-DD): ")
    blutgruppe = input("Blutgruppe: ")
    email = input("Email: ")
    data = {"vorname": vorname, "nachname": nachname, "geburtsdatum": geburtsdatum, "blutgruppe": blutgruppe, "email": email}
    r = requests.post(f"{API_URL}/spender", json=data, headers={"X-API-Key": API_KEY})
    print(r.json())

def list_zentrum():
    r = requests.get(f"{API_URL}/spendezentrum")
    print(r.json())

def create_zentrum():
    name = input("Name: ")
    adresse = input("Adresse: ")
    stadt = input("Stadt: ")
    data = {"name": name, "adresse": adresse, "stadt": stadt}
    r = requests.post(f"{API_URL}/spendezentrum", json=data, headers={"X-API-Key": API_KEY})
    print(r.json())

def list_spende():
    r = requests.get(f"{API_URL}/spende")
    print(r.json())

def create_spende():
    spender_id = input("Spender-ID: ")
    zentrum_id = input("Zentrum-ID: ")
    spende_datum = input("Datum (YYYY-MM-DD): ")
    menge_ml = input("Menge (ml): ")
    data = {"spender_id": int(spender_id), "zentrum_id": int(zentrum_id), "spende_datum": spende_datum, "menge_ml": int(menge_ml)}
    r = requests.post(f"{API_URL}/spende", json=data, headers={"X-API-Key": API_KEY})
    print(r.json())

def main():
    while True:
        menu()
        choice = input("Auswahl: ")
        if choice == "1":
            list_spender()
        elif choice == "2":
            create_spender()
        elif choice == "3":
            list_zentrum()
        elif choice == "4":
            create_zentrum()
        elif choice == "5":
            list_spende()
        elif choice == "6":
            create_spende()
        elif choice == "0":
            sys.exit(0)
        else:
            print("Ungültige Auswahl")

if __name__ == "__main__":
    main()
