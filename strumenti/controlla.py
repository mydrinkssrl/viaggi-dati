#!/usr/bin/env python3
"""Segnala le schede in out/ con voci di costo senza numeri o senza pasti/alloggio numerici."""
import json, glob, sys, os
for f in sorted(glob.glob('/home/claude/run/out/*.json')):
    m = json.load(open(f, encoding='utf-8'))
    g = m['durataGiorni']
    prob = []
    senza = [v['voce'] for v in m['costiDettaglio'] if v.get('min') is None]
    if senza: prob.append('senza numeri: ' + ', '.join(senza))
    voci = ' '.join(v['voce'].lower() for v in m['costiDettaglio'] if v.get('min') is not None)
    if not any(k in voci for k in ('past', 'pranzo', 'cena', 'cibo', 'ristor', 'mang')): prob.append('manca voce pasti con numeri')
    if g >= 2 and not any(k in voci for k in ('allogg', 'hotel', 'notte', 'b&b', 'pernott', 'soggiorno', 'lodge', 'ostell', 'riad', 'guesthouse')): prob.append('manca voce alloggio con numeri')
    print(('⚠ ' if prob else 'ok ') + os.path.basename(f) + (': ' + '; '.join(prob) if prob else ''))
