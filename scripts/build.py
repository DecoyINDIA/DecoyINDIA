"""Builds every SVG in assets/ for the profile README.

All text is shaped with HarfBuzz and converted to vector paths, so the
artwork looks identical on every machine (GitHub blocks web fonts inside
<img> SVGs). Animations are plain CSS, with a prefers-reduced-motion
fallback that shows the finished frame.

    pip install fonttools uharfbuzz
    python scripts/build.py
"""

from __future__ import annotations

import io
import math
import pathlib
import urllib.request

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
CACHE = ROOT / "scripts" / ".fonts"

GF = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
FONT_URLS = {
    "serif": GF + "instrumentserif/InstrumentSerif-Regular.ttf",
    "serif_it": GF + "instrumentserif/InstrumentSerif-Italic.ttf",
    "inter": GF + "inter/Inter%5Bopsz,wght%5D.ttf",
    "mono": GF + "jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
    "odia": GF + "notosansoriya/NotoSansOriya%5Bwdth,wght%5D.ttf",
    "deva": GF + "notosansdevanagari/NotoSansDevanagari%5Bwdth,wght%5D.ttf",
}

# Palette: warm paper-desk tones, one hot accent, one warm secondary.
BG = "#13100E"
CARD = "#181411"
LINE = "#2A231E"
INK = "#F4EEE6"
BODY = "#B8ACA0"
DIM = "#7D7268"
TERRA = "#E8501C"
MARI = "#F2A541"
TEAL = "#6FB3A8"


# --------------------------------------------------------------------------
# Type
# --------------------------------------------------------------------------


def _fetch(key: str) -> bytes:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{key}.ttf"
    if not path.exists():
        with urllib.request.urlopen(FONT_URLS[key]) as r:
            path.write_bytes(r.read())
    return path.read_bytes()


def _num(v: float) -> str:
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


class Font:
    def __init__(self, key: str, **axes: float):
        tt = TTFont(io.BytesIO(_fetch(key)))
        if "fvar" in tt:
            pins = {a.axisTag: a.defaultValue for a in tt["fvar"].axes}
            pins.update(axes)
            tt = instancer.instantiateVariableFont(tt, pins)
        buf = io.BytesIO()
        tt.save(buf)
        self.upem = tt["head"].unitsPerEm
        self.gs = tt.getGlyphSet()
        self.order = tt.getGlyphOrder()
        self.hb = hb.Font(hb.Face(hb.Blob(buf.getvalue())))

    def _shape(self, text: str):
        b = hb.Buffer()
        b.add_str(text)
        b.guess_segment_properties()
        hb.shape(self.hb, b, {"kern": True, "liga": True})
        return b.glyph_infos, b.glyph_positions

    def width(self, text: str, size: float, track: float = 0) -> float:
        _, pos = self._shape(text)
        s = size / self.upem
        return sum(p.x_advance * s + track for p in pos) - (track if pos else 0)

    def glyphs(self, text: str, size: float, x: float, y: float, track: float = 0):
        """Return [(path_d, x_of_glyph)] for each visible glyph."""
        infos, pos = self._shape(text)
        s = size / self.upem
        out = []
        cx = x
        for info, p in zip(infos, pos):
            name = self.order[info.codepoint]
            pen = SVGPathPen(self.gs, ntos=_num)
            gx = cx + p.x_offset * s
            gy = y - p.y_offset * s
            self.gs[name].draw(TransformPen(pen, (s, 0, 0, -s, gx, gy)))
            d = pen.getCommands()
            if d:
                out.append((d, cx))
            cx += p.x_advance * s + track
        return out

    def path(self, text: str, size: float, x: float, y: float, track: float = 0, anchor: str = "start") -> str:
        if anchor != "start":
            w = self.width(text, size, track)
            x -= w if anchor == "end" else w / 2
        return " ".join(d for d, _ in self.glyphs(text, size, x, y, track))

    def wrap(self, text: str, size: float, max_w: float) -> list[str]:
        lines, cur = [], ""
        for word in text.split():
            trial = f"{cur} {word}".strip()
            if cur and self.width(trial, size) > max_w:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        if cur:
            lines.append(cur)
        return lines


SERIF = Font("serif")
SERIF_IT = Font("serif_it")
SANS = Font("inter", wght=400, opsz=18)
SANS_MED = Font("inter", wght=500, opsz=18)
MONO = Font("mono", wght=400)
ODIA = Font("odia", wght=500)
DEVA = Font("deva", wght=500)


# --------------------------------------------------------------------------
# SVG helpers
# --------------------------------------------------------------------------

BASE_CSS = """
  @media (prefers-reduced-motion: reduce) {
    * { animation: none !important; }
  }
"""


def svg(w: int, h: int, body: str, css: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{title}">\n<title>{title}</title>\n'
        f"<style>{css}{BASE_CSS}</style>\n{body}\n</svg>\n"
    )


