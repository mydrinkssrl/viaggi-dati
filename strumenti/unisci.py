#!/usr/bin/env python3
"""Unisce le schede validate in out/ con il dataset pubblicato.
Uso: unisci.py [--scrivi]  (senza --scrivi fa solo il riepilogo)
Scrive /home/claude/viaggi-dati/mete-extra.json e, se esiste,
/home/claude/errore/data/mete-extra.json. A parità di id vince aggiuntaIl
più recente. Ordina per durataGiorni e id."""
import glob, json, os, subprocess, sys

OUT = '/home/claude/run/out'
LIVE = '/home/claude/viaggi-dati/mete-extra.json'
REPO = '/home/claude/app-famiglia/data/viaggi/mete-extra.json'  # Nido; l'app separata (errore) è stata ritirata

live = json.load(open(LIVE, encoding='utf-8'))
mete = {m['id']: m for m in live['mete']}
prima = len(mete)

files = sorted(glob.glob(os.path.join(OUT, '*.json')))
ok = subprocess.run([sys.executable, '-I', '/home/claude/run/valida.py', *files],
                    capture_output=True, text=True)
validi = {l.split()[1][:-5] for l in ok.stdout.splitlines() if l.startswith('OK ')}
scartati = [os.path.basename(f)[:-5] for f in files if os.path.basename(f)[:-5] not in validi]

nuove = []
for f in files:
    mid = os.path.basename(f)[:-5]
    if mid not in validi:
        continue
    m = json.load(open(f, encoding='utf-8'))
    if mid in mete and mete[mid].get('aggiuntaIl', '') >= m.get('aggiuntaIl', ''):
        continue
    mete[mid] = m
    nuove.append(mid)

ordinate = sorted(mete.values(), key=lambda m: (m['durataGiorni'], m['id']))
print(f'pubblicate prima: {prima} · valide in out/: {len(validi)} · nuove da aggiungere: {len(nuove)} · scartate: {len(scartati)}')
if scartati:
    print('scartate:', ', '.join(scartati))
per_durata = {}
for m in ordinate:
    per_durata[m['durataGiorni']] = per_durata.get(m['durataGiorni'], 0) + 1
print('totale extra dopo l\'unione:', len(ordinate), per_durata, '→ catalogo', 168 + len(ordinate))

if '--scrivi' in sys.argv:
    dati = {'$schema': live.get('$schema', 'vedi data/METE-EXTRA.md'), 'mete': ordinate}
    testo = json.dumps(dati, ensure_ascii=False, indent=2) + '\n'
    open(LIVE, 'w', encoding='utf-8').write(testo)
    if os.path.exists(os.path.dirname(REPO)):
        open(REPO, 'w', encoding='utf-8').write(testo)
    print('scritto', LIVE, 'e', REPO)
