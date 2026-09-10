"""HTML flow-diagram renderer.

Consumes the zone/node spec in diagrams_v2.py and emits a responsive,
icon-led three-or-four stage flow. Readable by someone who has never
seen the system: each zone has a plain-language heading, each node a
plain label with an optional technical sub-line.
"""
import html as _h

_I = {
 "calendar": '<rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/>',
 "receipt":  '<path d="M5 2.5h14v19l-2.3-1.6-2.35 1.6L12 19.9l-2.35 1.6L7.3 19.9 5 21.5z"/><path d="M9 8h6M9 12h6"/>',
 "document": '<path d="M13.5 2.5H7a2 2 0 0 0-2 2v15a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M13.5 2.5V8H19M8.5 13h7M8.5 17h4.5"/>',
 "folder":   '<path d="M3 7a2 2 0 0 1 2-2h4l2 2.5h8a2 2 0 0 1 2 2V18a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
 "cloud":    '<path d="M7 19h10.5a4.5 4.5 0 0 0 .4-8.98A6 6 0 0 0 6.4 11.2 4 4 0 0 0 7 19z"/>',
 "database": '<ellipse cx="12" cy="6" rx="7.5" ry="3.2"/><path d="M4.5 6v12c0 1.77 3.36 3.2 7.5 3.2s7.5-1.43 7.5-3.2V6"/><path d="M4.5 12c0 1.77 3.36 3.2 7.5 3.2s7.5-1.43 7.5-3.2"/>',
 "table":    '<rect x="3" y="4.5" width="18" height="15" rx="2"/><path d="M3 9.5h18M3 14.5h18M9.5 9.5v10"/>',
 "gear":     '<circle cx="12" cy="12" r="3.1"/><path d="M12 2.6v2.6M12 18.8v2.6M21.4 12h-2.6M5.2 12H2.6M18.6 5.4l-1.85 1.85M7.25 16.75 5.4 18.6M18.6 18.6l-1.85-1.85M7.25 7.25 5.4 5.4"/>',
 "robot":    '<rect x="3.5" y="8" width="17" height="12" rx="3"/><path d="M12 8V4.5M9 14h.01M15 14h.01M8.5 20v1.5M15.5 20v1.5"/><circle cx="12" cy="3.2" r="1.4"/>',
 "chart":    '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M8 17V12M12.5 17V7.5M17 17v-6"/>',
 "alert":    '<path d="M12 3.2 21.5 20H2.5z"/><path d="M12 9.5v4.5M12 17.2h.01"/>',
 "mail":     '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="M3 6.5l9 6.2 9-6.2"/>',
 "person":   '<circle cx="12" cy="8" r="3.7"/><path d="M4.5 20.5a7.5 7.5 0 0 1 15 0"/>',
 "phone":    '<rect x="6" y="2.5" width="12" height="19" rx="2.6"/><path d="M10.5 18.6h3"/>',
 "search":   '<circle cx="10.7" cy="10.7" r="6.7"/><path d="M15.6 15.6 21 21"/>',
 "clock":    '<circle cx="12" cy="12" r="9"/><path d="M12 6.8V12l3.4 2.1"/>',
 "check":    '<circle cx="12" cy="12" r="9"/><path d="M8 12.3l2.8 2.8L16.2 9.6"/>',
 "money":    '<circle cx="12" cy="12" r="9"/><path d="M14.8 9.2a3 3 0 0 0-2.8-1.6c-1.7 0-2.8.9-2.8 2.1 0 2.9 5.8 1.4 5.8 4.4 0 1.3-1.2 2.3-3 2.3a3.2 3.2 0 0 1-3-1.7M12 6v12"/>',
 "code":     '<path d="M8.5 8 4 12.2l4.5 4.2M15.5 8 20 12.2l-4.5 4.2M13.4 5.5l-2.8 13"/>',
 "filter":   '<path d="M3.5 5h17l-6.6 7.8v5.9l-3.8 2.3v-8.2z"/>',
}

_ZK = ["in", "eng", "out"]


def _e(s):
    return _h.escape(s or '', quote=False)


def _icon(name):
    return ('<svg class="fn-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            + _I.get(name, _I["gear"]) + '</svg>')


def _arrow():
    return ('<div class="fw" aria-hidden="true"><span class="fw-l"></span>'
            '<span class="fw-d"></span>'
            '<svg class="fw-a" viewBox="0 0 12 12" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M4 2.5 8 6l-4 3.5"/></svg></div>')


def flow(spec):
    """spec = {"zones":[...], "cols":[[node,...],...], "caption":str}"""
    zones, cols = spec["zones"], spec["cols"]
    n = len(cols)
    parts = []
    for zi, (zname, nodes) in enumerate(zip(zones, cols)):
        kind = _ZK[0] if zi == 0 else (_ZK[2] if zi == n - 1 else _ZK[1])
        items = []
        for nd in nodes:
            sub = f'<i class="fn-s">{_e(nd["sub"])}</i>' if nd.get("sub") else ''
            items.append(
                f'<div class="fn fn-{kind}" tabindex="0">{_icon(nd["icon"])}'
                f'<span class="fn-x"><b class="fn-l">{_e(nd["label"])}</b>{sub}</span></div>')
        parts.append(
            f'<div class="fz fz-{kind}" style="--zi:{zi}">'
            f'<div class="fz-h"><span class="fz-n">{zi+1}</span>{_e(zname)}</div>'
            f'<div class="fz-b">{"".join(items)}</div></div>')
        if zi < n - 1:
            parts.append(_arrow())
    cap = f'<p class="flow-c">{_e(spec.get("caption"))}</p>' if spec.get("caption") else ''
    return (f'<figure class="flow" data-z="{n}" role="group" aria-label="How it works, step by step">'
            f'<div class="flow-r">{"".join(parts)}</div>{cap}</figure>')
