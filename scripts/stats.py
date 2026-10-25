"""Builds dist/stats.svg from live GitHub data. Runs inside the GitHub Action; never fails the build."""
import os, json, html, sys, urllib.request
esc = html.escape
USER = os.environ.get("GH_USER", "Vinayakkilledarcode"); TOKEN = os.environ.get("GH_TOKEN", "")
SANS = "-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Inter,Roboto,Helvetica,Arial,sans-serif"
MONO = "'SF Mono',SFMono-Regular,Menlo,Monaco,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace"
COL = {"Python":"#3572A5","JavaScript":"#f1e05a","Kotlin":"#A97BFF","HTML":"#e34c26","CSS":"#a371f7","Java":"#b07219",
       "TypeScript":"#3178c6","Shell":"#89e051","C++":"#f34b7d","C":"#8e8e93","Jupyter Notebook":"#DA5B0B","Dart":"#00B4AB"}
FALL = ["#64d2ff", "#30d158", "#ff9f0a", "#ff375f", "#bf5af2"]

def api(path, body=None):
    url = path if path.startswith("http") else "https://api.github.com" + path
    h = {"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"}
    if TOKEN: h["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers=h)
    with urllib.request.urlopen(req, timeout=30) as r: return json.load(r)

def fetch():
    u = api(f"/users/{USER}")
    repos = [r for r in api(f"/users/{USER}/repos?per_page=100&type=owner") if not r["fork"]]
    langs = {}
    for r in repos:
        try:
            for k, v in api(f"/repos/{USER}/{r['name']}/languages").items(): langs[k] = langs.get(k, 0) + v
        except Exception: pass
    contrib = None
    try:
        q = {"query": "query($l:String!){user(login:$l){contributionsCollection{contributionCalendar{totalContributions}}}}", "variables": {"l": USER}}
        contrib = api("/graphql", q)["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    except Exception: pass
    return dict(repos=u["public_repos"], followers=u["followers"], stars=sum(r["stargazers_count"] for r in repos), contrib=contrib, langs=langs)

def render(d):
    W = 880; BW = W - 48
    tot = sum(d["langs"].values()) or 1
    items = sorted(d["langs"].items(), key=lambda kv: -kv[1])
    top = items[:5]; other = sum(v for _, v in items[5:])
    if other: top.append(("Other", other))
    segs = []; x = 24; fi = 0
    for name, v in top:
        c = COL.get(name) or ("#8e8e93" if name == "Other" else FALL[fi % len(FALL)]); fi += 0 if name in COL or name == "Other" else 1
        w = BW * v / tot; segs.append((name, v / tot * 100, c, x, w)); x += w
    # legend flow
    leg = ""; lx = 24; ly = 224; rows = 1
    for name, pct, c, *_ in segs:
        label = f"{name} {pct:.1f}%"; iw = 24 + len(label) * 7.3 + 18
        if lx + iw > W - 24: lx = 24; ly += 24; rows += 1
        leg += f'<circle cx="{lx+5}" cy="{ly-4}" r="5" fill="{c}"/><text x="{lx+16}" y="{ly}" font-family="{SANS}" font-size="12.5" fill="#c7c7cc">{esc(label)}</text>'
        lx += iw
    H = 252 + (rows - 1) * 24
    fmt = lambda n: "—" if n is None else f"{n:,}"
    tiles = [("PUBLIC REPOS", fmt(d["repos"]), "#64d2ff"), ("STARS EARNED", fmt(d["stars"]), "#ff9f0a"),
             ("FOLLOWERS", fmt(d["followers"]), "#30d158"), ("CONTRIBUTIONS · 1Y", fmt(d["contrib"]), "#bf5af2")]
    tw = (W - 48 - 3 * 14) / 4; tl = ""
    for i, (lab, val, c) in enumerate(tiles):
        tx = 24 + i * (tw + 14); b = 0.15 * i
        tl += (f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur=".6s" fill="freeze"/>'
               f'<animateTransform attributeName="transform" type="translate" from="0 10" to="0 0" begin="{b:.2f}s" dur=".6s" fill="freeze" calcMode="spline" keySplines=".2 .7 .3 1" keyTimes="0;1"/>'
               f'<rect x="{tx:.1f}" y="58" width="{tw:.1f}" height="86" rx="12" fill="#181a24" stroke="#2a2d3a"/>'
               f'<rect x="{tx:.1f}" y="58" width="4" height="86" rx="2" fill="{c}"/>'
               f'<text x="{tx+20:.1f}" y="86" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1.1" fill="#8e8e93">{lab}</text>'
               f'<text x="{tx+20:.1f}" y="128" font-family="{SANS}" font-size="38" font-weight="800" fill="{c}">{val}</text></g>')
    bars = ""
    for i, (name, pct, c, sx, sw) in enumerate(segs):
        bars += (f'<rect x="{sx:.1f}" y="180" width="0" height="12" fill="{c}"><animate attributeName="width" from="0" to="{max(sw-1.5,1):.1f}" begin="{0.7+i*0.12:.2f}s" dur=".7s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .7 .3 1"/></rect>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1c22"/><stop offset="1" stop-color="#13141a"/></linearGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath><clipPath id="bar"><rect x="24" y="180" width="{BW}" height="12" rx="6"/></clipPath></defs>
<g clip-path="url(#card)"><rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="38" fill="#2c2c2e"/><line x1="0" x2="{W}" y1="38" y2="38" stroke="#48484a"/>
<circle cx="22" cy="19" r="6" fill="#ff5f57"/><circle cx="42" cy="19" r="6" fill="#febc2e"/><circle cx="62" cy="19" r="6" fill="#28c840"/>
<text x="{W/2}" y="24" text-anchor="middle" font-family="{SANS}" font-size="13" fill="#98989d">stats.json — {esc(USER)}</text>
{tl}
<text x="24" y="170" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1.1" fill="#8e8e93">TOP LANGUAGES</text>
<rect x="24" y="180" width="{BW}" height="12" rx="6" fill="#2a2d3a"/>
<g clip-path="url(#bar)">{bars}<rect x="-120" y="180" width="120" height="12" fill="url(#sw)" opacity=".5"><animate attributeName="x" values="-120;{W}" begin="2s" dur="3.5s" repeatCount="indefinite"/></rect></g>
{leg}</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="13.5" fill="none" stroke="#fff" stroke-opacity=".10"/></svg>'''

if __name__ == "__main__":
    try:
        svg = render(fetch())
        os.makedirs("dist", exist_ok=True); open("dist/stats.svg", "w", encoding="utf-8").write(svg); print("stats.svg written")
    except Exception as e:
        print("stats skipped:", e); sys.exit(0)
