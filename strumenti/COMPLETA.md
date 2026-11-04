# Completamento di una scheda incompleta

La scheda in `/home/claude/run/out/<id>.json` è stata scritta quando il limite
di lettura web era esaurito: mancano una o più voci di costo (tipicamente
alloggio e/o pasti, a volte parcheggi o bus) o sono presenti senza `min`/`max`.
Leggi prima `/home/claude/run/BRIEF.md` (regole e schema) e poi la scheda.

Compito:
1. Individua le voci mancanti o senza numeri che DEVONO entrare nel totale
   (alloggio per ≥2 giorni, pasti sempre; eventuali trasporti locali citati).
2. Cerca sul web (WebSearch + WebFetch) fasce 2026 verificate con URL: hotel/B&B
   a notte in bassa e alta stagione nella località, prezzi realistici di pranzo e
   cena, ecc. Massimo 10 fetch: punta a pagine dense (portali hotel, guide con
   prezzi, siti ufficiali).
3. Aggiorna la scheda: voci con `min`/`max` (ricorda `perGiorno: true` se al
   giorno, con l'importo A PERSONA, cioè la doppia divisa per due), `alloggio`
   testuale con i numeri, `fonti` estese con gli URL nuovi, `costoNota` ripulita
   da frasi tipo "non verificato" se ora è verificato, e `costoMin`/`costoMax`
   RICALCOLATI: somma voci persona + voci vettura/2, voci `perGiorno`
   moltiplicate per i giorni, escluse quelle `confronto: true`.
4. `python3 -I /home/claude/run/valida.py /home/claude/run/out/<id>.json` deve
   stampare OK. Non cambiare id, nome, durata.
5. Se davvero non trovi fonti per un dato, lascialo testuale e dichiaralo in
   `costoNota`; non inventare.

Rispondi con UNA riga: `OK <id> <costoMin>-<costoMax> € · <n> fonti` oppure
`PARZIALE <id>: cosa manca ancora`.