def grain(id_: str, opacity: float = 0.07) -> tuple[str, str]:
    defs = (
        f'<filter id="{id_}" x="0" y="0" width="100%" height="100%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>'
        '<feColorMatrix values="0 0 0 0 1  0 0 0 0 0.95  0 0 0 0 0.9  0 0 0 0.55 0"/>'
        "</filter>"
    )
    return defs, f'<rect width="100%" height="100%" filter="url(#{id_})" opacity="{opacity}"/>'


def circle_d(cx: float, cy: float, r: float) -> str:
    return (
        f"M{_num(cx - r)} {_num(cy)}a{_num(r)} {_num(r)} 0 1 0 {_num(2 * r)} 0"
        f"a{_num(r)} {_num(r)} 0 1 0 {_num(-2 * r)} 0Z"
    )


def polar(cx: float, cy: float, r: float, deg: float) -> tuple[float, float]:
    a = math.radians(deg - 90)
    return cx + r * math.cos(a), cy + r * math.sin(a)


# --------------------------------------------------------------------------
# Hero
# --------------------------------------------------------------------------


def konark_wheel(cx: float, cy: float, R: float, start: float) -> tuple[str, float]:
    """Line drawing of a Konark Sun Temple wheel. Returns (svg, end_time)."""
    parts: list[str] = []
    t = start

    def draw(d: str, cls: str, dur: float, delay: float, extra: str = "") -> None:
        parts.append(
            f'<path d="{d}" pathLength="1" class="{cls} dr" '
            f'style="animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s" {extra}/>'
        )

    # Rims
    for i, (r, cls) in enumerate([(R, "w1"), (R * 0.93, "w2"), (R * 0.80, "w1"), (R * 0.76, "w2")]):
        draw(circle_d(cx, cy, r), cls, 1.6, t + i * 0.18)
    t += 0.9

    # Beads between the outer rims
    beads = []
    for k in range(48):
        x, y = polar(cx, cy, R * 0.965, k * 7.5)
        beads.append(
            f'<circle cx="{_num(x)}" cy="{_num(y)}" r="1.9" class="bead" '
            f'style="animation-delay:{t + k * 0.03:.2f}s"/>'
        )
    parts.append("".join(beads))

    r_in, r_out = R * 0.21, R * 0.76
    # Eight thick spokes: tapered lens shapes with a medallion in the middle
    for k in range(8):
        a = k * 45
        x0, y0 = polar(cx, cy, r_in, a)
        x1, y1 = polar(cx, cy, r_out, a)
        mid = (r_in + r_out) / 2
        lx, ly = polar(cx, cy, mid, a - 4.2)
        rx, ry = polar(cx, cy, mid, a + 4.2)
        d = (
            f"M{_num(x0)} {_num(y0)}Q{_num(lx)} {_num(ly)} {_num(x1)} {_num(y1)}"
            f"Q{_num(rx)} {_num(ry)} {_num(x0)} {_num(y0)}Z"
        )
        draw(d, "w1", 1.1, t + k * 0.09)
        mx, my = polar(cx, cy, mid, a)
        draw(circle_d(mx, my, R * 0.055), "w3", 0.8, t + 0.5 + k * 0.09)
        draw(circle_d(mx, my, R * 0.025), "w3", 0.6, t + 0.8 + k * 0.09)
    t += 0.8
    # Eight thin spokes
    for k in range(8):
        a = k * 45 + 22.5
        x0, y0 = polar(cx, cy, r_in, a)
        x1, y1 = polar(cx, cy, r_out, a)
        draw(f"M{_num(x0)} {_num(y0)}L{_num(x1)} {_num(y1)}", "w2", 0.9, t + k * 0.07)
    t += 0.6
    # Hub with lotus petals
    draw(circle_d(cx, cy, r_in), "w1", 1.0, t)
    draw(circle_d(cx, cy, R * 0.07), "w3", 0.8, t + 0.2)
    for k in range(16):
        a = k * 22.5
        x0, y0 = polar(cx, cy, R * 0.08, a)
        x1, y1 = polar(cx, cy, r_in * 0.92, a)
        lx, ly = polar(cx, cy, R * 0.15, a - 11)
        rx, ry = polar(cx, cy, R * 0.15, a + 11)
        d = (
            f"M{_num(x0)} {_num(y0)}Q{_num(lx)} {_num(ly)} {_num(x1)} {_num(y1)}"
            f"Q{_num(rx)} {_num(ry)} {_num(x0)} {_num(y0)}Z"
        )
        draw(d, "w2", 0.7, t + 0.3 + k * 0.04)
    t += 1.2
    return "".join(parts), t


