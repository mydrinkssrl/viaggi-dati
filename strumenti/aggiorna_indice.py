#!/usr/bin/env python3
"""Ricostruisce il campo extra dell'indice da mete-extra.json e aggiunge gli .SKIP di out/ a scartate."""
import json, glob, os
IDX = '/home/claude/viaggi-dati/indice-catalogo.json'
idx = json.load(open(IDX, encoding='utf-8'))
live = json.load(open('/home/claude/viaggi-dati/mete-extra.json', encoding='utf-8'))
idx['extra'] = [[m['id'], m['nome'], m['durataGiorni']] for m in live['mete']]
for f in glob.glob('/home/claude/run/out/*.SKIP') + glob.glob('/home/claude/run/skip/*.SKIP'):
    i = os.path.basename(f)[:-5]
    if i not in idx['scartate']: idx['scartate'].append(i)
json.dump(idx, open(IDX, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(IDX, 'a').write('\n')
print('documento', len(idx['documento']), 'extra', len(idx['extra']), 'totale', len(idx['documento']) + len(idx['extra']), 'scartate', len(idx['scartate']))
