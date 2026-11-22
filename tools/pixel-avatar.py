"""Pixel-art avatar generator for index.html.

Draws the avatar (head, eyes, brows, shirt, laptop with paw) on an 80x100 grid
where one art pixel is 5 SVG units (viewBox 400x500), and writes it into the
<svg id="avatar"> block of index.html, replacing the previous drawing.

Usage (from the repo root):
    python3 tools/pixel-avatar.py            # updates ./index.html
    python3 tools/pixel-avatar.py some.html  # updates another file

Tweak colours in `pal`, the eye colours in IRIS/IRIS2/PUPIL, shapes in the
sections below, then re-run and reload the page.
"""
import sys

P = 5
W, H = 80, 100
pal = {
    'k': '#3a2e28',                                   # outline
    'S': '#f3d4c0', 's': '#e6bca4', 'b': '#efb9a5',   # skin, shade, blush
    'E': '#ecc2a6', 'e': '#d49a7c',                   # ear, inner ear
    'H': '#8c847c', 'h': '#655c54', 'L': '#cbc4bd',   # hair base / dark / light
    'N': '#e9bda3', 'n': '#d29f84',                   # nose
    'T': '#4a4a4c', 't': '#3a3a3c', 'u': '#2a2a2c',   # shirt
    'M': '#c8ccd0', 'm': '#e3e6e9', 'q': '#d4d7db', 'g': '#a7acb1', 'o': '#7c8186',
    'X': '#eceef0',                                   # paw
}
LID, BROW, IRIS, IRIS2, PUPIL = '#5e4537', '#6b5444', '#6a4629', '#875d38', '#1e120c'


def grid():
    return [[None] * W for _ in range(H)]


def rr(c, r, c0, c1, r0, r1, rad):
    """inside a rounded rectangle (inclusive bounds)"""
    if not (c0 <= c <= c1 and r0 <= r <= r1):
        return False
    cx = min(max(c, c0 + rad), c1 - rad)
    cy = min(max(r, r0 + rad), r1 - rad)
    return (c - cx) ** 2 + (r - cy) ** 2 <= rad * rad + .5


def ell(c, r, cx, cy, rx, ry):
    return ((c - cx) / rx) ** 2 + ((r - cy) / ry) ** 2 <= 1


def line(g, a, b, v):
    (x0, y0), (x1, y1) = a, b
    n = max(abs(x1 - x0), abs(y1 - y0))
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n); y = round(y0 + (y1 - y0) * i / n)
        if g[y][x] in ('H', 'h', 'L'):
            g[y][x] = v


