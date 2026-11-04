# Brief per l'agente di una meta — «Viaggi da Firenze»

Devi produrre UNA scheda di destinazione, in italiano, per un'app di casa che
raccoglie viaggi "esauribili" da Firenze in 1, 2, 3, 7 o 14 giorni. Il risultato
è un file JSON in `/home/claude/run/out/<id>.json`. Niente altro va scritto.

## Regole non negoziabili
1. **Ogni numero deve avere una fonte URL** nel campo `fonti`: prezzi di treni,
   voli, traghetti, ingressi, parcheggi, alloggio, pasti; tempi di viaggio.
   Cerca sul web (WebSearch/WebFetch) e riporta **fasce verificate 2026**
   (es. "22–27 €"), non stime a memoria. Ciò che non riesci a verificare resta
   FUORI dal JSON o solo come testo senza `min`/`max`. Non inventare URL.
2. **Criterio del documento**: la meta deve essere visitabile in modo
   approfondito nella durata data, non di corsa. `percheDurata` lo motiva in
   3–5 righe concrete (distanze interne, quante attrazioni, ritmo).
3. **Motore costi (capitolo 3 del documento)**: due viaggiatori che condividono
   l'auto. Le voci della vettura (benzina, pedaggi, vignette, noleggio auto,
   parcheggio, traghetto per l'auto) hanno `tipo: "vettura"`; tutto il resto
   `tipo: "persona"`. `costoMin`/`costoMax` sono **a persona**, con 2 viaggiatori:
   somma delle voci persona + (somma voci vettura)/2. Devono tornare con
   `costiDettaglio` (tolleranza ±15 %).
   Parametri del documento da usare per l'auto: 0,129 €/km di carburante
   (benzina 1,98 €/l, 6,5 l/100 km); FI-PI-LI Firenze–Pisa gratuita (85 km);
   A1 Firenze–Bologna 8,90 € a tratta; accesso aeroporti: Firenze Peretola
   tram T2 3,40 € A/R a persona; Pisa in auto ≈ 22 € benzina + 12–18 €
   parcheggio per 2 giorni (vettura) oppure treno + Pisa Mover 30,40 € A/R a
   persona; Bologna aeroporto: treno A/R 20–50 € + Marconi Express 23,20 € A/R
   a persona. Per i voli cita rotte reali da Firenze (FLR), Pisa (PSA) o Bologna
   (BLQ) con fascia di prezzo verificata su un comparatore o sul sito della
   compagnia.
4. **Niente duplicati**: non proporre una meta diversa da quella assegnata. Se
   scopri che la meta assegnata NON regge il criterio (es. irraggiungibile in
   quella durata, chiusa, tutta ZTL senza alternative), scrivi
   `/home/claude/run/out/<id>.SKIP` con il motivo in una riga e fermati.
5. **Trasparenza**: `aggiuntaIl` = data odierna (YYYY-MM-DD) e
   `pertinenzaStimata` 1–5 (5 = imperdibile per chi parte da Firenze e cerca
   mete esauribili; 3 = buona; 1 = di nicchia).

## Come lavorare
Se hai a disposizione l'Agent tool, lancia in parallelo 3 sub-agenti
(`subagent_type: "general-purpose"`, `model: "haiku"`), uno per blocco, che
rispondano SOLO con un elenco "dato → valore → URL". Se NON ce l'hai (è il caso
normale), fai tu le ricerche con WebSearch e WebFetch, un blocco alla volta,
raccogliendo per ogni dato il valore e l'URL. I tre blocchi:
- **Trasporti**: come si arriva da Firenze (treno/auto/volo/traghetto), tempi,
  fasce di prezzo A/R 2026, km e pedaggi se in auto, ZTL e parcheggi.
- **Visite**: le 3–8 attrazioni principali, orari e giorni di chiusura 2026,
  prezzi dei biglietti, prenotazioni obbligatorie, eventi o periodi affollati.
- **Soggiorno e pasti** (solo se durata ≥ 2 giorni; per 1 giorno solo pasti):
  fasce a notte per B&B / hotel 3 stelle in bassa e alta stagione, prezzi
  realistici di pranzo e cena, mesi migliori e da evitare (clima).
Per le mete da 7 e 14 giorni aggiungi un quarto blocco **Spostamenti
interni** (treni/bus/noleggio auto tra le tappe, vignette, traghetti).
Poi componi la scheda. Se su un dato non trovi una fonte, non inventarlo:
riprova una volta sola, altrimenti ometti il dato. Prezzi in valuta estera:
converti in euro e dichiaralo in `costoNota`.

