"""
Izvoz loga izvršavanja procesa "Obrada narudžbe u web-trgovini" iz Camunde 8
u CSV datoteku pogodnu za uvoz u ProM.

Koristi REST API: POST /v2/element-instances/search
Izvozi samo dovršene servisne zadatke (aktivnosti), bez gatewaya i događaja.

Stupci CSV-a:
    case_id    - ključ instance procesa (jedan slučaj u process miningu)
    activity   - naziv aktivnosti
    start_time - vrijeme početka aktivnosti
    end_time   - vrijeme završetka aktivnosti

Pokretanje:
    python izvoz_loga.py
"""

import csv

import requests

BASE_URL = "http://localhost:8080/v2"
AUTH = ("demo", "demo")
PROCESS_ID = "ObradaNarudzbe"
IZLAZNA_DATOTEKA = "log_web_trgovina.csv"
VELICINA_STRANICE = 500

session = requests.Session()
session.auth = AUTH
session.headers.update({"Content-Type": "application/json"})


def dohvati_sve():
    zapisi = []
    kursor = None
    while True:
        page = {"limit": VELICINA_STRANICE}
        if kursor:
            page["after"] = kursor
        r = session.post(f"{BASE_URL}/element-instances/search", json={
            "filter": {
                "processDefinitionId": PROCESS_ID,
                "type": "SERVICE_TASK",
                "state": "COMPLETED",
            },
            "sort": [{"field": "startDate", "order": "ASC"}],
            "page": page,
        })
        r.raise_for_status()
        podaci = r.json()
        stavke = podaci.get("items", [])
        zapisi.extend(stavke)
        kursor = (podaci.get("page") or {}).get("endCursor")
        print(f"  dohvaćeno {len(zapisi)} zapisa")
        if len(stavke) < VELICINA_STRANICE or not kursor:
            break
    return zapisi


def main():
    print("Dohvaćam povijest izvršavanja...")
    zapisi = dohvati_sve()

    # Sortiranje po slučaju pa po vremenu završetka aktivnosti
    zapisi.sort(key=lambda z: (z["processInstanceKey"], z.get("endDate") or ""))

    with open(IZLAZNA_DATOTEKA, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "activity", "start_time", "end_time"])
        for z in zapisi:
            w.writerow([
                z["processInstanceKey"],
                z.get("elementName") or z["elementId"],
                z.get("startDate"),
                z.get("endDate"),
            ])

    slucajevi = len({z["processInstanceKey"] for z in zapisi})
    print(f"Spremljeno {len(zapisi)} događaja iz {slucajevi} slučajeva "
          f"u {IZLAZNA_DATOTEKA}.")


if __name__ == "__main__":
    main()
