"""Tiny architecture-diagram generator.

A spec is a list of columns; each column is a list of nodes.
A node is a string (label) or (label, kind) where kind is:
  in  = input / source system     (default for column 0)
  eng = the thing that does work  (accent)
  out = produced artifact         (mint)
Lines are split on '|'.
"""

W, PAD = 560, 6
NODE_H_BASE, LINE_H = 22, 12.5
COL_GAP, ROW_GAP = 26, 12


def _node_h(lines):
    return NODE_H_BASE + (len(lines) - 1) * LINE_H


def _esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def diagram(cols, caption=None):
    cols = [[(n, None) if isinstance(n, str) else n for n in col] for col in cols]
    ncol = len(cols)
    colw = (W - PAD * 2 - COL_GAP * (ncol - 1)) / ncol

    # geometry
    heights, blocks = [], []
    for ci, col in enumerate(cols):
        hs = [_node_h(n[0].split('|')) for n in col]
        heights.append(sum(hs) + ROW_GAP * (len(hs) - 1))
    H = max(heights) + PAD * 2 + (18 if caption else 0)

    for ci, col in enumerate(cols):
        x = PAD + ci * (colw + COL_GAP)
        hs = [_node_h(n[0].split('|')) for n in col]
        total = sum(hs) + ROW_GAP * (len(hs) - 1)
        y = (max(heights) - total) / 2 + PAD
        items = []
        for (label, kind), h in zip(col, hs):
            k = kind or ('in' if ci == 0 else ('out' if ci == ncol - 1 else 'eng'))
            items.append(dict(x=x, y=y, w=colw, h=h, label=label, kind=k))
            y += h + ROW_GAP
        blocks.append(items)

    out = [f'<svg class="dgm" viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
           f'preserveAspectRatio="xMidYMid meet" aria-label="Architecture diagram">',
           '<defs><marker id="ah" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" '
           'orient="auto"><path d="M0 1 L7 4 L0 7 z" class="dgm-ah"/></marker></defs>']

    # edges first so nodes sit on top
    for ci in range(ncol - 1):
        for a in blocks[ci]:
            for b in blocks[ci + 1]:
                x1, y1 = a['x'] + a['w'], a['y'] + a['h'] / 2
                x2, y2 = b['x'], b['y'] + b['h'] / 2
                mx = (x1 + x2) / 2
                out.append(f'<path class="dgm-e" d="M{x1:.1f} {y1:.1f} C{mx:.1f} {y1:.1f} {mx:.1f} {y2:.1f} '
                           f'{x2-7:.1f} {y2:.1f}" marker-end="url(#ah)"/>')

    for col in blocks:
        for n in col:
            lines = n['label'].split('|')
            out.append(f'<rect class="dgm-n dgm-{n["kind"]}" x="{n["x"]:.1f}" y="{n["y"]:.1f}" '
                       f'width="{n["w"]:.1f}" height="{n["h"]:.1f}" rx="6"/>')
            cy = n['y'] + n['h'] / 2 - (len(lines) - 1) * LINE_H / 2 + 3.4
            for i, ln in enumerate(lines):
                cls = 'dgm-t' + (' dgm-t2' if i else '')
                out.append(f'<text class="{cls}" x="{n["x"]+n["w"]/2:.1f}" y="{cy+i*LINE_H:.1f}" '
                           f'text-anchor="middle">{_esc(ln)}</text>')

    if caption:
        out.append(f'<text class="dgm-c" x="{PAD}" y="{H-4:.1f}">{_esc(caption)}</text>')
    out.append('</svg>')
    return ''.join(out)
