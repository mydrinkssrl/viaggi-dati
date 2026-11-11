# Strumenti della run notturna «verso le 1000 mete»

Questi file servono alla run automatica (attività pianificata) che ogni notte
aggiunge nuove destinazioni al catalogo finché non arriva a 1000. Sono gli
stessi usati per la run del 4 novembre 2026.

- `BRIEF.md` — il brief che riceve l'agente di una singola meta: regole,
  schema del JSON, motore costi, qualità del testo. Scrive in `/home/claude/run/out/<id>.json`.
- `COMPLETA.md` — brief per completare una scheda uscita con voci di costo
  senza numeri.
- `ESEMPIO.json` — una scheda reale del catalogo, come riferimento di tono.
- `valida.py` — validatore: replica `server/test/extra.test.ts` e le regole di
  `data/METE-EXTRA.md`, più coerenza dei costi, coordinate e giudizio bambini.
  Legge `/home/claude/viaggi-dati/indice-catalogo.json` per i doppioni.
- `unisci.py` — unisce le schede valide di `/home/claude/run/out/` con
  `mete-extra.json` (a parità di id vince `aggiuntaIl` più recente) e scrive
  anche `/home/claude/app-famiglia/data/viaggi/mete-extra.json` (Nido, dove dal 4 novembre 2026 vive la sezione Viaggi) se il repo è clonato lì.
- `candidati-YYYY-MM-DD.json` — gli elenchi di candidati usati nelle run
  precedenti (per non riproporre gli scartati).

Percorsi attesi: `viaggi-dati` clonato in `/home/claude/viaggi-dati`, `app-famiglia`
(Nido) in `/home/claude/app-famiglia`, cartella di lavoro `/home/claude/run/` con dentro una
copia di questi file e la sottocartella `out/`.

`indice-catalogo.json` va aggiornato dopo ogni pubblicazione (id, nome,
durata di tutte le mete, documento + extra) ed è la fonte per il controllo dei
doppioni.

## Nota dalla run del 5 novembre 2026
- Il limite delle ricerche web è **200 WebSearch per turno**, condivise tra tutti
  gli agenti (non un tetto orario): bastano per ~27 mete. Per arrivare a 45 la
  run pubblica ciò che ha, poi si riprogramma con `send_later` (nuovo turno,
  budget azzerato) e completa il resto. Conviene dire agli agenti di usare al
  massimo 6 WebSearch (3 per i completamenti) e preferire WebFetch.
- Gli agenti da 7-14 giorni spesso lasciano i pasti fuori dal totale: controllare
  che nei `costiDettaglio` ci sia una voce pasti con numeri e passare le schede
  a `COMPLETA.md` prima di pubblicarle.
- In questa sessione `app-famiglia` non era attaccabile (manca `add_repo`):
  basta pubblicare su `viaggi-dati`, Nido la scarica alle 07:30.

## Nota dalla run del 6 novembre 2026
- Con 8 agenti in parallelo e il tetto di 5 WebSearch ciascuno il budget di 200
  ricerche del turno è bastato per ~37 mete; le ultime 8 (quattro da 1-2 giorni e i
  due completamenti) sono rimaste senza ricerche e vanno fatte in un turno nuovo
  via `send_later`. Conviene lanciare prima le mete da 7-14 giorni (le più preziose)
  e tenere le 1-2 giorni per il secondo turno.
- WebFetch rifiuta gli URL digitati a mano (`PROVENANCE_REQUIRED`): gli agenti
  devono fetchare solo URL comparsi in una WebSearch precedente. Dirlo nel prompt.
- Il commit 7c7d6db riporta per errore «5 da 3, 18 da 7, 11 da 14»: le mete
  pubblicate sono 3 da 2 giorni, 6 da 3, 16 da 7 e 12 da 14 (37 in tutto).

