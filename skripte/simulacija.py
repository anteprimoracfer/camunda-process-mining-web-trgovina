"""
Simulacija procesa "Obrada narudžbe u web-trgovini" na Camundi 8.

Skripta radi dvije stvari:
  1. pokreće zadani broj instanci procesa (REST API: POST /v2/process-instances)
  2. radi kao job worker: preuzima zadatke tipa "web-trgovina", dovršava ih
     nasumičnim redoslijedom i s malim nasumičnim kašnjenjem, te pritom
     postavlja varijable o kojima ovise grananja.

Nasumičan redoslijed dovršavanja bitan je za process mining: tako se
paralelne grane (naplata, pakiranje, račun) u logu pojavljuju u
različitim redoslijedima, kao u stvarnom paralelnom izvršavanju.

Pokretanje:
    pip install requests
    python simulacija.py --instance 300
"""

import argparse
import random
import time

import requests

# --- Postavke (po potrebi prilagodi) ---------------------------------------
BASE_URL = "http://localhost:8080/v2"
AUTH = ("demo", "demo")            # zadani korisnik lokalne Camunde 8 Run
PROCESS_ID = "ObradaNarudzbe"
JOB_TYPE = "web-trgovina"

# Vjerojatnosti grananja
P_NA_ZALIHI = 0.75                 # roba je na zalihi
P_DOBAVLJAC = 0.70                 # dobavljač može isporučiti
P_PLACANJE = 0.80                  # pojedini pokušaj naplate uspijeva
MAX_POKUSAJA_NAPLATE = 3           # najkasnije treći pokušaj uspijeva
P_KURIR = 0.65                     # dostava kurirom (inače osobno preuzimanje)

# Završne aktivnosti: kad se jedna od njih dovrši, instanca je gotova
ZAVRSNE_AKTIVNOSTI = {"Task_ZatvoriNarudzbu", "Task_OtkaziNarudzbu"}
# ---------------------------------------------------------------------------

session = requests.Session()
session.auth = AUTH
session.headers.update({"Content-Type": "application/json"})


def pokreni_instancu():
    varijable = {
        "nacinDostave": "kurir" if random.random() < P_KURIR else "osobno",
        "brojPokusajaNaplate": 0,
    }
    r = session.post(f"{BASE_URL}/process-instances", json={
        "processDefinitionId": PROCESS_ID,
        "variables": varijable,
    })
    r.raise_for_status()
    return r.json().get("processInstanceKey")


def odluci(job):
    """Vraća varijable koje worker postavlja pri dovršavanju zadatka."""
    aktivnost = job["elementId"]
    var = job.get("variables") or {}

    if aktivnost == "Task_ProvjeriZalihe":
        return {"naZalihi": random.random() < P_NA_ZALIHI}

    if aktivnost == "Task_NaruciOdDobavljaca":
        return {"dobavljacDostupan": random.random() < P_DOBAVLJAC}

    if aktivnost == "Task_Naplati":
        pokusaj = int(var.get("brojPokusajaNaplate", 0)) + 1
        uspjeh = pokusaj >= MAX_POKUSAJA_NAPLATE or random.random() < P_PLACANJE
        return {"placanjeUspjesno": uspjeh, "brojPokusajaNaplate": pokusaj}

    return {}


def aktiviraj_poslove():
    r = session.post(f"{BASE_URL}/jobs/activation", json={
        "type": JOB_TYPE,
        "worker": "simulator",
        "timeout": 60000,
        "maxJobsToActivate": 50,
        "requestTimeout": 2000,
    })
    r.raise_for_status()
    return r.json().get("jobs", [])


def dovrsi_posao(job, varijable):
    r = session.post(f"{BASE_URL}/jobs/{job['jobKey']}/completion",
                     json={"variables": varijable})
    r.raise_for_status()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", type=int, default=300,
                        help="broj instanci procesa koje treba pokrenuti")
    parser.add_argument("--seed", type=int, default=None,
                        help="sjeme generatora slučajnih brojeva (za ponovljivost)")
    args = parser.parse_args()
    if args.seed is not None:
        random.seed(args.seed)

    print(f"Pokrećem {args.instance} instanci procesa {PROCESS_ID}...")
    for i in range(args.instance):
        pokreni_instancu()
        if (i + 1) % 50 == 0:
            print(f"  pokrenuto {i + 1}")

    zavrseno = 0
    dovrseno_poslova = 0
    print("Worker radi...")
    while zavrseno < args.instance:
        poslovi = aktiviraj_poslove()
        random.shuffle(poslovi)          # nasumičan redoslijed dovršavanja
        for job in poslovi:
            time.sleep(random.uniform(0.01, 0.08))
            dovrsi_posao(job, odluci(job))
            dovrseno_poslova += 1
            if job["elementId"] in ZAVRSNE_AKTIVNOSTI:
                zavrseno += 1
        if poslovi:
            print(f"  dovršeno poslova: {dovrseno_poslova}, "
                  f"završenih instanci: {zavrseno}/{args.instance}")

    print("Gotovo. Pričekaj desetak sekundi pa pokreni izvoz_loga.py.")


if __name__ == "__main__":
    main()
