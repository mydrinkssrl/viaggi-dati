#!/usr/bin/env python3
"""Valida una scheda di meta extra prima della pubblicazione.
Replica i controlli di server/test/extra.test.ts e le regole di METE-EXTRA.md,
più i controlli di coerenza dei costi. Uso: valida.py file.json [altri.json ...]
Stampa OK oppure l'elenco degli errori; exit code 1 se c'è un errore."""
import json, re, sys, os
from datetime import date

IDX = '/home/claude/viaggi-dati/indice-catalogo.json'
DURATE = {1, 2, 3, 7, 14}
MEZZI = {'treno', 'auto', 'volo', 'bus', 'traghetto', 'misto'}
AUTO = {'senza-auto', 'auto-opzionale', 'auto-parziale', 'autista-tour',
        'noleggio-obbligatorio', 'auto-propria-obbligatoria'}
VINC = {'accessi', 'chiusure', 'prenotazioni', None}
OBBL = ['id', 'nome', 'durataGiorni', 'mezzoConsigliato', 'mezzoCategoria',
        'durataViaggioTesto', 'durataViaggioMinuti', 'periodoMiglioreTesto',
        'mesi', 'costoMin', 'costoMax', 'dipendenzaAuto', 'pertinenzaStimata',
        'percheDurata', 'costiDettaglio', 'vincoli', 'note', 'fonti', 'aggiuntaIl']


def norm(s):
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()


def carica_indice():
    idx = json.load(open(IDX))
    esist = {(norm(n), g) for _, n, g in idx['documento'] + idx['extra']}
    ids = {i for i, _, _ in idx['documento'] + idx['extra']}
    escl = set()
    for e in idx['escluse']:
        n = e['nome'].lower()
        if n.startswith('tutta '):
            n = n.split(' ', 1)[1].replace("l'", '')
        escl.add(norm(n.split(' e ')[0]))
    return esist, ids, escl


