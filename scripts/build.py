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

import base64
import random
import struct
import zlib

BASE_CSS = """
  @media (prefers-reduced-motion: reduce) {
    * { animation: none !important; }
  }
"""


def svg(w: int, h: int, body: str, css: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{title}">\n'
        f"<title>{title}</title>\n<style>{css}{BASE_CSS}</style>\n{body}\n</svg>\n"
    )


def _noise_png(size: int = 72, seed: int = 7) -> str:
    """A tiny tileable film-grain PNG. Cheaper to paint than an SVG noise filter."""
    rnd = random.Random(seed)
    rows = b""
    for _ in range(size):
        row = bytearray([0])
        for _ in range(size):
            v = rnd.randint(150, 255)
            row += bytes([v, v, v, rnd.randint(0, 34)])
        rows += bytes(row)

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(rows, 9))
        + chunk(b"IEND", b"")
    )
    return base64.b64encode(png).decode()


NOISE = _noise_png()


def grain_defs(id_: str = "grain") -> str:
    return (
        f'<pattern id="{id_}" width="72" height="72" patternUnits="userSpaceOnUse">'
        f'<image width="72" height="72" href="data:image/png;base64,{NOISE}"/></pattern>'
    )


def circle_d(cx: float, cy: float, r: float) -> str:
    return (
        f"M{_num(cx - r)} {_num(cy)}a{_num(r)} {_num(r)} 0 1 0 {_num(2 * r)} 0"
        f"a{_num(r)} {_num(r)} 0 1 0 {_num(-2 * r)} 0Z"
    )


def circle_d_top(cx: float, cy: float, r: float) -> str:
    """Circle starting at 12 o'clock, clockwise (for dash-based comets)."""
    return (
        f"M{_num(cx)} {_num(cy - r)}a{_num(r)} {_num(r)} 0 1 1 0 {_num(2 * r)}"
        f"a{_num(r)} {_num(r)} 0 1 1 0 {_num(-2 * r)}Z"
    )


def rrect_d(x: float, y: float, w: float, h: float, r: float) -> str:
    return (
        f"M{_num(x + r)} {_num(y)}H{_num(x + w - r)}A{r} {r} 0 0 1 {_num(x + w)} {_num(y + r)}"
        f"V{_num(y + h - r)}A{r} {r} 0 0 1 {_num(x + w - r)} {_num(y + h)}H{_num(x + r)}"
        f"A{r} {r} 0 0 1 {_num(x)} {_num(y + h - r)}V{_num(y + r)}A{r} {r} 0 0 1 {_num(x + r)} {_num(y)}Z"
    )


