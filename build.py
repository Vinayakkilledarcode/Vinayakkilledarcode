"""Edit REPOS / STACK below, then run:  python build.py   (regenerates assets/terminal.svg)"""
import html

NAME   = "Vinayak Killedar (VK)"
LINE1  = "Final-year CSE @ VIT Chennai  ·  2026 batch"
LINE2  = "Algo trading  ·  Quant finance  ·  Fintech tools"
REPOS = [  # (repo name, one-line note shown under it)
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
STACK = [  # (label, colour)  -- add frameworks here, e.g. ("React","#61dafb")
 ("Python","#4b8bbe"),("JavaScript","#f7df1e"),("Kotlin","#a97bff"),("HTML","#e34f26"),
 ("Machine Learning","#30d158"),("NLP","#ff9f0a"),("Git","#f05032"),("Linux","#e5e5e7"),
]

MONO="'SF Mono',SFMono-Regular,Menlo,Monaco,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace"
SANS="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
W=880; FS=15; CW=9.0; X=28
PROMPT_STATIC="vinayak@macbook ~ % "
PROMPT_TYPE  ="vinayak@macbook ~/projects % open "
TYPE_D,HOLD,BACK_D,GAP=0.07,1.5,0.03,0.35

def seg_len(n): return n*TYPE_D+HOLD+n*BACK_D+GAP
T=round(sum(seg_len(len(r)) for r,_ in REPOS)+0.5,2)
x0=X+len(PROMPT_TYPE)*CW
yT=176   # typed line baseline
defs=""; typed=""; notes=""; cur_ev=[(0.0,x0)]
s=0.4
for i,(r,note) in enumerate(REPOS):
    n=len(r)
    ev=[(0.0,0.0)]
    for k in range(1,n+1): ev.append((s+k*TYPE_D,k*CW))
    hold_start=s+n*TYPE_D
    for k in range(1,n+1): ev.append((hold_start+HOLD+k*BACK_D,(n-k)*CW))
    kt=";".join(f"{t/T:.5f}" for t,_ in ev); vals=";".join(f"{w:.1f}" for _,w in ev)
    defs+=f'<clipPath id="c{i}"><rect x="{x0-1}" y="{yT-17}" height="24" width="0"><animate attributeName="width" calcMode="discrete" dur="{T}s" repeatCount="indefinite" keyTimes="{kt}" values="{vals}"/></rect></clipPath>'
    typed+=f'<text x="{x0}" y="{yT}" fill="#f5f5f7" clip-path="url(#c{i})" textLength="{n*CW}" lengthAdjust="spacing">{html.escape(r)}</text>'
    on=hold_start; off=hold_start+HOLD
    notes+=f'<text x="{X}" y="{yT+26}" fill="#8e8e93" font-style="italic" opacity="0"># {html.escape(note)}<animate attributeName="opacity" calcMode="discrete" dur="{T}s" repeatCount="indefinite" keyTimes="0;{on/T:.5f};{off/T:.5f}" values="0;1;0"/></text>'
    for k in range(1,n+1): cur_ev.append((s+k*TYPE_D,x0+k*CW))
    for k in range(1,n+1): cur_ev.append((hold_start+HOLD+k*BACK_D,x0+(n-k)*CW))
    s+=seg_len(n)
ckt=";".join(f"{t/T:.5f}" for t,_ in cur_ev); cv=";".join(f"{x:.1f}" for _,x in cur_ev)
cursor=(f'<rect y="{yT-15}" width="{CW}" height="19" fill="#d1d1d6" x="{x0}"><animate attributeName="x" calcMode="discrete" dur="{T}s" repeatCount="indefinite" keyTimes="{ckt}" values="{cv}"/>'
        f'<animate attributeName="opacity" calcMode="discrete" dur="1.1s" repeatCount="indefinite" keyTimes="0;0.6" values="1;0"/></rect>')

def prompt(y,rest,cmd):
    full=PROMPT_STATIC+cmd; n=len(full)
    return (f'<text x="{X}" y="{y}" textLength="{n*CW}" lengthAdjust="spacing" xml:space="preserve">'
            f'<tspan fill="#30d158">vinayak@macbook</tspan><tspan fill="#0a84ff"> ~</tspan><tspan fill="#d1d1d6"> % </tspan><tspan fill="#f5f5f7">{html.escape(cmd)}</tspan></text>')

# pills
pills=""; px=X; py=292
for i,(lab,col) in enumerate(STACK):
    w=len(lab)*7.9+30
    pills+=(f'<g transform="translate({px:.1f},{py})"><g>'
      f'<animateTransform attributeName="transform" type="translate" additive="sum" dur="2.6s" begin="{i*0.14:.2f}s" repeatCount="indefinite" calcMode="spline" '
      f'keyTimes="0;0.10;0.20;0.26;0.32;1" keySplines="0.2 0.6 0.4 1;0.6 0 0.8 0.4;0.2 0.6 0.4 1;0.6 0 0.8 0.4;0 0 1 1" values="0,0;0,-15;0,0;0,-6;0,0;0,0"/>'
      f'<rect width="{w:.1f}" height="28" rx="14" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".55"/>'
      f'<text x="{w/2:.1f}" y="19" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="600" fill="{col}">{html.escape(lab)}</text>'
      f'</g></g>')
    px+=w+10
H=372
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{MONO}" font-size="{FS}">
<defs>{defs}
<linearGradient id="tb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3c3c3e"/><stop offset="1" stop-color="#2c2c2e"/></linearGradient>
<filter id="sh" x="-5%" y="-5%" width="110%" height="115%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-opacity=".45"/></filter></defs>
<g filter="url(#sh)"><rect x="4" y="2" width="{W-8}" height="{H-12}" rx="12" fill="#1c1c1e" stroke="#48484a"/></g>
<path d="M4 14a12 12 0 0 1 12-12h{W-32}a12 12 0 0 1 12 12v26H4z" fill="url(#tb)"/>
<line x1="4" y1="40" x2="{W-4}" y2="40" stroke="#48484a"/>
<circle cx="26" cy="21" r="6.5" fill="#ff5f57"/><circle cx="46" cy="21" r="6.5" fill="#febc2e"/><circle cx="66" cy="21" r="6.5" fill="#28c840"/>
<text x="{W/2}" y="26" text-anchor="middle" font-family="{SANS}" font-size="13" fill="#98989d">vinayak — -zsh — 100×30</text>
{prompt(76,"","whoami")}
<text x="{X}" y="102" fill="#f5f5f7" font-weight="600">{html.escape(NAME)}</text>
<text x="{X}" y="126" fill="#aeaeb2">{html.escape(LINE1)}</text>
<text x="{X}" y="150" fill="#aeaeb2">{html.escape(LINE2)}</text>
<text x="{X}" y="{yT}" textLength="{len(PROMPT_TYPE)*CW}" lengthAdjust="spacing" xml:space="preserve"><tspan fill="#30d158">vinayak@macbook</tspan><tspan fill="#0a84ff"> ~/projects</tspan><tspan fill="#d1d1d6"> % </tspan><tspan fill="#ff9f0a">open </tspan></text>
{typed}{cursor}{notes}
{prompt(262,"","cat stack.txt")}
{pills}
<text x="{X}" y="{H-24}" xml:space="preserve"><tspan fill="#30d158">vinayak@macbook</tspan><tspan fill="#0a84ff"> ~</tspan><tspan fill="#d1d1d6"> % </tspan><tspan fill="#d1d1d6">open-to-work --role fintech</tspan></text>
</svg>'''
open("assets/terminal.svg","w",encoding="utf-8").write(svg)
print("ok, loop",T,"s")
