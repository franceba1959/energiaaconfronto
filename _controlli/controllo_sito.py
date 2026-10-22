#!/usr/bin/env python3
"""Controllo automatico del sito Energia a Confronto.

Legge tutte le pagine HTML e segnala le violazioni meccaniche delle regole
editoriali. Non modifica nulla: produce un report in Markdown su stdout
(o nel file indicato con --out). Le correzioni le decide chi esegue il
controllo, seguendo _controlli/REGOLE.md.

Uso: python3 _controlli/controllo_sito.py [--out report.md]
"""
import re, sys, os, glob, datetime, html
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGINE = sorted(glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "schede", "*.html")))

TECNOLOGIE = {
    "fotovoltaico": ["fotovoltaic"],
    "eolico-onshore": ["eolico a terra", "eolico onshore"],
    "eolico-offshore": ["eolico in mare", "offshore", "galleggiante"],
    "idroelettrico": ["idroelettric", "diga", "dighe"],
    "geotermico": ["geotermi"],
    "gas-naturale": ["gas naturale"],
    "carbone": ["carbone"],
    "biometano": ["biometano", "biogas"],
    "idrogeno-verde": ["idrogeno"],
    "nucleare-fissione-smr": ["fissione", "SMR "],
    "fusione-nucleare": ["fusione nucleare", " ITER "],
}
MESI = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]


