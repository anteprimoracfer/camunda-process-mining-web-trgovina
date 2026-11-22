# Upute korak po korak

Ove upute opisuju cijeli postupak iz rada, uključujući zamke na koje se naišlo tijekom izrade.
Testirano na Windowsu s Camundom 8.10, Camunda Modelerom 5.52, Pythonom 3.15 i ProM-om 6.15.

## 1. Instalacija alata

### Camunda 8 (lokalno)

1. Provjerite Javu: `java -version`. Potreban je OpenJDK 21 do 25 (npr. Eclipse Temurin).
2. Instalirajte Node.js, a zatim Camundin alat za naredbeni redak:

   ```bash
   npm install @camunda8/cli -g
   c8ctl cluster start 8.10
   ```

3. Nakon pokretanja u terminalu se ispisuju adrese sučelja (Operate, Tasklist). Zadani korisnik je `demo` / `demo`,
   a REST API je na `http://localhost:8080/v2`.

Lokalna instalacija odabrana je umjesto Camunda SaaS-a jer probni klaster u oblaku vrijedi 30 dana,
a lokalno su povijest izvršavanja i podaci u potpunosti pod vašom kontrolom.

### Camunda Desktop Modeler

Preuzima se sa službene stranice Camunde (Download → Modeler). Ne zahtijeva instalaciju: raspakirajte arhivu i pokrenite.

### Python

Instalirajte Python 3 s python.org. **Na prvom zaslonu instalacije označite „Add python.exe to PATH“**,
inače naredba `python` u naredbenom retku neće raditi. Zatim:

```bash
python -m pip install -r requirements.txt
```

### ProM 6.15