def hero() -> str:
    W, H = 1200, 460
    cx, cy, R = 968, 228, 178
    g_defs, g_rect = grain("hg", 0.08)

    # Name, drawn glyph by glyph
    name_size = 132
    name_glyphs = SERIF.glyphs("Subham Jena", name_size, 72, 232)
    name = "".join(
        f'<path d="{d}" pathLength="1" class="nm" style="animation-delay:{0.25 + i * 0.11:.2f}s"/>'
        for i, (d, _) in enumerate(name_glyphs)
    )

    # Rotating line: "I build" + phrases
    lead = "I build"
    lead_size = 25
    lead_d = SANS.path(lead, lead_size, 76, 310)
    ph_x = 76 + SANS.width(lead, lead_size) + 10
    phrases = [
        "front desks that answer in Odia.",
        "PDF tools that never phone home.",
        "download managers in Rust.",
        "scouting apps for small-town footballers.",
        "rental deals both sides sign off on.",
    ]
    period = 3.6
    total = period * len(phrases)
    ph_svg = []
    for i, text in enumerate(phrases):
        gl = SERIF_IT.glyphs(text, 33, ph_x, 311)
        ps = "".join(
            f'<path d="{d}" style="animation-delay:{6.0 + i * period + j * 0.018:.3f}s"/>'
            for j, (d, _) in enumerate(gl)
        )
        ph_svg.append(f'<g class="ph{" ph0" if i == 0 else ""}">{ps}</g>')
    vis = 100 / len(phrases)

    place = MONO.path("BHUBANESWAR, ODISHA", 13, 96, 98, track=2.6)
    studio = SANS.path("Founder, XolverLabs   ·   xolver.in", 15, 76, 392)
    wheel, wheel_end = konark_wheel(cx, cy, R, 0.6)

    css = f"""
  .bg {{ fill: {BG}; }}
  .nm {{ fill: {INK}; stroke: {INK}; stroke-width: 1.1; stroke-dasharray: 1; stroke-dashoffset: 0;
        fill-opacity: 1; stroke-opacity: 0;
        animation: draw 3.2s cubic-bezier(.6,.05,.3,1) both; }}
  @keyframes draw {{
    0% {{ stroke-dashoffset: 1; fill-opacity: 0; stroke-opacity: 1; }}
    55% {{ stroke-dashoffset: 0; fill-opacity: 0; stroke-opacity: 1; }}
    100% {{ stroke-dashoffset: 0; fill-opacity: 1; stroke-opacity: 0; }}
  }}
  .lead {{ fill: {BODY}; animation: rise 1.2s ease-out 4.8s both; }}
  .meta {{ fill: {DIM}; animation: rise 1.2s ease-out 5.4s both; }}
  .place {{ fill: {DIM}; animation: rise 1s ease-out 0.1s both; }}
  .dot {{ fill: {TERRA}; animation: pulse 2.4s ease-in-out infinite; transform-origin: 81px 93px; }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes pulse {{ 0%,100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: .35; transform: scale(.7); }} }}
  .ph path {{ fill: {MARI}; animation: cycle {total:.1f}s cubic-bezier(.2,.7,.2,1) infinite both; }}
  .ph {{ opacity: 1; }}
  @keyframes cycle {{
    0% {{ opacity: 0; transform: translateY(16px); }}
    {vis * 0.18:.2f}% {{ opacity: 1; transform: none; }}
    {vis * 0.86:.2f}% {{ opacity: 1; transform: none; }}
    {vis:.2f}% {{ opacity: 0; transform: translateY(-10px); }}
    100% {{ opacity: 0; transform: translateY(-10px); }}
  }}
  .dr {{ fill: none; stroke-dasharray: 1; stroke-dashoffset: 0; stroke-linecap: round; stroke-linejoin: round;
        animation-name: stroke; animation-timing-function: cubic-bezier(.6,.05,.3,1); animation-fill-mode: both; }}
  @keyframes stroke {{ from {{ stroke-dashoffset: 1; }} to {{ stroke-dashoffset: 0; }} }}
  .w1 {{ stroke: {INK}; stroke-opacity: .78; stroke-width: 1.3; }}
  .w2 {{ stroke: {INK}; stroke-opacity: .38; stroke-width: 1; }}
  .w3 {{ stroke: {TERRA}; stroke-width: 1.3; }}
  .bead {{ fill: {MARI}; opacity: .85; animation: pop .5s ease-out both; }}
  @keyframes pop {{ from {{ opacity: 0; }} to {{ opacity: .85; }} }}
  .spin {{ transform-origin: {cx}px {cy}px; animation: spin 140s linear infinite; }}
  .sun {{ transform-origin: {cx}px {cy}px; animation: spin 26s linear infinite, fadein 2s ease-out {wheel_end:.1f}s both; }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  @keyframes fadein {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
  .glow {{ animation: breathe 9s ease-in-out infinite; transform-origin: {cx}px {cy}px; }}
  @keyframes breathe {{ 0%,100% {{ opacity: .55; transform: scale(1); }} 50% {{ opacity: 1; transform: scale(1.06); }} }}
  .rule {{ stroke: {LINE}; stroke-width: 1; }}
"""
    # Sundial shadow: a soft wedge sweeping inside the wheel
    a0, a1 = -18, 18
    sx0, sy0 = polar(cx, cy, R * 0.76, a0)
    sx1, sy1 = polar(cx, cy, R * 0.76, a1)
    sun = (
        f'<path class="sun" d="M{cx} {cy}L{_num(sx0)} {_num(sy0)}A{_num(R * 0.76)} {_num(R * 0.76)} 0 0 1 '
        f'{_num(sx1)} {_num(sy1)}Z" fill="url(#wedge)"/>'
    )
    body = f"""<defs>{g_defs}
  <radialGradient id="glow" cx="{cx}" cy="{cy}" r="{R * 1.6}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{TERRA}" stop-opacity=".22"/>
    <stop offset=".45" stop-color="{TERRA}" stop-opacity=".06"/>
    <stop offset="1" stop-color="{TERRA}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="wedge" cx="{cx}" cy="{cy}" r="{R * 0.76}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{MARI}" stop-opacity="0"/>
    <stop offset=".6" stop-color="{MARI}" stop-opacity=".10"/>
    <stop offset="1" stop-color="{MARI}" stop-opacity=".22"/>
  </radialGradient>
  <clipPath id="clip"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#clip)">
  <rect class="bg" width="{W}" height="{H}"/>
  <circle class="glow" cx="{cx}" cy="{cy}" r="{R * 1.6}" fill="url(#glow)"/>
  {sun}
  <g class="spin">{wheel}</g>
  <circle class="dot" cx="81" cy="93" r="4"/>
  <path class="place" d="{place}"/>
  <g>{name}</g>
  <path class="lead" d="{lead_d}"/>
  {''.join(ph_svg)}
  <line class="rule meta" x1="76" y1="350" x2="660" y2="350"/>
  <path class="meta" d="{studio}"/>
  {g_rect}
</g>"""
    # Reduced motion: show only the first phrase.
    css += "\n  @media (prefers-reduced-motion: reduce) { .ph { opacity: 0; } .ph0 { opacity: 1; } }"
    return svg(W, H, body, css, "Subham Jena. I build software from Bhubaneswar, Odisha.")