def outline(g, col):
    out = [row[:] for row in g]
    for r in range(H):
        for c in range(W):
            if g[r][c] is None and any(0 <= r + dr < H and 0 <= c + dc < W and g[r + dr][c + dc]
                                       for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[r][c] = col
    return out


def rects(g):
    parts = []
    for r in range(H):
        c = 0
        while c < W:
            v = g[r][c]
            if v is None:
                c += 1; continue
            s = c
            while c < W and g[r][c] == v:
                c += 1
            parts.append(f'<rect x="{s*P}" y="{r*P}" width="{(c-s)*P}" height="{P}" fill="{pal[v]}"/>')
    return ''.join(parts)


def R(c, r, w, h, fill):
    return f'<rect x="{c*P}" y="{r*P}" width="{w*P}" height="{h*P}" fill="{fill}"/>'


# ---------------- head ----------------
g = grid()
for r in range(H):
    for c in range(W):
        if rr(c, r, 22, 57, 32, 79, 12):
            g[r][c] = 'S'
# ears
for r in range(H):
    for c in range(W):
        if rr(c, r, 19, 22, 49, 57, 2) or rr(c, r, 57, 60, 49, 57, 2):
            g[r][c] = 'E'
for r in range(51, 56):
    g[r][21] = 'e'; g[r][58] = 'e'
# soft shade down the right cheek, blush
for r in range(40, 80):
    if g[r][57] == 'S': g[r][57] = 's'
    if g[r][56] == 'S' and r > 52: g[r][56] = 's'


def hairline(c):
    if c <= 25 or c >= 54: return 44            # short sides reach the ear
    return 36                                   # straight hairline across the forehead


for r in range(H):
    for c in range(W):
        # swept left -> right: hair sits lower on the left and rises towards the right
        sh = round((c - 39.5) * 0.13)
        rs = r + sh
        top = rr(c, rs, 22, 57, 30, 80, 10) or (rs == 29 and 31 <= c <= 52) or (rs == 28 and 35 <= c <= 50)
        if top and r <= hairline(c):
            g[r][c] = 'H'
# texture: dark edge on the hairline, swept strands, grey sides
for r in range(H):
    for c in range(W):
        if g[r][c] == 'H' and r + 1 < H and g[r + 1][c] in ('S', 's', 'b'):
            g[r][c] = 'h'
for a, b in [((27, 37), (34, 31)), ((33, 34), (45, 29)), ((40, 35), (52, 31)), ((47, 33), (55, 36)),
             ((29, 33), (36, 30))]:
    line(g, a, b, 'L')
for a, b in [((31, 36), (40, 31)), ((44, 33), (53, 33)), ((36, 33), (40, 32))]:
    line(g, a, b, 'h')
for r in range(37, 45):
    for c in list(range(22, 26)) + list(range(54, 58)):
        if g[r][c] in ('H', 'h'):
            g[r][c] = 'L' if (r + c) % 3 == 0 else 'H'
# nose tip peeking over the laptop lid (row 60)
for c in (39, 40): g[56][c] = 'N'
for c in range(38, 42): g[57][c] = 'N'; g[58][c] = 'N'
for c in range(37, 43): g[59][c] = 'n'
g[57][39] = 'S'
g = outline(g, 'k')
head = rects(g)


# ---------------- eyes ----------------
def almond(c0):
    """white of the eye: 10 wide, 4 tall, corners trimmed"""
    return [(c0 + 2, 50, 6, 1), (c0, 51, 10, 2), (c0 + 2, 53, 6, 1)]


def eye(c0, side, cid):
    shape = almond(c0)
    white = ''.join(R(c, r, w, h, '#fff') for c, r, w, h in shape)
    clip = f'<clipPath id="{cid}">' + ''.join(R(c, r, w, h, '#000') for c, r, w, h in shape) + '</clipPath>'
    ic = c0 + 3
    iris = (f'<g clip-path="url(#{cid})"><g class="iris">'
            + R(ic, 50, 4, 4, IRIS) + R(ic, 53, 4, 1, IRIS2)
            + R(ic + 1, 51, 2, 2, PUPIL) + R(ic + 2, 51, 1, 1, '#fff') + '</g></g>')
    outer = c0 - 1 if side == 'L' else c0 + 10
    lid = (R(c0 + 2, 49, 6, 1, LID) + R(c0, 50, 2, 1, LID) + R(c0 + 8, 50, 2, 1, LID)
           + R(outer, 49, 1, 1, LID))
    closed = R(c0 - 1, 49, 12, 5, pal['S']) + R(c0, 52, 10, 1, LID) + R(outer, 51, 1, 1, LID)
    return (f'<defs>{clip}</defs><g class="eye-open">{white}{iris}{lid}</g>'
            f'<g class="eye-closed">{closed}</g>')


eyes = eye(26, 'L', 'pxEyeL') + eye(44, 'R', 'pxEyeR')
brows = (R(27, 43, 9, 1, BROW) + R(31, 44, 5, 1, BROW)
         + R(44, 43, 9, 1, BROW) + R(44, 44, 5, 1, BROW))

# ---------------- shirt ----------------
t = grid()
spans = {78: (24, 55), 79: (20, 59), 80: (18, 61), 81: (15, 64), 82: (13, 66)}
for r in range(78, H):
    c0, c1 = spans.get(r, (10, 69))
    for c in range(c0, c1 + 1):
        t[r][c] = 'T'
for c in range(32, 48): t[78][c] = 't'
for c in range(34, 46): t[79][c] = 't'
t = outline(t, 'u')
shirt = rects(t)

# ---------------- laptop ----------------
l = grid()
for r in range(60, 94):
    for c in range(14, 66):
        l[r][c] = 'M'
for c in range(14, 66): l[60][c] = 'm'
for r in range(61, 94): l[r][14] = 'm'
for r in (94, 95):
    for c in range(10, 70): l[r][c] = 'g'
PAW = ["....XX...XX....",
       "...XXXX.XXXX...",
       "...XXXX.XXXX...",
       ".XX.XX...XX.XX.",
       "XXXX.......XXXX",
       "XXXX.......XXXX",
       ".XX...XXX...XX.",
       ".....XXXXX.....",
       "...XXXXXXXXX...",
       "..XXXXXXXXXXX..",
       "..XXXXXXXXXXX..",
       "..XXXXXXXXXXX..",
       "...XXXXXXXXX...",
       "....XXX.XXX...."]
for i, row in enumerate(PAW):
    for j, ch in enumerate(row):
        if ch == 'X':
            l[70 + i][32 + j] = 'X'
l = outline(l, 'o')
laptop = rects(l)

svg = f'''            <!-- ===== Pixel-art avatar (80x100 grid, 1px = 5 units) ===== -->
            <g class="shirt">{shirt}</g>
            <!-- head is clipped at the laptop's base, so nothing shows below it when ducking -->
            <defs><clipPath id="behindLaptop"><rect x="0" y="0" width="400" height="{94*P}"/></clipPath></defs>
            <g clip-path="url(#behindLaptop)">
            <g class="head">
              {head}
              <g class="brows">{brows}</g>
              {eyes}
            </g>
            </g>
            <g class="laptop">{laptop}</g>
            <line class="desk" x1="0" y1="480" x2="400" y2="480"/>
'''

from pathlib import Path
path = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent.parent / 'index.html')
s = open(path).read()
start = s.find('            <!-- ===== Pixel-art avatar')
if start < 0:
    start = s.index('            <!-- Shoulders')
end = s.index('<line class="desk"', start)
end = s.index('\n', end) + 1
s = s[:start] + svg + s[end:]
open(path, 'w').write(s)
print('ok')
