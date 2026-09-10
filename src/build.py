import json, re, html
from venues import VENUES, REPOS

entries = json.load(open('content.json'))
plain   = json.load(open('plain.json'))
css     = ''.join(open(f).read() for f in ('style.css','alias.css','proto.css'))
js      = open('portfolio.js').read()

def dec(s): return html.unescape(s or '').replace('&middot;',',')

ICON = {
 "code":'<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8a8 8 0 005.47 7.59c.4.07.55-.17.55-.38l-.01-1.49c-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.4 7.4 0 014 0c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48l-.01 2.19c0 .21.15.46.55.38A8.01 8.01 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>',
 "demo":'<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 3.5v9l7-4.5z" fill="currentColor" stroke="none"/><circle cx="8" cy="8" r="7"/></svg>',
 "doc" :'<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 1.5H4a1 1 0 00-1 1v11a1 1 0 001 1h8a1 1 0 001-1V5.5z"/><path d="M9 1.5v4h4M5.5 8.5h5M5.5 11h3"/></svg>',
}
LI = '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M3.6 5.3H.7V15h2.9V5.3zM2.1.9A1.7 1.7 0 100 2.6 1.7 1.7 0 002.1.9zM15 9.5c0-2.8-1.5-4.1-3.5-4.1a3 3 0 00-2.7 1.5V5.3H5.9V15h2.9V9.9c0-1.2.2-2.4 1.7-2.4s1.5 1.4 1.5 2.5V15H15z"/></svg>'
MAIL = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1.2" y="3" width="13.6" height="10" rx="1.5"/><path d="M1.5 4l6.5 4.6L14.5 4"/></svg>'

def links_row(links):
    if not links: return ''
    out = ''.join(
        f'<a class="clink" href="{u}" target="_blank" rel="noopener" onclick="event.stopPropagation()">{ICON[k]}{t}</a>'
        for k, u, t in links)
    return f'<div class="card-links">{out}</div>'

def card(*, slug, human_title, plain_body, tech_body, prov, impact, live, tags,
         plain_pain, pain, plain_solve, solve, where, steps, why, proto='', links=None):
    chips = ''
    if live:   chips += '<span class="mchip live">running in production</span>'
    if prov:   chips += f'<span class="mchip">{dec(prov)}</span>'
    if impact: chips += f'<span class="mchip impact">{dec(impact)}</span>'
    tagshtml = ''.join(f'<span class="tag">{dec(t)}</span>' for t in tags)
    stepshtml = ''.join(f'<li>{s}</li>' for s in steps)
    return f'''
<article class="card" id="b-{slug}">
  <div class="card-top" onclick="this.parentNode.classList.toggle('open')" role="button" tabindex="0"
       onkeydown="if(event.key==='Enter'||event.key===' '){{event.preventDefault();this.parentNode.classList.toggle('open')}}">
    <div class="card-meta"><span class="slug">{slug}</span>{chips}</div>
    <h3 class="card-title">{human_title}</h3>
    <p class="card-body plain-only">{plain_body}</p>
    <p class="card-body tech-only">{tech_body}</p>
    <div class="tags">{tagshtml}</div>
    {links_row(links)}
  </div>
  <div class="detail" onclick="event.stopPropagation()"><div class="detail-in">
    <div class="frame">
      <div class="fc pain"><div class="fc-l">The problem</div>
        <p class="fc-t plain-only">{plain_pain}</p><p class="fc-t tech-only">{pain}</p></div>
      <div class="fc solve"><div class="fc-l">What changed</div>
        <p class="fc-t plain-only">{plain_solve}</p><p class="fc-t tech-only">{solve}</p></div>
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

# ---- build cards from extracted entries -------------------------------------
def from_entry(e):
    p = plain[e['title']]
    prov = dec(e['where'])
    if e['status'] == 'In Build': prov = 'In active development'
    return card(slug=e['title'], human_title=p['human_title'],
                plain_body=p['plain_body'], tech_body=e['body'],
                prov=prov, impact=p['impact'], live=False, tags=e['tags'],
                plain_pain=p['plain_pain'], pain=e['pain'],
                plain_solve=p['plain_solve'], solve=e['solve'],
                where=e['where'], steps=e['steps'], why=e['why'], proto=e['proto'])

by_cat = {}
for e in entries: by_cat.setdefault(e['cat'], []).append(e)

SECTIONS = [
 ("production", "In production", "Systems I own and operate",
  "Built for the two Austin venues I co-own and running unattended every week. These are the ones where the code, the tests, and a live demo are all public.",
  [card(**v) for v in VENUES]),
 ("clients", "Client delivery", "Shipped to enterprise customers",
  "Scoped with the customer, built, taken to production, and handed to their own team to run without me.",
  [from_entry(e) for e in by_cat.get('clients', [])]),
 ("solutions", "Architecture", "Tooling for the work itself",
  "So that scoping, account reviews, and debugging stop depending on one senior person being in the room.",
  [from_entry(e) for e in by_cat.get('solutions', [])]),
 ("operations", "Operations", "The unglamorous systems",
  "Internal process work. Rarely the thing anyone demos, usually the thing that decides whether output stays consistent.",
  [from_entry(e) for e in by_cat.get('operations', [])]),
 ("personal", "Personal", "Problems I had",
  "Solved end to end rather than tolerated.",
  [from_entry(e) for e in by_cat.get('personal', [])]),
]

secs = ''
for sid, eyebrow, title, note, cards in SECTIONS:
    secs += f'''
