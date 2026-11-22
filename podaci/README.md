# Podaci

| Datoteka | Sadržaj |
| --- | --- |
| `log_web_trgovina.csv` | Event log izvezen iz Camunde skriptom `izvoz_loga.py` (300 slučajeva, 2265 događaja) |
| `log_web_trgovina.xes` | Isti log pretvoren u format XES u ProM-u |

Stupci CSV-a:

| Stupac | Značenje |
| --- | --- |
| `case_id` | ključ instance procesa u Camundi (jedan slučaj) |
| `activity` | naziv aktivnosti |
| `start_time` | vrijeme početka aktivnosti (UTC, ISO 8601) |
| `end_time` | vrijeme završetka aktivnosti (UTC, ISO 8601) |

Trajanja aktivnosti ne odražavaju stvarno trajanje poslova: nastala su jer je jedan worker istodobno
obrađivao 300 instanci. Log je prikladan za analizu redoslijeda aktivnosti (kontrolnog toka), a ne vremena.
