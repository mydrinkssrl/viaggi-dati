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