# --------------------------------------------------------------------------
# Project cards
# --------------------------------------------------------------------------

CW, CH = 1200, 272
MX = 790  # motif area starts here


def card(idx: str, name: str, tagline: str, stack: str, motif: str, motif_css: str, accent: str) -> str:
    g_defs, g_rect = grain("cg", 0.06)
    num = MONO.path(idx, 13, 56, 66, track=2)
    title = SERIF.path(name, 64, 52, 136)
    lines = SANS.wrap(tagline, 19, 650)
    tag = "".join(
        f'<path class="tag" d="{SANS.path(line, 19, 56, 176 + i * 27)}"/>'
        for i, line in enumerate(lines)
    )
    st = MONO.path(stack.upper(), 11.5, 56, CH - 34, track=1.6)
    css = f"""
  .bg {{ fill: {CARD}; }}
  .frame {{ fill: none; stroke: {LINE}; }}
  .num {{ fill: {accent}; }}
  .ttl {{ fill: {INK}; }}
  .tag {{ fill: {BODY}; }}
  .stk {{ fill: {DIM}; }}
  .bar {{ fill: {accent}; }}
  .div {{ stroke: {LINE}; }}
{motif_css}"""
    body = f"""<defs>{g_defs}<clipPath id="c"><rect width="{CW}" height="{CH}" rx="20"/></clipPath></defs>
<g clip-path="url(#c)">
  <rect class="bg" width="{CW}" height="{CH}"/>
  <rect class="bar" x="56" y="40" width="28" height="2"/>
  <path class="num" d="{num}"/>
  <path class="ttl" d="{title}"/>
  {tag}
  <path class="stk" d="{st}"/>
  <line class="div" x1="{MX - 30}" y1="34" x2="{MX - 30}" y2="{CH - 34}"/>
  <g transform="translate(0 {(CH - 250) // 2})">{motif}</g>
  {g_rect}
</g>
<rect class="frame" x=".5" y=".5" width="{CW - 1}" height="{CH - 1}" rx="20"/>"""
    return svg(CW, CH, body, css, f"{name}. {tagline}")