## Schema del JSON (tutti i campi, nell'ordine; null dove indicato)
```
{
  "id": "slug-della-meta-Ng",            // solo a-z 0-9 e trattini, finisce con -1g/-2g/-3g/-7g/-14g
  "nome": "Nome come appare nell'app",
  "sottotitolo": "Regione/Paese, una riga che dice cos'è",
  "durataGiorni": 1 | 2 | 3 | 7 | 14,
  "mezzoConsigliato": "Testo: come arrivare, con i dettagli pratici",
  "mezzoCategoria": "treno" | "auto" | "volo" | "bus" | "traghetto" | "misto",
  "durataViaggioTesto": "Es. Circa 2h10 in treno; 1h50 in auto (160 km)",
  "durataViaggioMinuti": 130,            // porta a porta, sola andata, col mezzo consigliato
  "periodoMiglioreTesto": "Mesi consigliati e perché",
  "mesi": [4,5,6,9,10],                  // mesi consigliati (1-12), NON vuoto
  "mesiDaEvitare": [7,8],                // può essere []
  "costoMin": 41, "costoMax": 84,        // € a persona, viaggio intero, 2 viaggiatori
  "costoNota": null | "Testo breve se serve una precisazione",
  "dipendenzaAuto": "senza-auto" | "auto-opzionale" | "auto-parziale" | "autista-tour" | "noleggio-obbligatorio" | "auto-propria-obbligatoria",
  "pertinenzaStimata": 1..5,
  "percheDurata": "Perché è esauribile proprio in questa durata",
  "cosaVedere": ["..3–8 voci, ciascuna una frase con il perché.."] | null,   // obbligatorio per 1 e 2 giorni
  "itinerario": [{"giorno":1,"testo":"Giorno 1: ..."}, ...] | null,           // OBBLIGATORIO da 3 giorni in su, una voce per giorno
  "alloggio": "Fasce a notte, zone dove dormire, con numeri verificati" | null, // null solo per 1 giorno
  "costiDettaglio": [                    // NON vuoto: tutte le voci che compongono il totale
    {"voce":"Treno A/R","testo":"22–27 € in Regionale...","min":22,"max":27,"tipo":"persona","confronto":false,"perGiorno":false},
    {"voce":"Auto","testo":"320 km A/R, circa 41 € di carburante più 18 € di pedaggi","min":59,"max":59,"tipo":"vettura","confronto":true,"perGiorno":false},
    {"voce":"Alloggio","testo":"60–95 € a notte in B&B/3 stelle per due","min":30,"max":48,"tipo":"persona","confronto":false,"perGiorno":true}
  ],
  // "confronto": true per le alternative che NON entrano nella somma (es. l'auto quando il mezzo consigliato è il treno).
  // "perGiorno": true quando min/max sono AL GIORNO (alloggio, pasti): l'app li moltiplica per i giorni.
  "ripartizione": "Testo su cosa è a persona e cosa è della vettura" | null,
  "vincoli": [                           // 2–5 voci; categoria tra "accessi" (ZTL, parcheggi, isole, chiusure stradali), "chiusure" (giorni/orari), "prenotazioni"
    {"categoria":"accessi","testo":"..."},
    {"categoria":"chiusure","testo":"..."},
    {"categoria":"prenotazioni","testo":"..."}
  ],
  "note": "Consigli pratici, abbinamenti, avvertenze (NON vuoto)",
  "fonti": ["https://...", "..."],       // NON vuoto, 4–12 URL realmente consultati
  "aggiuntaIl": "YYYY-MM-DD",
  "coordinate": {"lat": 44.29, "lon": 11.88},   // centro della meta (o della tappa principale), per la mappa
  "bambini": {"adatta": "si" | "parziale" | "no", "nota": "Una riga: perché, con un bimbo di 4 anni"}
}
```

## Qualità del testo
Italiano naturale, concreto, come una guida scritta da un amico competente.
Niente frasi generiche ("città ricca di storia"). Ogni voce di `cosaVedere` dice
cosa si vede e perché vale. `note` contiene almeno un consiglio che si trova
solo sapendo il posto. Lunghezza: 1 giorno ≈ 350–500 parole totali; 2–3 giorni
≈ 500–800; 7–14 giorni ≈ 900–1400 (itinerario giorno per giorno completo).

## Esempio reale già in catalogo (1 giorno)
Vedi `/home/claude/run/ESEMPIO.json`. Non copiarne i contenuti: solo il tono e
la struttura.

## Chiusura
Scrivi il JSON (valido, UTF-8, indent 2) in `/home/claude/run/out/<id>.json`,
poi esegui `python3 -I /home/claude/run/valida.py /home/claude/run/out/<id>.json`
e correggi finché non stampa `OK`. Rispondi al chiamante con UNA sola riga:
`OK <id> <costoMin>-<costoMax> € · <n> fonti` oppure `SKIP <id>: motivo`.