## Nota dalla run del 7 novembre 2026
- Il tetto di WebSearch del turno si è esaurito dopo circa 42 agenti (34 schede
  nuove da 5 ricerche + 8 completamenti da 3): con 5 WebSearch a scheda il budget
  copre ~30 mete da 7-14 giorni più i completamenti; le 1-3 giorni vanno nel
  secondo turno (`send_later`). Gli agenti con tetto 4 ricerche hanno lasciato
  quasi tutti pasti/alloggio senza numeri: meglio 5 ricerche e meno mete.
- Le schede uscite senza budget (costi solo testuali) non vanno pubblicate: si
  spostano in `/home/claude/run/pending/` e si completano nel turno successivo
  con `COMPLETA.md`.
- `add_repo` non è disponibile nella sessione pianificata: `app-famiglia` non si
  attacca, si pubblica solo su `viaggi-dati`.
- Secondo turno (send_later dopo 3 minuti, budget azzerato): 4 completamenti + 7 mete
  nuove + 8 completamenti dei pasti in tre ondate, ~75 ricerche. Totale notte: 45 mete.
  Le schede già pubblicate vanno spostate fuori da `out/` (es. `pubblicate/`) prima
  di rifare `unisci.py`, altrimenti il validatore le segna come doppioni.

## Nota dalla run dell'8 novembre 2026
- Primo turno: 38 agenti (30 da 7-14 giorni con opus, 6 da 3 giorni e 2 da 2 con
  sonnet) in cinque ondate da 8, tetto 5 WebSearch ciascuno: 37 schede complete al
  primo colpo, una sola (alvernia-e-lione-7g) senza pasti/alloggio. Chiedere nel
  prompt «una delle prime ricerche a hotel/pasti con prezzi» ha quasi eliminato i
  completamenti. Pubblicate subito (commit ef898d8, catalogo a 444).
- Secondo turno (`send_later` dopo 3 minuti): 7 mete da 1-2 giorni + il
  completamento dei pasti di Alvernia, tutte OK in un'unica ondata. Totale notte: 45.
- Le schede da 1 giorno chiamano la voce pasti «Pranzo»: `controlla.py` (in
  /home/claude/run) deve cercare anche quella parola.
- `add_repo` ancora assente nella sessione pianificata: `app-famiglia` non si
  attacca, pubblicato solo su `viaggi-dati`.

## Nota dalla run del 9 novembre 2026
- Primo turno: 38 agenti in cinque ondate da 8 (30 da 7-14 giorni con opus, 6 da 3
  giorni e 2 da 2 con sonnet), tetto 5 WebSearch ciascuno: 37 schede valide e un solo
  SKIP (Ajaccio e Corsica del Sud in 3 giorni: nessun volo diretto, traghetto più
  5 ore di guida). Sei schede con voci vettura/trasporti senza numeri (carburante,
  pedaggi, treni interni) sono state tenute in `pending/` e completate nel secondo
  turno, perché `unisci.py` non sovrascrive una scheda con lo stesso `aggiuntaIl`.
- Il commit ee2959f riporta per errore «4 da 3, 12 da 7, 13 da 14»: le 31 mete
  pubblicate sono 2 da 2 giorni, 5 da 3, 15 da 7 e 9 da 14.
- Secondo turno (`send_later` dopo 3 minuti): 6 completamenti (sonnet, 3 WebSearch,
  COMPLETA.md) + 8 mete nuove (una sostituta da 3 giorni, 3 da 2, 4 da 1) in due ondate,
  tutte valide. Totale notte: 45 mete nuove, catalogo a 497.
- `aggiorna_indice.py` (in /home/claude/run) ricostruisce il campo `extra` dell'indice
  da `mete-extra.json` e aggiunge gli .SKIP a `scartate`.
- Il validatore esclude per parola anche a durate ammesse (es. «Milano» a 3 giorni,
  «Venezia» nel nome di Chioggia): scegliere nomi senza quelle parole.