def motif_vaani() -> tuple[str, str]:
    cx = (MX + CW) / 2 - 10
    greetings = [
        (ODIA, "ନମସ୍କାର", 40),
        (DEVA, "नमस्ते", 42),
        (SANS_MED, "Haan ji, boliye", 30),
        (SANS_MED, "Hello", 34),
    ]
    period = 2.6
    g = []
    for i, (f, text, size) in enumerate(greetings):
        d = f.path(text, size, cx, 112, anchor="middle")
        g.append(f'<path class="gr{" gr0" if i == 0 else ""}" style="animation-delay:{i * period:.1f}s" d="{d}"/>')
    bars = []
    n = 29
    for k in range(n):
        x = cx - (n - 1) * 6 + k * 12
        env = math.sin(math.pi * (k + 0.5) / n)
        h = 8 + 46 * env
        dur = 0.9 + (k * 37 % 11) / 14
        bars.append(
            f'<rect class="wv" x="{_num(x - 2.5)}" y="{_num(172 - h / 2)}" width="5" height="{_num(h)}" rx="2.5" '
            f'style="animation-duration:{dur:.2f}s;animation-delay:{-(k * 0.13):.2f}s"/>'
        )
    total = period * len(greetings)
    v = 100 / len(greetings)
    css = f"""
  .gr {{ fill: {INK}; opacity: 0; animation: say {total:.1f}s ease-in-out infinite both; }}
  @keyframes say {{
    0% {{ opacity: 0; transform: translateY(10px); }}
    {v * .2:.1f}% {{ opacity: 1; transform: none; }}
    {v * .85:.1f}% {{ opacity: 1; transform: none; }}
    {v:.1f}% {{ opacity: 0; transform: translateY(-8px); }}
    100% {{ opacity: 0; }}
  }}
  .wv {{ fill: {TERRA}; transform-box: fill-box; transform-origin: center; animation: talk 1s ease-in-out infinite alternate; }}
  @keyframes talk {{ from {{ transform: scaleY(.25); opacity: .55; }} to {{ transform: scaleY(1); opacity: 1; }} }}
  @media (prefers-reduced-motion: reduce) {{ .gr0 {{ opacity: 1; }} }}
"""
    return "".join(g) + "".join(bars), css


def motif_octapdf() -> tuple[str, str]:
    cx, cy = (MX + CW) / 2, 128
    pages = []
    for i, (rot, op) in enumerate([(-14, 0.45), (-5, 0.7), (6, 1)]):
        lines = "".join(
            f'<rect x="{cx - 44}" y="{cy - 52 + j * 14}" width="{88 - (j % 3) * 18}" height="4" rx="2" class="ln"/>'
            for j in range(7)
        )
        pages.append(
            f'<g class="pg p{i}" style="--r:{rot}deg;opacity:{op}">'
            f'<rect x="{cx - 62}" y="{cy - 80}" width="124" height="160" rx="8" class="sheet"/>{lines}</g>'
        )
    seal_x, seal_y = cx + 70, cy + 62
    seal = (
        f'<g class="seal"><circle cx="{seal_x}" cy="{seal_y}" r="24" fill="{TERRA}"/>'
        f'<path d="M{seal_x - 9} {seal_y}l6 6 12-13" fill="none" stroke="{INK}" stroke-width="3" '
        f'stroke-linecap="round" stroke-linejoin="round"/></g>'
    )
    key = MONO.path("⌘K", 14, cx - 88, cy + 96, anchor="middle")
    css = f"""
  .sheet {{ fill: {BG}; stroke: {INK}; stroke-opacity: .35; }}
  .ln {{ fill: {INK}; opacity: .22; }}
  .pg {{ transform-origin: {cx}px {cy + 80}px; animation: fan 6s cubic-bezier(.5,0,.2,1) infinite; }}
  .p2 .ln:nth-child(3), .p2 .ln:nth-child(5) {{ fill: {TERRA}; opacity: .9; animation: redact 6s ease-in-out infinite; }}
  @keyframes fan {{ 0%,100% {{ transform: rotate(0); }} 30%,70% {{ transform: rotate(var(--r)); }} }}
  @keyframes redact {{ 0%,40% {{ opacity: .22; fill: {INK}; }} 55%,90% {{ opacity: 1; fill: {INK}; }} }}
  .seal {{ transform-origin: {seal_x}px {seal_y}px; animation: stamp 6s cubic-bezier(.3,1.6,.5,1) infinite; }}
  @keyframes stamp {{ 0%,45% {{ transform: scale(0); }} 55%,92% {{ transform: scale(1); }} 100% {{ transform: scale(0); }} }}
  .kbd {{ fill: none; stroke: {DIM}; }}
  .kt {{ fill: {BODY}; }}
  @media (prefers-reduced-motion: reduce) {{ .seal {{ transform: none; }} }}
"""
    kbd = f'<rect class="kbd" x="{cx - 112}" y="{cy + 76}" width="48" height="30" rx="7"/><path class="kt" d="{key}"/>'
    return "".join(pages) + seal + kbd, css


def motif_bmd() -> tuple[str, str]:
    x0, w = MX + 20, CW - MX - 80
    rows = []
    durs = [2.1, 2.9, 2.4, 3.3, 2.6]
    for i, d in enumerate(durs):
        y = 58 + i * 22
        rows.append(
            f'<rect x="{x0}" y="{y}" width="{w}" height="8" rx="4" class="trk"/>'
            f'<rect x="{x0}" y="{y}" width="{w}" height="8" rx="4" class="seg" style="animation-duration:{d * 1.6:.1f}s"/>'
        )
    merged_y = 196
    rows.append(
        f'<rect x="{x0}" y="{merged_y}" width="{w}" height="14" rx="7" class="trk"/>'
        f'<rect x="{x0}" y="{merged_y}" width="{w}" height="14" rx="7" class="all"/>'
    )
    lbl = MONO.path("5 PARTS, ONE FILE", 11, x0, merged_y - 12, track=1.6)
    css = f"""
  .trk {{ fill: {LINE}; }}
  .seg {{ fill: {MARI}; transform-origin: {x0}px 0; animation: fill 4s cubic-bezier(.4,0,.2,1) infinite; }}
  .seg:nth-of-type(4n) {{ fill: {TERRA}; }}
  .all {{ fill: {TERRA}; transform-origin: {x0}px 0; animation: fill 5.3s cubic-bezier(.6,0,.2,1) infinite; }}
  @keyframes fill {{ 0% {{ transform: scaleX(0); }} 75%,92% {{ transform: scaleX(1); opacity: 1; }} 100% {{ transform: scaleX(1); opacity: 0; }} }}
  .lbl {{ fill: {DIM}; }}
"""
    return "".join(rows) + f'<path class="lbl" d="{lbl}"/>', css


