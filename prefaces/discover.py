import sys, re, time, urllib.request
sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
BASE = "https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build"
out = {}
for nn in [f"{i:02d}" for i in range(1, 27)]:
    img = ""
    for attempt in range(6):
        try:
            url = f"{BASE}/dictionaries/prefaces/pepref/pepref{nn}.html"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
            m = re.search(r'_images/([^"]+\.png)', html)
            if m:
                img = m.group(1)
                break
        except Exception as e:
            sys.stderr.write(f"{nn} attempt {attempt}: {e}\n")
        time.sleep(2)
    out[nn] = img
    print(f"{nn}|{img}", flush=True)
with open("_manifest.txt", "w", encoding="utf-8") as f:
    for nn in sorted(out):
        f.write(f"{nn}|{out[nn]}\n")
print("DONE", sum(1 for v in out.values() if v), "of 26")
