# Rezultati

Sažetak rezultata iz rada. Sve vrijednosti dobivene su u ProM-u 6.15 na logu iz mape [`../podaci/`](../podaci/).

## Event log

| Pokazatelj | Vrijednost |
| --- | --- |
| Slučajevi | 300 |
| Događaji | 2265 |
| Različite aktivnosti | 12 |
| Događaja po slučaju (min. / prosjek / maks.) | 4 / 7,55 / 13 |

## Provjera usklađenosti

| Model | Fitness | Preciznost | Generalizacija | Potpuno usklađenih slučajeva |
| --- | --- | --- | --- | --- |
| Inductive Miner (IM) | 1,000 | 0,722 | 0,993 | 300 od 300 |
| Alpha Miner | 0,91 | 0,869 | 0,991 | 186 od 300 |
| Heuristics Miner (pretvoren u Petrijevu mrežu) | 0,82 | 0,791 | 0,998 | 0 od 300 |

## Usporedba s izvornim modelom

| Konstrukt izvornog modela | Alpha Miner | Heuristics Miner | Inductive Miner |
| --- | --- | --- | --- |
| Početni slijed aktivnosti | ispravan | ispravan | ispravan |
| Grana dobavljača (ugniježđeni izbor) | otkrivena, spajanje neispravno | otkrivena | dva neovisna izbora |
| Paralelizam naplate, pakiranja i računa | ispravan | otkriven, izgubljen pri pretvorbi | ispravan |
| Petlja ponovljene naplate | nije otkrivena | ispravna | razdvojena na dvije petlje |
| Izbor načina dostave | ispravan | ispravan | ispravan |
| Ispravnost (soundness) mreže | ne | ne (nakon pretvorbe) | da |

Slike otkrivenih modela i rezultata provjere usklađenosti nalaze se u seminarskom radu, a mogu se ponovno dobiti
uvozom mreža iz mape [`../prom/mreze/`](../prom/mreze/) i loga u ProM.
