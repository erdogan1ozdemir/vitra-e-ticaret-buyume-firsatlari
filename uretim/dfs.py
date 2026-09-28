# -*- coding: utf-8 -*-
"""DataForSEO REST istemcisi · kimlik ~/.claude.json icindeki dfs-mcp env'inden okunur (ciktiya basilmaz).
Python SSL zinciri (VPN/proxy) nedeniyle istekler curl ile atilir."""
import json, os, subprocess, tempfile, time
def _kimlik():
    d = json.load(open(os.path.expanduser("~/.claude.json")))
    for scope in [d.get("mcpServers", {})] + [v.get("mcpServers", {}) for v in d.get("projects", {}).values()]:
        e = scope.get("dfs-mcp", {}).get("env", {})
        if e.get("DATAFORSEO_USERNAME"):
            return e["DATAFORSEO_USERNAME"], e["DATAFORSEO_PASSWORD"]
    raise SystemExit("dfs kimlik bulunamadi")
_U, _P = _kimlik()
def post(path, data, deneme=3):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(data, f); yol = f.name
    for i in range(deneme):
        r = subprocess.run(["curl", "-s", "-m", "300", "-u", "%s:%s" % (_U, _P), "-H", "Content-Type: application/json",
                            "--data-binary", "@" + yol, "https://api.dataforseo.com" + path], capture_output=True, text=True)
        try:
            out = json.loads(r.stdout)
            os.unlink(yol); return out
        except Exception:
            if i == deneme - 1:
                os.unlink(yol); raise SystemExit("dfs yanit okunamadi: " + r.stdout[:300] + r.stderr[:300])
            time.sleep(5)
