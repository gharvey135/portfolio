import json, re, html
from venues import VENUES, REPOS
from flow import flow
from diagrams_v2 import DGM, SHOTS

entries = json.load(open('content.json'))
plain   = json.load(open('plain.json'))
css     = ''.join(open(f).read() for f in ('style.css','alias.css','proto.css'))
js      = open('portfolio.js').read() + '\n' + open('ux.js').read()

def dec(s): return html.unescape(s or '').replace('&middot;', ',')

ICON = {
 "code":'<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8a8 8 0 005.47 7.59c.4.07.55-.17.55-.38l-.01-1.49c-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.4 7.4 0 014 0c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48l-.01 2.19c0 .21.15.46.55.38A8.01 8.01 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>',
 "demo":'<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 3.5v9l7-4.5z" fill="currentColor" stroke="none"/><circle cx="8" cy="8" r="7"/></svg>',
 "doc" :'<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 1.5H4a1 1 0 00-1 1v11a1 1 0 001 1h8a1 1 0 001-1V5.5z"/><path d="M9 1.5v4h4M5.5 8.5h5M5.5 11h3"/></svg>',
}
LI   = '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M3.6 5.3H.7V15h2.9V5.3zM2.1.9A1.7 1.7 0 100 2.6 1.7 1.7 0 002.1.9zM15 9.5c0-2.8-1.5-4.1-3.5-4.1a3 3 0 00-2.7 1.5V5.3H5.9V15h2.9V9.9c0-1.2.2-2.4 1.7-2.4s1.5 1.4 1.5 2.5V15H15z"/></svg>'
MAIL = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1.2" y="3" width="13.6" height="10" rx="1.5"/><path d="M1.5 4l6.5 4.6L14.5 4"/></svg>'

def links_row(links):
    if not links: return ''
    return '<div class="card-links">' + ''.join(
        f'<a class="clink" href="{u}" target="_blank" rel="noopener" onclick="event.stopPropagation()">{ICON[k]}{t}</a>'
        for k, u, t in links) + '</div>'

def card(*, slug, human_title, tech_body, prov, impact, live, tags,
         pain, solve, where, steps, why, proto='', links=None):
    chips  = '<span class="mchip live">personal project</span>' if live else ''
    chips += f'<span class="mchip">{dec(prov)}</span>' if prov else ''
    chips += f'<span class="mchip impact">{dec(impact)}</span>' if impact else ''
    tagshtml  = ''.join(f'<span class="tag">{dec(t)}</span>' for t in tags)
    stepshtml = ''.join(f'<li>{s}</li>' for s in steps)
    spec = DGM.get(slug)
    vis = f'<div class="card-vis">{flow(spec)}</div>' if spec else ''
    shot = ''
    if slug in SHOTS:
        src, alt = SHOTS[slug]
        shot = (f'<figure class="shot"><img src="{src}" alt="{alt}" loading="lazy" width="1400" height="760">'
                f'<figcaption>{alt}</figcaption></figure>')
    return f'''
<article class="card" id="b-{slug}" data-rv>
  <div class="card-top" onclick="this.parentNode.classList.toggle('open')" role="button" tabindex="0"
       onkeydown="if(event.key==='Enter'||event.key===' '){{event.preventDefault();this.parentNode.classList.toggle('open')}}">
    <div class="card-meta"><span class="slug">{slug}</span>{chips}</div>
    <div class="card-body-wrap">
      <div class="card-txt">
        <h3 class="card-title">{human_title}</h3>
        <p class="card-body">{tech_body}</p>
        <div class="tags">{tagshtml}</div>
        {links_row(links)}
      </div>
      {vis}
    </div>
  </div>
  <div class="detail" onclick="event.stopPropagation()"><div class="detail-in">
    {shot}
    <div class="frame">
      <div class="fc pain"><div class="fc-l">The problem</div><p class="fc-t">{pain}</p></div>
      <div class="fc solve"><div class="fc-l">What changed</div><p class="fc-t">{solve}</p></div>
    </div>
    <div class="build" onclick="event.stopPropagation(); this.classList.toggle('open')">
      <div class="build-h"><span class="build-i">&#9656;</span><span class="build-t">How it was built</span>
        <span class="build-w">{dec(where)}</span></div>
      <div class="build-b"><div class="build-in">
        <ol class="steps">{stepshtml}</ol>
        <p class="why">{why}</p>
      </div></div>
    </div>
    {proto}
  </div></div>
</article>'''