<section class="sec" id="{sid}"><div class="wrap">
  <div class="sec-head">
    <div class="sec-tag">{eyebrow}<span>{len(cards)}</span></div>
    <h2>{title}</h2>
    <p class="sec-note">{note}</p>
  </div>
  <div class="grid">{''.join(cards)}</div>
</div></section>'''

repos = ''.join(
  f'''<a class="repo" href="https://github.com/gharvey135/{n}" target="_blank" rel="noopener">
    <div class="repo-n">{ICON["code"]}{n}</div><p class="repo-d">{d}</p>
    <div class="repo-m"><span>{lang}</span><b>{t}</b></div></a>''' for n, d, lang, t in REPOS)

secs += f'''
<section class="sec" id="code"><div class="wrap">
  <div class="sec-head">
    <div class="sec-tag">Code<span>{len(REPOS)}</span></div>
    <h2>Open source</h2>
    <p class="sec-note">Standalone engineering work, each with tests and continuous integration. Every repository runs from a clean clone with no credentials.</p>
  </div>
  <div class="repos">{repos}</div>
</div></section>'''

NAV = [("production","production"),("clients","clients"),("solutions","architecture"),
       ("operations","operations"),("personal","personal"),("code","code")]
nav = ''.join(f'<a href="#{i}">{l}</a>' for i, l in NAV)

toggle_js = '''
(function(){
  var root=document.documentElement, seg=document.getElementById('seg'),
      btns=seg.querySelectorAll('button'), pill=seg.querySelector('.pill');
  function move(b){ pill.style.left=b.offsetLeft+'px'; pill.style.width=b.offsetWidth+'px'; }
  function set(m,save){
    root.setAttribute('data-mode',m);
    btns.forEach(function(b){
      var on=b.dataset.mode===m; b.setAttribute('aria-pressed',on?'true':'false'); if(on) move(b);
    });
    if(save){ try{ localStorage.setItem('pf-mode',m); }catch(e){} }
  }
  btns.forEach(function(b){ b.addEventListener('click',function(){ set(b.dataset.mode,true); }); });
  var saved=null; try{ saved=localStorage.getItem('pf-mode'); }catch(e){}
  set(saved==='tech'?'tech':'plain',false);
  window.addEventListener('resize',function(){ set(root.getAttribute('data-mode'),false); });
  window.addEventListener('load',function(){ set(root.getAttribute('data-mode'),false); });
})();
'''

DESC = ("Georgia Harvey, Solutions Architect in Austin, TX. Enterprise integrations and AI workflows, "
        "discovery through handoff. Production systems, client delivery, and open source, with the code.")

page = f'''<!doctype html>
<html lang="en" data-mode="plain">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Georgia Harvey, Solutions Architect</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="Georgia Harvey, Solutions Architect">
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
  <div class="eyebrow">Solutions Architect &middot; Austin, TX</div>
  <h1 class="name">Georgia Harvey</h1>
  <p class="lede">I connect the systems a business already runs, and then <em>hand them over working</em>.</p>
  <p class="sub">Seven years of enterprise integrations and AI workflows, from the first discovery call through launch and handoff. Everything below is something I built. Open any card to see the problem, the decisions, and in most cases a working prototype you can run right here.</p>
  <div class="links">
    <a class="lk primary" href="mailto:gharvey135@gmail.com">{MAIL}gharvey135@gmail.com</a>
    <a class="lk" href="https://github.com/gharvey135" target="_blank" rel="noopener">{ICON["code"]}GitHub</a>
    <a class="lk" href="https://www.linkedin.com/in/georgia-harvey/" target="_blank" rel="noopener">{LI}LinkedIn</a>
  </div>
  <div class="proof">
    <div class="pf"><b>7 yrs</b><span>Enterprise solutions and delivery</span></div>
    <div class="pf"><b>150+</b><span>Enterprise API accounts supported</span></div>
    <div class="pf"><b>3</b><span>Systems I run in production</span></div>
    <div class="pf"><b>389</b><span>Automated tests across public repos</span></div>
    <div class="pf"><b>21</b><span>Builds documented below</span></div>
  </div>
