# Gives every script word a time from the whisper transcript.
#   python3 tools/align.py   (reads assets/transcript.whisper.json, writes assets/transcript.json)
# Letters of both texts are normalised and aligned; each script word takes the time of the
# whisper word under its first and last letters. Unmatched words are interpolated.
import json, re, difflib, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def norm(s):
    s = re.sub(r"[ً-ْـ]", "", s)
    s = re.sub("[أإآ]", "ا", s).replace("ة", "ه").replace("ى", "ي").replace("ؤ", "و").replace("ئ", "ي")
    return re.sub(r"[^ء-ي]", "", s)
script = open("SCRIPT.md", encoding="utf-8").read().split("\n", 1)[1].split()
# whisper writes some numbers as digits; spell those the way the script does
SPELL = {"1790": "الف وسبعميه وتسعين", "100": "ميه"}
wh = json.load(open("assets/transcript.whisper.json", encoding="utf-8"))
for w in wh: w["text"] = SPELL.get(re.sub(r"\D", "", w["text"]) if re.search(r"\d", w["text"]) else "", w["text"])
wh = [w for w in wh if norm(w["text"])]
sc_chars, sc_of = [], []
for i, t in enumerate(script):
    for c in norm(t): sc_chars.append(c); sc_of.append(i)
wh_chars, wh_of = [], []
for j, w in enumerate(wh):
    for c in norm(w["text"]): wh_chars.append(c); wh_of.append(j)
sm = difflib.SequenceMatcher(None, sc_chars, wh_chars, autojunk=False)
first, last = {}, {}
for a, b, n in sm.get_matching_blocks():
    for k in range(n):
        i, j = sc_of[a + k], wh_of[b + k]
        first.setdefault(i, j); last[i] = j
out = [None] * len(script)
for i in range(len(script)):
    if i in first:
        out[i] = [wh[first[i]]["start"], wh[last[i]]["end"]]
# interpolate the gaps between matched words
known = [i for i in range(len(script)) if out[i]]
for i in range(len(script)):
    if out[i]: continue
    p = max([k for k in known if k < i], default=None); q = min([k for k in known if k > i], default=None)
    a = out[p][1] if p is not None else 0.1; b = out[q][0] if q is not None else a + 0.5
    span = [k for k in range(p + 1 if p is not None else 0, q if q is not None else len(script))]
    n = span.index(i); step = (b - a) / len(span)
    out[i] = [a + n * step, a + (n + 1) * step]
# a word that shares one whisper word with its neighbour splits that word's time
i = 0
while i < len(out):
    j = i
    while j + 1 < len(out) and abs(out[j + 1][0] - out[i][0]) < 0.05: j += 1
    if j > i:
        a, b = out[i][0], max(out[k][1] for k in range(i, j + 1)); step = (b - a) / (j - i + 1)
        for k in range(i, j + 1): out[k] = [a + (k - i) * step, a + (k - i + 1) * step]
    i = j + 1
res = [{"id": f"w{i}", "text": t, "start": round(s, 3), "end": round(max(e, s + 0.05), 3)} for i, (t, (s, e)) in enumerate(zip(script, out))]
json.dump(res, open("assets/transcript.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
miss = [script[i] for i in range(len(script)) if i not in first]
print(len(script), "words;", len(miss), "interpolated:", " ".join(miss))