def from_entry(e):
    p = plain[e['title']]
    prov = dec(e['where'])
    if prov.startswith('Design concept'): prov = 'Design study'
    if e['status'] == 'In Build': prov = 'In active development'
    return card(slug=e['title'], human_title=p['human_title'], tech_body=e['body'],
                prov=prov, impact=p['impact'], live=False, tags=e['tags'],
                pain=e['pain'], solve=e['solve'], where=e['where'],
                steps=e['steps'], why=e['why'], proto=e['proto'])

def from_venue(v):
    return card(slug=v['slug'], human_title=v['human_title'], tech_body=v['tech_body'],
                prov=v['prov'], impact=v['impact'], live=v['live'], tags=v['tags'],
                pain=v['pain'], solve=v['solve'], where=v['where'],
                steps=v['steps'], why=v['why'], proto=v['proto'], links=v['links'])

by_cat = {}
for e in entries: by_cat.setdefault(e['cat'], []).append(e)

SECTIONS = [
 ("clients", "Client delivery", "Shipped to enterprise customers",
  "Scoped, built, taken to production, and handed to their team to run. "
  "Mock data or changed names are used throughout for privacy where necessary.",
  [from_entry(e) for e in by_cat.get('clients', [])]),
 ("production", "Personal projects", "Systems I built and run",
  "Built for the two Austin venues I co-own, and running there now. The code and the live demos are public.",
  [from_venue(v) for v in VENUES]),
 ("solutions", "Internal tools", "Tools I built to do the job better",
  "Built between engagements, for scoping, account reviews, and integration debugging. "
  "Each one turns a task that used to need a senior engineer into something a team can run.",
  [from_entry(e) for e in by_cat.get('solutions', [])]),
 ("operations", "Back office automation", "The work nobody wants to do twice",
  "Recurring internal work turned into something that runs on a schedule: documents rebuilt, "
  "updates drafted, action items chased, renewals flagged before they lapse.",
  [from_entry(e) for e in by_cat.get('operations', [])]),
 ("personal", "Side builds", "Problems I had, solved end to end",
  "Built for myself rather than tolerated.",
  [from_entry(e) for e in by_cat.get('personal', [])]),
]

secs = ''
for sid, eyebrow, title, note, cards in SECTIONS:
    secs += f'''
<section class="sec" id="{sid}"><div class="wrap">
  <div class="sec-head" data-rv>
    <div class="sec-tag">{eyebrow}<span>{len(cards)}</span></div>
    <h2>{title}</h2>
    <p class="sec-note">{note}</p>
  </div>
  <div class="grid">{''.join(cards)}</div>
</div></section>'''

repos = ''.join(
  f'''<a class="repo" data-rv href="https://github.com/gharvey135/{n}" target="_blank" rel="noopener">
    <div class="repo-n">{ICON["code"]}{n}</div><p class="repo-d">{d}</p>
    <div class="repo-m"><span>{lang}</span></div></a>''' for n, d, lang, t in REPOS)

secs += f'''
<section class="sec" id="code"><div class="wrap">
  <div class="sec-head" data-rv>
    <div class="sec-tag">Code<span>{len(REPOS)}</span></div>
    <h2>Open source</h2>
    <p class="sec-note">Each one runs from a clean clone with no credentials, and ships with continuous integration.</p>
  </div>
  <div class="repos">{repos}</div>
</div></section>'''

NAV = [("clients","client delivery"),("production","personal projects"),("solutions","internal tools"),
       ("operations","back office"),("personal","side builds"),("code","open source")]
nav = ''.join(f'<a href="#{i}">{l}</a>' for i, l in NAV)

HERO_MAP = flow({
  "zones": ["Systems you already run", "What I do", "What you are left with"],
  "cols": [
    [{"label": "CRM and support", "sub": "Salesforce, HubSpot, Zendesk", "icon": "cloud"},
     {"label": "Payments and POS", "sub": "Toast, Melio, billing", "icon": "receipt"},
     {"label": "Files and spreadsheets", "sub": "Dropbox, Google Workspace", "icon": "folder"}],
    [{"label": "Design and build the join", "sub": "discovery through launch", "icon": "gear"},
     {"label": "Add AI where it pays", "sub": "with a person in the loop", "icon": "robot"}],
    [{"label": "One set of numbers", "sub": "that everyone agrees on", "icon": "database"},
     {"label": "Reports people read", "sub": "answers, not raw exports", "icon": "chart"},
     {"label": "A team that runs it", "sub": "without needing me", "icon": "person"}],
  ],
  "caption": "The shape of most of my work",
})

STAGES = ["Discovery", "Architecture", "Build", "Launch", "Handoff"]
stages = ''.join(
  f'<li><span class="st-n">{i+1}</span><span class="st-t">{t}</span></li>'
  for i, t in enumerate(STAGES))

