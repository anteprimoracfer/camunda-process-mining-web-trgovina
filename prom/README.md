# Modeli iz ProM-a

Petrijeve mreže dobivene u ProM-u 6.15, izvezene u formatu PNML. Mogu se ponovno uvesti u ProM (Import)
i koristiti za provjeru usklađenosti bez ponovnog pokretanja algoritama.

| Datoteka | Algoritam | Napomena |
| --- | --- | --- |
| `mreze/mreza_alpha.pnml` | Alpha Miner (klasični) | nema završnog označavanja; pri replayu odabrati mjesto `End` |
| `mreze/mreza_inductive.pnml` | Inductive Miner (IM) | uključuje početno i završno označavanje |
| `mreze/mreza_heuristics.pnml` | Heuristics Miner, pretvoren pluginom *Convert Heuristics net into Petri net* | početno mjesto `pi9`; za završno odabrati `po11` |