def motif_formspear() -> tuple[str, str]:
    x0 = MX + 30
    heights = [10, 6, 8, 12, 14, 20, 26, 40, 66, 98, 82]
    bars = []
    for i, h in enumerate(heights):
        color = TERRA if i <= 6 else (MARI if i <= 8 else TEAL)
        x = x0 + i * 30
        bars.append(
            f'<rect x="{x}" y="{190 - h}" width="20" height="{h}" rx="4" fill="{color}" class="nps" '
            f'style="animation-delay:{i * 0.07:.2f}s"/>'
            f'<path class="ax" d="{MONO.path(str(i), 11, x + 10, 212, anchor="middle")}"/>'
        )
    lbl = MONO.path("HOW LIKELY ARE YOU TO RECOMMEND US?", 10.5, x0, 52, track=1.2)
    css = f"""
  .nps {{ transform-box: fill-box; transform-origin: bottom; animation: up 5s cubic-bezier(.3,1.3,.5,1) infinite both; }}
  @keyframes up {{ 0% {{ transform: scaleY(0); }} 25%,88% {{ transform: scaleY(1); }} 100% {{ transform: scaleY(0); }} }}
  .ax, .lbl {{ fill: {DIM}; }}
  @media (prefers-reduced-motion: reduce) {{ .nps {{ transform: none; }} }}
"""
    return f'<path class="lbl" d="{lbl}"/>' + "".join(bars), css


def motif_settlr() -> tuple[str, str]:
    y = 112
    xs = [MX + 30, MX + 150, MX + 270]
    blocks, links = [], []
    for i, x in enumerate(xs):
        blocks.append(
            f'<g class="blk" style="animation-delay:{i * 0.9:.1f}s">'
            f'<rect x="{x}" y="{y - 40}" width="80" height="80" rx="12" class="bx"/>'
            f'<rect x="{x + 14}" y="{y - 20}" width="52" height="5" rx="2.5" class="bl"/>'
            f'<rect x="{x + 14}" y="{y - 8}" width="38" height="5" rx="2.5" class="bl"/>'
            f'<rect x="{x + 14}" y="{y + 4}" width="46" height="5" rx="2.5" class="bl"/></g>'
        )
        if i:
            links.append(
                f'<path d="M{xs[i - 1] + 80} {y}H{x}" class="lk" pathLength="1" '
                f'style="animation-delay:{i * 0.9 - 0.4:.1f}s"/>'
            )
    sx = xs[-1]
    sig = (
        f'<g class="sig"><circle cx="{sx + 4}" cy="{y + 70}" r="12" fill="{TEAL}"/>'
        f'<circle cx="{sx + 76}" cy="{y + 70}" r="12" fill="{MARI}"/>'
        f'<path d="M{sx - 2} {y + 70}l4 4 8-9M{sx + 70} {y + 70}l4 4 8-9" fill="none" stroke="{BG}" '
        f'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></g>'
    )
    lt = MONO.path("TENANT", 10, sx + 4, y + 100, anchor="middle", track=1)
    lo = MONO.path("OWNER", 10, sx + 76, y + 100, anchor="middle", track=1)
    css = f"""
  .bx {{ fill: {BG}; stroke: {INK}; stroke-opacity: .4; }}
  .bl {{ fill: {INK}; opacity: .25; }}
  .blk {{ animation: on 6s ease-in-out infinite both; }}
  @keyframes on {{ 0% {{ opacity: .25; }} 10%,85% {{ opacity: 1; }} 100% {{ opacity: .25; }} }}
  .lk {{ stroke: {TERRA}; stroke-width: 2; stroke-dasharray: 1; fill: none;
        animation: link 6s ease-in-out infinite both; }}
  @keyframes link {{ 0% {{ stroke-dashoffset: 1; }} 12%,85% {{ stroke-dashoffset: 0; }} 100% {{ stroke-dashoffset: 1; }} }}
  .sig {{ animation: on 6s ease-in-out 2.4s infinite both; }}
  .sl {{ fill: {DIM}; animation: on 6s ease-in-out 2.4s infinite both; }}
  @media (prefers-reduced-motion: reduce) {{ .lk {{ stroke-dashoffset: 0; }} }}
"""
    return "".join(links) + "".join(blocks) + sig + f'<path class="sl" d="{lt} {lo}"/>', css