def valida(path, esist, ids, escl, visti):
    err = []
    try:
        m = json.load(open(path, encoding='utf-8'))
    except Exception as e:
        return [f'JSON non valido: {e}']
    for k in OBBL:
        if k not in m or m[k] in (None, '', []):
            err.append(f'campo obbligatorio mancante o vuoto: {k}')
    if err:
        return err
    g = m['durataGiorni']
    if g not in DURATE:
        err.append(f'durataGiorni {g} non in {sorted(DURATE)}')
    if not re.fullmatch(r'[a-z0-9-]+-(1|2|3|7|14)g', m['id']):
        err.append(f'id non valido: {m["id"]}')
    elif not m['id'].endswith(f'-{g}g'):
        err.append('id non coerente con durataGiorni')
    if os.path.basename(path) != m['id'] + '.json':
        err.append(f'il file deve chiamarsi {m["id"]}.json')
    if m['id'] in ids:
        err.append('id già presente in catalogo')
    if m['id'] in visti:
        err.append('id duplicato in questa run')
    visti.add(m['id'])
    n = norm(m['nome'])
    if (n, g) in esist:
        err.append('stessa meta alla stessa durata già in catalogo')
    for e in escl:
        if e and (n == e or n.startswith(e + ' ') or f' {e} ' in f' {n} '):
            err.append(f'meta esclusa dal documento: {e}')
    if m['mezzoCategoria'] not in MEZZI:
        err.append(f'mezzoCategoria non valido: {m["mezzoCategoria"]}')
    if m['dipendenzaAuto'] not in AUTO:
        err.append(f'dipendenzaAuto non valido: {m["dipendenzaAuto"]}')
    if not isinstance(m['durataViaggioMinuti'], int) or m['durataViaggioMinuti'] <= 0:
        err.append('durataViaggioMinuti deve essere un intero > 0')
    mesi = m['mesi']
    if not all(isinstance(x, int) and 1 <= x <= 12 for x in mesi):
        err.append('mesi deve contenere interi 1-12')
    if set(mesi) & set(m.get('mesiDaEvitare') or []):
        err.append('un mese è sia consigliato sia da evitare')
    if not (isinstance(m['costoMin'], (int, float)) and isinstance(m['costoMax'], (int, float))):
        err.append('costoMin/costoMax devono essere numeri')
    elif not (0 < m['costoMin'] <= m['costoMax']):
        err.append('serve 0 < costoMin <= costoMax')
    p = m['pertinenzaStimata']
    if not (isinstance(p, int) and 1 <= p <= 5):
        err.append('pertinenzaStimata deve essere un intero 1-5')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(m['aggiuntaIl'])):
        err.append('aggiuntaIl deve essere YYYY-MM-DD')
    cv = m.get('cosaVedere') or []
    it = m.get('itinerario') or []
    if len(cv) + len(it) == 0:
        err.append('serve cosaVedere oppure itinerario')
    if g >= 3 and len(it) == 0:
        err.append('da 3 giorni in su serve itinerario giorno per giorno')
    if g >= 3 and it and len(it) < g:
        err.append(f'itinerario con {len(it)} voci per {g} giorni')
    for v in it:
        if not isinstance(v, dict) or 'testo' not in v or not v['testo']:
            err.append('voce di itinerario senza testo')
    if g >= 2 and not m.get('alloggio'):
        err.append('da 2 giorni in su serve alloggio')
    if g < 2 and len(cv) < 3:
        err.append('cosaVedere: almeno 3 voci')
    # costi
    sp = sv = 0.0; sp_max = sv_max = 0.0
    for v in m['costiDettaglio']:
        if not isinstance(v, dict) or not v.get('voce') or not v.get('testo'):
            err.append('voce di costo senza voce/testo'); continue
        if v.get('tipo') not in ('persona', 'vettura'):
            err.append(f'tipo costo non valido in «{v["voce"]}»')
        mn, mx = v.get('min'), v.get('max')
        if (mn is None) != (mx is None):
            err.append(f'min/max incoerenti in «{v["voce"]}»')
        if mn is not None and mx is not None:
            if not (isinstance(mn, (int, float)) and isinstance(mx, (int, float))) or mn < 0 or mx < mn:
                err.append(f'min/max non validi in «{v["voce"]}»')
            elif not v.get('confronto'):
                k = g if v.get('perGiorno') else 1
                if v['tipo'] == 'vettura':
                    sv += mn * k; sv_max += mx * k
                else:
                    sp += mn * k; sp_max += mx * k
    tot_min = sp + sv / 2; tot_max = sp_max + sv_max / 2
    if tot_max > 0:
        if abs(tot_min - m['costoMin']) > max(8, 0.15 * tot_min):
            err.append(f'costoMin {m["costoMin"]} non torna con le voci (atteso ≈ {round(tot_min)})')
        if abs(tot_max - m['costoMax']) > max(8, 0.15 * tot_max):
            err.append(f'costoMax {m["costoMax"]} non torna con le voci (atteso ≈ {round(tot_max)})')
    else:
        err.append('nessuna voce di costo con numeri che entri nel totale')
    for v in m['vincoli']:
        if not isinstance(v, dict) or v.get('categoria') not in VINC or not v.get('testo'):
            err.append('vincolo non valido')
    if len(m['vincoli']) < 2:
        err.append('vincoli: almeno 2 voci')
    for u in m['fonti']:
        if not isinstance(u, str) or not re.match(r'https?://[^\s]+\.[^\s]+', u):
            err.append(f'fonte non è un URL: {u!r}')
    if len(m['fonti']) < 3:
        err.append('fonti: almeno 3 URL')
    c = m.get('coordinate')
    if not (isinstance(c, dict) and isinstance(c.get('lat'), (int, float)) and isinstance(c.get('lon'), (int, float))
            and -90 <= c['lat'] <= 90 and -180 <= c['lon'] <= 180):
        err.append('coordinate {lat, lon} mancanti o non valide')
    b = m.get('bambini')
    if not (isinstance(b, dict) and b.get('adatta') in ('si', 'parziale', 'no') and b.get('nota')):
        err.append('bambini {adatta: si|parziale|no, nota} mancante')
    # lunghezza testo
    parole = len(json.dumps([m.get(k) for k in ('percheDurata', 'cosaVedere', 'itinerario', 'note', 'alloggio', 'vincoli')], ensure_ascii=False).split())
    minimo = {1: 220, 2: 330, 3: 400, 7: 650, 14: 650}[g] if g in DURATE else 0
    if parole < minimo:
        err.append(f'testo troppo scarno: {parole} parole, minimo {minimo}')
    return err


if __name__ == '__main__':
    esist, ids, escl = carica_indice()
    visti = set()
    ko = 0
    for pth in sys.argv[1:]:
        e = valida(pth, esist, ids, escl, visti)
        if e:
            ko += 1
            print(f'✖ {os.path.basename(pth)}')
            for x in e:
                print('   -', x)
        else:
            print(f'OK {os.path.basename(pth)}')
    sys.exit(1 if ko else 0)
