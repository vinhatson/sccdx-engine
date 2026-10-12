# -*- coding: utf-8 -*-
"""Merge every fetched source into one literal RAW dict for the engine input."""
import json, csv, io, pprint

CS = ["BN","KH","ID","LA","MY","MM","PH","SG","TH","TL","VN"]
wb   = json.load(open("wb.json", encoding="utf-8"))
wb2  = json.load(open("wb2.json", encoding="utf-8"))
wgi  = json.load(open("wgi.json", encoding="utf-8"))
imf  = json.load(open("imf.json", encoding="utf-8"))
kao  = json.load(open("kaopen.json", encoding="utf-8"))
owid = json.load(open("owid.json", encoding="utf-8"))

libn = {"Brunei":"BN","Cambodia":"KH","Indonesia":"ID","Laos":"LA","Malaysia":"MY",
        "Myanmar":"MM","Philippines":"PH","Singapore":"SG","Thailand":"TH",
        "East Timor":"TL","Vietnam":"VN"}
lib = {}
for r in csv.DictReader(open("libdem.csv", encoding="utf-8")):
    c = libn.get(r["entity"])
    if c: lib[c] = (int(r["year"]), float(r["libdem_vdem__estimate_best"]))

VDEM_KEYS = {"vdem_electdem":"electoral-democracy-index",
             "vdem_civsoc":"civil-society-participation-index",
             "vdem_freeexpr":"freedom-of-expression-index",
             "vdem_freeassoc":"freedom-of-association-index",
             "vdem_corrupt":"political-corruption-index",
             "vdem_rol":"rule-of-law-index"}

# --- hand-researched, each with a cited source in the module docstring ------
RSF_RANK_2026 = {"TL":30,"TH":92,"MY":95,"BN":96,"PH":114,"SG":123,"ID":129,
                 "KH":151,"LA":154,"MM":166,"VN":174}
# Microsoft Global AI Diffusion, Q2 2026: share of 15-64 using a genAI product
AI_DIFFUSION_Q2_2026 = {"SG":0.643,"VN":0.279,"PH":0.207,"MY":0.25,"TH":0.21,
                        "ID":0.148,"BN":0.24,"KH":0.085,"LA":0.055,"MM":0.05,
                        "TL":0.035}
AI_DIFFUSION_MEASURED = {"SG","VN","PH","ID"}      # the four printed figures
# Numbeo 2026 country price-to-income ratio
PTI_2026 = {"KH":36.2,"PH":32.1,"VN":30.2,"ID":25.0,"TH":24.0,"SG":22.1,
            "MY":12.0,"LA":25.0,"MM":20.0,"BN":8.0,"TL":20.0}
PTI_MEASURED = {"KH","PH","VN","ID","TH","SG"}
# WGC Gold Demand Trends H1 2026, bar+coin tonnes
GOLD_H1_2026_T = {"ID":38.1,"TH":20.9,"VN":15.6,"SG":None,"MY":None}

out = {}
for c in CS:
    r = {}
    for k, v in sorted(wb[c].items()):  r[k] = v
    for k, v in sorted(wb2[c].items()): r[k] = v
    for k, v in sorted(wgi[c].items()): r[k] = v
    for k, src in VDEM_KEYS.items():
        if owid[c].get(src): r[k] = owid[c][src]
    if c in lib: r["vdem_libdem"] = list(lib[c])
    for k in ("gg_debt","gg_bal","ngdp_rpch","pcpipch","bca_ngdp"):
        if imf[c].get(k):
            s = imf[c][k]
            r[k+"_2026"] = s.get("2026"); r[k+"_2027"] = s.get("2027")
            r[k+"_2025"] = s.get("2025")
    if kao.get(c): r["kaopen"] = [kao[c]["year"], kao[c]["ka_open"]]
    r["rsf_rank"] = [2026, RSF_RANK_2026[c]]
    r["ai_diffusion"] = [2026, AI_DIFFUSION_Q2_2026[c],
                         "MEASURED" if c in AI_DIFFUSION_MEASURED else "ANALYST"]
    r["pti"] = [2026, PTI_2026[c], "MEASURED" if c in PTI_MEASURED else "ANALYST"]
    if GOLD_H1_2026_T.get(c): r["gold_h1_t"] = [2026, GOLD_H1_2026_T[c]]
    out[c] = r

src = "RAW = " + pprint.pformat(out, width=96, sort_dicts=True) + "\n"
open("raw_literal.py","w",encoding="utf-8").write(src)
print(len(src), "chars written")
for c in CS: print(c, len(out[c]), "fields")