DESC = ("Georgia Harvey. Eight years of enterprise integrations and AI workflows: solutions architecture, "
        "sales engineering, and forward deployed delivery, discovery through handoff. Client delivery, "
        "systems I run, and open source, with the code.")

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Georgia Harvey, Solutions and Forward Deployed Engineering</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="Georgia Harvey, Solutions and Forward Deployed Engineering">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#08090C">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2220%22 fill=%22%2308090C%22/><text y=%2270%22 x=%2250%22 text-anchor=%22middle%22 font-size=%2258%22 font-family=%22monospace%22 fill=%22%23F0B429%22>G</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<div class="shell">

<div class="chrome"><div class="chrome-in">
  <div class="dots"><i></i><i></i><i></i></div>
  <span class="chrome-path"><b>georgia</b>@build-log ~ $ cat portfolio.md</span><span class="caret"></span>
</div></div>

<header class="hero"><div class="wrap">
  <div class="hero-txt" data-rv>
  <div class="avi"><img src="/assets/avatar.jpg" alt="Georgia Harvey" width="240" height="240" fetchpriority="high"></div>
  <div class="eyebrow"><span class="wave" role="img" aria-label="waving hand">&#128075;</span>Hi y&#8217;all, I am</div>
  <h1 class="name">Georgia</h1>
  <p class="lede">I sit between the people with the problem and the systems that could solve it, and I <em>make sure to connect the two as the part in the middle</em>.</p>
  <p class="sub">Eight years of connecting systems, building the pieces that make them work together, and connecting the dots on client solutions that are forward looking, not just short term. Every build below opens up to show the architecture, the decisions, and usually a prototype you can run right here.</p>
  <div class="links">
    <a class="lk primary" href="mailto:gharvey135@gmail.com">{MAIL}gharvey135@gmail.com</a>
    <a class="lk" href="https://github.com/gharvey135" target="_blank" rel="noopener">{ICON["code"]}GitHub</a>
    <a class="lk" href="https://www.linkedin.com/in/georgia-harvey/" target="_blank" rel="noopener">{LI}LinkedIn</a>
  </div>
  </div>
  <div class="hero-vis" data-rv>{HERO_MAP}</div>
  <ol class="stages" data-rv>{stages}</ol>
</div></header>

<div class="bar"><div class="bar-in">
  <nav class="nav">{nav}</nav>
  <a class="bar-cta" href="mailto:gharvey135@gmail.com">{MAIL}<span>Get in touch</span></a>
</div></div>

{secs}

</div>
<footer><div class="foot">
  <div class="foot-p">$ echo $CONTACT</div>
  <h3>Happy to walk through any of it live.</h3>
  <p>Architecture, code, or the parts that went wrong first. Austin, TX and open to remote.</p>
  <div class="links">
    <a class="lk primary" href="mailto:gharvey135@gmail.com">{MAIL}gharvey135@gmail.com</a>
    <a class="lk" href="https://github.com/gharvey135" target="_blank" rel="noopener">{ICON["code"]}github.com/gharvey135</a>
    <a class="lk" href="https://www.linkedin.com/in/georgia-harvey/" target="_blank" rel="noopener">{LI}LinkedIn</a>
  </div>
  <div class="foot-b"><span>Georgia Harvey, Austin TX</span><span>Built by hand. No template.</span></div>
</div></footer>

<script>{js}</script>
</body>
</html>'''

def _mincss(m):
    c = re.sub(r'/\*.*?\*/', '', m.group(1), flags=re.S)
    c = re.sub(r'\s*([{}:;,>])\s*', r'\1', c)
    c = re.sub(r';}', '}', c)
    return '<style>' + re.sub(r'\s+', ' ', c).strip() + '</style>'
page = re.sub(r'<style>(.*?)</style>', _mincss, page, flags=re.S)
page = re.sub(r'>\n\s+<', '><', page)
page = re.sub(r'\n{2,}', '\n', page)

import os
_css = re.search(r'<style>(.*?)</style>', page, re.S).group(1)
_scr = re.findall(r'<script>(.*?)</script>', page, re.S)
page = re.sub(r'<style>.*?</style>', '<link rel="stylesheet" href="/assets/style.css">', page, flags=re.S)
page = re.sub(r'<script>.*?</script>', '<script src="/assets/app.js" defer></script>', page, flags=re.S)
os.makedirs('../assets', exist_ok=True)
open('../assets/style.css','w').write(_css)
open('../assets/app.js','w').write(_scr[0])
if os.path.exists('../assets/toggle.js'): os.remove('../assets/toggle.js')
open('../index.html','w').write(page)
print('index.html', len(page), '| style.css', len(_css), '| app.js', len(_scr[0]))
