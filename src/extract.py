import re, json, html
s = open('/tmp/portfolio.html').read()

# section labels -> category
cats = []
for m in re.finditer(r'<div class="section-label" id="([a-z]+)"[^>]*>(.*?)</div>', s, re.S):
    cats.append((m.start(), m.group(1), re.sub(r'<[^>]+>', ' ', m.group(2)).strip()))

def cat_for(pos):
    c = None
    for p, cid, label in cats:
        if p < pos: c = (cid, label)
    return c or ('solutions', 'Solutions Architecture')

def grab(block, pattern, flags=re.S):
    m = re.search(pattern, block, flags)
    return m.group(1).strip() if m else ''

# split entries by locating each '<div class="entry"' and taking up to the next one
starts = [m.start() for m in re.finditer(r'<div class="entry" onclick', s)]
starts.append(s.index('<footer>'))

entries = []
for i in range(len(starts) - 1):
    b = s[starts[i]:starts[i+1]]
    cid, clabel = cat_for(starts[i])
    title = grab(b, r'<span class="entry-title">(.*?)</span>')
    status = grab(b, r'<span class="status[^"]*">(.*?)</span>')
    body = grab(b, r'<div class="entry-body">(.*?)</div>')
    tags = re.findall(r'<span class="tag">(.*?)</span>', b)
    pain = grab(b, r'frame-cell pain".*?<div class="fc-text">(.*?)</div>')
    solve = grab(b, r'frame-cell solve".*?<div class="fc-text">(.*?)</div>')
    where = grab(b, r'<span class="bh-where">(.*?)</span>')
    steps = re.findall(r'<li>(.*?)</li>', grab(b, r'<ol class="build-steps">(.*?)</ol>'), re.S)
    why = grab(b, r'<div class="build-why">(.*?)</div>')
    # proto box: from '<div class="proto-box">' to end of entry, trimmed of trailing wrappers
    pm = re.search(r'(<div class="proto-box">.*)', b, re.S)
    proto = pm.group(1) if pm else ''
    # trim trailing closing divs that belonged to entry/detail wrappers
    proto = re.sub(r'<!--.*?-->', '', proto, flags=re.S).rstrip()
    proto = re.sub(r'(?:\s*</div>)+\s*$', '', proto).rstrip()
    # robust rebalance: drop excess trailing closes, then add any that are missing
    while proto.count('</div>') > len(re.findall(r'<div\b', proto)):
        i = proto.rfind('</div>'); proto = (proto[:i] + proto[i+6:]).rstrip()
    opens = len(re.findall(r'<div\b', proto)); closes = proto.count('</div>')
    proto += '</div>' * max(0, opens - closes)
    entries.append(dict(cat=cid, cat_label=clabel, title=title, status=status, body=body,
                        tags=[t.strip() for t in tags], pain=pain, solve=solve,
                        where=where, steps=[st.strip() for st in steps], why=why, proto=proto))

json.dump(entries, open('content.json', 'w'), indent=1)
print('entries:', len(entries))
for e in entries:
    print(f"  {e['cat']:<10} {e['title']:<42} {e['status']:<10} steps={len(e['steps'])} tags={len(e['tags'])} proto={len(e['proto'])}")
