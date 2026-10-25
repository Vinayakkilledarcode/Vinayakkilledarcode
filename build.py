"""
Regenerates every SVG in ./assets and README.md.
Edit the CONFIG block, then run:  python build.py
"""
import html, math, random, os
esc = html.escape

# ───────────────────────── CONFIG ─────────────────────────
USER     = "Vinayakkilledarcode"
NAME     = "Vinayak Killedar"
LINKEDIN = ""            # e.g. "https://www.linkedin.com/in/your-id"  (optional)
EMAIL    = ""            # e.g. "you@example.com"                      (optional)

ROLES = ["Algorithmic Trading", "Quantitative Finance", "Fintech Engineering",
         "Machine Learning", "Full-Stack Development"]
TERM_LINES = ["Final-year CSE @ VIT Chennai  ·  2026 batch",
              "Algo trading  ·  Quant finance  ·  Fintech tools"]
REPOS = [  # typed + backspaced in the terminal: (repo, note)
 ("ai-binary-bot",              "AI binary trading bot · ML predictions + risk management"),
 ("deriv-trading-bot",          "Trading bot · JavaScript"),
 ("thrice-nomisma",             "Bloomberg-style trading terminal · Python"),
 ("finquery",                   "Python"),
 ("nutriwise-ai",               "Explainable nutrition-risk assessment · Python"),
 ("Insight-Ink",                "News scraper, summarizer & categorizer · NLP · Python"),
 ("cancer-detection-app",       "Python"),
 ("Last-Mile-Delivery",         "JavaScript"),
 ("ration-distribution-system", "JavaScript"),
 ("HostelDietLedger",           "HTML"),
 ("secureappvult",              "Kotlin"),
]
STACK = [  # jumping pills: (label, colour)
 ("Python","#4b8bbe"),("JavaScript","#f7df1e"),("Kotlin","#a97bff"),("HTML","#e34f26"),
 ("Machine Learning","#30d158"),("NLP","#ff9f0a"),("Git","#f05032"),("Linux","#e5e5e7"),
]
CARDS = [  # featured project cards: (repo, [desc lines], language, dot colour)
 ("ai-binary-bot",    ["AI-powered binary trading bot with machine","learning predictions and risk management."], "Python",     "#3572A5"),
 ("thrice-nomisma",   ["Bloomberg-style trading terminal —","flagship fintech project."],                                     "Python",     "#3572A5"),
 ("nutriwise-ai",     ["Explainable nutrition-risk assessment","web application."],                                          "Python",     "#3572A5"),
 ("Insight-Ink",      ["AI news scraper, summarizer and categorizer","with a personalized feed using NLP."],                 "Python",     "#3572A5"),
 ("deriv-trading-bot",["Trading bot for the Deriv platform."],                                                                "JavaScript", "#f1e05a"),
 ("secureappvult",    ["Secure app vault built in Kotlin."],                                                                  "Kotlin",     "#A97BFF"),
]
TICKER = ["PYTHON","JAVASCRIPT","KOTLIN","MACHINE LEARNING","ALGORITHMIC TRADING",
          "QUANT FINANCE","FINTECH","NLP","FULL-STACK"]
# ───────────────────────────────────────────────────────────

SANS = "-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Inter,Roboto,Helvetica,Arial,sans-serif"
MONO = "'SF Mono',SFMono-Regular,Menlo,Monaco,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace"
os.makedirs("assets", exist_ok=True)
def write(name, s): open(f"assets/{name}", "w", encoding="utf-8").write(s)


