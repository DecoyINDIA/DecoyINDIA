"""Draws assets/stats.svg from live GitHub data, in the same style as the rest
of the profile. Runs daily from .github/workflows/stats.yml.

    GITHUB_TOKEN=... python scripts/stats.py      # live data
    python scripts/stats.py --sample              # offline preview with fake data
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import urllib.request

from build import (
    BODY, CARD, DIM, INK, LINE, MARI, MONO, OUT, SANS, SERIF, TEAL, TERRA,
    _num, card_frame, grain_defs, svg,
)

LOGIN = os.environ.get("STATS_LOGIN", "DecoyINDIA")

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes { languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
    }
  }
}
"""

LEVELS = ["#241E1A", "#5C2B18", "#923B1B", TERRA, MARI]
LANG_COLORS = [TERRA, MARI, TEAL, "#C9B8A6", "#9B5B7A", "#5E5249"]


# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------


def fetch(token: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if payload.get("errors"):
        raise SystemExit(f"GitHub API error: {payload['errors']}")
    return payload["data"]["user"]


def sample() -> dict:
    """Plausible fake data, only for previewing the design offline."""
    rnd = random.Random(3)
    today = dt.date.today()
    start = today - dt.timedelta(days=364 + (today.weekday() + 1) % 7)
    weeks, week = [], []
    for i in range((today - start).days + 1):
        d = start + dt.timedelta(days=i)
        active = d > today - dt.timedelta(days=270)
        c = 0
        if active and rnd.random() < 0.72:
            c = int(rnd.expovariate(1 / 7)) + 1
        week.append({"date": d.isoformat(), "contributionCount": c})
        if len(week) == 7:
            weeks.append({"contributionDays": week})
            week = []
    if week:
        weeks.append({"contributionDays": week})
    total = sum(x["contributionCount"] for w in weeks for x in w["contributionDays"])
    langs = [("TypeScript", 41), ("Python", 24), ("Java", 13), ("Rust", 9), ("JavaScript", 8), ("Dart", 5)]
    return {
        "contributionsCollection": {
            "totalCommitContributions": int(total * 0.82),
            "contributionCalendar": {"totalContributions": total, "weeks": weeks},
        },
        "repositories": {
            "totalCount": 13,
            "nodes": [{"languages": {"edges": [{"size": s * 1000, "node": {"name": n}} for n, s in langs]}}],
        },
    }


def summarize(user: dict) -> dict:
    cal = user["contributionsCollection"]["contributionCalendar"]
    days = [(dt.date.fromisoformat(d["date"]), d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
    longest = run = 0
    for _, c in days:
        run = run + 1 if c else 0
        longest = max(longest, run)
    # current streak: allow today to be empty (the day isn't over yet)
    current = 0
    for i, (_, c) in enumerate(reversed(days)):
        if c:
            current += 1
        elif i > 0:
            break
    busiest = max(days, key=lambda x: x[1])
    sizes: dict[str, int] = {}
    for repo in user["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            sizes[e["node"]["name"]] = sizes.get(e["node"]["name"], 0) + e["size"]
    total_size = sum(sizes.values()) or 1
    langs = sorted(sizes.items(), key=lambda x: -x[1])
    top = [(n, s / total_size) for n, s in langs[:5]]
    rest = 1 - sum(p for _, p in top)
    if rest > 0.005:
        top.append(("Other", rest))
    return {
        "days": days,
        "total": cal["totalContributions"],
        "commits": user["contributionsCollection"]["totalCommitContributions"],
        "active": sum(1 for _, c in days if c),
        "longest": longest,
        "current": current,
        "busiest": busiest,
        "repos": user["repositories"]["totalCount"],
        "langs": top,
    }


# --------------------------------------------------------------------------
# Drawing
# --------------------------------------------------------------------------


def counter(value: int, size: float, x: float, base: float, name: str, delay: float) -> tuple[str, str, float]:
    """A number that rolls up into place once. Returns (svg, css, width)."""
    text = f"{value:,}"
    lh = size * 1.0
    colw = max(SERIF.width(str(d), size) for d in range(10))
    comma = SERIF.width(",", size)
    width = sum(comma if ch == "," else colw for ch in text)
    out, css = [], []
    cx = x
    digits_seen = 0
    n_digits = sum(ch.isdigit() for ch in text)
    for ch in text:
        if ch == ",":
            out.append(f'<path class="cn" d="{SERIF.path(",", size, cx, base)}"/>')
            cx += comma
            continue
        place = n_digits - 1 - digits_seen  # 0 = ones column
        digits_seen += 1
        seq = [str(d) for d in range(10)] * min(place, 1) + [str(d) for d in range(int(ch) + 1)]
        final = (len(seq) - 1) * lh
        cid = f"{name}{place}"
        glyphs = "".join(
            f'<path d="{SERIF.path(dg, size, cx + colw / 2, base + k * lh, anchor="middle")}"/>' for k, dg in enumerate(seq)
        )
        out.append(
            f'<clipPath id="k{cid}"><rect x="{_num(cx - 2)}" y="{_num(base - size * 0.76)}" width="{_num(colw + 4)}" height="{_num(size * 0.8)}"/></clipPath>'
            f'<g clip-path="url(#k{cid})"><g class="cn r{cid}" style="transform:translateY({-final:.1f}px)">{glyphs}</g></g>'
        )
        css.append(
            f"  .r{cid} {{ animation: r{cid} {1.4 + place * 0.35:.2f}s cubic-bezier(.2,.8,.15,1) {delay:.2f}s both; }}\n"
            f"  @keyframes r{cid} {{ from {{ transform: translateY(0); }} to {{ transform: translateY({-final:.1f}px); }} }}\n"
        )
        cx += colw
    return "".join(out), "".join(css), width


def render(s: dict, updated: dt.date) -> str:
    W, H = 1200, 420
    parts, css = [], []

    # header
    parts.append(f'<rect x="56" y="40" width="28" height="2" fill="{TERRA}"/>')
    parts.append(f'<path class="lb" d="{MONO.path("GITHUB, THE LAST 12 MONTHS", 11, 56, 66, track=2.4)}"/>')
    upd = f"UPDATED {updated.strftime('%d %b %Y').upper()}"
    uw = MONO.width(upd, 10, 2)
    parts.append(
        f'<circle class="live" cx="{_num(1144 - uw - 14)}" cy="62" r="3.5"/>'
        f'<circle class="liveh" cx="{_num(1144 - uw - 14)}" cy="62" r="3.5"/>'
        f'<path class="lb" d="{MONO.path(upd, 10, 1144, 66, anchor="end", track=2)}"/>'
    )

    # big numbers
    tiles = [
        (s["total"], "CONTRIBUTIONS"),
        (s["commits"], "COMMITS"),
        (s["active"], "DAYS I SHIPPED SOMETHING"),
        (s["longest"], "LONGEST STREAK, DAYS"),
    ]
    for i, (val, label) in enumerate(tiles):
        x = 56 + i * 272
        svg_n, css_n, _ = counter(val, 74, x, 160, f"t{i}", 0.3 + i * 0.18)
        parts.append(svg_n)
        css.append(css_n)
        parts.append(f'<path class="tl" style="animation-delay:{0.5 + i * 0.18:.2f}s" d="{MONO.path(label, 10, x + 2, 190, track=2)}"/>')

    # heatmap
    hx, hy, pitch, cell = 56, 254, 16, 12
    days = s["days"]
    first = days[0][0]
    offset = (first.weekday() + 1) % 7  # GitHub weeks start on Sunday
    nz = sorted(c for _, c in days if c)
    q = [nz[int(len(nz) * f)] for f in (0.25, 0.5, 0.8)] if nz else [1, 2, 3]

    def level(c: int) -> int:
        if c == 0:
            return 0
        return 1 + sum(c > t for t in q)

    cells, months = [], []
    last_month, last_col = None, -9
    for i, (d, c) in enumerate(days):
        col, row = divmod(i + offset, 7)
        x, y = hx + col * pitch, hy + row * pitch
        lv = level(c)
        if d.month != last_month and row == 0:
            if col - last_col >= 3 and col < 51:
                months.append(f'<path class="mo" d="{MONO.path(d.strftime("%b").upper(), 9.5, x, hy - 12, track=1.4)}"/>')
                last_col = col
            last_month = d.month
        appear = 0.6 + col * 0.016 + row * 0.03
        cls = "c on" if lv else "c"
        anim = f"animation-delay:{appear:.2f}s" + (f",{3.2 + col * 0.045:.2f}s" if lv else "")
        cells.append(
            f'<rect class="{cls}" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" '
            f'style="--f:{LEVELS[lv]};fill:{LEVELS[lv]};{anim}"/>'
        )
    tcol, trow = divmod(len(days) - 1 + offset, 7)
    tx, ty = hx + tcol * pitch + cell / 2, hy + trow * pitch + cell / 2
    parts.append("".join(months) + "".join(cells))
    parts.append(f'<rect class="today" x="{tx - 8}" y="{ty - 8}" width="16" height="16" rx="5"/>')

    # legend + busiest day
    lg_y = hy + 7 * pitch + 22
    bd, bc = s["busiest"]
    busy = f"Busiest day: {bd.day} {bd:%B}, with {bc} contributions." if bc else "Quiet year so far."
    parts.append(f'<path class="bs" d="{SANS.path(busy, 13, hx, lg_y + 9)}"/>')
    lx = hx + 53 * pitch - 3
    parts.append(f'<path class="lb" d="{MONO.path("MORE", 9.5, lx, lg_y + 9, anchor="end", track=1.4)}"/>')
    lx -= MONO.width("MORE", 9.5, 1.4) + 10
    for lv in range(4, -1, -1):
        lx -= cell
        parts.append(f'<rect x="{lx}" y="{lg_y}" width="{cell}" height="{cell}" rx="3" fill="{LEVELS[lv]}"/>')
        lx -= 4
    parts.append(f'<path class="lb" d="{MONO.path("LESS", 9.5, lx - 6, lg_y + 9, anchor="end", track=1.4)}"/>')

    # languages
    px, pw = 944, 200
    parts.append(f'<path class="lb" d="{MONO.path(f"LANGUAGES, {s["repos"]} REPOS", 9.5, px, hy - 12, track=1.6)}"/>')
    bx = px
    for i, (name, p) in enumerate(s["langs"]):
        w = max(2.0, pw * p - 2)
        col = LANG_COLORS[i % len(LANG_COLORS)]
        parts.append(
            f'<rect class="seg" x="{_num(bx)}" y="{hy}" width="{_num(w)}" height="8" rx="2" fill="{col}" '
            f'style="animation-delay:{1.0 + i * 0.15:.2f}s"/>'
        )
        bx += pw * p
        ry = hy + 34 + i * 21
        parts.append(
            f'<g class="lr" style="animation-delay:{1.2 + i * 0.12:.2f}s"><circle cx="{px + 4}" cy="{ry - 4}" r="4" fill="{col}"/>'
            f'<path class="ln" d="{SANS.path(name, 13, px + 16, ry)}"/>'
            f'<path class="lp" d="{MONO.path(f"{p * 100:.0f}%", 10.5, px + pw, ry, anchor="end")}"/></g>'
        )

    frame, frame_css = card_frame(W, H, TEAL, 13)
    style = f"""
  .bg {{ fill: {CARD}; }}
  .glow {{ animation: glow 14s ease-in-out infinite alternate; }}
  @keyframes glow {{ from {{ transform: translate(0,0); }} to {{ transform: translate(-120px,30px); }} }}
  .lb, .mo {{ fill: {DIM}; }}
  .tl {{ fill: {DIM}; animation: rise .9s ease-out both; }}
  .cn {{ fill: {INK}; }}
  .vd {{ stroke: {LINE}; }}
  .bs {{ fill: {BODY}; }}
  .ln {{ fill: {INK}; }}
  .lp {{ fill: {DIM}; }}
  .live {{ fill: {TEAL}; }}
  .liveh {{ fill: none; stroke: {TEAL}; transform-box: fill-box; transform-origin: center; animation: halo 2.2s ease-out infinite; }}
  @keyframes halo {{ from {{ transform: scale(1); opacity: .9; }} to {{ transform: scale(3.4); opacity: 0; }} }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
  .c {{ transform-box: fill-box; transform-origin: center; animation: cin .7s cubic-bezier(.3,1.5,.5,1) both; }}
  .c.on {{ animation: cin .7s cubic-bezier(.3,1.5,.5,1) both, glint 8s ease-in-out infinite; }}
  @keyframes cin {{ from {{ transform: scale(0); opacity: 0; }} to {{ transform: scale(1); opacity: 1; }} }}
  @keyframes glint {{ 0%, 3.5%, 100% {{ fill: var(--f); }} 1.5% {{ fill: #F9CF8E; }} }}
  .today {{ fill: none; stroke: {MARI}; stroke-width: 1.6; transform-box: fill-box; transform-origin: center; animation: today 2s ease-in-out infinite; }}
  @keyframes today {{ 0%,100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: .3; transform: scale(1.25); }} }}
  .seg {{ transform-box: fill-box; transform-origin: 0 50%; animation: grow .8s cubic-bezier(.6,.05,.3,1) both; }}
  @keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
  .lr {{ animation: rise .8s ease-out both; }}
{frame_css}{''.join(css)}"""
    body = f"""<defs>{grain_defs()}
  <radialGradient id="cgl"><stop offset="0" stop-color="{TEAL}" stop-opacity=".14"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>
  <radialGradient id="cgl2"><stop offset="0" stop-color="{TERRA}" stop-opacity=".16"/><stop offset="1" stop-color="{TERRA}" stop-opacity="0"/></radialGradient>
  <clipPath id="c"><rect width="{W}" height="{H}" rx="20"/></clipPath></defs>
<g clip-path="url(#c)">
  <rect class="bg" width="{W}" height="{H}"/>
  <ellipse class="glow" cx="900" cy="140" rx="420" ry="220" fill="url(#cgl)"/>
  <ellipse cx="300" cy="380" rx="420" ry="180" fill="url(#cgl2)"/>
  {''.join(parts)}
  <rect width="{W}" height="{H}" fill="url(#grain)" opacity=".5"/>
</g>
{frame}"""
    alt = (
        f"GitHub, last 12 months: {s['total']:,} contributions, {s['commits']:,} commits, "
        f"{s['active']} active days, longest streak {s['longest']} days."
    )
    return svg(W, H, body, style, alt)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true", help="use fake data (offline preview)")
    ap.add_argument("--out", default=str(OUT / "stats.svg"))
    args = ap.parse_args()
    if args.sample:
        user = sample()
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise SystemExit("Set GITHUB_TOKEN, or pass --sample for a preview.")
        user = fetch(token)
    s = summarize(user)
    with open(args.out, "w") as f:
        f.write(render(s, dt.datetime.now(dt.timezone.utc).date()))
    print(f"{args.out}: {s['total']} contributions, {s['commits']} commits, {s['active']} active days, "
          f"longest streak {s['longest']}, {len(s['langs'])} languages")


if __name__ == "__main__":
    main()