def motif_sportshawk() -> tuple[str, str]:
    # A stick figure mid-kick, built from pose keypoints like an on-device model would see it.
    ox, oy = MX + 120, 50
    P = {
        "head": (40, 18), "neck": (40, 40), "ls": (24, 46), "rs": (56, 46),
        "le": (8, 70), "re": (74, 64), "lw": (4, 96), "rw": (92, 80),
        "hip": (40, 100), "lh": (30, 102), "rh": (50, 102),
        "lk": (24, 140), "la": (22, 178),
    }
    P = {k: (ox + x, oy + y) for k, (x, y) in P.items()}
    bones = [
        ("neck", "ls"), ("neck", "rs"), ("ls", "le"), ("le", "lw"), ("rs", "re"), ("re", "rw"),
        ("neck", "hip"), ("hip", "lh"), ("hip", "rh"), ("lh", "lk"), ("lk", "la"),
    ]
    lines = "".join(
        f'<line x1="{P[a][0]}" y1="{P[a][1]}" x2="{P[b][0]}" y2="{P[b][1]}" class="bn"/>' for a, b in bones
    )
    pts = "".join(
        f'<circle cx="{x}" cy="{y}" r="4.5" class="kp" style="animation-delay:{i * 0.12:.2f}s"/>'
        for i, (k, (x, y)) in enumerate(P.items()) if k not in ("head", "hip")
    )
    hx, hy = P["head"]
    rh = P["rh"]
    # Kicking leg rotates around the right hip
    leg = (
        f'<g class="leg"><line x1="{rh[0]}" y1="{rh[1]}" x2="{rh[0] + 18}" y2="{rh[1] + 36}" class="bn"/>'
        f'<line x1="{rh[0] + 18}" y1="{rh[1] + 36}" x2="{rh[0] + 30}" y2="{rh[1] + 74}" class="bn"/>'
        f'<circle cx="{rh[0] + 18}" cy="{rh[1] + 36}" r="4.5" class="kp"/>'
        f'<circle cx="{rh[0] + 30}" cy="{rh[1] + 74}" r="4.5" class="kp"/></g>'
    )
    ball = f'<circle class="ball" cx="{rh[0] + 44}" cy="{rh[1] + 80}" r="10"/>'
    ground = f'<line x1="{MX + 20}" y1="{oy + 190}" x2="{CW - 40}" y2="{oy + 190}" class="gd"/>'
    fps = MONO.path("ON-DEVICE · 60 FPS", 10.5, CW - 56, 52, anchor="end", track=1.4)
    css = f"""
  .bn {{ stroke: {INK}; stroke-opacity: .65; stroke-width: 2.4; stroke-linecap: round; }}
  .kp {{ fill: {TEAL}; animation: blink 2s ease-in-out infinite; }}
  .hd {{ fill: none; stroke: {INK}; stroke-opacity: .65; stroke-width: 2.4; }}
  @keyframes blink {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .45; }} }}
  .leg {{ transform-origin: {rh[0]}px {rh[1]}px; animation: kick 2.4s cubic-bezier(.5,0,.2,1) infinite; }}
  @keyframes kick {{ 0%,100% {{ transform: rotate(18deg); }} 35% {{ transform: rotate(32deg); }} 55% {{ transform: rotate(-52deg); }} 70% {{ transform: rotate(-30deg); }} }}
  .ball {{ fill: {MARI}; animation: fly 2.4s cubic-bezier(.2,.6,.3,1) infinite; }}
  @keyframes fly {{ 0%,52% {{ transform: none; opacity: 1; }} 85% {{ transform: translate(170px,-120px); opacity: 1; }} 86%,100% {{ transform: translate(170px,-120px); opacity: 0; }} }}
  .gd {{ stroke: {LINE}; stroke-width: 2; }}
  .fps {{ fill: {DIM}; }}
"""
    head = f'<circle cx="{hx}" cy="{hy}" r="13" class="hd"/>'
    return ground + lines + head + leg + pts + ball + f'<path class="fps" d="{fps}"/>', css


def motif_lawflow() -> tuple[str, str]:
    x0, y0 = MX + 40, 64
    cells = []
    hearings = {3, 9, 12, 17, 23, 26}
    for i in range(28):
        r, c = divmod(i, 7)
        x, y = x0 + c * 44, y0 + r * 40
        cls = "hr" if i in hearings else "dy"
        delay = sorted(hearings).index(i) * 0.6 if i in hearings else 0
        cells.append(
            f'<rect x="{x}" y="{y}" width="34" height="30" rx="7" class="{cls}" '
            f'style="animation-delay:{delay:.1f}s"/>'
        )
    days = "".join(
        f'<path class="dw" d="{MONO.path(d, 10, x0 + 17 + i * 44, y0 - 12, anchor="middle")}"/>'
        for i, d in enumerate("MTWTFSS")
    )
    css = f"""
  .dy {{ fill: {LINE}; }}
  .hr {{ fill: {LINE}; animation: hear 6s ease-in-out infinite both; }}
  @keyframes hear {{ 0% {{ fill: {LINE}; }} 6%,80% {{ fill: {TERRA}; }} 100% {{ fill: {LINE}; }} }}
  .dw {{ fill: {DIM}; }}
  @media (prefers-reduced-motion: reduce) {{ .hr {{ fill: {TERRA}; }} }}
"""
    return days + "".join(cells), css