def polar(cx: float, cy: float, r: float, deg: float) -> tuple[float, float]:
    a = math.radians(deg - 90)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def text_ring(font: Font, text: str, size: float, cx: float, cy: float, r: float, cls: str) -> str:
    """Set `text` (repeated) around a circle, reading clockwise."""
    unit = font.width(text, size)
    reps = max(1, int(2 * math.pi * r // unit))
    track = (2 * math.pi * r - reps * unit) / max(1, reps * len(text))
    out, x = [], 0.0
    for _ in range(reps):
        for ch in text:
            adv = font.width(ch, size)
            if ch.strip():
                d = font.path(ch, size, -adv / 2, 0)
                ang = math.degrees((x + adv / 2) / r)
                out.append(
                    f'<path d="{d}" transform="translate({_num(cx)} {_num(cy)}) rotate({ang:.2f}) translate(0 {-r:.1f})"/>'
                )
            x += adv + track
    return f'<g class="{cls}">{"".join(out)}</g>'


def odometer(font: Font, value: str, size: float, x_right: float, base: float, name: str,
             start: float, end: float, loop: float, spins: int = 1) -> tuple[str, str]:
    """Rolling digit counter. Returns (svg, css). Percentages are of `loop` seconds."""
    lh = size * 1.02
    colw = max(font.width(str(d), size) for d in range(10))
    out, css = [], []
    x = x_right
    for ci, ch in enumerate(reversed(value)):
        if not ch.isdigit():
            w = font.width(ch, size)
            x -= w
            out.append(f'<path class="odx" d="{font.path(ch, size, x, base)}"/>')
            continue
        x -= colw
        seq = [str(d) for d in range(10)] * (spins + ci) + [str(d) for d in range(int(ch) + 1)]
        final = len(seq) - 1
        glyphs = "".join(
            f'<path d="{font.path(dg, size, x + colw / 2, base + k * lh, anchor="middle")}"/>'
            for k, dg in enumerate(seq)
        )
        cid = f"{name}c{ci}"
        out.append(
            f'<clipPath id="{cid}"><rect x="{_num(x - 2)}" y="{_num(base - size * 0.8)}" width="{_num(colw + 4)}" '
            f'height="{_num(size * 1.0)}"/></clipPath>'
            f'<g clip-path="url(#{cid})"><g class="{cid} odc" style="transform:translateY({-final * lh:.1f}px)">{glyphs}</g></g>'
        )
        css.append(
            f"  .{cid} {{ animation: {cid} {loop}s cubic-bezier(.2,.8,.2,1) infinite both; }}\n"
            f"  @keyframes {cid} {{ 0%,{start}% {{ transform: translateY(0); }} "
            f"{end + ci * 3}%,100% {{ transform: translateY({-final * lh:.1f}px); }} }}\n"
        )
    return "".join(out), "".join(css)


def card_frame(w: int, h: int, accent: str, speed: float = 11) -> tuple[str, str]:
    """Rounded border with a light that travels around it."""
    d = rrect_d(0.75, 0.75, w - 1.5, h - 1.5, 20)
    body = (
        f'<path d="{d}" class="fr"/>'
        f'<path d="{d}" pathLength="1" class="cm cmg"/>'
        f'<path d="{d}" pathLength="1" class="cm"/>'
    )
    css = f"""
  .fr {{ fill: none; stroke: {LINE}; stroke-width: 1.5; }}
  .cm {{ fill: none; stroke: {accent}; stroke-width: 1.6; stroke-linecap: round; stroke-dasharray: .07 .93;
        animation: orbit {speed}s linear infinite; }}
  .cmg {{ stroke-width: 7; opacity: .16; }}
  @keyframes orbit {{ from {{ stroke-dashoffset: 1; }} to {{ stroke-dashoffset: 0; }} }}
"""
    return body, css


# --------------------------------------------------------------------------
# Hero
# --------------------------------------------------------------------------


def konark_wheel(cx: float, cy: float, R: float, start: float) -> tuple[str, float]:
    """Line drawing of a Konark Sun Temple wheel. Returns (svg, time drawing ends)."""
    parts: list[str] = []
    t = start

    def draw(d: str, cls: str, dur: float, delay: float) -> None:
        parts.append(
            f'<path d="{d}" pathLength="1" class="{cls} dr" '
            f'style="animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s"/>'
        )

    for i, (r, cls) in enumerate([(R, "w1"), (R * 0.93, "w2"), (R * 0.80, "w1"), (R * 0.76, "w2")]):
        draw(circle_d(cx, cy, r), cls, 1.6, t + i * 0.18)
    t += 0.9
    beads = "".join(
        f'<circle cx="{_num(polar(cx, cy, R * 0.965, k * 7.5)[0])}" cy="{_num(polar(cx, cy, R * 0.965, k * 7.5)[1])}" '
        f'r="1.9" class="bead" style="animation-delay:{t + k * 0.03:.2f}s"/>'
        for k in range(48)
    )
    parts.append(beads)
    # scalloped band between the inner rims
    sc = []
    for k in range(32):
        a0, a1 = k * 11.25, (k + 1) * 11.25
        x0, y0 = polar(cx, cy, R * 0.80, a0)
        x1, y1 = polar(cx, cy, R * 0.80, a1)
        mx, my = polar(cx, cy, R * 0.845, (a0 + a1) / 2)
        sc.append(f"M{_num(x0)} {_num(y0)}Q{_num(mx)} {_num(my)} {_num(x1)} {_num(y1)}")
    draw("".join(sc), "w2", 1.8, t)

    r_in, r_out = R * 0.21, R * 0.76
    for k in range(8):
        a = k * 45
        x0, y0 = polar(cx, cy, r_in, a)
        x1, y1 = polar(cx, cy, r_out, a)
        mid = (r_in + r_out) / 2
        lx, ly = polar(cx, cy, mid, a - 4.4)
        rx, ry = polar(cx, cy, mid, a + 4.4)
        draw(
            f"M{_num(x0)} {_num(y0)}Q{_num(lx)} {_num(ly)} {_num(x1)} {_num(y1)}"
            f"Q{_num(rx)} {_num(ry)} {_num(x0)} {_num(y0)}Z",
            "w1", 1.1, t + k * 0.09,
        )
        mx, my = polar(cx, cy, mid, a)
        draw(circle_d(mx, my, R * 0.06), "w3", 0.8, t + 0.5 + k * 0.09)
        draw(circle_d(mx, my, R * 0.028), "w3", 0.6, t + 0.8 + k * 0.09)
    t += 0.8
    for k in range(8):
        a = k * 45 + 22.5
        x0, y0 = polar(cx, cy, r_in, a)
        x1, y1 = polar(cx, cy, r_out, a)
        draw(f"M{_num(x0)} {_num(y0)}L{_num(x1)} {_num(y1)}", "w2", 0.9, t + k * 0.07)
    t += 0.6
    draw(circle_d(cx, cy, r_in), "w1", 1.0, t)
    draw(circle_d(cx, cy, R * 0.07), "w3", 0.8, t + 0.2)
    for k in range(16):
        a = k * 22.5
        x0, y0 = polar(cx, cy, R * 0.08, a)
        x1, y1 = polar(cx, cy, r_in * 0.92, a)
        lx, ly = polar(cx, cy, R * 0.15, a - 11)
        rx, ry = polar(cx, cy, R * 0.15, a + 11)
        draw(
            f"M{_num(x0)} {_num(y0)}Q{_num(lx)} {_num(ly)} {_num(x1)} {_num(y1)}"
            f"Q{_num(rx)} {_num(ry)} {_num(x0)} {_num(y0)}Z",
            "w2", 0.7, t + 0.3 + k * 0.04,
        )
    t += 1.2
    return "".join(parts), t


def hero() -> str:
    W, H = 1200, 520
    cx, cy, R = 968, 262, 172
    rnd = random.Random(42)

    # --- name, drawn then lit by a gold sheen
    name_glyphs = SERIF.glyphs("Subham Jena", 134, 72, 244)
    name = "".join(
        f'<path d="{d}" pathLength="1" class="nm" style="animation-delay:{0.25 + i * 0.11:.2f}s"/>'
        for i, (d, _) in enumerate(name_glyphs)
    )
    name_clip = "".join(f'<path d="{d}"/>' for d, _ in name_glyphs)

    # --- "I build ..." with phrases revealed letter by letter
    lead_size = 25
    lead_d = SANS.path("I build", lead_size, 76, 324)
    ph_x = 76 + SANS.width("I build", lead_size) + 11
    phrases = [
        "front desks that answer in Odia.",
        "PDF tools that never phone home.",
        "download managers in Rust.",
        "scouting apps for small-town footballers.",
        "rental deals both sides sign off on.",
    ]
    period, first = 3.8, 6.2
    total = period * len(phrases)
    vis = 100 / len(phrases)
    ph_svg = []
    for i, text in enumerate(phrases):
        gl = SERIF_IT.glyphs(text, 34, ph_x, 325)
        w = SERIF_IT.width(text, 34)
        t0 = first + i * period
        ps = "".join(
            f'<path d="{d}" style="animation-delay:{t0 + j * 0.022:.3f}s"/>' for j, (d, _) in enumerate(gl)
        )
        ul = f'<path class="ul" pathLength="1" d="M{_num(ph_x)} 340H{_num(ph_x + w)}" style="animation-delay:{t0 + 0.15:.2f}s"/>'
        caret = (
            f'<g class="cw" style="animation-delay:{t0:.2f}s"><rect class="caret" x="{_num(ph_x + w + 6)}" '
            f'y="298" width="2.5" height="34" rx="1"/></g>'
        )
        ph_svg.append(f'<g class="ph{" ph0" if i == 0 else ""}">{ps}{ul}{caret}</g>')

    place = MONO.path("BHUBANESWAR, ODISHA", 13, 96, 100, track=2.6)
    studio = SANS.path("Founder, XolverLabs   ·   xolver.in", 15, 76, 416)

    # --- wheel, rays, text ring, comets, embers
    wheel, wheel_end = konark_wheel(cx, cy, R, 0.6)
    rays = []
    nr = 90
    for k in range(nr):
        a = k * 360 / nr
        long = 1.55 if k % 2 == 0 else 1.38
        x0, y0 = polar(cx, cy, R * 1.17, a)
        x1, y1 = polar(cx, cy, R * long, a)
        rays.append(
            f'<line x1="{_num(x0)}" y1="{_num(y0)}" x2="{_num(x1)}" y2="{_num(y1)}" '
            f'style="animation-delay:{-(k / nr) * 7:.2f}s"/>'
        )
    ring = text_ring(MONO, "KONARK · SUN TEMPLE · ODISHA · 1250 CE · ", 10.5, cx, cy, R * 1.08, "tr")
    comets = (
        f'<path class="cmt cg" pathLength="1" d="{circle_d_top(cx, cy, R)}"/>'
        f'<path class="cmt" pathLength="1" d="{circle_d_top(cx, cy, R)}"/>'
        f'<path class="cmt2 cg" pathLength="1" d="{circle_d_top(cx, cy, R * 0.76)}"/>'
        f'<path class="cmt2" pathLength="1" d="{circle_d_top(cx, cy, R * 0.76)}"/>'
    )
    embers = []
    for k in range(34):
        x = rnd.uniform(640, 1190)
        y = rnd.uniform(380, 540)
        r = rnd.uniform(0.8, 2.3)
        dur = rnd.uniform(7, 14)
        dx = rnd.uniform(-40, 40)
        col = MARI if k % 3 else TERRA
        embers.append(
            f'<circle cx="{_num(x)}" cy="{_num(y)}" r="{_num(r)}" fill="{col}" class="em" '
            f'style="--dx:{dx:.0f}px;animation-duration:{dur:.1f}s;animation-delay:{-rnd.uniform(0, dur):.1f}s"/>'
        )

    a0, a1 = -16, 16
    sx0, sy0 = polar(cx, cy, R * 0.76, a0)
    sx1, sy1 = polar(cx, cy, R * 0.76, a1)
    sun = (
        f'<path class="sun" d="M{cx} {cy}L{_num(sx0)} {_num(sy0)}A{_num(R * 0.76)} {_num(R * 0.76)} 0 0 1 '
        f'{_num(sx1)} {_num(sy1)}Z" fill="url(#wedge)"/>'
    )

    css = f"""
  .bg {{ fill: {BG}; }}
  .au {{ animation: drift 26s ease-in-out infinite alternate; }}
  .au2 {{ animation-duration: 34s; animation-direction: alternate-reverse; }}
  .au3 {{ animation-duration: 41s; }}
  @keyframes drift {{ 0% {{ transform: translate(0,0) scale(1); }} 50% {{ transform: translate(-70px,40px) scale(1.15); }} 100% {{ transform: translate(50px,-30px) scale(.95); }} }}
  .nm {{ fill: {INK}; stroke: {INK}; stroke-width: 1.1; stroke-dasharray: 1; stroke-dashoffset: 0;
        fill-opacity: 1; stroke-opacity: 0; animation: draw 3.2s cubic-bezier(.6,.05,.3,1) both; }}
  @keyframes draw {{
    0% {{ stroke-dashoffset: 1; fill-opacity: 0; stroke-opacity: 1; }}
    55% {{ stroke-dashoffset: 0; fill-opacity: 0; stroke-opacity: 1; }}
    100% {{ stroke-dashoffset: 0; fill-opacity: 1; stroke-opacity: 0; }}
  }}
  .sheen {{ animation: sheen 7s cubic-bezier(.5,0,.3,1) 4.2s infinite both; }}
  @keyframes sheen {{ 0% {{ transform: translateX(-320px) skewX(-18deg); }} 35%,100% {{ transform: translateX(760px) skewX(-18deg); }} }}
  .lead {{ fill: {BODY}; animation: rise 1.2s ease-out 5s both; }}
  .meta {{ fill: {DIM}; animation: rise 1.2s ease-out 5.6s both; }}
  .rule {{ stroke: {LINE}; animation: grow 1.6s cubic-bezier(.6,.05,.3,1) 5.2s both; transform-origin: 76px 0; }}
  .place {{ fill: {DIM}; animation: rise 1s ease-out .1s both; }}
  .dot {{ fill: {TERRA}; animation: pulse 2.4s ease-in-out infinite; transform-origin: 81px 95px; }}
  .halo {{ fill: none; stroke: {TERRA}; animation: halo 2.4s ease-out infinite; transform-origin: 81px 95px; }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
  @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .5; }} }}
  @keyframes halo {{ from {{ transform: scale(1); opacity: .8; }} to {{ transform: scale(3.2); opacity: 0; }} }}
  .ph path:not(.ul) {{ fill: {MARI}; transform-box: fill-box; transform-origin: 0 100%;
        animation: glyph {total:.1f}s cubic-bezier(.2,.8,.2,1) infinite both; }}
  @keyframes glyph {{
    0% {{ opacity: 0; transform: translateY(18px) rotate(10deg); }}
    {vis * 0.14:.2f}% {{ opacity: 1; transform: none; }}
    {vis * 0.84:.2f}% {{ opacity: 1; transform: none; }}
    {vis * 0.97:.2f}% {{ opacity: 0; transform: translateY(-12px) rotate(-6deg); }}
    100% {{ opacity: 0; transform: translateY(-12px); }}
  }}
  .ul {{ fill: none; stroke: {TERRA}; stroke-width: 2; stroke-linecap: round; stroke-dasharray: 1 1;
        stroke-dashoffset: 0; animation: ul {total:.1f}s cubic-bezier(.6,.05,.3,1) infinite both; }}
  @keyframes ul {{ 0% {{ stroke-dashoffset: 1; }} {vis * 0.3:.2f}% {{ stroke-dashoffset: 0; }}
    {vis * 0.78:.2f}% {{ stroke-dashoffset: 0; }} {vis * 0.97:.2f}%,100% {{ stroke-dashoffset: -1; }} }}
  .cw {{ animation: cw {total:.1f}s linear infinite both; }}
  @keyframes cw {{ 0% {{ opacity: 0; }} {vis * 0.12:.2f}% {{ opacity: 1; }} {vis * 0.9:.2f}% {{ opacity: 1; }} {vis * 0.95:.2f}%,100% {{ opacity: 0; }} }}
  .caret {{ fill: {TERRA}; animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .dr {{ fill: none; stroke-dasharray: 1; stroke-dashoffset: 0; stroke-linecap: round; stroke-linejoin: round;
        animation-name: stroke; animation-timing-function: cubic-bezier(.6,.05,.3,1); animation-fill-mode: both; }}
  @keyframes stroke {{ from {{ stroke-dashoffset: 1; }} to {{ stroke-dashoffset: 0; }} }}
  .w1 {{ stroke: {INK}; stroke-opacity: .8; stroke-width: 1.3; }}
  .w2 {{ stroke: {INK}; stroke-opacity: .36; stroke-width: 1; }}
  .w3 {{ stroke: {TERRA}; stroke-width: 1.4; }}
  .bead {{ fill: {MARI}; animation: pop .5s ease-out both; }}
  @keyframes pop {{ from {{ opacity: 0; }} to {{ opacity: .9; }} }}
  .spin {{ transform-origin: {cx}px {cy}px; animation: spin 150s linear infinite; }}
  .tr {{ fill: {DIM}; transform-origin: {cx}px {cy}px; animation: spin 90s linear infinite reverse, fadein 2s ease-out 2.6s both; }}
  .sun {{ transform-origin: {cx}px {cy}px; animation: spin 24s linear infinite, fadein 2s ease-out {wheel_end:.1f}s both; }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  @keyframes fadein {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
  .rays line {{ stroke: {MARI}; stroke-width: 1.2; stroke-linecap: round; opacity: .08;
        animation: ray 7s linear infinite; }}
  .rays {{ animation: fadein 3s ease-out 3s both; }}
  @keyframes ray {{ 0%,100% {{ opacity: .06; }} 8% {{ opacity: .75; }} 26% {{ opacity: .06; }} }}
  .cmt, .cmt2 {{ fill: none; stroke: {MARI}; stroke-width: 2; stroke-linecap: round; stroke-dasharray: .05 .95;
        animation: orbit 9s linear infinite, fadein 2s ease-out {wheel_end:.1f}s both; }}
  .cmt2 {{ stroke: {TERRA}; animation-duration: 6s, 2s; animation-direction: reverse, normal; }}
  .cg {{ stroke-width: 8; opacity: .18; }}
  @keyframes orbit {{ from {{ stroke-dashoffset: 1; }} to {{ stroke-dashoffset: 0; }} }}
  .hub {{ transform-origin: {cx}px {cy}px; animation: hub 4s ease-in-out infinite; }}
  @keyframes hub {{ 0%,100% {{ opacity: .35; transform: scale(.9); }} 50% {{ opacity: .9; transform: scale(1.1); }} }}
  .em {{ opacity: 0; animation: ember 10s linear infinite; }}
  @keyframes ember {{ 0% {{ opacity: 0; transform: translate(0,0); }} 15% {{ opacity: .9; }}
    80% {{ opacity: .4; }} 100% {{ opacity: 0; transform: translate(var(--dx), -300px); }} }}
  @media (prefers-reduced-motion: reduce) {{ .ph {{ opacity: 0; }} .ph0 {{ opacity: 1; }} .em {{ opacity: .5; }} }}
"""
    body = f"""<defs>{grain_defs()}
  <radialGradient id="a1"><stop offset="0" stop-color="{TERRA}" stop-opacity=".30"/><stop offset="1" stop-color="{TERRA}" stop-opacity="0"/></radialGradient>
  <radialGradient id="a2"><stop offset="0" stop-color="#7A2E4A" stop-opacity=".34"/><stop offset="1" stop-color="#7A2E4A" stop-opacity="0"/></radialGradient>
  <radialGradient id="a3"><stop offset="0" stop-color="{MARI}" stop-opacity=".16"/><stop offset="1" stop-color="{MARI}" stop-opacity="0"/></radialGradient>
  <radialGradient id="hubg"><stop offset="0" stop-color="{MARI}" stop-opacity=".9"/><stop offset=".4" stop-color="{TERRA}" stop-opacity=".35"/><stop offset="1" stop-color="{TERRA}" stop-opacity="0"/></radialGradient>
  <radialGradient id="wedge" cx="{cx}" cy="{cy}" r="{R * 0.76}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{MARI}" stop-opacity="0"/><stop offset=".6" stop-color="{MARI}" stop-opacity=".12"/><stop offset="1" stop-color="{MARI}" stop-opacity=".26"/>
  </radialGradient>
  <linearGradient id="sheen" x1="0" x2="1"><stop offset="0" stop-color="{MARI}" stop-opacity="0"/>
    <stop offset=".5" stop-color="#FFE2B0" stop-opacity=".95"/><stop offset="1" stop-color="{MARI}" stop-opacity="0"/></linearGradient>
  <clipPath id="nameclip">{name_clip}</clipPath>
  <clipPath id="clip"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#clip)">
  <rect class="bg" width="{W}" height="{H}"/>
  <ellipse class="au" cx="1000" cy="250" rx="420" ry="320" fill="url(#a1)"/>
  <ellipse class="au au2" cx="300" cy="520" rx="520" ry="300" fill="url(#a2)"/>
  <ellipse class="au au3" cx="620" cy="40" rx="420" ry="220" fill="url(#a3)"/>
  <g class="rays">{''.join(rays)}</g>
  {ring}
  <circle class="hub" cx="{cx}" cy="{cy}" r="{R * 0.5}" fill="url(#hubg)"/>
  {sun}
  <g class="spin">{wheel}</g>
  {comets}
  {''.join(embers)}
  <circle class="halo" cx="81" cy="95" r="4"/>
  <circle class="dot" cx="81" cy="95" r="4"/>
  <path class="place" d="{place}"/>
  <g>{name}</g>
  <g clip-path="url(#nameclip)"><rect class="sheen" x="40" y="100" width="200" height="200" fill="url(#sheen)"/></g>
  <path class="lead" d="{lead_d}"/>
  {''.join(ph_svg)}
  <line class="rule" x1="76" y1="376" x2="660" y2="376"/>
  <path class="meta" d="{studio}"/>
  <rect width="{W}" height="{H}" fill="url(#grain)" opacity=".55"/>
</g>"""
    return svg(W, H, body, css, "Subham Jena. I build software from Bhubaneswar, Odisha.")


# --------------------------------------------------------------------------
# Project cards
# --------------------------------------------------------------------------

CW, CH = 1200, 290
MX = 660  # motif area starts here; centre of motif area ~ 915


def card(idx: str, name: str, tagline: str, stack: str, motif: str, motif_css: str, accent: str) -> str:
    num = MONO.path(idx, 13, 56, 74, track=2)
    title = SERIF.path(name, 66, 52, 152)
    lines = SANS.wrap(tagline, 19, 560)
    assert len(lines) <= 2, f"{name}: tagline wraps to {len(lines)} lines"
    tag = "".join(f'<path class="tag" d="{SANS.path(line, 19, 56, 194 + i * 28)}"/>' for i, line in enumerate(lines))
    st = MONO.path(stack.upper(), 11.5, 56, CH - 34, track=1.6)
    frame, frame_css = card_frame(CW, CH, accent)
    css = f"""
  .bg {{ fill: {CARD}; }}
  .num {{ fill: {accent}; }}
  .ttl {{ fill: {INK}; }}
  .tag {{ fill: {BODY}; }}
  .stk {{ fill: {DIM}; }}
  .bar {{ fill: {accent}; }}
  .glow {{ animation: glow 12s ease-in-out infinite alternate; }}
  @keyframes glow {{ from {{ transform: translate(0,0); opacity: .7; }} to {{ transform: translate(-60px,20px); opacity: 1; }} }}
{frame_css}{motif_css}"""
    body = f"""<defs>{grain_defs()}
  <radialGradient id="cgl"><stop offset="0" stop-color="{accent}" stop-opacity=".20"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
  <clipPath id="c"><rect width="{CW}" height="{CH}" rx="20"/></clipPath></defs>
<g clip-path="url(#c)">
  <rect class="bg" width="{CW}" height="{CH}"/>
  <ellipse class="glow" cx="930" cy="150" rx="340" ry="220" fill="url(#cgl)"/>
  <rect class="bar" x="56" y="48" width="28" height="2"/>
  <path class="num" d="{num}"/>
  <path class="ttl" d="{title}"/>
  {tag}
  <path class="stk" d="{st}"/>
  {motif}
  <rect width="{CW}" height="{CH}" fill="url(#grain)" opacity=".5"/>
</g>
{frame}"""
    return svg(CW, CH, body, css, f"{name}. {tagline}")


def bubble(x: float, y: float, text: str, fill: str, ink: str, cls: str, right: bool = False, icon: str = "") -> str:
    size = 14.5
    w = SANS.width(text, size) + 30 + (20 if icon else 0)
    h = 38
    if right:
        x -= w
    corner = f"M{_num(x + (w - 8 if right else 8))} {y + h}l{'6' if right else '-6'} 6 2-8z"
    tx = x + 15
    return (
        f'<g class="{cls}"><rect x="{_num(x)}" y="{y}" width="{_num(w)}" height="{h}" rx="15" fill="{fill}"/>'
        f'<path d="{corner}" fill="{fill}"/>'
        f'<path d="{SANS.path(text, size, tx, y + 24)}" fill="{ink}"/>{icon.format(x=x + w - 26, y=y + 19)}</g>'
    )


def motif_vaani() -> tuple[str, str]:
    ox, oy = 748, 118
    ripples = "".join(
        f'<circle class="rp" cx="{ox}" cy="{oy}" r="34" style="animation-delay:{i * 0.9:.1f}s"/>' for i in range(3)
    )
    mic = (
        f'<circle cx="{ox}" cy="{oy}" r="34" fill="url(#orb)"/>'
        f'<rect x="{ox - 7}" y="{oy - 16}" width="14" height="22" rx="7" fill="{BG}"/>'
        f'<path d="M{ox - 12} {oy}a12 12 0 0 0 24 0M{ox} {oy + 12}v8" fill="none" stroke="{BG}" stroke-width="2.6" stroke-linecap="round"/>'
    )
    greetings = [(ODIA, "ନମସ୍କାର", 26), (DEVA, "नमस्ते", 28), (SANS_MED, "Haan ji", 22), (SANS_MED, "Hello", 22)]
    gp = 2.4
    gr = "".join(
        f'<path class="gr{" gr0" if i == 0 else ""}" style="animation-delay:{i * gp:.1f}s" d="{f.path(t, s, ox, 196, anchor="middle")}"/>'
        for i, (f, t, s) in enumerate(greetings)
    )
    bars = []
    for k in range(15):
        x = ox - 49 + k * 7
        h = 4 + 16 * math.sin(math.pi * (k + 0.5) / 15)
        bars.append(
            f'<rect class="wv" x="{_num(x)}" y="{_num(234 - h / 2)}" width="3.5" height="{_num(h)}" rx="1.75" '
            f'style="animation-duration:{0.7 + (k * 37 % 9) / 12:.2f}s;animation-delay:{-k * 0.11:.2f}s"/>'
        )
    check = (
        '<path d="M{x} {y}l4 4 8-9" fill="none" stroke="' + INK + '" stroke-width="2.2" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
    )
    b1 = bubble(860, 44, "Kal subah 11 baje slot hai?", "#2C2520", INK, "b b1")
    typing = (
        f'<g class="b ty"><rect x="1092" y="98" width="62" height="34" rx="15" fill="{TERRA}"/>'
        + "".join(f'<circle class="td" cx="{1110 + i * 13}" cy="115" r="3.6" fill="{INK}" style="animation-delay:{i * 0.15:.2f}s"/>' for i in range(3))
        + "</g>"
    )
    b2 = bubble(1154, 98, "Haan ji, 11 baje book ho gaya", TERRA, INK, "b b2", right=True, icon=check)
    b3 = bubble(860, 160, "Thank you!", "#2C2520", INK, "b b3")
    meta = MONO.path("WHATSAPP · VOICE", 10, 1154, 254, anchor="end", track=1.6)
    loop = 9
    css = f"""
  .rp {{ fill: none; stroke: {TERRA}; stroke-width: 1.4; transform-origin: {ox}px {oy}px; animation: rp 2.7s cubic-bezier(.2,.6,.3,1) infinite both; }}
  @keyframes rp {{ from {{ transform: scale(1); opacity: .9; }} to {{ transform: scale(2.5); opacity: 0; }} }}
  .gr {{ fill: {INK}; opacity: 0; animation: say {gp * 4:.1f}s ease-in-out infinite both; }}
  @keyframes say {{ 0% {{ opacity: 0; transform: translateY(8px); }} 5% {{ opacity: 1; transform: none; }}
    21% {{ opacity: 1; transform: none; }} 25%,100% {{ opacity: 0; transform: translateY(-6px); }} }}
  .wv {{ fill: {MARI}; transform-box: fill-box; transform-origin: center; animation: talk 1s ease-in-out infinite alternate; }}
  @keyframes talk {{ from {{ transform: scaleY(.25); }} to {{ transform: scaleY(1); }} }}
  .b {{ transform-box: fill-box; animation: {loop}s cubic-bezier(.3,1.5,.5,1) infinite both; }}
  .b1 {{ transform-origin: 0 100%; animation-name: b1; }}
  .ty {{ transform-origin: 100% 100%; animation-name: ty; }}
  .b2 {{ transform-origin: 100% 100%; animation-name: b2; }}
  .b3 {{ transform-origin: 0 100%; animation-name: b3; }}
  @keyframes b1 {{ 0%,4% {{ opacity: 0; transform: scale(.6); }} 10%,90% {{ opacity: 1; transform: none; }} 96%,100% {{ opacity: 0; }} }}
  @keyframes ty {{ 0%,16% {{ opacity: 0; transform: scale(.6); }} 21%,33% {{ opacity: 1; transform: none; }} 35%,100% {{ opacity: 0; }} }}
  @keyframes b2 {{ 0%,34% {{ opacity: 0; transform: scale(.6); }} 40%,90% {{ opacity: 1; transform: none; }} 96%,100% {{ opacity: 0; }} }}
  @keyframes b3 {{ 0%,54% {{ opacity: 0; transform: scale(.6); }} 60%,90% {{ opacity: 1; transform: none; }} 96%,100% {{ opacity: 0; }} }}
  .td {{ animation: td .9s ease-in-out infinite; }}
  @keyframes td {{ 0%,100% {{ transform: translateY(0); opacity: .5; }} 40% {{ transform: translateY(-4px); opacity: 1; }} }}
  .mt {{ fill: {DIM}; }}
  @media (prefers-reduced-motion: reduce) {{ .gr0 {{ opacity: 1; }} .ty {{ opacity: 0; }} }}
"""
    defs = (
        f'<defs><radialGradient id="orb" cx=".35" cy=".3"><stop offset="0" stop-color="{MARI}"/>'
        f'<stop offset="1" stop-color="{TERRA}"/></radialGradient></defs>'
    )
    return defs + ripples + mic + gr + "".join(bars) + b1 + typing + b2 + b3 + f'<path class="mt" d="{meta}"/>', css


def motif_octapdf() -> tuple[str, str]:
    cx, cy = 915, 150
    pw, ph = 124, 162
    px, py = cx - pw / 2, cy - ph / 2
    ring = (
        f'<circle class="gap" cx="{cx}" cy="{cy}" r="126"/><circle class="gap2" cx="{cx}" cy="{cy}" r="140"/>'
    )
    pill_t = "STAYS ON YOUR MACHINE"
    pill_w = MONO.width(pill_t, 9.5, 1.4) + 24
    pill = (
        f'<rect x="{_num(cx - pill_w / 2)}" y="2" width="{_num(pill_w)}" height="22" rx="11" class="pill"/>'
        f'<path class="pt" d="{MONO.path(pill_t, 9.5, cx, 17, anchor="middle", track=1.4)}"/>'
    )
    back = "".join(
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" class="bk bk{i}" fill="{c}"/>'
        for i, c in enumerate(["#8F8578", "#BDB2A4"])
    )
    lines, reds = [], []
    widths = [92, 80, 96, 64, 90, 84, 70, 94, 58]
    targets = {1, 3, 4, 6}
    loop, sweep = 6.0, 2.4
    css_r = []
    for j, w in enumerate(widths):
        y = py + 22 + j * 15
        lines.append(f'<rect x="{px + 16}" y="{y}" width="{w}" height="5" rx="2.5" fill="#3A322C" opacity=".55"/>')
        if j in targets:
            p = (y - py) / ph * (sweep / loop) * 100
            reds.append(f'<rect x="{px + 13}" y="{y - 3}" width="{w + 6}" height="11" rx="2" class="rd rd{j}"/>')
            css_r.append(
                f"  .rd{j} {{ animation: rd{j} {loop}s cubic-bezier(.7,0,.2,1) infinite both; }}\n"
                f"  @keyframes rd{j} {{ 0%,{p:.1f}% {{ transform: scaleX(0); }} {p + 5:.1f}%,93% {{ transform: scaleX(1); }} 100% {{ transform: scaleX(0); }} }}\n"
            )
    page = (
        f'<g class="pg"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="#F1E9DD"/>'
        + "".join(lines) + "".join(reds)
        + f'<g clip-path="url(#pclip)"><g class="beam"><rect x="{px}" y="{py - 40}" width="{pw}" height="40" fill="url(#beam)"/>'
        f'<rect x="{px}" y="{py - 1.5}" width="{pw}" height="2" fill="{TERRA}"/></g></g></g>'
    )
    sx, sy = px + pw - 6, py + ph - 10
    seal = (
        f'<circle class="burst" cx="{sx}" cy="{sy}" r="22"/>'
        f'<g class="seal"><circle cx="{sx}" cy="{sy}" r="22" fill="{TERRA}"/>'
        f'<path d="M{sx - 9} {sy}l6 6 12-13" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>'
    )
    kx, ky = 712, 214
    key = (
        f'<g class="key"><rect x="{kx}" y="{ky + 4}" width="56" height="38" rx="9" fill="#0E0B09"/>'
        f'<rect class="kt" x="{kx}" y="{ky}" width="56" height="38" rx="9" fill="#2C2520" stroke="{LINE}"/>'
        f'<path class="kt" d="{MONO.path("⌘K", 15, kx + 28, ky + 24, anchor="middle")}" fill="{INK}"/></g>'
    )
    css = f"""
  .gap {{ fill: none; stroke: {DIM}; stroke-width: 1.2; stroke-dasharray: 2 7; transform-origin: {cx}px {cy}px; animation: rot 40s linear infinite; }}
  .gap2 {{ fill: none; stroke: {LINE}; }}
  @keyframes rot {{ to {{ transform: rotate(360deg); }} }}
  .pill {{ fill: {CARD}; stroke: {LINE}; }}
  .pt {{ fill: {BODY}; }}
  .bk {{ transform-origin: {cx}px {cy + ph / 2}px; animation: sway 6s ease-in-out infinite alternate; }}
  .bk0 {{ --r: -13deg; }} .bk1 {{ --r: 9deg; }}
  @keyframes sway {{ from {{ transform: rotate(var(--r)); }} to {{ transform: rotate(calc(var(--r) * 1.4)); }} }}
  .bk0 {{ transform: rotate(-13deg); }} .bk1 {{ transform: rotate(9deg); }}
  .rd {{ fill: #13100E; transform-box: fill-box; transform-origin: 0 50%; }}
  .beam {{ animation: beam {loop}s cubic-bezier(.45,0,.55,1) infinite both; }}
  @keyframes beam {{ 0% {{ transform: translateY(0); opacity: 1; }} {sweep / loop * 100:.1f}% {{ transform: translateY({ph + 40}px); opacity: 1; }} {sweep / loop * 100 + .1:.1f}%,100% {{ opacity: 0; transform: translateY({ph + 40}px); }} }}
  .seal {{ transform-origin: {sx}px {sy}px; animation: stamp {loop}s cubic-bezier(.3,1.7,.5,1) infinite both; }}
  @keyframes stamp {{ 0%,48% {{ transform: scale(0) rotate(-30deg); }} 56%,93% {{ transform: scale(1) rotate(0); }} 100% {{ transform: scale(0); }} }}
  .burst {{ fill: none; stroke: {TERRA}; stroke-width: 2; transform-origin: {sx}px {sy}px; animation: burst {loop}s ease-out infinite both; }}
  @keyframes burst {{ 0%,52% {{ transform: scale(1); opacity: 0; }} 54% {{ opacity: .9; }} 70%,100% {{ transform: scale(2.6); opacity: 0; }} }}
  .kt {{ animation: press 3s cubic-bezier(.3,1.6,.5,1) infinite; }}
  @keyframes press {{ 0%,80%,100% {{ transform: none; }} 86% {{ transform: translateY(4px); }} }}
{''.join(css_r)}  @media (prefers-reduced-motion: reduce) {{ .rd {{ transform: none; }} .beam {{ opacity: 0; }} }}
"""
    defs = (
        f'<defs><clipPath id="pclip"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6"/></clipPath>'
        f'<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TERRA}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{TERRA}" stop-opacity=".45"/></linearGradient></defs>'
    )
    return defs + ring + back + page + seal + key + pill, css


def motif_bmd() -> tuple[str, str]:
    sx, sy = 690, 150
    srv = []
    for i in range(3):
        y = sy - 52 + i * 36
        srv.append(
            f'<rect x="{sx}" y="{y}" width="78" height="28" rx="6" class="srv"/>'
            f'<circle cx="{sx + 14}" cy="{y + 14}" r="3" class="led" style="animation-delay:{i * 0.3:.1f}s"/>'
            f'<rect x="{sx + 26}" y="{y + 12}" width="38" height="4" rx="2" class="slot"/>'
        )
    fx, fy, fw, fh = 1010, 54, 140, 192
    doc = (
        f'<path class="doc" d="M{fx} {fy + 8}a8 8 0 0 1 8-8H{fx + fw - 30}L{fx + fw} {fy + 30}V{fy + fh - 8}a8 8 0 0 1-8 8H{fx + 8}a8 8 0 0 1-8-8Z"/>'
        f'<path class="doc" d="M{fx + fw - 30} {fy}V{fy + 22}a8 8 0 0 0 8 8H{fx + fw}"/>'
    )
    n = 5
    lanes, segs, dots, css_s = [], [], [], []
    loop = 7.0
    for i in range(n):
        ey = fy + 50 + i * 26
        sxx, syy = sx + 78, sy - 38 + i * 19
        d = f"M{sxx} {syy}C{sxx + 110} {syy} {fx - 110} {ey + 5} {fx + 14} {ey + 5}"
        lanes.append(f'<path id="ln{i}" class="lane" d="{d}"/>')
        segs.append(
            f'<rect x="{fx + 16}" y="{ey}" width="{fw - 32}" height="10" rx="5" class="trk"/>'
            f'<rect x="{fx + 16}" y="{ey}" width="{fw - 32}" height="10" rx="5" class="seg s{i}"/>'
        )
        end = 38 + i * 9 + (i % 2) * 6
        css_s.append(
            f"  .s{i} {{ animation: s{i} {loop}s cubic-bezier(.4,0,.3,1) infinite both; }}\n"
            f"  @keyframes s{i} {{ 0%,4% {{ transform: scaleX(0); opacity: 1; }} {end}%,92% {{ transform: scaleX(1); opacity: 1; }} 100% {{ transform: scaleX(1); opacity: 0; }} }}\n"
        )
        for k in range(3):
            dur = 1.3 + (i % 3) * 0.25
            col = MARI if (i + k) % 2 else TERRA
            dots.append(
                f'<circle r="3" fill="{col}" class="pk"><animateMotion dur="{dur:.2f}s" begin="{k * dur / 3:.2f}s" '
                f'repeatCount="indefinite" rotate="auto"><mpath href="#ln{i}" xlink:href="#ln{i}"/></animateMotion></circle>'
            )
    ok = (
        f'<g class="ok"><circle cx="{fx + fw}" cy="{fy + fh}" r="17" fill="{TERRA}"/>'
        f'<path d="M{fx + fw - 7} {fy + fh}l5 5 9-10" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></g>'
    )
    l1 = MONO.path("5 PARTS IN PARALLEL", 10, sx, sy + 76, track=1.4)
    l2 = MONO.path("RESUMES AFTER A CRASH", 10, fx + fw / 2, fy + fh + 30, anchor="middle", track=1.4)
    css = f"""
  .srv {{ fill: #221C18; stroke: {LINE}; }}
  .slot {{ fill: {LINE}; }}
  .led {{ fill: {TEAL}; animation: led 1.1s steps(2) infinite; }}
  @keyframes led {{ 50% {{ opacity: .2; }} }}
  .lane {{ fill: none; stroke: #54463B; stroke-width: 1.4; stroke-dasharray: 3 6; animation: flow 1s linear infinite; }}
  @keyframes flow {{ to {{ stroke-dashoffset: -9; }} }}
  .doc {{ fill: none; stroke: {INK}; stroke-opacity: .5; stroke-width: 1.4; stroke-linejoin: round; }}
  .trk {{ fill: {LINE}; }}
  .seg {{ fill: url(#segg); transform-box: fill-box; transform-origin: 0 50%; }}
  .ok {{ transform-origin: {fx + fw}px {fy + fh}px; animation: ok {loop}s cubic-bezier(.3,1.7,.5,1) infinite both; }}
  @keyframes ok {{ 0%,78% {{ transform: scale(0); }} 84%,93% {{ transform: scale(1); }} 100% {{ transform: scale(0); }} }}
  .lb {{ fill: {DIM}; }}
{''.join(css_s)}  @media (prefers-reduced-motion: reduce) {{ .seg {{ transform: none; }} }}
"""
    defs = (
        f'<defs><linearGradient id="segg"><stop offset="0" stop-color="{TERRA}"/><stop offset="1" stop-color="{MARI}"/></linearGradient></defs>'
    )
    return (
        defs + "".join(lanes) + "".join(srv) + doc + "".join(segs) + "".join(dots) + ok
        + f'<path class="lb" d="{l1} {l2}"/>', css
    )


def motif_formspear() -> tuple[str, str]:
    x0, base = 684, 236
    heights = [10, 7, 9, 14, 16, 24, 30, 48, 80, 128, 104]
    bars, labels, pts = [], [], []
    loop = 7.0
    for i, h in enumerate(heights):
        g = "gd" if i <= 6 else ("gp" if i <= 8 else "gpr")
        x = x0 + i * 31
        bars.append(
            f'<rect x="{x}" y="{base - h}" width="21" height="{h}" rx="4" fill="url(#{g})" class="nps" '
            f'style="animation-delay:{i * 0.06:.2f}s"/>'
        )
        labels.append(MONO.path(str(i), 10, x + 10.5, base + 18, anchor="middle"))
        pts.append((x + 10.5, base - h - 10))
    d = f"M{pts[0][0]} {pts[0][1]}"
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        mx = (xa + xb) / 2
        d += f"C{mx} {ya} {mx} {yb} {xb} {yb}"
    line = f'<path id="npsl" class="nl" pathLength="1" d="{d}"/>'
    dot = (
        f'<g><circle r="9" fill="{INK}" opacity=".15"/><circle r="4.5" fill="{INK}"/>'
        f'<animateMotion dur="{loop}s" repeatCount="indefinite" keyPoints="0;0;1;1" keyTimes="0;.22;.5;1" calcMode="linear">'
        f'<mpath href="#npsl" xlink:href="#npsl"/></animateMotion></g>'
    )
    q = MONO.path("HOW LIKELY ARE YOU TO RECOMMEND US?", 10, x0, 40, track=1.3)
    od, od_css = odometer(SERIF, "+62", 64, 1156, 108, "o", 18, 46, loop)
    nps = MONO.path("NPS", 10, 1156, 128, anchor="end", track=2)
    css = f"""
  .nps {{ transform-box: fill-box; transform-origin: 50% 100%; animation: up {loop}s cubic-bezier(.3,1.4,.5,1) infinite both; }}
  @keyframes up {{ 0% {{ transform: scaleY(0); }} 18%,92% {{ transform: scaleY(1); }} 100% {{ transform: scaleY(0); }} }}
  .nl {{ fill: none; stroke: {INK}; stroke-opacity: .7; stroke-width: 1.5; stroke-dasharray: 1; animation: nl {loop}s ease-in-out infinite both; }}
  @keyframes nl {{ 0%,20% {{ stroke-dashoffset: 1; opacity: 1; }} 50%,92% {{ stroke-dashoffset: 0; opacity: 1; }} 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}
  .ax, .q {{ fill: {DIM}; }}
  .odx, .odc path {{ fill: {INK}; }}
{od_css}  @media (prefers-reduced-motion: reduce) {{ .nl {{ stroke-dashoffset: 0; }} }}
"""
    defs = (
        "<defs>"
        + "".join(
            f'<linearGradient id="{n}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c}"/>'
            f'<stop offset="1" stop-color="{c}" stop-opacity=".35"/></linearGradient>'
            for n, c in (("gd", TERRA), ("gp", MARI), ("gpr", TEAL))
        )
        + "</defs>"
    )
    return (
        defs + f'<path class="q" d="{q}"/>' + "".join(bars) + f'<path class="ax" d="{" ".join(labels)}"/>'
        + line + dot + od + f'<path class="q" d="{nps}"/>', css
    )


def signature_path(x0: float, y0: float, w: float, loops: int, a: float, b: float, tilt: float) -> str:
    """A looping, cursive-looking scribble (a prolate trochoid with a flourish)."""
    pts = []
    n = 220
    T = loops * 2 * math.pi
    for i in range(n + 1):
        t = i / n * T
        x = a * t - b * math.sin(t)
        y = -b * math.cos(t) * (0.55 + 0.45 * abs(math.sin(t / (2 * loops) * 3.1)))
        pts.append((x - 0.45 * y, y))
    xs = [p[0] for p in pts]
    sx = w / (max(xs) - min(xs))
    out = []
    for i, (x, y) in enumerate(pts):
        X = x0 + (x - min(xs)) * sx
        Y = y0 + y + tilt * (X - x0) / w
        out.append(f"{'M' if i == 0 else 'L'}{X:.1f} {Y:.1f}")
    X = x0 + w
    out.append(f"Q{X + 14:.1f} {y0 + 16:.1f} {X - w * 0.6:.1f} {y0 + 12:.1f}")
    return "".join(out)


def motif_settlr() -> tuple[str, str]:
    y = 92
    xs = [684, 804, 924]
    loop = 7.0
    hashes = ["0x8a2f", "0xb73d", "0x41c9"]
    chain = f'<path id="ch" class="chl" d="M{xs[0] - 20} {y}H1090"/>'
    blocks = []
    for i, x in enumerate(xs):
        p = 8 + i * 12
        blocks.append(
            f'<g class="blk k{i}"><rect x="{x}" y="{y - 46}" width="92" height="92" rx="14" class="bx"/>'
            f'<path class="hs" d="{MONO.path(hashes[i], 10, x + 14, y - 22)}"/>'
            f'<rect x="{x + 14}" y="{y - 8}" width="60" height="5" rx="2.5" class="bl"/>'
            f'<rect x="{x + 14}" y="{y + 4}" width="44" height="5" rx="2.5" class="bl"/>'
            f'<rect x="{x + 14}" y="{y + 16}" width="52" height="5" rx="2.5" class="bl"/></g>'
        )
    css_k = "".join(
        f"  .k{i} .bx {{ animation: lit{i} {loop}s ease-out infinite both; }}\n"
        f"  @keyframes lit{i} {{ 0%,{8 + i * 12}% {{ stroke: {LINE}; }} {12 + i * 12}%,90% {{ stroke: {TERRA}; }} 100% {{ stroke: {LINE}; }} }}\n"
        for i in range(3)
    )
    packet = (
        f'<g><circle r="10" fill="{TERRA}" opacity=".25"/><circle r="5" fill="{MARI}"/>'
        f'<animateMotion dur="{loop}s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.5;1" calcMode="linear">'
        f'<mpath href="#ch" xlink:href="#ch"/></animateMotion></g>'
    )
    lx, ly = 1110, y
    lock = (
        f'<g class="lk"><path class="sh" d="M{lx - 11} {ly - 4}v-10a11 11 0 0 1 22 0v10" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>'
        f'<rect x="{lx - 18}" y="{ly - 4}" width="36" height="30" rx="7" class="lb"/>'
        f'<circle cx="{lx}" cy="{ly + 10}" r="3.5" fill="{BG}"/></g>'
    )
    sigs = []
    for i, (sx, who, col, lo, a, b, tilt) in enumerate(
        [(700, "TENANT", TEAL, 4, 4.2, 11, -8), (944, "OWNER", MARI, 3, 5.0, 12, -12)]
    ):
        d = signature_path(sx, 214, 156, lo, a, b, tilt)
        sigs.append(
            f'<path class="sig sg{i}" pathLength="1" d="{d}"/>'
            f'<line x1="{sx - 6}" y1="240" x2="{sx + 170}" y2="240" class="sln"/>'
            f'<path class="who" d="{MONO.path(who, 9.5, sx - 6, 258, track=1.6)}"/>'
            f'<g class="ck ck{i}"><circle cx="{sx + MONO.width(who, 9.5, 1.6) + 8}" cy="254.5" r="8" fill="{col}"/>'
            f'<path d="M{sx + MONO.width(who, 9.5, 1.6) + 4} 254.5l2.6 2.6 5.4-6" fill="none" stroke="{BG}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></g>'
        )
    css = f"""
  .chl {{ stroke: {LINE}; stroke-width: 2; }}
  .bx {{ fill: #1F1A16; stroke: {LINE}; stroke-width: 1.5; }}
  .bl {{ fill: {INK}; opacity: .22; }}
  .hs {{ fill: {MARI}; opacity: .85; }}
  .lb {{ fill: #2C2520; animation: lb {loop}s ease-out infinite both; }}
  @keyframes lb {{ 0%,48% {{ fill: #2C2520; }} 52%,90% {{ fill: {TERRA}; }} 100% {{ fill: #2C2520; }} }}
  .sh {{ animation: sh {loop}s cubic-bezier(.3,1.6,.5,1) infinite both; }}
  @keyframes sh {{ 0%,46% {{ transform: translateY(-9px); }} 52%,92% {{ transform: none; }} 100% {{ transform: translateY(-9px); }} }}
  .sig {{ fill: none; stroke: {INK}; stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1; }}
  .sg0 {{ animation: sig0 {loop}s cubic-bezier(.5,0,.4,1) infinite both; }}
  .sg1 {{ animation: sig1 {loop}s cubic-bezier(.5,0,.4,1) infinite both; }}
  @keyframes sig0 {{ 0%,52% {{ stroke-dashoffset: 1; opacity: 1; }} 66%,93% {{ stroke-dashoffset: 0; opacity: 1; }} 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}
  @keyframes sig1 {{ 0%,64% {{ stroke-dashoffset: 1; opacity: 1; }} 78%,93% {{ stroke-dashoffset: 0; opacity: 1; }} 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}
  .sln {{ stroke: {LINE}; }}
  .who {{ fill: {DIM}; }}
  .ck {{ transform-box: fill-box; transform-origin: center; }}
  .ck0 {{ animation: ck0 {loop}s cubic-bezier(.3,1.7,.5,1) infinite both; }}
  .ck1 {{ animation: ck1 {loop}s cubic-bezier(.3,1.7,.5,1) infinite both; }}
  @keyframes ck0 {{ 0%,66% {{ transform: scale(0); }} 71%,93% {{ transform: scale(1); }} 100% {{ transform: scale(0); }} }}
  @keyframes ck1 {{ 0%,78% {{ transform: scale(0); }} 83%,93% {{ transform: scale(1); }} 100% {{ transform: scale(0); }} }}
{css_k}  @media (prefers-reduced-motion: reduce) {{ .sig {{ stroke-dashoffset: 0; }} .ck {{ transform: none; }} }}
"""
    return chain + packet + "".join(blocks) + lock + "".join(sigs), css


def motif_sportshawk() -> tuple[str, str]:
    hx, hy = 760, 150  # hip
    loop = 2.6
    ground = 254

    def leg(cls: str, extra: str = "") -> str:
        return (
            f'<g class="thigh {cls}" {extra}><line x1="{hx}" y1="{hy}" x2="{hx}" y2="{hy + 50}" class="bn"/>'
            f'<g class="shin"><line x1="{hx}" y1="{hy + 50}" x2="{hx}" y2="{hy + 98}" class="bn"/>'
            f'<circle cx="{hx}" cy="{hy + 98}" r="4.5" class="kp"/></g>'
            f'<circle cx="{hx}" cy="{hy + 50}" r="4.5" class="kp"/></g>'
        )

    ghosts = "".join(leg(f"gh gh{i}", f'style="opacity:{o};animation-delay:{d}s"') for i, (o, d) in enumerate([(0.28, 0.05), (0.16, 0.1), (0.08, 0.15)]))
    nx, ny = hx + 6, hy - 62
    body = (
        f'<line x1="{hx}" y1="{hy}" x2="{nx}" y2="{ny}" class="bn"/>'
        f'<circle cx="{nx + 3}" cy="{ny - 22}" r="14" class="hd"/>'
        # standing leg
        f'<path d="M{hx} {hy}L{hx - 10} {hy + 50}L{hx - 14} {hy + 98}" class="bn" fill="none"/>'
        f'<circle cx="{hx - 10}" cy="{hy + 50}" r="4.5" class="kp"/><circle cx="{hx - 14}" cy="{hy + 98}" r="4.5" class="kp"/>'
        # arms
        f'<g class="arm a1"><path d="M{nx} {ny + 6}l-26 22l-8 28" class="bn" fill="none"/><circle cx="{nx - 26}" cy="{ny + 28}" r="4.5" class="kp"/><circle cx="{nx - 34}" cy="{ny + 56}" r="4.5" class="kp"/></g>'
        f'<g class="arm a2"><path d="M{nx} {ny + 6}l28 16l20 -14" class="bn" fill="none"/><circle cx="{nx + 28}" cy="{ny + 22}" r="4.5" class="kp"/><circle cx="{nx + 48}" cy="{ny + 8}" r="4.5" class="kp"/></g>'
        f'<circle cx="{nx}" cy="{ny + 6}" r="4.5" class="kp"/><circle cx="{hx}" cy="{hy}" r="5" class="kp"/>'
    )
    bx, by = 822, ground - 11
    ball = (
        f'<path class="trail" pathLength="1" d="M{bx} {by}Q{bx + 80} {by - 175} {bx + 170} {by - 140}"/>'
        f'<g class="ballw"><g><circle cx="{bx}" cy="{by}" r="11" fill="{MARI}"/>'
        f'<path class="pent" d="M{bx} {by - 5}l4.8 3.5-1.8 5.6h-6l-1.8-5.6z" fill="{BG}"/>'
        f'<animateMotion dur="{loop}s" repeatCount="indefinite" keyPoints="0;0;1;1" keyTimes="0;.5;.82;1" calcMode="spline" '
        f'keySplines="0 0 1 1;.2 .6 .3 1;0 0 1 1" path="M0 0Q80 -175 170 -140"/></g></g>'
    )
    bb_x0, bb_y0, bb_x1, bb_y1 = 700, 50, 860, ground + 4
    c = 16
    brackets = (
        f'<path class="bb" d="M{bb_x0} {bb_y0 + c}V{bb_y0}H{bb_x0 + c}M{bb_x1 - c} {bb_y0}H{bb_x1}V{bb_y0 + c}'
        f'M{bb_x1} {bb_y1 - c}V{bb_y1}H{bb_x1 - c}M{bb_x0 + c} {bb_y1}H{bb_x0}V{bb_y1 - c}"/>'
        f'<path class="bbl" d="{MONO.path("PLAYER 07 · 0.94", 9.5, bb_x0, bb_y0 - 9, track=1.2)}"/>'
    )
    rx, ry, rr = 1090, 140, 52
    od, od_css = odometer(SERIF, "87", 44, rx + 23, ry + 15, "s", 30, 62, loop * 2, spins=0)
    ring = (
        f'<circle cx="{rx}" cy="{ry}" r="{rr}" class="rt"/>'
        f'<path class="rg" pathLength="1" d="{circle_d_top(rx, ry, rr)}"/>' + od
        + f'<path class="rl" d="{MONO.path("AGILITY", 10, rx, ry + rr + 26, anchor="middle", track=2)}"/>'
    )
    gl = f'<line x1="{MX + 20}" y1="{ground + 4}" x2="1000" y2="{ground + 4}" class="gd"/>'
    css = f"""
  .bn {{ stroke: {INK}; stroke-opacity: .75; stroke-width: 2.6; stroke-linecap: round; stroke-linejoin: round; }}
  .kp {{ fill: {TEAL}; }}
  .hd {{ fill: none; stroke: {INK}; stroke-opacity: .75; stroke-width: 2.6; }}
  .thigh {{ transform-origin: {hx}px {hy}px; animation: thigh {loop}s cubic-bezier(.5,0,.25,1) infinite both; }}
  .shin {{ transform-origin: {hx}px {hy + 50}px; animation: shin {loop}s cubic-bezier(.5,0,.25,1) infinite both; }}
  .gh .shin {{ animation-delay: inherit; }}
  .gh .kp {{ display: none; }}
  @keyframes thigh {{ 0%,100% {{ transform: rotate(8deg); }} 30% {{ transform: rotate(38deg); }} 52% {{ transform: rotate(-58deg); }} 66% {{ transform: rotate(-70deg); }} 84% {{ transform: rotate(-10deg); }} }}
  @keyframes shin {{ 0%,100% {{ transform: rotate(0); }} 30% {{ transform: rotate(78deg); }} 50% {{ transform: rotate(12deg); }} 60% {{ transform: rotate(-4deg); }} 84% {{ transform: rotate(20deg); }} }}
  .arm {{ transform-origin: {nx}px {ny + 6}px; animation: arm {loop}s ease-in-out infinite both; }}
  .a2 {{ animation-name: arm2; }}
  @keyframes arm {{ 0%,100% {{ transform: rotate(0); }} 52% {{ transform: rotate(-26deg); }} }}
  @keyframes arm2 {{ 0%,100% {{ transform: rotate(0); }} 52% {{ transform: rotate(22deg); }} }}
  .trail {{ fill: none; stroke: {MARI}; stroke-width: 2; stroke-linecap: round; stroke-dasharray: 1; opacity: .5;
        animation: trail {loop}s ease-out infinite both; }}
  @keyframes trail {{ 0%,50% {{ stroke-dashoffset: 1; opacity: .5; }} 82% {{ stroke-dashoffset: 0; opacity: .5; }} 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}
  .ballw {{ animation: ballw {loop}s linear infinite both; }}
  @keyframes ballw {{ 0%,84% {{ opacity: 1; }} 88%,96% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
  .pent {{ transform-box: fill-box; transform-origin: center; animation: rot .5s linear infinite; }}
  @keyframes rot {{ to {{ transform: rotate(360deg); }} }}
  .bb {{ fill: none; stroke: {TEAL}; stroke-width: 2; animation: jit 1.3s steps(3) infinite; }}
  .bbl {{ fill: {TEAL}; animation: jit 1.3s steps(3) infinite; }}
  @keyframes jit {{ 33% {{ transform: translate(2px,-1px); }} 66% {{ transform: translate(-1px,2px); }} }}
  .rt {{ fill: none; stroke: {LINE}; stroke-width: 6; }}
  .rg {{ fill: none; stroke: {TEAL}; stroke-width: 6; stroke-linecap: round; stroke-dasharray: 1; stroke-dashoffset: .13;
        animation: rg {loop * 2}s cubic-bezier(.2,.8,.2,1) infinite both; }}
  @keyframes rg {{ 0%,30% {{ stroke-dashoffset: 1; }} 62%,94% {{ stroke-dashoffset: .13; }} 100% {{ stroke-dashoffset: 1; }} }}
  .odx, .odc path {{ fill: {INK}; }}
  .rl {{ fill: {DIM}; }}
  .gd {{ stroke: {LINE}; stroke-width: 2; }}
{od_css}"""
    return gl + brackets + ghosts + body + leg("main") + ball + ring, css


def motif_lawflow() -> tuple[str, str]:
    x0, y0 = 684, 70
    hearings = [3, 9, 12, 17, 23, 26, 31]
    loop = 8.0
    cells, css_h = [], []
    for i in range(35):
        r, c = divmod(i, 7)
        x, y = x0 + c * 32, y0 + r * 32
        if i in hearings:
            k = hearings.index(i)
            p = 4 + k * 8
            cells.append(
                f'<rect x="{x}" y="{y}" width="26" height="26" rx="6" class="hr h{k}"/>'
                f'<rect x="{x}" y="{y}" width="26" height="26" rx="6" class="hp h{k}p"/>'
            )
            css_h.append(
                f"  .h{k} {{ animation: h{k} {loop}s ease-out infinite both; }}\n"
                f"  @keyframes h{k} {{ 0%,{p}% {{ fill: #261F1A; }} {p + 2}%,90% {{ fill: {TERRA}; }} 100% {{ fill: #261F1A; }} }}\n"
                f"  .h{k}p {{ animation: hp{k} {loop}s ease-out infinite both; }}\n"
                f"  @keyframes hp{k} {{ 0%,{p}% {{ opacity: 0; transform: scale(1); }} {p + 1}% {{ opacity: .9; }} {p + 10}%,100% {{ opacity: 0; transform: scale(2); }} }}\n"
            )
        else:
            cells.append(f'<rect x="{x}" y="{y}" width="26" height="26" rx="6" fill="#261F1A"/>')
    days = "".join(
        f'<path class="dw" d="{MONO.path(d, 9.5, x0 + 13 + i * 32, y0 - 12, anchor="middle")}"/>' for i, d in enumerate("MTWTFSS")
    )
    mon = MONO.path("DECEMBER", 10, x0, y0 - 34, track=2.4)
    sx, sy = 1050, 64
    pan = lambda px, cls: (
        f'<g class="pan {cls}"><path d="M{px} {sy}L{px - 26} {sy + 52}M{px} {sy}L{px + 26} {sy + 52}" class="str"/>'
        f'<path d="M{px - 30} {sy + 52}h60a30 14 0 0 1-60 0z" class="bowl"/></g>'
    )
    scales = (
        f'<path d="M{sx} {sy - 14}V{sy + 108}M{sx - 34} {sy + 112}h68" class="pil"/>'
        f'<circle cx="{sx}" cy="{sy - 18}" r="6" class="knob"/>'
        f'<g class="beamg"><path d="M{sx - 70} {sy}H{sx + 70}" class="pil"/>{pan(sx - 70, "pl")}{pan(sx + 70, "pr")}</g>'
    )
    nx, ny = 940, 202
    note = (
        f'<g class="note"><rect x="{nx}" y="{ny}" width="220" height="56" rx="14" fill="#2C2520" stroke="{LINE}"/>'
        f'<circle cx="{nx + 26}" cy="{ny + 28}" r="13" fill="{TERRA}"/>'
        f'<path d="M{nx + 20} {ny + 32}h12l-2-3v-5a4 4 0 0 0-8 0v5zM{nx + 24.5} {ny + 34}a1.5 1.5 0 0 0 3 0" fill="{INK}"/>'
        f'<path d="{SANS.path("Hearing tomorrow, 10:30", 13.5, nx + 50, ny + 25)}" fill="{INK}"/>'
        f'<path d="{MONO.path("COURT 4 · BHUBANESWAR", 9, nx + 50, ny + 42, track=1)}" fill="{DIM}"/></g>'
    )
    css = f"""
  .hr {{ fill: #261F1A; }}
  .hp {{ fill: none; stroke: {TERRA}; stroke-width: 2; transform-box: fill-box; transform-origin: center; }}
  .dw {{ fill: {DIM}; }}
  .pil {{ stroke: {INK}; stroke-opacity: .7; stroke-width: 2.4; stroke-linecap: round; fill: none; }}
  .knob {{ fill: {MARI}; }}
  .str {{ stroke: {INK}; stroke-opacity: .4; stroke-width: 1.2; }}
  .bowl {{ fill: {MARI}; opacity: .9; }}
  .beamg {{ transform-origin: {sx}px {sy}px; animation: tilt 4s ease-in-out infinite alternate; }}
  .pl {{ transform-origin: {sx - 70}px {sy}px; animation: untilt 4s ease-in-out infinite alternate; }}
  .pr {{ transform-origin: {sx + 70}px {sy}px; animation: untilt 4s ease-in-out infinite alternate; }}
  @keyframes tilt {{ from {{ transform: rotate(-7deg); }} to {{ transform: rotate(7deg); }} }}
  @keyframes untilt {{ from {{ transform: rotate(7deg); }} to {{ transform: rotate(-7deg); }} }}
  .note {{ animation: note {loop}s cubic-bezier(.2,.9,.2,1) infinite both; }}
  @keyframes note {{ 0%,40% {{ opacity: 0; transform: translateX(60px); }} 46%,90% {{ opacity: 1; transform: none; }} 96%,100% {{ opacity: 0; transform: translateY(8px); }} }}
  .mon {{ fill: {BODY}; }}
{''.join(css_h)}  @media (prefers-reduced-motion: reduce) {{ .hr {{ fill: {TERRA}; }} .note {{ opacity: 1; }} }}
"""
    return f'<path class="mon" d="{mon}"/>' + days + "".join(cells) + scales + note, css


PROJECTS = [
    ("vaani", "01", "Vaani", "An AI front desk for clinics and salons. Answers calls and WhatsApp, and books appointments in Odia, Hindi or English.", "Python · LangGraph · FastAPI · MongoDB", motif_vaani, TERRA),
    ("octapdf", "02", "OctaPDF", "A PDF workspace that runs on your own machine. Edit, split, redact and convert, and your files never leave.", "Java 21 · Spring Boot · Docker", motif_octapdf, TERRA),
    ("bmd", "03", "Black Marlin", "A free download manager for Windows, Linux and macOS. Splits files into parallel parts and picks up where it left off.", "Rust · Tokio", motif_bmd, MARI),
    ("formspear", "04", "Formspear", "Forms, surveys and feedback with real analytics. Plain Node.js, no framework, Postgres underneath.", "Node.js · PostgreSQL · Redis · BullMQ", motif_formspear, TEAL),
    ("settlr", "05", "Settlr", "Renting in Delhi without blind trust. Owner-verified listings, and every rent or deposit decision needs both signatures.", "FastAPI · Next.js · Postgres · Expo", motif_settlr, MARI),
    ("sportshawk", "06", "SportsHawk", "Free football training for kids outside the big cities. Film a drill on any phone and get scored on the phone itself.", "React · MediaPipe · On-device ML", motif_sportshawk, TEAL),
    ("lawflow", "07", "LawFlow", "A practice manager for Indian advocates. Cases, hearings, clients and documents, at the desk and in court.", "Rust · Tauri · Expo · SQLite", motif_lawflow, TERRA),
]


# --------------------------------------------------------------------------
# Marquee and signature
# --------------------------------------------------------------------------


def star(cx: float, cy: float, r: float) -> str:
    i = r * 0.28
    return (
        f"M{_num(cx)} {_num(cy - r)}Q{_num(cx + i)} {_num(cy - i)} {_num(cx + r)} {_num(cy)}"
        f"Q{_num(cx + i)} {_num(cy + i)} {_num(cx)} {_num(cy + r)}Q{_num(cx - i)} {_num(cy + i)} {_num(cx - r)} {_num(cy)}"
        f"Q{_num(cx - i)} {_num(cy - i)} {_num(cx)} {_num(cy - r)}Z"
    )


def marquee() -> str:
    W, H = 1200, 170
    words = ["Rust", "Java", "Python", "TypeScript", "Postgres", "Next.js", "Flutter", "Tauri"]
    size, gap = 62, 34

    def row1(x0: float) -> tuple[str, float]:
        out, x = [], x0
        for i, w in enumerate(words):
            cls = "wf" if i % 2 == 0 else "wo"
            out.append(f'<path class="{cls}" d="{SERIF.path(w, size, x, 86)}"/>')
            x += SERIF.width(w, size) + gap
            out.append(f'<path class="st" d="{star(x, 66, 9)}"/>')
            x += gap
        return "".join(out), x - x0

    one, w1 = row1(0)
    reps1 = math.ceil(W / w1) + 1
    r1 = "".join(f'<g transform="translate({_num(k * w1)} 0)">{one}</g>' for k in range(reps1))

    small = "TOKIO · SPRING BOOT · FASTAPI · LANGGRAPH · EXPO · DOCKER · REDIS · MONGODB · SUPABASE · CANVAS 2D · "
    sw = MONO.width(small, 12, 2.2) + 2.2
    two = MONO.path(small, 12, 0, 136, track=2.2)
    reps2 = math.ceil(W / sw) + 1
    r2 = "".join(f'<path class="sm" transform="translate({_num(k * sw)} 0)" d="{two}"/>' for k in range(reps2))
    frame, frame_css = card_frame(W, H, TERRA, 14)
    css = f"""
  .bg {{ fill: {CARD}; }}
  .wf {{ fill: {INK}; }}
  .wo {{ fill: none; stroke: {INK}; stroke-opacity: .7; stroke-width: 1; }}
  .st {{ fill: {TERRA}; transform-box: fill-box; transform-origin: center; animation: tw 3s ease-in-out infinite; }}
  @keyframes tw {{ 0%,100% {{ transform: rotate(0) scale(1); }} 50% {{ transform: rotate(90deg) scale(.7); }} }}
  .sm {{ fill: {DIM}; }}
  .r1 {{ animation: m1 {w1 / 38:.1f}s linear infinite; }}
  .r2 {{ animation: m2 {sw / 30:.1f}s linear infinite; }}
  @keyframes m1 {{ from {{ transform: translateX(0); }} to {{ transform: translateX({-w1:.1f}px); }} }}
  @keyframes m2 {{ from {{ transform: translateX({-sw:.1f}px); }} to {{ transform: translateX(0); }} }}
{frame_css}"""
    body = f"""<defs>{grain_defs()}
  <linearGradient id="fade"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".12" stop-color="#fff"/>
    <stop offset=".88" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <clipPath id="c"><rect width="{W}" height="{H}" rx="20"/></clipPath></defs>
<g clip-path="url(#c)">
  <rect class="bg" width="{W}" height="{H}"/>
  <g mask="url(#m)"><g class="r1">{r1}</g><g class="r2">{r2}</g></g>
  <rect width="{W}" height="{H}" fill="url(#grain)" opacity=".5"/>
</g>
{frame}"""
    return svg(W, H, body, css, "Rust, Java, Python, TypeScript, Postgres, Next.js, Flutter, Tauri.")


def footer() -> str:
    W, H = 1200, 240
    hz = 168
    sw = SERIF_IT.width("Subham", 88)
    sig = SERIF_IT.glyphs("Subham", 88, (W - sw) / 2, 140)
    paths = "".join(
        f'<path d="{d}" pathLength="1" class="sg" style="animation-delay:{0.9 + i * 0.16:.2f}s"/>' for i, (d, _) in enumerate(sig)
    )
    rays = "".join(
        f'<line x1="{_num(polar(600, hz, 96, a)[0])}" y1="{_num(polar(600, hz, 96, a)[1])}" '
        f'x2="{_num(polar(600, hz, 96 + (40 if k % 2 else 22), a)[0])}" y2="{_num(polar(600, hz, 96 + (40 if k % 2 else 22), a)[1])}"/>'
        for k, a in enumerate(range(-90, 91, 12))
    )
    line = MONO.path("MADE IN BHUBANESWAR", 11, W / 2, hz + 40, anchor="middle", track=3.2)
    ux0, ux1 = (W - sw) / 2 + 10, (W + sw) / 2 + 6
    under = f'<path class="u" pathLength="1" d="M{_num(ux0)} 160C{_num(ux0 + 80)} 151 {_num(ux1 - 60)} 154 {_num(ux1)} 147"/>'
    frame, frame_css = card_frame(W, H, MARI, 16)
    css = f"""
  .bg {{ fill: {CARD}; }}
  .sunw {{ animation: sunup 3.2s cubic-bezier(.2,.8,.2,1) both; }}
  @keyframes sunup {{ from {{ transform: translateY(70px); }} to {{ transform: none; }} }}
  .rays {{ transform-origin: 600px {hz}px; animation: spin 60s linear infinite; }}
  .rays line {{ stroke: {MARI}; stroke-width: 1.4; stroke-linecap: round; opacity: .35; }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  .hz {{ stroke: {LINE}; stroke-width: 1.5; }}
  .sg {{ fill: {INK}; stroke: {INK}; stroke-width: 1; stroke-dasharray: 1; fill-opacity: 1; stroke-opacity: 0;
        animation: draw 3s cubic-bezier(.6,.05,.3,1) both; }}
  @keyframes draw {{ 0% {{ stroke-dashoffset: 1; fill-opacity: 0; stroke-opacity: 1; }}
    60% {{ stroke-dashoffset: 0; fill-opacity: 0; stroke-opacity: 1; }} 100% {{ stroke-dashoffset: 0; fill-opacity: 1; stroke-opacity: 0; }} }}
  .ml {{ fill: {DIM}; animation: in 1.5s ease-out 3s both; }}
  .u {{ stroke: {TERRA}; stroke-width: 2.2; stroke-linecap: round; stroke-dasharray: 1; fill: none;
       animation: under 1.4s cubic-bezier(.6,.05,.3,1) 2.4s both; }}
  @keyframes under {{ from {{ stroke-dashoffset: 1; }} to {{ stroke-dashoffset: 0; }} }}
  @keyframes in {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
{frame_css}"""
    body = f"""<defs>{grain_defs()}
  <radialGradient id="sun" cx="600" cy="{hz}" r="90" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{MARI}" stop-opacity=".55"/>
    <stop offset=".7" stop-color="{TERRA}" stop-opacity=".28"/><stop offset="1" stop-color="{TERRA}" stop-opacity="0"/></radialGradient>
  <clipPath id="sky"><rect width="{W}" height="{hz}"/></clipPath>
  <clipPath id="c"><rect width="{W}" height="{H}" rx="20"/></clipPath></defs>
<g clip-path="url(#c)">
  <rect class="bg" width="{W}" height="{H}"/>
  <g clip-path="url(#sky)"><g class="sunw"><circle cx="600" cy="{hz}" r="90" fill="url(#sun)"/><g class="rays">{rays}</g></g></g>
  <line class="hz" x1="360" y1="{hz}" x2="840" y2="{hz}"/>
  {paths}{under}<path class="ml" d="{line}"/>
  <rect width="{W}" height="{H}" fill="url(#grain)" opacity=".5"/>
</g>
{frame}"""
    return svg(W, H, body, css, "Subham. Made in Bhubaneswar.")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "hero.svg").write_text(hero())
    for slug, idx, name, tagline, stack, motif_fn, accent in PROJECTS:
        motif, mcss = motif_fn()
        (OUT / f"{slug}.svg").write_text(card(idx, name, tagline, stack, motif, mcss, accent))
    (OUT / "stack.svg").write_text(marquee())
    (OUT / "signature.svg").write_text(footer())
    for p in sorted(OUT.glob("*.svg")):
        print(f"{p.relative_to(ROOT)}  {p.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