Preuzima se s [promtools.org](https://promtools.org). **Važno:** nakon instalacije ProM često nema nijedan plugin
(gumb Import javlja *No import plugins available*). Pluginove treba instalirati upraviteljem paketa:

1. Zatvorite ProM i pokrenite upravitelj paketa (`ProMPM615.bat` ili `ProMPM615.exe` u instalacijskoj mapi,
   npr. `C:\Users\<korisnik>\ProM 6.15`). Pokretanje iz naredbenog retka prikazuje eventualne greške.
2. Na kartici **Not installed** instalirajte pakete: `Log`, `AlphaMiner`, `HeuristicsMiner`, `InductiveMiner`,
   `PNetReplayer` i `PNetAlignmentAnalysis` (ili skupni paket `RunnerUpPackages`, koji zauzima znatno više prostora).
3. Instalirani paketi pojavljuju se na kartici **Up to date**.

## 2. Deploy modela

1. Otvorite `bpmn/web_trgovina_c8.bpmn` u Camunda Modeleru (File → Open File).
2. Provjerite da je ciljna platforma Camunda 8 (donji desni kut).
3. Kliknite ikonu rakete (donji lijevi kut), odaberite lokalni klaster i potvrdite deploy.

Sve aktivnosti modelirane su kao servisni zadaci s tipom posla `web-trgovina`, a uvjeti na grananjima napisani su u FEEL-u.
Grananja ovise o varijablama `naZalihi`, `dobavljacDostupan`, `placanjeUspjesno` i `nacinDostave`, koje postavlja simulator.

**Zašto job workeri, a ne skripte?** Automatske skripte izvršile bi se jedna za drugom u istoj transakciji,
pa bi paralelne grane u logu uvijek imale isti redoslijed i nijedan algoritam ne bi otkrio paralelizam.
Vanjski worker dovršava zadatke nasumičnim redoslijedom, pa log sadrži stvarna ispreplitanja.

## 3. Simulacija

```bash
python skripte/simulacija.py --instance 300 --seed 42
```

Skripta pokreće zadani broj instanci, a zatim kao worker preuzima zadatke, dovršava ih nasumičnim redoslijedom
s kratkim kašnjenjem i postavlja varijable prema vjerojatnostima zadanima na vrhu datoteke:

| Parametar | Vrijednost |
| --- | --- |
| Roba na zalihi | 0,75 |
| Dobavljač može isporučiti | 0,70 |
| Pojedini pokušaj naplate uspijeva | 0,80 (treći pokušaj uvijek uspijeva) |
| Dostava kurirom | 0,65 |

Adresa i korisnik Camunde podešavaju se konstantama `BASE_URL` i `AUTH` na vrhu skripte.
Tijekom simulacije napredak se može pratiti u sučelju Operate.

## 4. Izvoz loga

Pričekajte desetak sekundi nakon simulacije (Camunda povijest upisuje asinkrono), pa pokrenite:

```bash
python skripte/izvoz_loga.py
```

Rezultat je `log_web_trgovina.csv` sa stupcima `case_id`, `activity`, `start_time` i `end_time`,
dobiven preko endpointa `/v2/element-instances/search`. Ako je broj događaja manji od broja dovršenih zadataka
koji je ispisala simulacija, pričekajte još malo i ponovite izvoz.

**Napomena:** CSV nemojte otvarati dvostrukim klikom u Excelu s hrvatskim postavkama (razdjelnik i dugački brojevi
pogrešno se prikazuju) i nikako ga ne spremajte iz Excela.

## 5. Analiza u ProM-u

**Savjet:** ProM ne pamti radni prostor i zna zablokirati. Svaki važan rezultat odmah izvezite
(log kao `.xes`, mreže kao `.pnml`). Prije rada zatvorite programe koji troše puno memorije.

### 5.1. Pretvorba CSV-a u XES

1. Kopirajte CSV u putanju bez razmaka i dijakritičkih znakova (npr. `C:\ProM`).
2. Workspace → **Import** → odaberite CSV.
3. Označite uvezenu datoteku, Actions → **Convert CSV to XES**:
   - razdjelnik: zarez, kodna stranica: UTF-8
   - Case column: `case_id`, Event column: `activity`
   - Completion time: `end_time`, Start time: bez odabira
   - format vremena (ako ga ProM ne prepozna sam): `yyyy-M-d'T'H:mm:ss.SSSXXX`
4. Provjerite sažetak loga. Za log iz rada: 300 slučajeva, 2265 događaja, 12 aktivnosti.

Vrijeme početka namjerno se izostavlja: paralelni gateway sve tri paralelne aktivnosti pokreće u istoj milisekundi,
pa vrijeme početka ne nosi informaciju o redoslijedu.

### 5.2. Otkrivanje procesa

Za sve algoritme klasifikator je **Event Name**.

| Algoritam | Plugin | Postavke |
| --- | --- | --- |
| Alpha Miner | Alpha Miner | klasična varijanta, izlaz Petri net |
| Heuristics Miner | Mine for a Heuristics Net using Heuristics Miner (onaj koji traži samo log) | zadane |
| Inductive Miner | Mine Petri net with Inductive Miner | varijanta **IM** (ne zadana IMf) |

Heuristička mreža za provjeru usklađenosti pretvara se pluginom **Convert Heuristics net into Petri net**.

### 5.3. Provjera usklađenosti

Plugin **Replay a Log on Petri Net for Conformance Analysis** (ne *…for All Optimal Alignments*):

- svrha *Measuring fitness*, *penalize improper completion* = **Yes**, algoritam **ILP-based replayer**
- mapiranje: 12 aktivnosti na istoimene, nevidljivi prijelazi (*tau*) na **NONE**
- troškovi: 1 za aktivnosti, **0 za nevidljive prijelaze**

Završno označavanje (ako ga ProM traži):

| Mreža | Završno mjesto |
| --- | --- |
| Inductive Miner | već je definirano uz mrežu |
| Alpha Miner | mjesto `End` |
| Heuristics Miner (pretvorena) | `po11` (izlazno mjesto aktivnosti *Zatvori narudžbu*) |

Pretvorena heuristička mreža nema zajedničko završno mjesto za zatvorene i otkazane narudžbe.
Pokušaj s praznim završnim označavanjem i *penalize improper completion* = No u ProM-u 6.15 završava greškom
(`NullPointerException`) i blokira čarobnjak, pa je korišteno mjesto `po11`, uz posljedicu da su otkazane narudžbe dodatno kažnjene.

Fitness se čita u desnom stupcu rezultata (*Alignment statistics* → **Trace Fitness**).
Preciznost i generalizacija računaju se pluginom **Measure Precision/Generalization**,
s mrežom, logom i rezultatom replaya kao ulazima.