PROJECTS = [
    ("vaani", "01", "Vaani", "An AI front desk for clinics and salons that picks up the phone, replies on WhatsApp, and books the appointment in Odia, Hindi or English.", "Python · LangGraph · FastAPI · MongoDB", motif_vaani, TERRA),
    ("octapdf", "02", "OctaPDF", "A PDF workspace that runs on your own machine. Edit, split, redact and convert without your files going anywhere.", "Java 21 · Spring Boot · Docker", motif_octapdf, TERRA),
    ("bmd", "03", "Black Marlin", "A free download manager for Windows, Linux and macOS. Splits files into parallel parts and picks up where it left off after a crash.", "Rust · Tokio", motif_bmd, MARI),
    ("formspear", "04", "Formspear", "Forms, surveys and feedback with real analytics. Written on plain Node.js, no framework, with Postgres doing the heavy lifting.", "Node.js · PostgreSQL · Redis · BullMQ", motif_formspear, TEAL),
    ("settlr", "05", "Settlr", "Renting in Delhi without blind trust. Only owner-verified listings, and every rent or deposit decision needs both sides to sign.", "FastAPI · Next.js · Postgres · Expo", motif_settlr, MARI),
    ("sportshawk", "06", "SportsHawk", "Free football training for kids outside the big cities. Film a drill on any phone, get scored on the phone itself, build a Player Card.", "React · MediaPipe · On-device ML", motif_sportshawk, TEAL),
    ("lawflow", "07", "LawFlow", "A practice manager for Indian advocates. Cases, hearing dates, clients and documents, on a desktop in chambers and a phone in court.", "Rust · Tauri · Expo · SQLite", motif_lawflow, TERRA),
]


# --------------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------------


def footer() -> str:
    W, H = 1200, 200
    sig = SERIF_IT.glyphs("Subham", 84, 0, 0)
    sw = SERIF_IT.width("Subham", 84)
    sig = SERIF_IT.glyphs("Subham", 84, (W - sw) / 2, 112)
    paths = "".join(
        f'<path d="{d}" pathLength="1" class="sg" style="animation-delay:{0.2 + i * 0.16:.2f}s"/>'
        for i, (d, _) in enumerate(sig)
    )
    line = MONO.path("MADE IN BHUBANESWAR", 11, W / 2, 162, anchor="middle", track=3)
    css = f"""
  .sg {{ fill: {INK}; stroke: {INK}; stroke-width: 1; stroke-dasharray: 1; fill-opacity: 1; stroke-opacity: 0;
        animation: draw 3s cubic-bezier(.6,.05,.3,1) both; }}
  @keyframes draw {{
    0% {{ stroke-dashoffset: 1; fill-opacity: 0; stroke-opacity: 1; }}
    60% {{ stroke-dashoffset: 0; fill-opacity: 0; stroke-opacity: 1; }}
    100% {{ stroke-dashoffset: 0; fill-opacity: 1; stroke-opacity: 0; }}
  }}
  .ml {{ fill: {DIM}; animation: in 1.5s ease-out 2.2s both; }}
  .u {{ stroke: {TERRA}; stroke-width: 2; stroke-linecap: round; stroke-dasharray: 1; fill: none;
       animation: under 1.4s cubic-bezier(.6,.05,.3,1) 1.6s both; }}
  @keyframes under {{ from {{ stroke-dashoffset: 1; }} to {{ stroke-dashoffset: 0; }} }}
  @keyframes in {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
"""
    ux0, ux1 = (W - sw) / 2 + 10, (W + sw) / 2 + 6
    under = f'<path class="u" pathLength="1" d="M{_num(ux0)} 132C{_num(ux0 + 80)} 124 {_num(ux1 - 60)} 126 {_num(ux1)} 120"/>'
    body = (f'<rect width="{W}" height="{H}" rx="20" fill="{CARD}"/>'
            f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="none" stroke="{LINE}"/>'
            f'{paths}{under}<path class="ml" d="{line}"/>')
    return svg(W, H, body, css, "Subham. Made in Bhubaneswar.")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "hero.svg").write_text(hero())
    for slug, idx, name, tagline, stack, motif_fn, accent in PROJECTS:
        motif, mcss = motif_fn()
        (OUT / f"{slug}.svg").write_text(card(idx, name, tagline, stack, motif, mcss, accent))
    (OUT / "signature.svg").write_text(footer())
    for p in sorted(OUT.glob("*.svg")):
        print(f"{p.relative_to(ROOT)}  {p.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