def testo(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def rel(p):
    return os.path.relpath(p, ROOT)


def note_gialle(s):
    """Restituisce il testo di ogni nota gialla (hl-note)."""
    out = []
    for m in re.finditer(r'<span class="hl-note[^"]*">', s):
        i = m.end(); depth = 1; j = i
        while depth and j < len(s):
            a = s.find("<span", j); b = s.find("</span>", j)
            if b < 0: break
            if 0 <= a < b: depth += 1; j = a + 5
            else: depth -= 1; j = b + 7
        out.append(testo(s[i:j - 7]).strip())
    return out


def main():
    righe = []
    def sez(t): righe.append(f"\n## {t}\n")
    def r(t): righe.append(f"- {t}")
    oggi = datetime.date.today()
    righe.append(f"# Controllo automatico del sito — {oggi.isoformat()}\n")
    righe.append(f"Pagine controllate: {len(PAGINE)}\n")
    contenuti = {p: open(p, encoding="utf-8").read() for p in PAGINE}
    conteggi = {}

    # 1. Tag sbilanciati
    sez("1. Struttura HTML (tag aperti e chiusi)")
    n = 0
    for p, s in contenuti.items():
        body = re.sub(r"<script.*?</script>|<style.*?</style>|<!--.*?-->", "", s, flags=re.S)
        for t in ["span", "a", "p", "div", "table", "tr", "td", "ul", "li", "strong"]:
            o = len(re.findall(rf"<{t}[\s>]", body)); c = body.count(f"</{t}>")
            if o != c:
                r(f"`{rel(p)}`: `<{t}>` aperti {o}, chiusi {c}"); n += 1
    if not n: r("nessun problema")
    conteggi["struttura"] = n

    # 2. Note DA VERIFICARE
    sez("2. Note «DA VERIFICARE» presenti (vuoti dichiarati)")
    n = 0
    for p, s in contenuti.items():
        for m in re.finditer(r"\[DA VERIFICARE:[^\]]*\]", testo(s)):
            r(f"`{rel(p)}`: {m.group(0)[:300]}"); n += 1
    if not n: r("nessuna")
    conteggi["da_verificare"] = n

    # 3. Note che parlano di frasi già tolte
    sez("3. Note che si riferiscono a frasi già rimosse (da togliere)")
    n = 0
    pat = re.compile(r"(è stato rimoss|era priv[ao] di fonte|pubblicato in precedenza|riportat[ao] in precedenza|è superat)", re.I)
    for p, s in contenuti.items():
        for m in re.finditer(r"\[DA VERIFICARE:[^\]]*\]", testo(s)):
            if pat.search(m.group(0)):
                r(f"`{rel(p)}`: {m.group(0)[:300]}"); n += 1
    if not n: r("nessuna")
    conteggi["note_superate"] = n

    # 4. Note copiate che citano un'altra tecnologia
    sez("4. Note gialle che citano una tecnologia diversa da quella della scheda")
    n = 0
    for p, s in contenuti.items():
        nome = os.path.splitext(os.path.basename(p))[0]
        if nome not in TECNOLOGIE or "schede" not in p: continue
        for nota in note_gialle(s):
            nl = " " + nota + " "
            for altra, chiavi in TECNOLOGIE.items():
                if altra == nome or {altra, nome} == {"nucleare-fissione-smr", "fusione-nucleare"} or (nome, altra) == ("fusione-nucleare", "idrogeno-verde"): continue
                if any(k.lower() in nl.lower() for k in TECNOLOGIE[nome]): continue
                hit = [k for k in chiavi if (k in nl if k.strip().isupper() else k.lower() in nl.lower())]
                if hit:
                    r(f"`{rel(p)}`: nota che cita «{hit[0]}» senza citare la tecnologia della scheda: «{nota[:200]}»"); n += 1
                    break
    if not n: r("nessuna")
    conteggi["note_altra_tecnologia"] = n

    # 5. Note identiche copiate in più pagine
    sez("5. Note gialle identiche in più pagine (copia e incolla: controllare che vadano bene ovunque)")
    viste = defaultdict(set)
    for p, s in contenuti.items():
        for nota in note_gialle(s):
            if len(nota) > 120: viste[nota].add(rel(p))
    n = 0
    for nota, pag in viste.items():
        if len(pag) > 1:
            r(f"{len(pag)} pagine ({', '.join(sorted(pag))}): «{nota[:160]}…»"); n += 1
    if not n: r("nessuna")
    conteggi["note_copiate"] = n

    # 6. Schede della home: numeri ripetuti fra pillole, riquadri e descrizione
    sez("6. Home: lo stesso numero ripetuto nella stessa scheda")
    n = 0
    s = contenuti[os.path.join(ROOT, "index.html")]
    for m in re.finditer(r'<span class="scheda-name">(.*?)</span>(.*?)<a href="schede/', s, re.S):
        nome, corpo = m.group(1), m.group(2)
        numeri = re.findall(r"\d[\d.,–\-]*\d(?:\s?%)?|\d+\s?%", testo(corpo))
        conta = defaultdict(int)
        for x in numeri:
            if re.fullmatch(r"20\d\d", x) or re.fullmatch(r"\d\.0", x) or len(x) < 3: continue
            conta[x] += 1
        dup = [x for x, c in conta.items() if c > 1]
        if dup:
            r(f"{nome}: ripetuti {', '.join(dup)}"); n += 1
    if not n: r("nessuna ripetizione")
    conteggi["home_ripetizioni"] = n

    # 7. Home e schede: valori dei riquadri assenti dalla scheda
    sez("7. Home: valori dei riquadri che non compaiono nella scheda di dettaglio")
    n = 0
    for m in re.finditer(r'<div class="scheda-kpi">(.*?)</div>\s*<p class="scheda-desc">.*?<a href="(schede/[^"]+)"', s, re.S):
        dest = os.path.join(ROOT, m.group(2))
        if not os.path.exists(dest): continue
        tsch = testo(contenuti.get(dest, "")).replace(" ", " ")
        for v in re.findall(r'kpi-value">(.*?)</div>', m.group(1)):
            v = html.unescape(re.sub(r"<[^>]+>", "", v)).strip()
            mm = re.search(r"\d[\d.,–]*", v)
            core = mm.group(0).rstrip(".,") if mm else ""
            if core and core not in tsch:
                r(f"`{m.group(2)}`: in home «{v}», nella scheda non compare «{core}»"); n += 1
    if not n: r("nessuna incongruenza")
    conteggi["home_vs_schede"] = n

    # 8. Date «Aggiornato» vecchie
    sez("8. Date «Aggiornato» più vecchie di 3 mesi")
    n = 0
    for p, s in contenuti.items():
        for m in re.finditer(r"Aggiornato:\s*([a-z]+)\s+(20\d\d)", testo(s)):
            if m.group(1) in MESI:
                d = datetime.date(int(m.group(2)), MESI.index(m.group(1)) + 1, 1)
                if (oggi - d).days > 100:
                    r(f"`{rel(p)}`: Aggiornato {m.group(1)} {m.group(2)}"); n += 1
    if not n: r("nessuna")
    conteggi["date_vecchie"] = n

    # 9. Possibili calcoli nostri
    sez("9. Possibili calcoli nostri (differenze, «punti», percentuali di completamento)")
    n = 0
    pat = re.compile(r"[−-]\d+[.,]?\d*\s*punti|\d+\s*% completat|\bGap\b|calcolat[oa] da noi|nostra elaborazione")
    for p, s in contenuti.items():
        for m in pat.finditer(testo(s)):
            t = testo(s); i = m.start()
            if "riportava" in t[max(0,i-200):i+60]: continue  # correzione già dichiarata in pagina
            r(f"`{rel(p)}`: «…{t[max(0,i-80):i+60].strip()}…»"); n += 1
    if not n: r("nessuno")
    conteggi["calcoli"] = n

    # 10. Link esterni senza fonte-link o link a home page generiche
    sez("10. Link a home page generiche (le citazioni devono puntare al documento)")
    n = 0
    for p, s in contenuti.items():
        for u in re.findall(r'href="(https?://[^"]+)"[^>]*class="fonte-link"', s) + re.findall(r'class="fonte-link"[^>]*href="(https?://[^"]+)"', s):
            if re.fullmatch(r"https?://(www\.)?[^/]+/?", u):
                r(f"`{rel(p)}`: {u}"); n += 1
    if not n: r("nessuno")
    conteggi["link_generici"] = n

    sez("Riepilogo")
    for k, v in conteggi.items():
        r(f"{k}: {v}")
    out = "\n".join(righe) + "\n"
    if "--out" in sys.argv:
        open(sys.argv[sys.argv.index("--out") + 1], "w", encoding="utf-8").write(out)
    else:
        print(out)


if __name__ == "__main__":
    main()
