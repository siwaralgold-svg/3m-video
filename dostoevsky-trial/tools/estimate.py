# Estimated word times for the script until the real voiceover exists.
# Calibrated on the Edison voiceover: about 2.0 words a second.
import re, json, sys
txt = open("SCRIPT.md", encoding="utf-8").read().split("\n", 1)[1]
paras = [p.strip() for p in txt.split("\n\n") if p.strip()]
t = 0.15; words = []; SEC_PER_CHAR = 0.062; BASE = 0.11
for pi, p in enumerate(paras):
    for line in p.split("\n"):
        for tok in line.split():
            core = re.sub(r"[.,،؟:…!]", "", tok)
            n = len(re.sub(r"[ً-ْ]", "", core))
            d = BASE + SEC_PER_CHAR * n
            words.append({"id": f"w{len(words)}", "text": tok, "start": round(t, 2), "end": round(t + d, 2), "p": pi})
            t += d + 0.03
            if tok.endswith("…"): t += 0.36
            elif re.search(r"[.؟!]$", tok): t += 0.36
            elif tok.endswith(":"): t += 0.3
            elif tok.endswith("،"): t += 0.22
        t += 0.1
    t += 0.3
json.dump(words, open("assets/transcript.estimate.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
cur = -1
for w in words:
    if w["p"] != cur: cur = w["p"]; print(f"\n--- P{cur} @ {w['start']}")
    print(f"{w['id']}:{w['text']}@{w['start']}", end="  ")
print("\nEND", round(t, 2), len(words))
