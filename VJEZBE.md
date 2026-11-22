# Vježbe

Vježbe nastavljaju na postupak iz rada i otvorena pitanja iz njegove rasprave (poglavlje 9).
Pretpostavlja se da je postupak iz [`docs/UPUTE.md`](docs/UPUTE.md) barem jednom proveden.
Vježbe 1 do 3 ne zahtijevaju Camundu, nego samo log iz mape [`podaci/`](podaci/) i ProM.

## Vježba 1. Ponavljanje analize na priloženom logu

**Cilj:** upoznati se s alatom ProM i dobiti iste rezultate kao u radu.

1. Uvezite `podaci/log_web_trgovina.csv`, pretvorite ga u XES i provjerite sažetak loga.
2. Pokrenite Alpha, Heuristics i Inductive Miner te provjeru usklađenosti za sve tri mreže.
3. Usporedite svoje vrijednosti fitnessa, preciznosti i generalizacije s tablicom u [`rezultati/README.md`](rezultati/README.md).

**Pitanja:** Zašto Alpha Miner ne otkriva petlju naplate? Zašto Alpha mreža ima višu preciznost od mreže Inductive Minera, iako je očito lošija?

## Vježba 2. Inductive Miner s filtriranjem šuma

**Cilj:** istražiti kompromis između fitnessa i preciznosti.

1. Pokrenite Inductive Miner u varijanti **IMf** s pragovima šuma 0,0, 0,1, 0,2, 0,4 i 0,6.
2. Za svaki model izmjerite fitness i preciznost i prikažite ih u tablici ili grafu.

**Pitanja:** Pri kojem pragu nestaje grana otkazivanja (19 slučajeva)? Postoji li prag koji daje bolju ravnotežu od osnovne varijante IM?

## Vježba 3. Poboljšane varijante Alpha algoritma

**Cilj:** provjeriti rješavaju li proširenja Alpha algoritma uočene probleme.

1. Pokrenite Alpha+ (ili Alpha#, ovisno o dostupnim varijantama u ProM-u) na istom logu.
2. Provjerite je li petlja ponovljene naplate sada otkrivena i izmjerite fitness.

## Vježba 4. Ponovljiva simulacija i veličina loga

**Cilj:** ispitati koliko rezultati ovise o slučajnosti i broju slučajeva.

1. Pokrenite simulaciju s `--seed 1` i 300 instanci, a zatim s `--seed 2` i 300 instanci.
2. Ponovite simulaciju s 50 i s 1000 instanci.
3. Za svaki log pokrenite Inductive Miner i izmjerite fitness i preciznost.

**Pitanja:** Mijenja li se struktura otkrivenog modela? Pojavljuju li se kod malog loga rijetke putanje uopće?

## Vježba 5. Uklanjanje artefakta simulatora

**Cilj:** provjeriti hipotezu iz rada (odjeljak 9.2) da lažne veze prema obavijesti o neuspjelom plaćanju nastaju zbog načina rada simulatora.

Worker u `simulacija.py` preuzima zadatke u skupinama (do 50 odjednom), pa se obavijest o neuspjelom plaćanju u logu
uvijek pojavljuje nakon pakiranja i izdavanja računa.

1. Izmijenite worker tako da preuzima po jedan zadatak (`maxJobsToActivate: 1`) ili da zadatke dovršava u slučajnom
   trenutku umjesto po skupinama.
2. Ponovite simulaciju, izvoz i otkrivanje procesa Heuristics i Inductive Minerom.

**Pitanja:** Nestaju li veze iz *Zapakiraj robu* i *Izdaj račun* prema *Obavijesti kupca o neuspjelom plaćanju*?
Otkriva li Inductive Miner sada ispravnu petlju naplate?

## Vježba 6. Vlastito logiranje

**Cilj:** usporediti log iz povijesti Camunde s logom koji bilježi sam worker.

1. Proširite worker tako da pri dovršavanju svakog zadatka zapiše redak (`case_id`, aktivnost, vrijeme) u vlastitu CSV datoteku.
2. Nakon simulacije usporedite tu datoteku s logom dobivenim skriptom `izvoz_loga.py`: broj događaja, redoslijed i vremena.

**Pitanja:** Razlikuju li se vremenske oznake i zašto? Koji je izvor pouzdaniji za process mining?

## Vježba 7. Životni ciklus aktivnosti (start i complete)

**Cilj:** iskoristiti i vrijeme početka aktivnosti.

1. Pri pretvorbi CSV-a u XES mapirajte i stupac `start_time` kao vrijeme početka.
2. Pokrenite Inductive Miner (ili Inductive visual Miner) s klasifikatorom koji uzima u obzir životni ciklus.

**Pitanja:** Kako se mijenja otkriveni model? Pomaže li vrijeme početka pri prepoznavanju paralelizma ili, naprotiv, smeta?

## Vježba 8. Šum u logu

**Cilj:** usporediti otpornost algoritama na šum.

1. Napišite skriptu koja u određenom postotku slučajeva (npr. 5 %) nasumično izostavi, udvostruči ili zamijeni dvije susjedne aktivnosti.
2. Na tako izmijenjenom logu pokrenite sva tri algoritma.

**Pitanja:** Koji je algoritam najotporniji? Kako se mijenjaju fitness i preciznost s porastom šuma?