# ═════════════════════════ HERO ═════════════════════════
def hero():
    W, H, T = 880, 340, 12
    R = random.Random(11)
    n = 38; cx0, cx1 = 508, 850; step = (cx1 - cx0) / (n - 1)
    price = 0.0; raw = []
    for i in range(n):
        o = price; c = o + R.uniform(-1, 1) + 0.11
        raw.append((o, c, max(o, c) + R.uniform(.15, .8), min(o, c) - R.uniform(.15, .8))); price = c
    mn = min(r[3] for r in raw); mx = max(r[2] for r in raw); top, bot = 62, 220
    Y = lambda v: bot - (v - mn) / (mx - mn) * (bot - top)
    candles = ""
    for i, (o, c, hi, lo) in enumerate(raw):
        x = cx0 + i * step; col = "#30d158" if c >= o else "#ff453a"
        candles += (f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{Y(hi):.1f}" y2="{Y(lo):.1f}" stroke="{col}" stroke-width="1.4"/>'
                    f'<rect x="{x-3:.1f}" y="{Y(max(o,c)):.1f}" width="6" height="{max(2.5,abs(Y(o)-Y(c))):.1f}" rx="1.5" fill="{col}"/>')
    ma = []
    for i in range(n):
        w = [raw[j][1] for j in range(max(0, i - 3), i + 1)]; ma.append(sum(w) / len(w))
    P = [(cx0 + i * step, Y(m)) for i, m in enumerate(ma)]
    d = f"M{P[0][0]:.1f},{P[0][1]:.1f}"; samples = [P[0]]
    for i in range(n - 1):
        p0, p1, p2, p3 = P[max(i-1, 0)], P[i], P[i+1], P[min(i+2, n-1)]
        c1 = (p1[0] + (p2[0]-p0[0])/6, p1[1] + (p2[1]-p0[1])/6)
        c2 = (p2[0] - (p3[0]-p1[0])/6, p2[1] - (p3[1]-p1[1])/6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
        for k in range(1, 13):
            t = k / 12; m = 1 - t
            samples.append((m**3*p1[0] + 3*m*m*t*c1[0] + 3*m*t*t*c2[0] + t**3*p2[0],
                            m**3*p1[1] + 3*m*m*t*c1[1] + 3*m*t*t*c2[1] + t**3*p2[1]))
    area = d + f" L{P[-1][0]:.1f},{bot+12} L{P[0][0]:.1f},{bot+12} Z"
    def y_at(xq):
        for a, b in zip(samples, samples[1:]):
            if a[0] <= xq <= b[0]:
                return a[1] if b[0] == a[0] else a[1] + (b[1]-a[1]) * (xq-a[0]) / (b[0]-a[0])
        return samples[-1][1]
    N = 72; t0, t1 = 0.05, 0.68
    xs = [cx0 + (cx1-cx0) * i / (N-1) for i in range(N)]; ys = [y_at(x) for x in xs]
    kt = ";".join(f"{v:.4f}" for v in [0] + [t0 + (t1-t0) * i / (N-1) for i in range(N)] + [0.97, 1])
    vx = ";".join(f"{v:.1f}" for v in [xs[0]] + xs + [xs[-1]] * 2)
    vy = ";".join(f"{v:.1f}" for v in [ys[0]] + ys + [ys[-1]] * 2)
    rw = cx1 - cx0 + 28
    grid = "".join(f'<line x1="470" x2="{W}" y1="{y}" y2="{y}" stroke="#fff" stroke-opacity=".05"/>' for y in range(top, bot + 1, 48))
    grid += "".join(f'<line x1="{x}" x2="{x}" y1="{top-10}" y2="{bot+10}" stroke="#fff" stroke-opacity=".04"/>' for x in range(508, W, 86))
    dotanim = (f'<animate attributeName="cx" values="{vx}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/>'
               f'<animate attributeName="cy" values="{vy}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/>')
    fade = f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.05;0.9;0.97;1" dur="{T}s" repeatCount="indefinite"/>'
    # roles
    roles = ""
    k = len(ROLES)
    for i, r in enumerate(ROLES):
        a, b = i / k, (i + 1) / k
        kts = ";".join(f"{v:.4f}" for v in [0, a, a + .025, b - .025, b, 1]); vals = "0;0;1;1;0;0"
        if i == 0: vals = "0;0;1;1;0;0"
        roles += (f'<text x="78" y="196" font-family="{MONO}" font-size="24" font-weight="700" fill="url(#rg)" opacity="0">{esc(r)}'
                  f'<animate attributeName="opacity" values="{vals}" keyTimes="{kts}" dur="{T*2.5:.0f}s" repeatCount="indefinite"/></text>')
    # ticker
    P_W = 1180
    tick = "".join(f'<tspan fill="#c7c7cc">{esc(t)}</tspan><tspan fill="#30d158" dx="9"> ▲</tspan><tspan dx="34"> </tspan>' for t in TICKER)
    ticker = "".join(
        f'<text x="{o}" y="{H-13}" font-family="{MONO}" font-size="11.5" font-weight="700" xml:space="preserve" textLength="{P_W}" lengthAdjust="spacing">{tick}</text>'
        for o in (0, P_W))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0c14"/><stop offset=".55" stop-color="#11142a"/><stop offset="1" stop-color="#0b0d16"/></linearGradient>
<radialGradient id="o1"><stop offset="0" stop-color="#0a84ff" stop-opacity=".55"/><stop offset="1" stop-color="#0a84ff" stop-opacity="0"/></radialGradient>
<radialGradient id="o2"><stop offset="0" stop-color="#bf5af2" stop-opacity=".45"/><stop offset="1" stop-color="#bf5af2" stop-opacity="0"/></radialGradient>
<radialGradient id="o3"><stop offset="0" stop-color="#30d158" stop-opacity=".22"/><stop offset="1" stop-color="#30d158" stop-opacity="0"/></radialGradient>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="#fff" fill-opacity=".07"/></pattern>
<linearGradient id="tg" gradientUnits="userSpaceOnUse" x1="48" y1="0" x2="448" y2="0" spreadMethod="reflect"><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#7db7ff"/><stop offset="1" stop-color="#c58bff"/><animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="800 0" dur="9s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="rg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#64d2ff"/><stop offset="1" stop-color="#30d158"/></linearGradient>
<linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a84ff" stop-opacity=".30"/><stop offset="1" stop-color="#0a84ff" stop-opacity="0"/></linearGradient>
<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0a84ff"/><stop offset="1" stop-color="#64d2ff"/></linearGradient>
<linearGradient id="lb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0a84ff" stop-opacity="0"/><stop offset=".5" stop-color="#64d2ff"/><stop offset="1" stop-color="#bf5af2" stop-opacity="0"/></linearGradient>
<linearGradient id="mg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000"/><stop offset=".52" stop-color="#000"/><stop offset=".64" stop-color="#fff"/><stop offset="1" stop-color="#fff"/></linearGradient>
<mask id="mk"><rect width="{W}" height="{H}" fill="url(#mg)"/></mask>
<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<clipPath id="rv"><rect x="{cx0-14}" y="0" width="0" height="{H}"><animate attributeName="width" values="0;0;{rw};{rw}" keyTimes="0;{t0};{t1};1" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>
<clipPath id="tk"><rect y="{H-34}" width="{W}" height="34"/></clipPath>
<filter id="gl" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<circle cx="150" cy="80" r="190" fill="url(#o1)"><animateTransform attributeName="transform" type="translate" values="0,0;70,40;-30,60;0,0" dur="19s" repeatCount="indefinite"/></circle>
<circle cx="720" cy="70" r="170" fill="url(#o2)"><animateTransform attributeName="transform" type="translate" values="0,0;-60,50;30,-10;0,0" dur="23s" repeatCount="indefinite"/></circle>
<circle cx="520" cy="320" r="150" fill="url(#o3)"><animateTransform attributeName="transform" type="translate" values="0,0;-50,-30;40,-10;0,0" dur="17s" repeatCount="indefinite"/></circle>
<rect width="{W}" height="{H}" fill="url(#dots)"/>
<g mask="url(#mk)">{grid}
<g clip-path="url(#rv)"><g><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.9;0.97;1" dur="{T}s" repeatCount="indefinite"/>
<path d="{area}" fill="url(#ar)"/>
<g opacity=".92">{candles}</g>
<path d="{d}" fill="none" stroke="#0a84ff" stroke-width="7" stroke-opacity=".55" filter="url(#gl)"/>
<path d="{d}" fill="none" stroke="url(#ln)" stroke-width="2.4" stroke-linecap="round"/></g></g>
<circle r="4.5" fill="#fff" opacity="0">{dotanim}{fade}</circle>
<circle r="6" fill="none" stroke="#64d2ff" stroke-width="2" opacity="0">{dotanim}{fade}<animate attributeName="r" values="5;17" dur="1.6s" repeatCount="indefinite"/></circle>
</g>
<rect y="0" x="-260" width="260" height="3" fill="url(#lb)"><animate attributeName="x" values="-260;{W}" dur="3.4s" repeatCount="indefinite"/></rect>
<g transform="translate({W-176},22)"><rect width="150" height="24" rx="12" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".12"/>
<circle cx="15" cy="12" r="3.5" fill="#30d158"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
<text x="27" y="16.5" font-family="{MONO}" font-size="11" font-weight="700" fill="#c7c7cc">PORTFOLIO · LIVE</text></g>
<text x="48" y="94" font-family="{MONO}" font-size="14" xml:space="preserve"><tspan fill="#6e6e73">// </tspan><tspan fill="#98989d">hello, world. I'm</tspan></text>
<text x="46" y="148" font-family="{SANS}" font-size="58" font-weight="800" letter-spacing="-1.5" fill="url(#tg)">{esc(NAME)}</text>
<text x="48" y="196" font-family="{MONO}" font-size="24" font-weight="700" fill="#30d158">&gt;</text>
{roles}
<text x="48" y="230" font-family="{SANS}" font-size="15" fill="#a1a1a6">Final-year CSE student @ VIT Chennai · 2026 batch</text>
<text x="48" y="252" font-family="{SANS}" font-size="15" fill="#a1a1a6">Building algorithmic-trading systems, ML tools and fintech products.</text>
<g transform="translate(48,266)"><rect width="206" height="28" rx="14" fill="#30d158" fill-opacity=".12" stroke="#30d158" stroke-opacity=".55"/>
<circle cx="17" cy="14" r="4" fill="#30d158"/><circle cx="17" cy="14" r="4" fill="none" stroke="#30d158"><animate attributeName="r" values="4;11" dur="1.8s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".9;0" dur="1.8s" repeatCount="indefinite"/></circle>
<text x="32" y="19" font-family="{SANS}" font-size="13" font-weight="600" fill="#30d158">Open to full-time roles</text></g>
<rect y="{H-34}" width="{W}" height="34" fill="#fff" fill-opacity=".04"/><line x1="0" x2="{W}" y1="{H-34}" y2="{H-34}" stroke="#fff" stroke-opacity=".08"/>
<g clip-path="url(#tk)"><g>{ticker}<animateTransform attributeName="transform" type="translate" from="0 0" to="-{P_W} 0" dur="30s" repeatCount="indefinite"/></g></g>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="17.5" fill="none" stroke="#fff" stroke-opacity=".10"/>
</svg>'''


# ═════════════════════════ TERMINAL ═════════════════════════
def terminal():
    W, FS, CW, X = 880, 15, 9.0, 28
    PS = "vinayak@macbook ~ % "; PT = "vinayak@macbook ~/projects % open "
    TYPE_D, HOLD, BACK_D, GAP = 0.07, 1.5, 0.03, 0.35
    seg = lambda n: n*TYPE_D + HOLD + n*BACK_D + GAP
    T = round(sum(seg(len(r)) for r, _ in REPOS) + 0.5, 2)
    x0 = X + len(PT) * CW; yT = 176
    defs = typed = notes = ""; cur = [(0.0, x0)]; s = 0.4
    for i, (r, note) in enumerate(REPOS):
        n = len(r); ev = [(0.0, 0.0)]
        for k in range(1, n+1): ev.append((s + k*TYPE_D, k*CW))
        hs = s + n*TYPE_D
        for k in range(1, n+1): ev.append((hs + HOLD + k*BACK_D, (n-k)*CW))
        kt = ";".join(f"{t/T:.5f}" for t, _ in ev); vals = ";".join(f"{w:.1f}" for _, w in ev)
        defs += (f'<clipPath id="c{i}"><rect x="{x0-1}" y="{yT-17}" height="24" width="0"><animate attributeName="width" calcMode="discrete" '
                 f'dur="{T}s" repeatCount="indefinite" keyTimes="{kt}" values="{vals}"/></rect></clipPath>')
        typed += f'<text x="{x0}" y="{yT}" fill="#f5f5f7" clip-path="url(#c{i})" textLength="{n*CW}" lengthAdjust="spacing">{esc(r)}</text>'
        notes += (f'<text x="{X}" y="{yT+26}" fill="#8e8e93" font-style="italic" opacity="0"># {esc(note)}'
                  f'<animate attributeName="opacity" calcMode="discrete" dur="{T}s" repeatCount="indefinite" '
                  f'keyTimes="0;{hs/T:.5f};{(hs+HOLD)/T:.5f}" values="0;1;0"/></text>')
        for k in range(1, n+1): cur.append((s + k*TYPE_D, x0 + k*CW))
        for k in range(1, n+1): cur.append((hs + HOLD + k*BACK_D, x0 + (n-k)*CW))
        s += seg(n)
    ckt = ";".join(f"{t/T:.5f}" for t, _ in cur); cv = ";".join(f"{x:.1f}" for _, x in cur)
    cursor = (f'<rect y="{yT-15}" width="{CW}" height="19" fill="#d1d1d6" x="{x0}"><animate attributeName="x" calcMode="discrete" dur="{T}s" '
              f'repeatCount="indefinite" keyTimes="{ckt}" values="{cv}"/><animate attributeName="opacity" calcMode="discrete" dur="1.1s" '
              f'repeatCount="indefinite" keyTimes="0;0.6" values="1;0"/></rect>')
    def prompt(y, cmd):
        n = len(PS + cmd)
        return (f'<text x="{X}" y="{y}" textLength="{n*CW}" lengthAdjust="spacing" xml:space="preserve"><tspan fill="#30d158">vinayak@macbook</tspan>'
                f'<tspan fill="#0a84ff"> ~</tspan><tspan fill="#d1d1d6"> % </tspan><tspan fill="#f5f5f7">{esc(cmd)}</tspan></text>')
    pills = ""; px = X; py = 292
    for i, (lab, col) in enumerate(STACK):
        w = len(lab) * 7.9 + 30
        pills += (f'<g transform="translate({px:.1f},{py})"><g><animateTransform attributeName="transform" type="translate" additive="sum" dur="2.6s" '
                  f'begin="{i*0.14:.2f}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.10;0.20;0.26;0.32;1" '
                  f'keySplines="0.2 0.6 0.4 1;0.6 0 0.8 0.4;0.2 0.6 0.4 1;0.6 0 0.8 0.4;0 0 1 1" values="0,0;0,-15;0,0;0,-6;0,0;0,0"/>'
                  f'<rect width="{w:.1f}" height="28" rx="14" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".55"/>'
                  f'<text x="{w/2:.1f}" y="19" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="600" fill="{col}">{esc(lab)}</text></g></g>')
        px += w + 10
    H = 372
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{MONO}" font-size="{FS}">
<defs>{defs}
<linearGradient id="tb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3c3c3e"/><stop offset="1" stop-color="#2c2c2e"/></linearGradient>
<linearGradient id="bd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e1e20"/><stop offset="1" stop-color="#161618"/></linearGradient>
<filter id="sh" x="-5%" y="-5%" width="110%" height="115%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-opacity=".45"/></filter></defs>
<g filter="url(#sh)"><rect x="4" y="2" width="{W-8}" height="{H-12}" rx="12" fill="url(#bd)" stroke="#48484a"/></g>
<path d="M4 14a12 12 0 0 1 12-12h{W-32}a12 12 0 0 1 12 12v26H4z" fill="url(#tb)"/>
<line x1="4" y1="40" x2="{W-4}" y2="40" stroke="#48484a"/>
<circle cx="26" cy="21" r="6.5" fill="#ff5f57"/><circle cx="46" cy="21" r="6.5" fill="#febc2e"/><circle cx="66" cy="21" r="6.5" fill="#28c840"/>
<text x="{W/2}" y="26" text-anchor="middle" font-family="{SANS}" font-size="13" fill="#98989d">vinayak — -zsh — 100×30</text>
{prompt(76, "whoami")}
<text x="{X}" y="102" fill="#f5f5f7" font-weight="600">{esc(NAME)} (VK)</text>
<text x="{X}" y="126" fill="#aeaeb2">{esc(TERM_LINES[0])}</text>
<text x="{X}" y="150" fill="#aeaeb2">{esc(TERM_LINES[1])}</text>
<text x="{X}" y="{yT}" textLength="{len(PT)*CW}" lengthAdjust="spacing" xml:space="preserve"><tspan fill="#30d158">vinayak@macbook</tspan><tspan fill="#0a84ff"> ~/projects</tspan><tspan fill="#d1d1d6"> % </tspan><tspan fill="#ff9f0a">open </tspan></text>
{typed}{cursor}{notes}
{prompt(262, "cat stack.txt")}
{pills}
<text x="{X}" y="{H-24}" xml:space="preserve"><tspan fill="#30d158">vinayak@macbook</tspan><tspan fill="#0a84ff"> ~</tspan><tspan fill="#d1d1d6"> % </tspan><tspan fill="#d1d1d6">open-to-work --role fintech</tspan></text>
</svg>'''


# ═════════════════════════ SECTION HEADER ═════════════════════════
def header(cmd):
    W, H, CW = 880, 46, 10.2
    PS = "vinayak@macbook ~ % "; n = len(PS + cmd)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{MONO}" font-size="17">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0a84ff" stop-opacity="0"/><stop offset=".5" stop-color="#64d2ff"/><stop offset="1" stop-color="#bf5af2" stop-opacity="0"/></linearGradient>
<clipPath id="c"><rect x="0" y="0" width="{W}" height="{H}" rx="12"/></clipPath></defs>
<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="#1c1c1e"/><rect width="{W}" height="{H}" fill="#fff" fill-opacity=".03"/>
<circle cx="22" cy="23" r="5.5" fill="#ff5f57"/><circle cx="40" cy="23" r="5.5" fill="#febc2e"/><circle cx="58" cy="23" r="5.5" fill="#28c840"/>
<text x="84" y="29" textLength="{n*CW}" lengthAdjust="spacing" xml:space="preserve"><tspan fill="#30d158">vinayak@macbook</tspan><tspan fill="#0a84ff"> ~</tspan><tspan fill="#d1d1d6"> % </tspan><tspan fill="#f5f5f7">{esc(cmd)}</tspan></text>
<rect x="{84+n*CW+6}" y="12" width="10" height="21" fill="#d1d1d6"><animate attributeName="opacity" calcMode="discrete" values="1;0" keyTimes="0;.6" dur="1.1s" repeatCount="indefinite"/></rect>
<rect x="-300" y="{H-2}" width="300" height="2" fill="url(#g)"><animate attributeName="x" values="-300;{W}" dur="4s" repeatCount="indefinite"/></rect></g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="11.5" fill="none" stroke="#fff" stroke-opacity=".10"/></svg>'''


# ═════════════════════════ PROJECT CARD ═════════════════════════
def card(repo, lines, lang, col):
    W, H = 436, 158
    delay = sum(map(ord, repo)) % 6
    desc = "".join(f'<text x="26" y="{70+i*22}" font-family="{SANS}" font-size="13.5" fill="#a1a1aa">{esc(l)}</text>' for i, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#181a24"/><stop offset="1" stop-color="#11121a"/></linearGradient>
<linearGradient id="bd" gradientUnits="userSpaceOnUse" x1="-{W}" y1="0" x2="0" y2="{H}"><stop offset="0" stop-color="#2a2d3a"/><stop offset=".5" stop-color="#4f9dff"/><stop offset=".75" stop-color="#bf5af2"/><stop offset="1" stop-color="#2a2d3a"/>
<animate attributeName="x1" values="-{W};{W}" dur="6s" repeatCount="indefinite"/><animate attributeName="x2" values="0;{W*2}" dur="6s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="nm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7db7ff"/><stop offset="1" stop-color="#c58bff"/></linearGradient>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="c"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14"/></clipPath></defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="url(#bg)"/>
<g clip-path="url(#c)"><rect x="-140" y="-20" width="90" height="{H+40}" fill="url(#sh)" transform="skewX(-20)"><animate attributeName="x" values="-140;{W+60}" dur="7s" begin="{delay}s" repeatCount="indefinite"/></rect></g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="url(#bd)" stroke-width="1.4"/>
<g transform="translate(26,21)" fill="none" stroke="#8e9aff" stroke-width="1.6" stroke-linecap="round"><rect width="13" height="16" rx="2.5"/><path d="M4 5h5M4 9h5"/></g>
<text x="50" y="35" font-family="{SANS}" font-size="18" font-weight="700" fill="url(#nm)">{esc(repo)}</text>
<g transform="translate({W-78},19)"><rect width="52" height="21" rx="10.5" fill="none" stroke="#3a3a3c"/><text x="26" y="14.5" text-anchor="middle" font-family="{SANS}" font-size="11" font-weight="600" fill="#8e8e93">Public</text></g>
{desc}
<line x1="26" x2="{W-26}" y1="112" y2="112" stroke="#fff" stroke-opacity=".07"/>
<circle cx="31" cy="136" r="5.5" fill="{col}"/><circle cx="31" cy="136" r="5.5" fill="none" stroke="{col}"><animate attributeName="r" values="5.5;11" dur="2.4s" begin="{delay*0.3:.1f}s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".8;0" dur="2.4s" begin="{delay*0.3:.1f}s" repeatCount="indefinite"/></circle>
<text x="45" y="141" font-family="{SANS}" font-size="13" font-weight="500" fill="#c7c7cc">{esc(lang)}</text>
<text x="{W-52}" y="141" text-anchor="end" font-family="{SANS}" font-size="13" font-weight="600" fill="#0a84ff">View repository</text>
<path transform="translate({W-44},132)" d="M0 1l6 4-6 4" fill="none" stroke="#0a84ff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><animateTransform attributeName="transform" type="translate" additive="sum" values="0,0;4,0;0,0" dur="1.6s" repeatCount="indefinite"/></path>
</svg>'''


# ═════════════════════════ FOOTER ═════════════════════════
def footer():
    W, H, PER = 880, 150, 440
    def wave(amp, phase, base):
        pts = [f"{x},{base + amp*math.sin((x/PER)*2*math.pi + phase):.1f}" for x in range(0, W + PER + 8, 8)]
        return "M" + " L".join(pts) + f" L{W+PER+8},{H} L0,{H} Z"
    layers = [(14, 0.0, 96, "#0a84ff", .30, 10), (18, 2.1, 104, "#5e5ce6", .45, 14), (12, 4.2, 116, "#bf5af2", .75, 19)]
    ws = "".join(f'<path d="{wave(a, p, b)}" fill="{c}" fill-opacity="{o}"><animateTransform attributeName="transform" type="translate" from="0 0" to="-{PER} 0" dur="{d}s" repeatCount="indefinite"/></path>'
                 for a, p, b, c, o, d in layers)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><linearGradient id="t" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0a84ff"/><stop offset=".5" stop-color="#bf5af2"/><stop offset="1" stop-color="#ff375f"/></linearGradient></defs>
<text x="{W/2}" y="42" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="700" fill="url(#t)">Let’s build something great together.</text>
<text x="{W/2}" y="68" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#8e8e93">© 2026 {esc(NAME)}  ·  animated with pure SVG, refreshed by a GitHub Action</text>
{ws}</svg>'''


# ═════════════════════════ WRITE EVERYTHING ═════════════════════════
write("hero.svg", hero()); write("terminal.svg", terminal())
write("h-projects.svg", header("ls ~/featured-projects"))
write("h-activity.svg", header("git log --graph --contributions"))
write("h-stats.svg", header("cat ~/stats.json"))
write("footer.svg", footer())
for repo, lines, lang, col in CARDS: write(f"card-{repo}.svg", card(repo, lines, lang, col))

cards_html = "\n".join(
    f'<a href="https://github.com/{USER}/{r}"><img src="./assets/card-{r}.svg" alt="{r}" width="49%"/></a>' for r, *_ in CARDS)
links = ""
if LINKEDIN: links += f'<a href="{LINKEDIN}"><img src="https://img.shields.io/badge/LinkedIn-0a84ff?style=for-the-badge&logo=linkedin&logoColor=white"/></a> '
if EMAIL:    links += f'<a href="mailto:{EMAIL}"><img src="https://img.shields.io/badge/Email-30d158?style=for-the-badge&logo=gmail&logoColor=white"/></a>'
links = f"\n<p>{links.strip()}</p>\n" if links else ""
raw = f"https://raw.githubusercontent.com/{USER}/{USER}/output"
readme = f'''<div align="center">

<img src="./assets/hero.svg" alt="{NAME}: fintech and algorithmic trading" width="100%"/>

<img src="./assets/terminal.svg" alt="terminal" width="100%"/>

<img src="./assets/h-projects.svg" alt="featured projects" width="100%"/>

{cards_html}

<img src="./assets/h-activity.svg" alt="activity" width="100%"/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{raw}/github-snake-dark.svg"/>
  <img alt="contribution snake" src="{raw}/github-snake.svg" width="100%"/>
</picture>

<img src="./assets/h-stats.svg" alt="stats" width="100%"/>

<img src="{raw}/stats.svg" alt="GitHub stats" width="100%"/>
{links}
<img src="./assets/footer.svg" alt="footer" width="100%"/>

</div>
'''
open("README.md", "w", encoding="utf-8").write(readme)
print("built:", sorted(os.listdir("assets")))