</div></header>

<div class="bar"><div class="bar-in">
  <nav class="nav">{nav}</nav>
  <div class="mode">
    <span class="mode-lbl">Read as</span>
    <div class="seg" id="seg" role="group" aria-label="Reading mode">
      <span class="pill"></span>
      <button data-mode="plain" aria-pressed="true">Plain English</button>
      <button data-mode="tech" aria-pressed="false">Technical</button>
    </div>
  </div>
</div></div>

{secs}

</div>
<footer><div class="foot">
  <div class="foot-p">$ echo $CONTACT</div>
  <h3>Happy to walk through any of it live.</h3>
  <p>Architecture, code, or the parts that went wrong first. Based in Austin, TX and open to remote.</p>
  <div class="links">
    <a class="lk primary" href="mailto:gharvey135@gmail.com">{MAIL}gharvey135@gmail.com</a>
    <a class="lk" href="https://github.com/gharvey135" target="_blank" rel="noopener">{ICON["code"]}github.com/gharvey135</a>
    <a class="lk" href="https://www.linkedin.com/in/georgia-harvey/" target="_blank" rel="noopener">{LI}LinkedIn</a>
  </div>
  <div class="foot-b"><span>Georgia Harvey, Austin TX</span><span>Built by hand. No template.</span></div>
</div></footer>

<script>{js}</script>
<script>{toggle_js}</script>
</body>
</html>'''

# minify: CSS block, plus indentation-only whitespace between tags
def _mincss(m):
    c = re.sub(r'/\*.*?\*/', '', m.group(1), flags=re.S)
    c = re.sub(r'\s*([{}:;,>])\s*', r'\1', c)
    c = re.sub(r';}', '}', c)
    return '<style>' + re.sub(r'\s+', ' ', c).strip() + '</style>'
page = re.sub(r'<style>(.*?)</style>', _mincss, page, flags=re.S)
page = re.sub(r'>\n\s+<', '><', page)
page = re.sub(r'\n{2,}', '\n', page)

open('../index.html','w').write(page)
print('index.html', len(page), 'chars')