- `add_repo` ancora assente nella sessione pianificata: `app-famiglia` non si
  attacca, pubblicato solo su `viaggi-dati`.

## Nota dalla run del 10 novembre 2026
- Primo turno: 38 agenti in cinque ondate da 8 (30 da 7-14 giorni con opus, 6 da 3
  giorni e 2 da 2 con sonnet), tetto 5 WebSearch ciascuno: 36 schede valide pubblicate
  subito (commit b76ef31, catalogo a 535), 2 SKIP (Skopje e Ohrid in 3 giorni: 5 giorni
  reali più bus di 3h e volo Wizz solo serale; Stoccarda, Heidelberg e Tubinga: nessun
  volo diretto da FLR/PSA/BLQ, 8 ore d'auto) e 2 schede tenute in `pending/` (Molise
  con pasti non verificati, parchi del Sud-Ovest USA con carburante senza numeri).
- Secondo turno (`send_later` dopo 3 minuti): 2 completamenti + 7 mete nuove (Bologna
  completa da 2 giorni, 4 da 1 giorno, 2 sostitute da 3: Cuneo e Valle Maira, Cefalonia
  e Itaca) in un'unica ondata di 9, più un completamento per Cefalonia (noleggio e
  traghetto). Totale notte: 45 mete nuove (4 da 1, 5 da 2, 6 da 3, 18 da 7, 12 da 14),
  catalogo a 544.
- Alcune voci di costo marginali restano solo testuali (parcheggi, un pedaggio, Pilatus,
  taxi d'acqua per Spetses, e-Visa India): dichiarate nel testo e fuori dal totale.
- `add_repo` ancora assente nella sessione pianificata: `app-famiglia` non si attacca,
  pubblicato solo su `viaggi-dati`.

## Nota dalla run dell'11 novembre 2026
- Primo turno: 40 agenti in cinque ondate da 8 (30 da 7-14 giorni con opus, 6 da 3 giorni e
  4 da 2 con sonnet), tetto 5 WebSearch ciascuno: 36 schede valide pubblicate subito
  (commit 7a2b9b2, catalogo a 580), 2 SKIP (Sinai e Mar Rosso: Viaggiare Sicuri sconsiglia
  Dahab e gli spostamenti nel Sinai; Santiago de Compostela: nessun volo diretto da
  FLR/PSA/BLQ) e 2 schede tenute in `pending/` (Parma con pasti senza fonte, Zante senza
  diretto verificato).
- Secondo turno (`send_later` dopo 3 minuti): 5 mete nuove (Alba da 2, 4 da 1 giorno), i
  completamenti di Parma (pasti e Torrechiara) e delle Cicladi settentrionali (traghetti
  interni), più tre ritocchi (Alba, Castelli del Ducato, Amiata). Zante è diventata SKIP
  (nessun diretto 2026 da Bologna/Pisa). Totale notte: 41 mete nuove (3 da 1, 5 da 2, 4 da 3,
  17 da 7, 11 da 14), catalogo a 585.
- Una scheda sonnet (Alba) è uscita senza lettere accentate: controllare `grep -c è` sulle
  schede da 1-2 giorni prima di pubblicare e far ripassare il testo se manca.
- I pranzi delle mete da 1 giorno in zone poco coperte (Amiata, Bassa parmense) spesso non
  hanno un listino verificabile: se restano stime vanno messi come voce testuale fuori dal
  totale, dichiarati in `costoNota`.
- Per aggiornare una scheda già pubblicata il validatore la segna come doppione: validarla
  a parte (togliendo il suo id dall'indice) e sostituirla a mano in `mete-extra.json`.
- `controlla.py` e `aggiorna_indice.py` ora stanno in `strumenti/` e vanno copiati in
  /home/claude/run insieme agli altri file.
- `add_repo` ancora assente nella sessione pianificata: `app-famiglia` non si attacca,
  pubblicato solo su `viaggi-dati`.
