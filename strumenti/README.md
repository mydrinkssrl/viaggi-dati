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
