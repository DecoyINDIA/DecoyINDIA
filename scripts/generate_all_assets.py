"""
OPUS VITAE // Generative Creative Code Engine
Author: motion-engineer (Swarm Motion Systems Engineer)
Target: assets/profile/
Constitution: C:/Users/subha/.gemini/antigravity/brain/82727ad7-2c20-4d1c-8825-1fc2c179bdfe/design_constitution.md

Generates 12 production-grade, mathematically grounded, dual-mode animated SVGs:
1. hero_signature.svg (960x340)
2. systems_topology.svg (960x420)
3. product_vaani.svg (880x260)
4. product_octapdf.svg (880x260)
5. product_bmd.svg (880x260)
6. product_formspear.svg (880x260)
7. product_settlr.svg (880x260)
8. product_sportshawk.svg (880x260)
9. product_xanalgo.svg (880x260)
10. product_candy_drop.svg (880x260)
11. divider_quantum.svg (960x40)
12. footer_console.svg (960x120)
"""

import math
import os
import sys

OUTPUT_DIR = r"C:\Users\subha\.gemini\antigravity\scratch\DecoyINDIA\assets\profile"

# Shared CSS styles with dual-mode (Dark / Light) resilience and Static Frame Test guarantees
SHARED_CSS = """
    :root {
      --bg-base: #080B10;
      --bg-card: #0D1117;
      --bg-elevated: #161B22;
      --border-line: #21262D;
      --border-accent: #30363D;
      --text-head: #F8FAFC;
      --text-body: #94A3B8;
      --text-dim: #475569;
      --accent-cyan: #00F2FE;
      --accent-amber: #FF8C00;
      --accent-emerald: #00E599;
      --accent-violet: #A855F7;
      --grid-line: #151926;
      --glass-glow: rgba(0, 242, 254, 0.08);
    }
    @media (prefers-color-scheme: light) {
      :root {
        --bg-base: #F8FAFC;
        --bg-card: #FFFFFF;
        --bg-elevated: #F1F5F9;
        --border-line: #CBD5E1;
        --border-accent: #94A3B8;
        --text-head: #0F172A;
        --text-body: #334155;
        --text-dim: #64748B;
        --accent-cyan: #007799;
        --accent-amber: #C25E00;
        --accent-emerald: #059669;
        --accent-violet: #7C3AED;
        --grid-line: #E2E8F0;
        --glass-glow: rgba(0, 119, 153, 0.04);
      }
      .theme-bg { fill: #F8FAFC !important; }
      .theme-card { fill: #FFFFFF !important; }
      .theme-elevated { fill: #F1F5F9 !important; }
      .theme-border { stroke: #CBD5E1 !important; }
      .theme-border-accent { stroke: #94A3B8 !important; }
      .theme-text-head { fill: #0F172A !important; }
      .theme-text-body { fill: #334155 !important; }
      .theme-text-dim { fill: #64748B !important; }
      .theme-grid { stroke: #E2E8F0 !important; }
      .theme-cyan-stroke { stroke: #007799 !important; }
      .theme-cyan-fill { fill: #007799 !important; }
      .theme-amber-stroke { stroke: #C25E00 !important; }
      .theme-amber-fill { fill: #C25E00 !important; }
      .theme-emerald-stroke { stroke: #059669 !important; }
      .theme-emerald-fill { fill: #059669 !important; }
      .theme-violet-stroke { stroke: #7C3AED !important; }
      .theme-violet-fill { fill: #7C3AED !important; }
    }
    @media (prefers-reduced-motion: reduce) {
      *, .anim-spin, .anim-pulse, .anim-flow, .anim-dash {
        animation: none !important;
      }
    }
    .mono { font-family: ui-monospace, 'SF Mono', 'JetBrains Mono', 'Cascadia Code', Menlo, Consolas, monospace; }
    .sans { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', 'Helvetica Neue', Arial, sans-serif; }
    
    @keyframes spinCW {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    @keyframes spinCCW {
      from { transform: rotate(360deg); }
      to { transform: rotate(0deg); }
    }
    @keyframes pulseGlow {
      0%, 100% { opacity: 0.4; }
      50% { opacity: 1.0; }
    }
    @keyframes dashStream {
      to { stroke-dashoffset: -40; }
    }
    @keyframes packetFlow {
      0% { stroke-dashoffset: 80; }
      100% { stroke-dashoffset: 0; }
    }
    @keyframes waveOscillate {
      0%, 100% { transform: translateY(0px) scaleY(1); }
      50% { transform: translateY(-2px) scaleY(1.06); }
    }
"""

def generate_hero():
    """Generates assets/profile/hero_signature.svg (960x340)"""
    w, h = 960, 340
    
    # Generate Lissajous curves mathematically
    lissajous_paths = []
    cx, cy = 720, 170
    a, b = 3, 4
    delta = math.pi / 2
    r_scale_x, r_scale_y = 85, 80
    
    # 3 harmonic Lissajous layers with phase shifts
    for layer_idx, (phase, stroke, op) in enumerate([
        (0.0, "#00F2FE", 0.85),
        (math.pi / 6, "#FF8C00", 0.55),
        (math.pi / 3, "#A855F7", 0.40)
    ]):
        pts = []
        steps = 120
        for i in range(steps + 1):
            t = (i / steps) * 2 * math.pi
            x = cx + r_scale_x * math.sin(a * t + delta + phase)
            y = cy + r_scale_y * math.sin(b * t)
            pts.append(f"{x:.1f},{y:.1f}")
        d = "M " + " L ".join(pts) + " Z"
        lissajous_paths.append((d, stroke, op))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <!-- Gradients -->
    <linearGradient id="heroBgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080B10" />
      <stop offset="50%" stop-color="#0D1117" />
      <stop offset="100%" stop-color="#05070A" />
    </linearGradient>
    <linearGradient id="topHairline" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#21262D" stop-opacity="0.2" />
      <stop offset="25%" stop-color="#00F2FE" stop-opacity="0.8" />
      <stop offset="50%" stop-color="#FF8C00" stop-opacity="0.9" />
      <stop offset="75%" stop-color="#00E599" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#21262D" stop-opacity="0.2" />
    </linearGradient>
    <radialGradient id="centerOrbGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00F2FE" stop-opacity="0.18" />
      <stop offset="40%" stop-color="#FF8C00" stop-opacity="0.06" />
      <stop offset="100%" stop-color="#080B10" stop-opacity="0" />
    </radialGradient>
    <pattern id="heroGridPattern" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M 32 0 L 0 0 0 32" fill="none" stroke="#151926" stroke-width="0.75" class="theme-grid" />
      <circle cx="32" cy="32" r="0.8" fill="#21262D" class="theme-border" />
    </pattern>
  </defs>

  <style>
{SHARED_CSS}
    .spin-caliper-slow {{ transform-origin: {cx}px {cy}px; animation: spinCW 48s linear infinite; }}
    .spin-caliper-rev {{ transform-origin: {cx}px {cy}px; animation: spinCCW 32s linear infinite; }}
    .pulse-core {{ transform-origin: {cx}px {cy}px; animation: pulseGlow 3s ease-in-out infinite; }}
    .wave-harmonic {{ animation: waveOscillate 4s ease-in-out infinite; transform-origin: {cx}px {cy}px; }}
  </style>

  <!-- Canvas Surface -->
  <rect width="{w}" height="{h}" rx="8" fill="url(#heroBgGrad)" class="theme-bg" />
  <rect width="{w}" height="{h}" rx="8" fill="url(#heroGridPattern)" />
  <circle cx="{cx}" cy="{cy}" r="140" fill="url(#centerOrbGlow)" />
  <rect width="{w}" height="{h}" rx="8" fill="none" stroke="#21262D" stroke-width="1.2" class="theme-border" />

  <!-- Top Specular Rule -->
  <line x1="20" y1="1" x2="{w - 20}" y2="1" stroke="url(#topHairline)" stroke-width="1.5" />

  <!-- Corner Precision Crosshairs -->
  <g stroke="#30363D" stroke-width="1" opacity="0.8" class="theme-border-accent">
    <path d="M 12 18 L 24 18 M 18 12 L 18 24" />
    <path d="M {w - 24} 18 L {w - 12} 18 M {w - 18} 12 L {w - 18} 24" />
    <path d="M 12 {h - 18} L 24 {h - 18} M 18 {h - 24} L 18 {h - 12}" />
    <path d="M {w - 24} {h - 18} L {w - 12} {h - 18} M {w - 18} {h - 24} L {w - 18} {h - 12}" />
  </g>

  <!-- ==================== LEFT COLUMN: EDITORIAL IDENTITY ==================== -->
  <g transform="translate(48, 40)">
    <!-- Metadata Eyebrow & Status Beacon -->
    <g transform="translate(0, 0)">
      <circle cx="4" cy="4" r="3.5" fill="#00E599" class="theme-emerald-fill">
        <animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite" />
      </circle>
      <text x="16" y="7" fill="#00F2FE" font-size="9" font-weight="700" letter-spacing="0.18em" class="mono theme-cyan-fill">DECOYINDIA // XOLVERLABS ATELIER</text>
      <text x="252" y="7" fill="#475569" font-size="9" font-weight="500" letter-spacing="0.12em" class="mono theme-text-dim">• 2026 SOVEREIGN SYSTEMS</text>
    </g>

    <!-- Sovereign Monogram + Logotype -->
    <g transform="translate(0, 24)">
      <!-- Hexagonal Monogram (Concurrency Knot) -->
      <g transform="translate(0, 4)">
        <polygon points="24,2 44,14 44,38 24,50 4,38 4,14" fill="none" stroke="#21262D" stroke-width="1.2" class="theme-border" />
        <polygon points="24,7 39,16 39,34 24,43 9,34 9,16" fill="none" stroke="#00F2FE" stroke-width="1.2" stroke-dasharray="3 3" class="theme-cyan-stroke" />
        <!-- Inner Knot -->
        <path d="M 24 7 L 24 43 M 9 16 L 39 34 M 9 34 L 39 16" fill="none" stroke="#F8FAFC" stroke-width="1" opacity="0.9" class="theme-text-head" />
        <circle cx="24" cy="25" r="3" fill="#FF8C00" class="theme-amber-fill" />
      </g>

      <!-- Primary Typography: Full Name -->
      <g transform="translate(62, 18)">
        <text x="0" y="0" fill="#F8FAFC" font-size="34" font-weight="800" letter-spacing="0.04em" class="sans theme-text-head">SUBHAM JENA</text>
        <text x="0" y="24" fill="#94A3B8" font-size="11" font-weight="600" letter-spacing="0.16em" class="mono theme-text-body">
          PRINCIPAL SYSTEMS ARCHITECT <tspan fill="#FF8C00" class="theme-amber-fill">//</tspan> FOUNDER, XOLVERLABS
        </text>
      </g>
    </g>

    <!-- Operational Positioning Statement -->
    <g transform="translate(0, 106)">
      <text x="0" y="0" fill="#E2E8F0" font-size="12" font-weight="400" letter-spacing="0.01em" class="sans theme-text-head">
        Engineering deterministic software: low-latency concurrency in <tspan fill="#00F2FE" font-weight="600" class="theme-cyan-fill">Rust</tspan> &amp; <tspan fill="#00F2FE" font-weight="600" class="theme-cyan-fill">Project Loom</tspan>,
      </text>
      <text x="0" y="18" fill="#94A3B8" font-size="12" font-weight="400" letter-spacing="0.01em" class="sans theme-text-body">
        un-hallucinated Indic vernacular voice pipelines, and air-gapped local-first runtimes.
      </text>
    </g>

    <!-- 3 Engineered Specification Telemetry Blocks -->
    <g transform="translate(0, 150)">
      <!-- Block 1: Concurrency -->
      <g transform="translate(0, 0)">
        <rect width="142" height="52" rx="4" fill="#0D1117" stroke="#21262D" stroke-width="1" class="theme-card theme-border" />
        <line x1="0" y1="0" x2="142" y2="0" stroke="#00F2FE" stroke-width="1.5" class="theme-cyan-stroke" />
        <text x="12" y="17" fill="#94A3B8" font-size="8.5" font-weight="700" letter-spacing="0.12em" class="mono theme-text-body">CONCURRENCY</text>
        <text x="12" y="34" fill="#F8FAFC" font-size="12" font-weight="700" class="mono theme-text-head">RUST · LOOM 21</text>
        <text x="12" y="45" fill="#00F2FE" font-size="8" font-weight="600" class="mono theme-cyan-fill">&lt; 2MS P99 TAIL</text>
      </g>

      <!-- Block 2: Vernacular Voice -->
      <g transform="translate(152, 0)">
        <rect width="150" height="52" rx="4" fill="#0D1117" stroke="#21262D" stroke-width="1" class="theme-card theme-border" />
        <line x1="0" y1="0" x2="150" y2="0" stroke="#FF8C00" stroke-width="1.5" class="theme-amber-stroke" />
        <text x="12" y="17" fill="#94A3B8" font-size="8.5" font-weight="700" letter-spacing="0.12em" class="mono theme-text-body">VOICE RUNTIME</text>
        <text x="12" y="34" fill="#F8FAFC" font-size="12" font-weight="700" class="mono theme-text-head">LANGGRAPH · INDIC</text>
        <text x="12" y="45" fill="#FF8C00" font-size="8" font-weight="600" class="mono theme-amber-fill">0-HALLUCINATION</text>
      </g>

      <!-- Block 3: Sovereign Trust -->
      <g transform="translate(312, 0)">
        <rect width="156" height="52" rx="4" fill="#0D1117" stroke="#21262D" stroke-width="1" class="theme-card theme-border" />
        <line x1="0" y1="0" x2="156" y2="0" stroke="#00E599" stroke-width="1.5" class="theme-emerald-stroke" />
        <text x="12" y="17" fill="#94A3B8" font-size="8.5" font-weight="700" letter-spacing="0.12em" class="mono theme-text-body">DATA INTEGRITY</text>
        <text x="12" y="34" fill="#F8FAFC" font-size="12" font-weight="700" class="mono theme-text-head">ZERO-EGRESS · ESCROW</text>
        <text x="12" y="45" fill="#00E599" font-size="8" font-weight="600" class="mono theme-emerald-fill">DPDP 2025 COMPLIANT</text>
      </g>
    </g>

    <!-- Real-time Systems Telemetry Footnote -->
    <g transform="translate(0, 222)">
      <text x="0" y="0" fill="#475569" font-size="8.5" font-weight="500" letter-spacing="0.14em" class="mono theme-text-dim">
        SYS_STATUS: <tspan fill="#00E599" font-weight="700" class="theme-emerald-fill">DETERMINISTIC</tspan> | GPS: 20.2961°N, 85.8245°E | REPOS: 18+ AUDITED | INVARIANTS: PASS
      </text>
    </g>
  </g>

  <!-- ==================== RIGHT COLUMN: PARAMETRIC KINETIC INSTRUMENT ==================== -->
  <g id="hero-instrument">
    <!-- Outer Cardinal Caliper Ring (48s linear rotation) -->
    <g class="spin-caliper-slow">
      <circle cx="{cx}" cy="{cy}" r="118" fill="none" stroke="#21262D" stroke-width="1" stroke-dasharray="2 10" class="theme-border" />
      <circle cx="{cx}" cy="{cy}" r="110" fill="none" stroke="#30363D" stroke-width="0.8" class="theme-border-accent" />
      <!-- Cardinal Caliper Ticks -->
      <line x1="{cx}" y1="{cy - 118}" x2="{cx}" y2="{cy - 108}" stroke="#00F2FE" stroke-width="1.5" class="theme-cyan-stroke" />
      <line x1="{cx}" y1="{cy + 108}" x2="{cx}" y2="{cy + 118}" stroke="#00F2FE" stroke-width="1.5" class="theme-cyan-stroke" />
      <line x1="{cx - 118}" y1="{cy}" x2="{cx - 108}" y2="{cy}" stroke="#FF8C00" stroke-width="1.5" class="theme-amber-stroke" />
      <line x1="{cx + 108}" y1="{cy}" x2="{cx + 118}" y2="{cy}" stroke="#FF8C00" stroke-width="1.5" class="theme-amber-stroke" />
      <text x="{cx}" y="{cy - 122}" fill="#94A3B8" font-size="7.5" font-weight="600" text-anchor="middle" class="mono theme-text-body">000°</text>
      <text x="{cx + 128}" y="{cy + 3}" fill="#94A3B8" font-size="7.5" font-weight="600" text-anchor="start" class="mono theme-text-body">090°</text>
      <text x="{cx}" y="{cy + 130}" fill="#94A3B8" font-size="7.5" font-weight="600" text-anchor="middle" class="mono theme-text-body">180°</text>
      <text x="{cx - 128}" y="{cy + 3}" fill="#94A3B8" font-size="7.5" font-weight="600" text-anchor="end" class="mono theme-text-body">270°</text>
    </g>

    <!-- Secondary Harmonic Caliper (32s reverse rotation) -->
    <g class="spin-caliper-rev">
      <circle cx="{cx}" cy="{cy}" r="96" fill="none" stroke="#00F2FE" stroke-width="1" stroke-dasharray="4 8" opacity="0.6" class="theme-cyan-stroke" />
      <!-- Radial Satellite Nodes -->
      <circle cx="{cx + 96}" cy="{cy}" r="3.5" fill="#00F2FE" class="theme-cyan-fill" />
      <circle cx="{cx - 96}" cy="{cy}" r="3.5" fill="#FF8C00" class="theme-amber-fill" />
      <circle cx="{cx}" cy="{cy + 96}" r="3" fill="#00E599" class="theme-emerald-fill" />
    </g>

    <!-- Parametric Lissajous Waves -->
    <g class="wave-harmonic">
"""
    for d, stroke, op in lissajous_paths:
        svg += f'      <path d="{d}" fill="none" stroke="{stroke}" stroke-width="1.2" opacity="{op}" />\n'

    svg += f"""    </g>

    <!-- Central Quantum Core -->
    <g class="pulse-core">
      <circle cx="{cx}" cy="{cy}" r="22" fill="#0D1117" stroke="#21262D" stroke-width="1.2" class="theme-card theme-border" />
      <circle cx="{cx}" cy="{cy}" r="14" fill="#00F2FE" fill-opacity="0.15" stroke="#00F2FE" stroke-width="1.2" class="theme-cyan-stroke" />
      <circle cx="{cx}" cy="{cy}" r="5" fill="#FF8C00" class="theme-amber-fill" />
    </g>

    <!-- Floating HUD Telemetry Chips -->
    <g transform="translate({cx - 90}, {cy + 124})">
      <rect width="180" height="20" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
      <text x="90" y="13" fill="#94A3B8" font-size="8" font-weight="600" letter-spacing="0.08em" text-anchor="middle" class="mono theme-text-body">
        ORBIT: <tspan fill="#00F2FE" class="theme-cyan-fill">HARMONIC</tspan> // JITTER: &lt;0.04MS
      </text>
    </g>
  </g>
</svg>"""
    return svg

def generate_systems_topology():
    """Generates assets/profile/systems_topology.svg (960x420)"""
    w, h = 960, 420
    cx, cy = 480, 210

    # Nodes definition
    nodes = [
        # (id, name, stack, role, x, y, accent, border_clr)
        ("vaani", "VAANI", "Python 3.12 / LangGraph", "Vernacular Voice Agent", 200, 90, "#FF8C00", "#FF8C00"),
        ("octapdf", "OCTAPDF", "Java 21 / Loom / Air-Gap", "Local-First PDF OS", 760, 90, "#00F2FE", "#00F2FE"),
        ("bmd", "BMD", "Rust / Tokio Async", "High-Throughput Downloader", 140, 220, "#00F2FE", "#00F2FE"),
        ("formspear", "FORMSPEAR", "Bare Node 20 / 39-Table SQL", "Feedback Telemetry OS", 820, 220, "#00E599", "#00E599"),
        ("settlr", "SETTLR", "SHA-256 / FastAPI / Postgres", "Dual-Consent Rental Ledger", 210, 340, "#FF8C00", "#FF8C00"),
        ("sportshawk", "SPORTSHAWK", "Edge CV / 60 FPS Pose", "Grassroots Athletic CV", 750, 340, "#00F2FE", "#00F2FE"),
        ("lawflow", "LAWFLOW", "Rust Axum / Tauri 2", "Judicial Chambers OS", 480, 65, "#00E599", "#00E599"),
        ("xanalgo", "XENALGO", "Python 3.12 / Fyers API", "Risk-Governed Execution", 480, 355, "#A855F7", "#A855F7"),
    ]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="topoBgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080B10" />
      <stop offset="50%" stop-color="#0D1117" />
      <stop offset="100%" stop-color="#06080C" />
    </linearGradient>
    <radialGradient id="hubGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00F2FE" stop-opacity="0.18" />
      <stop offset="50%" stop-color="#FF8C00" stop-opacity="0.05" />
      <stop offset="100%" stop-color="#080B10" stop-opacity="0" />
    </radialGradient>
    <pattern id="topoGrid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#151926" stroke-width="0.6" class="theme-grid" />
      <circle cx="24" cy="24" r="0.6" fill="#21262D" class="theme-border" />
    </pattern>
  </defs>

  <style>
{SHARED_CSS}
    .flow-stream {{ stroke-dasharray: 6 8; animation: dashStream 3s linear infinite; }}
    .flow-stream-fast {{ stroke-dasharray: 4 6; animation: dashStream 1.8s linear infinite; }}
    .flow-stream-rev {{ stroke-dasharray: 6 8; animation: dashStream 3s linear infinite reverse; }}
    .spin-hub {{ transform-origin: {cx}px {cy}px; animation: spinCW 60s linear infinite; }}
    .pulse-hub {{ transform-origin: {cx}px {cy}px; animation: pulseGlow 3s ease-in-out infinite; }}
  </style>

  <!-- Canvas Surface -->
  <rect width="{w}" height="{h}" rx="8" fill="url(#topoBgGrad)" class="theme-bg" />
  <rect width="{w}" height="{h}" rx="8" fill="url(#topoGrid)" />
  <circle cx="{cx}" cy="{cy}" r="170" fill="url(#hubGlow)" />
  <rect width="{w}" height="{h}" rx="8" fill="none" stroke="#21262D" stroke-width="1.2" class="theme-border" />

  <!-- Corner Precision Crosshairs -->
  <g stroke="#30363D" stroke-width="1" opacity="0.8" class="theme-border-accent">
    <path d="M 14 20 L 26 20 M 20 14 L 20 26" />
    <path d="M {w - 26} 20 L {w - 14} 20 M {w - 20} 14 L {w - 20} 26" />
    <path d="M 14 {h - 20} L 26 {h - 20} M 20 {h - 26} L 20 {h - 14}" />
    <path d="M {w - 26} {h - 20} L {w - 14} {h - 20} M {w - 20} {h - 26} L {w - 20} {h - 14}" />
  </g>

  <!-- Top Topology Header Bar -->
  <g transform="translate(36, 32)">
    <circle cx="4" cy="4" r="3" fill="#00F2FE" class="theme-cyan-fill" />
    <text x="14" y="7" fill="#F8FAFC" font-size="11" font-weight="700" letter-spacing="0.14em" class="mono theme-text-head">
      SYSTEMS TOPOLOGY MATRIX // XOLVERLABS SOVEREIGN BUS ARCHITECTURE
    </text>
    <text x="{w - 72}" y="7" fill="#00E599" font-size="9" font-weight="600" letter-spacing="0.1em" text-anchor="end" class="mono theme-emerald-fill">
      STATUS: ALL 8 ENCLAVES OPERATIONAL
    </text>
  </g>

  <!-- Connecting Bus Lines (Hub to Nodes + Inter-node bridges) -->
  <g stroke-width="1.2">
"""
    # Generate bus lines from nodes to hub
    for nid, name, stack, role, nx, ny, acc, bclr in nodes:
        svg += f'    <!-- Data Bus to {name} -->\n'
        svg += f'    <line x1="{cx}" y1="{cy}" x2="{nx}" y2="{ny}" stroke="{acc}" stroke-opacity="0.35" />\n'
        svg += f'    <line x1="{cx}" y1="{cy}" x2="{nx}" y2="{ny}" stroke="{acc}" stroke-opacity="0.9" class="flow-stream" />\n'

    # Inter-node synergies
    # Vaani <-> Settlr
    svg += f'    <path d="M 200 120 Q 150 215 210 315" fill="none" stroke="#FF8C00" stroke-opacity="0.4" stroke-dasharray="3 5" class="flow-stream-fast" />\n'
    # OctaPDF <-> LawFlow
    svg += f'    <path d="M 760 120 Q 620 60 550 70" fill="none" stroke="#00F2FE" stroke-opacity="0.4" stroke-dasharray="3 5" class="flow-stream-rev" />\n'
    # BMD <-> OctaPDF (concurrency data transfer)
    svg += f'    <path d="M 140 200 Q 480 130 760 120" fill="none" stroke="#00F2FE" stroke-opacity="0.25" stroke-dasharray="2 6" />\n'
    # Formspear <-> SportsHawk
    svg += f'    <path d="M 820 245 Q 810 300 750 320" fill="none" stroke="#00E599" stroke-opacity="0.4" stroke-dasharray="3 5" class="flow-stream-fast" />\n'

    svg += f"""  </g>

  <!-- Central Nexus Hub: XOLVERLABS RUNTIME -->
  <g transform="translate({cx}, {cy})">
    <!-- Rotating Compass Ring -->
    <g class="spin-hub">
      <circle cx="0" cy="0" r="54" fill="none" stroke="#21262D" stroke-width="1" stroke-dasharray="3 7" class="theme-border" />
      <circle cx="0" cy="0" r="46" fill="none" stroke="#30363D" stroke-width="0.8" class="theme-border-accent" />
      <line x1="0" y1="-54" x2="0" y2="-46" stroke="#00F2FE" stroke-width="1.5" class="theme-cyan-stroke" />
      <line x1="0" y1="54" x2="0" y2="46" stroke="#00F2FE" stroke-width="1.5" class="theme-cyan-stroke" />
      <line x1="-54" y1="0" x2="-46" y2="0" stroke="#FF8C00" stroke-width="1.5" class="theme-amber-stroke" />
      <line x1="54" y1="0" x2="46" y2="0" stroke="#FF8C00" stroke-width="1.5" class="theme-amber-stroke" />
    </g>

    <!-- Hub Body -->
    <g class="pulse-hub">
      <polygon points="0,-36 32,-18 32,18 0,36 -32,18 -32,-18" fill="#0D1117" stroke="#00F2FE" stroke-width="1.5" class="theme-card theme-cyan-stroke" />
      <circle cx="0" cy="0" r="14" fill="#00F2FE" fill-opacity="0.2" stroke="#FF8C00" stroke-width="1.2" class="theme-amber-stroke" />
      <circle cx="0" cy="0" r="4" fill="#00E599" class="theme-emerald-fill" />
    </g>

    <!-- Hub Labels -->
    <text x="0" y="48" fill="#F8FAFC" font-size="9" font-weight="700" letter-spacing="0.12em" text-anchor="middle" class="mono theme-text-head">XOLVERLABS CORE</text>
    <text x="0" y="58" fill="#00F2FE" font-size="7.5" font-weight="600" letter-spacing="0.08em" text-anchor="middle" class="mono theme-cyan-fill">DETERMINISTIC BUS</text>
  </g>

  <!-- Peripheral Enclave Cards -->
"""
    for nid, name, stack, role, nx, ny, acc, bclr in nodes:
        cw, ch = 146, 50
        x0 = nx - cw // 2
        y0 = ny - ch // 2
        svg += f"""  <!-- Node: {name} -->
  <g transform="translate({x0}, {y0})">
    <rect width="{cw}" height="{ch}" rx="4" fill="#0D1117" stroke="{bclr}" stroke-width="1" stroke-opacity="0.8" class="theme-card" />
    <line x1="0" y1="0" x2="{cw}" y2="0" stroke="{acc}" stroke-width="1.5" />
    <circle cx="10" cy="14" r="3" fill="{acc}" />
    <text x="18" y="17" fill="#F8FAFC" font-size="10.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-head">{name}</text>
    <text x="10" y="31" fill="#94A3B8" font-size="7.5" font-weight="600" class="mono theme-text-body">{stack}</text>
    <text x="10" y="42" fill="#475569" font-size="7" font-weight="500" class="sans theme-text-dim">{role}</text>
  </g>
"""

    svg += f"""  <!-- Bottom Telemetry Footer Strip -->
  <g transform="translate(36, {h - 22})">
    <text x="0" y="0" fill="#475569" font-size="8.5" font-weight="500" letter-spacing="0.1em" class="mono theme-text-dim">
      DATA FLOW: <tspan fill="#00F2FE" class="theme-cyan-fill">LOCK-FREE RING BUFFERS</tspan> · ZERO THIRD-PARTY PHONE-HOME · SHA-256 APPEND-ONLY JOURNAL · DPDP 2025 CERTIFIED
    </text>
  </g>
</svg>"""
    return svg

def generate_product_vaani():
    """Generates assets/profile/product_vaani.svg (880x260)"""
    w, h = 880, 260
    
    # Generate multi-harmonic acoustic waveform
    wave_pts = []
    wx_start, wx_end = 510, 830
    wy_center = 100
    steps = 80
    for i in range(steps + 1):
        x = wx_start + (i / steps) * (wx_end - wx_start)
        t = (i / steps) * 4 * math.pi
        # Superposition of 3 harmonics
        y = wy_center + 18 * math.sin(t) + 10 * math.sin(2.4 * t + 0.8) + 6 * math.sin(3.8 * t + 1.6)
        wave_pts.append(f"{x:.1f},{y:.1f}")
    wave_path = "M " + " L ".join(wave_pts)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="vaaniBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080B10" />
      <stop offset="60%" stop-color="#0D1117" />
      <stop offset="100%" stop-color="#070A0F" />
    </linearGradient>
    <linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF8C00" />
      <stop offset="50%" stop-color="#00F2FE" />
      <stop offset="100%" stop-color="#00E599" />
    </linearGradient>
  </defs>

  <style>
{SHARED_CSS}
    .flow-wave {{ stroke-dasharray: 6 4; animation: dashStream 4s linear infinite; }}
    .pulse-node {{ animation: pulseGlow 2.4s ease-in-out infinite; }}
  </style>

  <!-- Canvas Surface -->
  <rect width="{w}" height="{h}" rx="6" fill="url(#vaaniBg)" class="theme-bg" />
  <rect width="{w}" height="{h}" rx="6" fill="none" stroke="#21262D" stroke-width="1.2" class="theme-border" />
  <line x1="0" y1="0" x2="{w}" y2="0" stroke="#FF8C00" stroke-width="2" class="theme-amber-stroke" />

  <!-- Corner Crosshairs -->
  <g stroke="#30363D" stroke-width="0.8" opacity="0.7" class="theme-border-accent">
    <path d="M 10 14 L 18 14 M 14 10 L 14 18" />
    <path d="M {w - 18} 14 L {w - 10} 14 M {w - 14} 10 L {w - 14} 18" />
    <path d="M 10 {h - 14} L 18 {h - 14} M 14 {h - 18} L 14 {h - 10}" />
    <path d="M {w - 18} {h - 14} L {w - 10} {h - 14} M {w - 14} {h - 18} L {w - 14} {h - 10}" />
  </g>

  <!-- ==================== LEFT COLUMN: EDITORIAL SPECS ==================== -->
  <g transform="translate(36, 32)">
    <g transform="translate(0, 0)">
      <circle cx="4" cy="4" r="3.5" fill="#FF8C00" class="theme-amber-fill" />
      <text x="14" y="7" fill="#FF8C00" font-size="9" font-weight="700" letter-spacing="0.14em" class="mono theme-amber-fill">SYSTEM 01 // VERNACULAR TELEPHONY</text>
    </g>

    <!-- Main Title -->
    <text x="0" y="32" fill="#F8FAFC" font-size="22" font-weight="800" letter-spacing="0.02em" class="sans theme-text-head">
      VAANI: MULTILINGUAL AI FRONT DESK
    </text>
    <text x="0" y="48" fill="#94A3B8" font-size="11" font-weight="500" class="sans theme-text-body">
      Autonomous Vernacular Voice &amp; WhatsApp Receptionist for Indian SMBs
    </text>

    <!-- 3 Telemetry Spec Chips -->
    <g transform="translate(0, 68)">
      <g transform="translate(0, 0)">
        <rect width="138" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">SCOPE ENFORCEMENT</text>
        <text x="10" y="28" fill="#00F2FE" font-size="10.5" font-weight="700" class="mono theme-cyan-fill">0-HALLUCINATION</text>
      </g>
      <g transform="translate(146, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">VOICE DISPATCH</text>
        <text x="10" y="28" fill="#FF8C00" font-size="10.5" font-weight="700" class="mono theme-amber-fill">SUB-3S END-TO-END</text>
      </g>
      <g transform="translate(298, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">STATUTORY PRIVACY</text>
        <text x="10" y="28" fill="#00E599" font-size="10.5" font-weight="700" class="mono theme-emerald-fill">DPDP ACT 2025</text>
      </g>
    </g>

    <!-- Verified Metric Badge -->
    <g transform="translate(0, 122)">
      <rect width="442" height="34" rx="3" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <text x="12" y="16" fill="#94A3B8" font-size="8" font-weight="700" letter-spacing="0.1em" class="mono theme-text-body">VERIFIED BENCHMARKS:</text>
      <text x="12" y="27" fill="#F8FAFC" font-size="9" font-weight="600" class="mono theme-text-head">
        386 PYTESTS PASSING · 500 CONCURRENT CLAIMS RACE-TESTED (0 DOUBLE-BOOKINGS)
      </text>
    </g>

    <!-- Stack Footnote -->
    <text x="0" y="180" fill="#475569" font-size="9" font-weight="500" class="mono theme-text-dim">
      STACK: Python 3.12 · LangGraph 7-Node State Machine · FastAPI · MongoDB Replica · Twilio SIP
    </text>
  </g>

  <!-- ==================== RIGHT COLUMN: WAVEFORM & 7-NODE STATE MACHINE ==================== -->
  <g id="vaani-schematic">
    <!-- Acoustic Waveform Display Box -->
    <g transform="translate(500, 28)">
      <rect width="344" height="92" rx="4" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
      <text x="12" y="16" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">
        ACOUSTIC HARMONICS // INDIC SPEECH DYNAMICS (HINDI, ODIA, HINGLISH)
      </text>
      <!-- Base center line -->
      <line x1="10" y1="54" x2="334" y2="54" stroke="#21262D" stroke-width="0.75" class="theme-border" />
      <!-- Waveform path -->
      <path d="{wave_path}" fill="none" stroke="url(#waveGrad)" stroke-width="1.8" class="flow-wave" />
      <!-- Spectrum frequency bars -->
      <g transform="translate(14, 72)" stroke="#00F2FE" stroke-width="1.5" opacity="0.7" class="theme-cyan-stroke">
        <line x1="10" y1="12" x2="10" y2="2" />
        <line x1="25" y1="12" x2="25" y2="0" />
        <line x1="40" y1="12" x2="40" y2="5" />
        <line x1="55" y1="12" x2="55" y2="1" />
        <line x1="70" y1="12" x2="70" y2="8" />
        <line x1="85" y1="12" x2="85" y2="3" />
        <line x1="100" y1="12" x2="100" y2="9" />
        <line x1="115" y1="12" x2="115" y2="0" />
        <line x1="130" y1="12" x2="130" y2="4" />
        <line x1="145" y1="12" x2="145" y2="11" />
      </g>
      <text x="330" y="82" fill="#00E599" font-size="7.5" font-weight="600" text-anchor="end" class="mono theme-emerald-fill">
        SUB-3S LATENCY
      </text>
    </g>

    <!-- 7-Node LangGraph Flowchart Representation -->
    <g transform="translate(500, 134)">
      <rect width="344" height="96" rx="4" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
      <text x="12" y="16" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">
        LANGGRAPH DETERMINISTIC STATE GRAPH (FAIL-CLOSED)
      </text>

      <!-- Nodes -->
      <g transform="translate(12, 28)">
        <!-- Node 1 -->
        <rect x="0" y="0" width="60" height="24" rx="2" fill="#161B22" stroke="#00F2FE" stroke-width="0.8" class="theme-elevated theme-cyan-stroke" />
        <text x="30" y="15" fill="#F8FAFC" font-size="7.5" font-weight="600" text-anchor="middle" class="mono theme-text-head">SIP Ingest</text>
        <!-- Arrow -->
        <line x1="60" y1="12" x2="72" y2="12" stroke="#00F2FE" stroke-width="1" class="theme-cyan-stroke" />

        <!-- Node 2 -->
        <rect x="72" y="0" width="70" height="24" rx="2" fill="#161B22" stroke="#FF8C00" stroke-width="0.8" class="theme-elevated theme-amber-stroke" />
        <text x="107" y="15" fill="#F8FAFC" font-size="7.5" font-weight="600" text-anchor="middle" class="mono theme-text-head">Scope Gate</text>
        <!-- Arrow -->
        <line x1="142" y1="12" x2="154" y2="12" stroke="#FF8C00" stroke-width="1" class="theme-amber-stroke" />

        <!-- Node 3 -->
        <rect x="154" y="0" width="76" height="24" rx="2" fill="#161B22" stroke="#00E599" stroke-width="0.8" class="theme-elevated theme-emerald-stroke" />
        <text x="192" y="15" fill="#F8FAFC" font-size="7.5" font-weight="600" text-anchor="middle" class="mono theme-text-head">Fact Ground</text>
        <!-- Arrow -->
        <line x1="230" y1="12" x2="242" y2="12" stroke="#00E599" stroke-width="1" class="theme-emerald-stroke" />

        <!-- Node 4 -->
        <rect x="242" y="0" width="74" height="24" rx="2" fill="#161B22" stroke="#00F2FE" stroke-width="0.8" class="theme-elevated theme-cyan-stroke" />
        <text x="279" y="15" fill="#F8FAFC" font-size="7.5" font-weight="600" text-anchor="middle" class="mono theme-text-head">Atomic Lock</text>

        <!-- Down Arrow from Node 4 to Node 5 -->
        <line x1="279" y1="24" x2="279" y2="34" stroke="#00F2FE" stroke-width="1" class="theme-cyan-stroke" />

        <!-- Lower Row: Nodes 5, 6, 7 -->
        <rect x="232" y="34" width="94" height="22" rx="2" fill="#161B22" stroke="#00E599" stroke-width="0.8" class="theme-elevated theme-emerald-stroke" />
        <text x="279" y="48" fill="#F8FAFC" font-size="7.5" font-weight="600" text-anchor="middle" class="mono theme-text-head">WhatsApp Ingest</text>

        <line x1="232" y1="45" x2="204" y2="45" stroke="#00E599" stroke-width="1" class="theme-emerald-stroke" />

        <rect x="100" y="34" width="104" height="22" rx="2" fill="#161B22" stroke="#FF8C00" stroke-width="0.8" class="theme-elevated theme-amber-stroke" />
        <text x="152" y="48" fill="#F8FAFC" font-size="7.5" font-weight="600" text-anchor="middle" class="mono theme-text-head">DPDP Erasure (7D)</text>
      </g>
    </g>
  </g>
</svg>"""
    return svg

def generate_product_octapdf():
    """Generates assets/profile/product_octapdf.svg (880x260)"""
    w, h = 880, 260
    cx, cy = 670, 130

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="octaBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080B10" />
      <stop offset="60%" stop-color="#0D1117" />
      <stop offset="100%" stop-color="#06090D" />
    </linearGradient>
    <radialGradient id="ringGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00F2FE" stop-opacity="0.14" />
      <stop offset="60%" stop-color="#00E599" stop-opacity="0.04" />
      <stop offset="100%" stop-color="#080B10" stop-opacity="0" />
    </radialGradient>
  </defs>

  <style>
{SHARED_CSS}
    .spin-ring-loom {{ transform-origin: {cx}px {cy}px; animation: spinCW 24s linear infinite; }}
    .spin-ring-inner {{ transform-origin: {cx}px {cy}px; animation: spinCCW 16s linear infinite; }}
    .pulse-shield {{ animation: pulseGlow 3.2s ease-in-out infinite; }}
  </style>

  <!-- Canvas Surface -->
  <rect width="{w}" height="{h}" rx="6" fill="url(#octaBg)" class="theme-bg" />
  <circle cx="{cx}" cy="{cy}" r="110" fill="url(#ringGlow)" />
  <rect width="{w}" height="{h}" rx="6" fill="none" stroke="#21262D" stroke-width="1.2" class="theme-border" />
  <line x1="0" y1="0" x2="{w}" y2="0" stroke="#00F2FE" stroke-width="2" class="theme-cyan-stroke" />

  <!-- Corner Crosshairs -->
  <g stroke="#30363D" stroke-width="0.8" opacity="0.7" class="theme-border-accent">
    <path d="M 10 14 L 18 14 M 14 10 L 14 18" />
    <path d="M {w - 18} 14 L {w - 10} 14 M {w - 14} 10 L {w - 14} 18" />
    <path d="M 10 {h - 14} L 18 {h - 14} M 14 {h - 18} L 14 {h - 10}" />
    <path d="M {w - 18} {h - 14} L {w - 10} {h - 14} M {w - 14} {h - 18} L {w - 14} {h - 10}" />
  </g>

  <!-- ==================== LEFT COLUMN: EDITORIAL SPECS ==================== -->
  <g transform="translate(36, 32)">
    <g transform="translate(0, 0)">
      <circle cx="4" cy="4" r="3.5" fill="#00F2FE" class="theme-cyan-fill" />
      <text x="14" y="7" fill="#00F2FE" font-size="9" font-weight="700" letter-spacing="0.14em" class="mono theme-cyan-fill">SYSTEM 02 // LOCAL-FIRST RUNTIMES</text>
    </g>

    <!-- Main Title -->
    <text x="0" y="32" fill="#F8FAFC" font-size="22" font-weight="800" letter-spacing="0.02em" class="sans theme-text-head">
      OCTAPDF: ZERO-EGRESS DOCUMENT ENGINE
    </text>
    <text x="0" y="48" fill="#94A3B8" font-size="11" font-weight="500" class="sans theme-text-body">
      Air-Gapped High-Throughput PDF Workspace in Java 21+ &amp; Project Loom
    </text>

    <!-- 3 Telemetry Spec Chips -->
    <g transform="translate(0, 68)">
      <g transform="translate(0, 0)">
        <rect width="138" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">AIR-GAP SECURITY</text>
        <text x="10" y="28" fill="#00E599" font-size="10.5" font-weight="700" class="mono theme-emerald-fill">ZERO EGRESS</text>
      </g>
      <g transform="translate(146, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">CONCURRENCY RUNTIME</text>
        <text x="10" y="28" fill="#00F2FE" font-size="10.5" font-weight="700" class="mono theme-cyan-fill">PROJECT LOOM</text>
      </g>
      <g transform="translate(298, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">PAGE BREAKOUT</text>
        <text x="10" y="28" fill="#FF8C00" font-size="10.5" font-weight="700" class="mono theme-amber-fill">SUB-12MS INTAKE</text>
      </g>
    </g>

    <!-- Architecture Standard Box -->
    <g transform="translate(0, 122)">
      <rect width="442" height="34" rx="3" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <text x="12" y="16" fill="#94A3B8" font-size="8" font-weight="700" letter-spacing="0.1em" class="mono theme-text-body">DESIGN SYSTEM &amp; COMMAND PALETTE:</text>
      <text x="12" y="27" fill="#F8FAFC" font-size="9" font-weight="600" class="mono theme-text-head">
        PAPER DESK SYSTEM · 50+ COMMAND PALETTE TOOLS · 100% PRIVATE IN-MEMORY
      </text>
    </g>

    <!-- Stack Footnote -->
    <text x="0" y="180" fill="#475569" font-size="9" font-weight="500" class="mono theme-text-dim">
      INVARIANTS: Read-Only Root Filesystems · internal: true Docker Network · 0 WAN Calls
    </text>
  </g>

  <!-- ==================== RIGHT COLUMN: AIR-GAP SHIELD & LOOM VIRTUAL THREADS ==================== -->
  <g id="octapdf-instrument">
    <!-- Air-Gap Boundary Circle -->
    <circle cx="{cx}" cy="{cy}" r="92" fill="none" stroke="#21262D" stroke-width="1.2" stroke-dasharray="4 6" class="theme-border" />
    <text x="{cx}" y="{cy - 98}" fill="#00E599" font-size="7.5" font-weight="700" letter-spacing="0.14em" text-anchor="middle" class="mono theme-emerald-fill">
      [ AIR-GAP BOUNDARY // INTERNAL: TRUE ]
    </text>

    <!-- Orbiting Virtual Thread Ring (Project Loom) -->
    <g class="spin-ring-loom">
      <circle cx="{cx}" cy="{cy}" r="74" fill="none" stroke="#00F2FE" stroke-width="1" stroke-dasharray="2 8" opacity="0.7" class="theme-cyan-stroke" />
"""
    # 8 Virtual thread nodes around ring
    for i in range(8):
        angle = (i / 8) * 2 * math.pi
        rx = cx + 74 * math.cos(angle)
        ry = cy + 74 * math.sin(angle)
        clr = "#00F2FE" if i % 2 == 0 else "#00E599"
        svg += f'      <circle cx="{rx:.1f}" cy="{ry:.1f}" r="3" fill="{clr}" />\n'

    svg += f"""    </g>

    <!-- Inner Document Core Deck -->
    <g class="spin-ring-inner">
      <circle cx="{cx}" cy="{cy}" r="48" fill="none" stroke="#30363D" stroke-width="0.8" class="theme-border-accent" />
      <rect x="{cx - 18}" y="{cy - 24}" width="36" height="48" rx="2" fill="#0D1117" stroke="#F8FAFC" stroke-width="1.2" class="theme-card theme-text-head" />
      <line x1="{cx - 12}" y1="{cy - 14}" x2="{cx + 12}" y2="{cy - 14}" stroke="#00F2FE" stroke-width="1" class="theme-cyan-stroke" />
      <line x1="{cx - 12}" y1="{cy - 6}" x2="{cx + 12}" y2="{cy - 6}" stroke="#94A3B8" stroke-width="0.8" class="theme-text-body" />
      <line x1="{cx - 12}" y1="{cy + 2}" x2="{cx + 6}" y2="{cy + 2}" stroke="#94A3B8" stroke-width="0.8" class="theme-text-body" />
      <line x1="{cx - 12}" y1="{cy + 10}" x2="{cx + 10}" y2="{cy + 10}" stroke="#00E599" stroke-width="1" class="theme-emerald-stroke" />
    </g>

    <!-- Center Pulse Core -->
    <circle cx="{cx}" cy="{cy}" r="4" fill="#00E599" class="pulse-shield theme-emerald-fill" />

    <!-- Telemetry Footnote -->
    <text x="{cx}" y="{cy + 105}" fill="#94A3B8" font-size="8" font-weight="600" text-anchor="middle" class="mono theme-text-body">
      WAN EGRESS: <tspan fill="#00E599" class="theme-emerald-fill">BLOCKED</tspan> | HEAP LEAK: 0 KB
    </text>
  </g>
</svg>"""
    return svg

def generate_product_bmd():
    """Generates assets/profile/product_bmd.svg (880x260)"""
    w, h = 880, 260
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="bmdBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080B10" />
      <stop offset="60%" stop-color="#0D1117" />
      <stop offset="100%" stop-color="#05080C" />
    </linearGradient>
    <linearGradient id="chunkGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00F2FE" />
      <stop offset="100%" stop-color="#00E599" />
    </linearGradient>
  </defs>

  <style>
{SHARED_CSS}
    .chunk-anim-1 {{ stroke-dashoffset: 60; animation: packetFlow 2s linear infinite; }}
    .chunk-anim-2 {{ stroke-dashoffset: 80; animation: packetFlow 1.6s linear infinite; }}
    .chunk-anim-3 {{ stroke-dashoffset: 40; animation: packetFlow 2.4s linear infinite; }}
    .chunk-anim-4 {{ stroke-dashoffset: 70; animation: packetFlow 1.8s linear infinite; }}
  </style>

  <!-- Canvas Surface -->
  <rect width="{w}" height="{h}" rx="6" fill="url(#bmdBg)" class="theme-bg" />
  <rect width="{w}" height="{h}" rx="6" fill="none" stroke="#21262D" stroke-width="1.2" class="theme-border" />
  <line x1="0" y1="0" x2="{w}" y2="0" stroke="#00F2FE" stroke-width="2" class="theme-cyan-stroke" />

  <!-- Corner Crosshairs -->
  <g stroke="#30363D" stroke-width="0.8" opacity="0.7" class="theme-border-accent">
    <path d="M 10 14 L 18 14 M 14 10 L 14 18" />
    <path d="M {w - 18} 14 L {w - 10} 14 M {w - 14} 10 L {w - 14} 18" />
    <path d="M 10 {h - 14} L 18 {h - 14} M 14 {h - 18} L 14 {h - 10}" />
    <path d="M {w - 18} {h - 14} L {w - 10} {h - 14} M {w - 14} {h - 18} L {w - 14} {h - 10}" />
  </g>

  <!-- ==================== LEFT COLUMN: EDITORIAL SPECS ==================== -->
  <g transform="translate(36, 32)">
    <g transform="translate(0, 0)">
      <circle cx="4" cy="4" r="3.5" fill="#00F2FE" class="theme-cyan-fill" />
      <text x="14" y="7" fill="#00F2FE" font-size="9" font-weight="700" letter-spacing="0.14em" class="mono theme-cyan-fill">SYSTEM 03 // SYSTEMS CONCURRENCY</text>
    </g>

    <!-- Main Title -->
    <text x="0" y="32" fill="#F8FAFC" font-size="22" font-weight="800" letter-spacing="0.02em" class="sans theme-text-head">
      BMD: BLACK MARLIN ACCELERATOR
    </text>
    <text x="0" y="48" fill="#94A3B8" font-size="11" font-weight="500" class="sans theme-text-body">
      Line-Rate Multi-Threaded Dynamic Byte Chunking Engine in Rust
    </text>

    <!-- 3 Telemetry Spec Chips -->
    <g transform="translate(0, 68)">
      <g transform="translate(0, 0)">
        <rect width="138" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">ASYNC RUNTIME</text>
        <text x="10" y="28" fill="#00F2FE" font-size="10.5" font-weight="700" class="mono theme-cyan-fill">RUST + TOKIO</text>
      </g>
      <g transform="translate(146, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">STREAM RESILIENCE</text>
        <text x="10" y="28" fill="#FF8C00" font-size="10.5" font-weight="700" class="mono theme-amber-fill">BINARY JOURNAL</text>
      </g>
      <g transform="translate(298, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">PROTOCOL INGEST</text>
        <text x="10" y="28" fill="#00E599" font-size="10.5" font-weight="700" class="mono theme-emerald-fill">HTTP / TORRENT</text>
      </g>
    </g>

    <!-- Verified Metric Box -->
    <g transform="translate(0, 122)">
      <rect width="442" height="34" rx="3" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <text x="12" y="16" fill="#94A3B8" font-size="8" font-weight="700" letter-spacing="0.1em" class="mono theme-text-body">BANDWIDTH SATURATION:</text>
      <text x="12" y="27" fill="#F8FAFC" font-size="9" font-weight="600" class="mono theme-text-head">
        LINE-RATE GIGABIT THROUGHPUT · CRASH-PROOF BINARY STATE RECOVERY
      </text>
    </g>

    <!-- Stack Footnote -->
    <text x="0" y="180" fill="#475569" font-size="9" font-weight="500" class="mono theme-text-dim">
      ENGINE: Rust 2024 · Tokio Channels · Dynamic Byte Allocator · Native Messaging Host
    </text>
  </g>

  <!-- ==================== RIGHT COLUMN: DYNAMIC CHUNKING LANES ==================== -->
  <g id="bmd-lanes" transform="translate(500, 32)">
    <rect width="344" height="196" rx="4" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
    <text x="12" y="18" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">
      PARALLEL BYTE-RANGE CHUNKING PIPELINES (SATURATION: 99.4%)
    </text>

    <!-- 4 Dynamic Chunk Stream Channels -->
    <!-- Lane 1 -->
    <g transform="translate(12, 32)">
      <text x="0" y="10" fill="#94A3B8" font-size="8" font-weight="600" class="mono theme-text-body">CH_01 [000-025%]</text>
      <rect x="90" y="2" width="230" height="12" rx="2" fill="#161B22" class="theme-elevated" />
      <rect x="90" y="2" width="180" height="12" rx="2" fill="url(#chunkGrad)" opacity="0.85" />
      <line x1="90" y1="8" x2="270" y2="8" stroke="#F8FAFC" stroke-width="1.5" stroke-dasharray="4 8" class="chunk-anim-1" />
    </g>

    <!-- Lane 2 -->
    <g transform="translate(12, 62)">
      <text x="0" y="10" fill="#94A3B8" font-size="8" font-weight="600" class="mono theme-text-body">CH_02 [025-050%]</text>
      <rect x="90" y="2" width="230" height="12" rx="2" fill="#161B22" class="theme-elevated" />
      <rect x="90" y="2" width="210" height="12" rx="2" fill="url(#chunkGrad)" opacity="0.85" />
      <line x1="90" y1="8" x2="300" y2="8" stroke="#F8FAFC" stroke-width="1.5" stroke-dasharray="4 8" class="chunk-anim-2" />
    </g>

    <!-- Lane 3 -->
    <g transform="translate(12, 92)">
      <text x="0" y="10" fill="#94A3B8" font-size="8" font-weight="600" class="mono theme-text-body">CH_03 [050-075%]</text>
      <rect x="90" y="2" width="230" height="12" rx="2" fill="#161B22" class="theme-elevated" />
      <rect x="90" y="2" width="160" height="12" rx="2" fill="url(#chunkGrad)" opacity="0.85" />
      <line x1="90" y1="8" x2="250" y2="8" stroke="#F8FAFC" stroke-width="1.5" stroke-dasharray="4 8" class="chunk-anim-3" />
    </g>

    <!-- Lane 4 -->
    <g transform="translate(12, 122)">
      <text x="0" y="10" fill="#94A3B8" font-size="8" font-weight="600" class="mono theme-text-body">CH_04 [075-100%]</text>
      <rect x="90" y="2" width="230" height="12" rx="2" fill="#161B22" class="theme-elevated" />
      <rect x="90" y="2" width="195" height="12" rx="2" fill="url(#chunkGrad)" opacity="0.85" />
      <line x1="90" y1="8" x2="285" y2="8" stroke="#F8FAFC" stroke-width="1.5" stroke-dasharray="4 8" class="chunk-anim-4" />
    </g>

    <!-- Live Telemetry Status Bar -->
    <g transform="translate(12, 154)">
      <rect width="320" height="26" rx="2" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <circle cx="12" cy="13" r="3" fill="#00E599" class="theme-emerald-fill" />
      <text x="22" y="17" fill="#F8FAFC" font-size="8.5" font-weight="600" class="mono theme-text-head">
        THROUGHPUT: 112.4 MB/S // RESUME JOURNAL: SYNCHRONIZED
      </text>
    </g>
  </g>
</svg>"""
    return svg

def generate_product_settlr():
    """Generates assets/profile/product_settlr.svg (880x260)"""
    w, h = 880, 260
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="settlrBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080B10" />
      <stop offset="60%" stop-color="#0D1117" />
      <stop offset="100%" stop-color="#07090E" />
    </linearGradient>
  </defs>

  <style>
{SHARED_CSS}
    .hash-flow {{ stroke-dasharray: 4 6; animation: dashStream 3s linear infinite; }}
    .pulse-ledger {{ animation: pulseGlow 2.8s ease-in-out infinite; }}
  </style>

  <!-- Canvas Surface -->
  <rect width="{w}" height="{h}" rx="6" fill="url(#settlrBg)" class="theme-bg" />
  <rect width="{w}" height="{h}" rx="6" fill="none" stroke="#21262D" stroke-width="1.2" class="theme-border" />
  <line x1="0" y1="0" x2="{w}" y2="0" stroke="#FF8C00" stroke-width="2" class="theme-amber-stroke" />

  <!-- Corner Crosshairs -->
  <g stroke="#30363D" stroke-width="0.8" opacity="0.7" class="theme-border-accent">
    <path d="M 10 14 L 18 14 M 14 10 L 14 18" />
    <path d="M {w - 18} 14 L {w - 10} 14 M {w - 14} 10 L {w - 14} 18" />
    <path d="M 10 {h - 14} L 18 {h - 14} M 14 {h - 18} L 14 {h - 10}" />
    <path d="M {w - 18} {h - 14} L {w - 10} {h - 14} M {w - 14} {h - 18} L {w - 14} {h - 10}" />
  </g>

  <!-- ==================== LEFT COLUMN: EDITORIAL SPECS ==================== -->
  <g transform="translate(36, 32)">
    <g transform="translate(0, 0)">
      <circle cx="4" cy="4" r="3.5" fill="#FF8C00" class="theme-amber-fill" />
      <text x="14" y="7" fill="#FF8C00" font-size="9" font-weight="700" letter-spacing="0.14em" class="mono theme-amber-fill">SYSTEM 04 // CRYPTOGRAPHIC TRUST</text>
    </g>

    <!-- Main Title -->
    <text x="0" y="32" fill="#F8FAFC" font-size="22" font-weight="800" letter-spacing="0.02em" class="sans theme-text-head">
      SETTLR: DUAL-CONSENT RENTAL ESCROW
    </text>
    <text x="0" y="48" fill="#94A3B8" font-size="11" font-weight="500" class="sans theme-text-body">
      Ownership-Gated Rental Trust Platform Neutralizing Broker Asymmetry
    </text>

    <!-- 3 Telemetry Spec Chips -->
    <g transform="translate(0, 68)">
      <g transform="translate(0, 0)">
        <rect width="138" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">IMMUTABLE RECORD</text>
        <text x="10" y="28" fill="#FF8C00" font-size="10.5" font-weight="700" class="mono theme-amber-fill">SHA-256 LEDGER</text>
      </g>
      <g transform="translate(146, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">OWNERSHIP MOAT</text>
        <text x="10" y="28" fill="#00E599" font-size="10.5" font-weight="700" class="mono theme-emerald-fill">MUNICIPAL DEED</text>
      </g>
      <g transform="translate(298, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">FUNDS SECURITY</text>
        <text x="10" y="28" fill="#00F2FE" font-size="10.5" font-weight="700" class="mono theme-cyan-fill">ZERO CUSTODY</text>
      </g>
    </g>

    <!-- Target Rollout Cluster Box -->
    <g transform="translate(0, 122)">
      <rect width="442" height="34" rx="3" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <text x="12" y="16" fill="#94A3B8" font-size="8" font-weight="700" letter-spacing="0.1em" class="mono theme-text-body">TARGET LAUNCH METROPOLIS:</text>
      <text x="12" y="27" fill="#F8FAFC" font-size="9" font-weight="600" class="mono theme-text-head">
        DELHI NCR CLUSTER · SAKET · HAUZ KHAS · GK · VASANT KUNJ
      </text>
    </g>

    <!-- Stack Footnote -->
    <text x="0" y="180" fill="#475569" font-size="9" font-weight="500" class="mono theme-text-dim">
      SECURITY: Tamper-Evident Hash Chain · Dual Cryptographic Co-Signatures · Fail-Closed
    </text>
  </g>

  <!-- ==================== RIGHT COLUMN: SHA-256 BLOCKCHAIN SCHEMATIC ==================== -->
  <g id="settlr-blocks" transform="translate(500, 32)">
    <rect width="344" height="196" rx="4" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
    <text x="12" y="18" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">
      APPEND-ONLY DUAL-CONSENT BLOCK CHAIN (TAMPER DETECTION: ACTIVE)
    </text>

    <!-- Block 1084 -->
    <g transform="translate(14, 34)">
      <rect width="144" height="66" rx="3" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <text x="10" y="16" fill="#FF8C00" font-size="8.5" font-weight="700" class="mono theme-amber-fill">BLOCK #1084 [LEASE]</text>
      <text x="10" y="30" fill="#94A3B8" font-size="7.5" font-weight="500" class="mono theme-text-body">PREV: 0x8a2f4c1e</text>
      <text x="10" y="42" fill="#00E599" font-size="7.5" font-weight="600" class="mono theme-emerald-fill">SIGN: TENANT + OWNER</text>
      <text x="10" y="54" fill="#475569" font-size="7" font-weight="500" class="mono theme-text-dim">DEED: DIGILOCKER VERIFIED</text>
    </g>

    <!-- Hash Pointer Arrow 1 to 2 -->
    <line x1="158" y1="67" x2="186" y2="67" stroke="#FF8C00" stroke-width="1.2" class="hash-flow theme-amber-stroke" />

    <!-- Block 1085 -->
    <g transform="translate(186, 34)">
      <rect width="144" height="66" rx="3" fill="#161B22" stroke="#00E599" stroke-width="1" class="theme-elevated theme-emerald-stroke" />
      <text x="10" y="16" fill="#00E599" font-size="8.5" font-weight="700" class="mono theme-emerald-fill">BLOCK #1085 [ESCROW]</text>
      <text x="10" y="30" fill="#94A3B8" font-size="7.5" font-weight="500" class="mono theme-text-body">PREV: 0xb73d810a</text>
      <text x="10" y="42" fill="#00F2FE" font-size="7.5" font-weight="600" class="mono theme-cyan-fill">STATUS: MILESTONE LOCKED</text>
      <text x="10" y="54" fill="#475569" font-size="7" font-weight="500" class="mono theme-text-dim">CLAIM: DUAL-KEY REQUIRED</text>
    </g>

    <!-- Verification Audit Banner -->
    <g transform="translate(14, 114)">
      <rect width="316" height="66" rx="3" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <circle cx="14" cy="18" r="4" fill="#00E599" class="pulse-ledger theme-emerald-fill" />
      <text x="26" y="21" fill="#F8FAFC" font-size="9" font-weight="700" class="mono theme-text-head">
        CRYPTOGRAPHIC INTEGRITY: 100% UNBROKEN
      </text>
      <text x="14" y="38" fill="#94A3B8" font-size="7.5" font-weight="500" class="mono theme-text-body">
        • Zero chain fracture detected across all recorded transactions
      </text>
      <text x="14" y="52" fill="#94A3B8" font-size="7.5" font-weight="500" class="mono theme-text-body">
        • Direct municipal record validation neutralizes ghost broker listings
      </text>
    </g>
  </g>
</svg>"""
    return svg

def generate_product_sportshawk():
    """Generates assets/profile/product_sportshawk.svg (880x260)"""
    w, h = 880, 260
    
    # 2D Kinematic Skeleton Points (x, y)
    kx, ky = 660, 125
    # Head, Shoulders, Elbows, Hands, Hips, Knees, Feet
    joints = {
        "head": (kx, ky - 60),
        "neck": (kx, ky - 45),
        "r_shoulder": (kx - 22, ky - 40),
        "l_shoulder": (kx + 22, ky - 40),
        "r_elbow": (kx - 34, ky - 20),
        "l_elbow": (kx + 36, ky - 18),
        "r_wrist": (kx - 42, ky + 2),
        "l_wrist": (kx + 44, ky + 4),
        "pelvis": (kx, ky - 5),
        "r_hip": (kx - 16, ky - 5),
        "l_hip": (kx + 16, ky - 5),
        "r_knee": (kx - 26, ky + 30),
        "l_knee": (kx + 24, ky + 34),
        "r_ankle": (kx - 32, ky + 65),
        "l_ankle": (kx + 30, ky + 70)
    }

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="shBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080B10" />
      <stop offset="60%" stop-color="#0D1117" />
      <stop offset="100%" stop-color="#05080D" />
    </linearGradient>
  </defs>

  <style>
{SHARED_CSS}
    .pulse-joint {{ animation: pulseGlow 2s ease-in-out infinite; }}
  </style>

  <!-- Canvas Surface -->
  <rect width="{w}" height="{h}" rx="6" fill="url(#shBg)" class="theme-bg" />
  <rect width="{w}" height="{h}" rx="6" fill="none" stroke="#21262D" stroke-width="1.2" class="theme-border" />
  <line x1="0" y1="0" x2="{w}" y2="0" stroke="#00F2FE" stroke-width="2" class="theme-cyan-stroke" />

  <!-- Corner Crosshairs -->
  <g stroke="#30363D" stroke-width="0.8" opacity="0.7" class="theme-border-accent">
    <path d="M 10 14 L 18 14 M 14 10 L 14 18" />
    <path d="M {w - 18} 14 L {w - 10} 14 M {w - 14} 10 L {w - 14} 18" />
    <path d="M 10 {h - 14} L 18 {h - 14} M 14 {h - 18} L 14 {h - 10}" />
    <path d="M {w - 18} {h - 14} L {w - 10} {h - 14} M {w - 14} {h - 18} L {w - 14} {h - 10}" />
  </g>

  <!-- ==================== LEFT COLUMN: EDITORIAL SPECS ==================== -->
  <g transform="translate(36, 32)">
    <g transform="translate(0, 0)">
      <circle cx="4" cy="4" r="3.5" fill="#00F2FE" class="theme-cyan-fill" />
      <text x="14" y="7" fill="#00F2FE" font-size="9" font-weight="700" letter-spacing="0.14em" class="mono theme-cyan-fill">SYSTEM 05 // EDGE COMPUTER VISION</text>
    </g>

    <!-- Main Title -->
    <text x="0" y="32" fill="#F8FAFC" font-size="22" font-weight="800" letter-spacing="0.02em" class="sans theme-text-head">
      SPORTSHAWK: GRASSROOTS FOOTBALL CV
    </text>
    <text x="0" y="48" fill="#94A3B8" font-size="11" font-weight="500" class="sans theme-text-body">
      100% On-Device Kinematic Tracking &amp; Verified Scout Discovery Cards
    </text>

    <!-- 3 Telemetry Spec Chips -->
    <g transform="translate(0, 68)">
      <g transform="translate(0, 0)">
        <rect width="138" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">PROCESSING EDGE</text>
        <text x="10" y="28" fill="#00F2FE" font-size="10.5" font-weight="700" class="mono theme-cyan-fill">60 FPS ON-DEVICE</text>
      </g>
      <g transform="translate(146, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">CLOUD OVERHEAD</text>
        <text x="10" y="28" fill="#00E599" font-size="10.5" font-weight="700" class="mono theme-emerald-fill">ZERO GPU OVERHEAD</text>
      </g>
      <g transform="translate(298, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">PRIVACY BY DESIGN</text>
        <text x="10" y="28" fill="#FF8C00" font-size="10.5" font-weight="700" class="mono theme-amber-fill">NO VIDEO UPLOAD</text>
      </g>
    </g>

    <!-- Grassroots Invariant Box -->
    <g transform="translate(0, 122)">
      <rect width="442" height="34" rx="3" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <text x="12" y="16" fill="#94A3B8" font-size="8" font-weight="700" letter-spacing="0.1em" class="mono theme-text-body">ACCESSIBILITY &amp; LOCALIZATION:</text>
      <text x="12" y="27" fill="#F8FAFC" font-size="9" font-weight="600" class="mono theme-text-head">
        9 INDIAN REGIONAL LANGUAGES · ZERO SUBSCRIPTION FEES · PURE PUBLIC GOOD
      </text>
    </g>

    <!-- Stack Footnote -->
    <text x="0" y="180" fill="#475569" font-size="9" font-weight="500" class="mono theme-text-dim">
      TECHNOLOGY: MediaPipe Edge · Apple Vision Framework · React 19 · DPDP Child Safety
    </text>
  </g>

  <!-- ==================== RIGHT COLUMN: POSE KINEMATICS & HUD ==================== -->
  <g id="sportshawk-hud" transform="translate(500, 24)">
    <rect width="344" height="204" rx="4" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
    <text x="12" y="18" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">
      EDGE COMPUTER VISION KINEMATIC POSE ESTIMATION (60 FPS)
    </text>

    <!-- Bounding Tracking Box -->
    <rect x="{kx - 55}" y="{ky - 75}" width="110" height="155" rx="3" fill="none" stroke="#00F2FE" stroke-width="0.8" stroke-dasharray="3 3" opacity="0.6" class="theme-cyan-stroke" />
    <text x="{kx - 50}" y="{ky - 66}" fill="#00F2FE" font-size="7" font-weight="600" class="mono theme-cyan-fill">TARGET: ATHLETE_01</text>

    <!-- Skeleton Bones -->
    <g stroke="#00F2FE" stroke-width="1.5" opacity="0.85" class="theme-cyan-stroke">
      <!-- Spine -->
      <line x1="{joints['head'][0]}" y1="{joints['head'][1]}" x2="{joints['neck'][0]}" y2="{joints['neck'][1]}" />
      <line x1="{joints['neck'][0]}" y1="{joints['neck'][1]}" x2="{joints['pelvis'][0]}" y2="{joints['pelvis'][1]}" />
      <!-- Arms -->
      <line x1="{joints['neck'][0]}" y1="{joints['neck'][1]}" x2="{joints['r_shoulder'][0]}" y2="{joints['r_shoulder'][1]}" />
      <line x1="{joints['neck'][0]}" y1="{joints['neck'][1]}" x2="{joints['l_shoulder'][0]}" y2="{joints['l_shoulder'][1]}" />
      <line x1="{joints['r_shoulder'][0]}" y1="{joints['r_shoulder'][1]}" x2="{joints['r_elbow'][0]}" y2="{joints['r_elbow'][1]}" />
      <line x1="{joints['l_shoulder'][0]}" y1="{joints['l_shoulder'][1]}" x2="{joints['l_elbow'][0]}" y2="{joints['l_elbow'][1]}" />
      <line x1="{joints['r_elbow'][0]}" y1="{joints['r_elbow'][1]}" x2="{joints['r_wrist'][0]}" y2="{joints['r_wrist'][1]}" />
      <line x1="{joints['l_elbow'][0]}" y1="{joints['l_elbow'][1]}" x2="{joints['l_wrist'][0]}" y2="{joints['l_wrist'][1]}" />
      <!-- Legs -->
      <line x1="{joints['pelvis'][0]}" y1="{joints['pelvis'][1]}" x2="{joints['r_hip'][0]}" y2="{joints['r_hip'][1]}" />
      <line x1="{joints['pelvis'][0]}" y1="{joints['pelvis'][1]}" x2="{joints['l_hip'][0]}" y2="{joints['l_hip'][1]}" />
      <line x1="{joints['r_hip'][0]}" y1="{joints['r_hip'][1]}" x2="{joints['r_knee'][0]}" y2="{joints['r_knee'][1]}" />
      <line x1="{joints['l_hip'][0]}" y1="{joints['l_hip'][1]}" x2="{joints['l_knee'][0]}" y2="{joints['l_knee'][1]}" />
      <line x1="{joints['r_knee'][0]}" y1="{joints['r_knee'][1]}" x2="{joints['r_ankle'][0]}" y2="{joints['r_ankle'][1]}" />
      <line x1="{joints['l_knee'][0]}" y1="{joints['l_knee'][1]}" x2="{joints['l_ankle'][0]}" y2="{joints['l_ankle'][1]}" />
    </g>

    <!-- Joint Markers -->
    <g class="pulse-joint">
"""
    for j_name, (jx, jy) in joints.items():
        r = 3.5 if j_name in ["head", "pelvis"] else 2.5
        svg += f'      <circle cx="{jx}" cy="{jy}" r="{r}" fill="#FF8C00" />\n'

    svg += f"""    </g>

    <!-- Velocity Vector Arrow -->
    <line x1="{joints['r_ankle'][0]}" y1="{joints['r_ankle'][1]}" x2="{joints['r_ankle'][0] + 24}" y2="{joints['r_ankle'][1] - 8}" stroke="#00E599" stroke-width="1.5" class="theme-emerald-stroke" />
    <circle cx="{joints['r_ankle'][0] + 24}" cy="{joints['r_ankle'][1] - 8}" r="2" fill="#00E599" class="theme-emerald-fill" />

    <!-- Telemetry Readouts -->
    <g transform="translate(14, 168)">
      <rect width="316" height="24" rx="2" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <text x="12" y="16" fill="#F8FAFC" font-size="8" font-weight="600" class="mono theme-text-head">
        CADENCE: 184 BPM // STABILITY: 98.4% // VELOCITY: 6.2 M/S
      </text>
    </g>
  </g>
</svg>"""
    return svg

def generate_product_formspear():
    """Generates assets/profile/product_formspear.svg (880x260)"""
    w, h = 880, 260
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="fsBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080B10" />
      <stop offset="60%" stop-color="#0D1117" />
      <stop offset="100%" stop-color="#06090D" />
    </linearGradient>
  </defs>

  <style>
{SHARED_CSS}
    .flow-sync {{ stroke-dasharray: 4 6; animation: dashStream 2.4s linear infinite; }}
  </style>

  <!-- Canvas Surface -->
  <rect width="{w}" height="{h}" rx="6" fill="url(#fsBg)" class="theme-bg" />
  <rect width="{w}" height="{h}" rx="6" fill="none" stroke="#21262D" stroke-width="1.2" class="theme-border" />
  <line x1="0" y1="0" x2="{w}" y2="0" stroke="#00E599" stroke-width="2" class="theme-emerald-stroke" />

  <!-- Corner Crosshairs -->
  <g stroke="#30363D" stroke-width="0.8" opacity="0.7" class="theme-border-accent">
    <path d="M 10 14 L 18 14 M 14 10 L 14 18" />
    <path d="M {w - 18} 14 L {w - 10} 14 M {w - 14} 10 L {w - 14} 18" />
    <path d="M 10 {h - 14} L 18 {h - 14} M 14 {h - 18} L 14 {h - 10}" />
    <path d="M {w - 18} {h - 14} L {w - 10} {h - 14} M {w - 14} {h - 18} L {w - 14} {h - 10}" />
  </g>

  <!-- ==================== LEFT COLUMN: EDITORIAL SPECS ==================== -->
  <g transform="translate(36, 32)">
    <g transform="translate(0, 0)">
      <circle cx="4" cy="4" r="3.5" fill="#00E599" class="theme-emerald-fill" />
      <text x="14" y="7" fill="#00E599" font-size="9" font-weight="700" letter-spacing="0.14em" class="mono theme-emerald-fill">SYSTEM 06 // RELATIONAL RIGOR &amp; TELEMETRY</text>
    </g>

    <!-- Main Title -->
    <text x="0" y="32" fill="#F8FAFC" font-size="22" font-weight="800" letter-spacing="0.02em" class="sans theme-text-head">
      FORMSPEAR: ZERO-FRAMEWORK SURVEY OS
    </text>
    <text x="0" y="48" fill="#94A3B8" font-size="11" font-weight="500" class="sans theme-text-body">
      Dual-Store Architecture with 39-Table Postgres Schema &amp; Sub-12ms Dispatch
    </text>

    <!-- 3 Telemetry Spec Chips -->
    <g transform="translate(0, 68)">
      <g transform="translate(0, 0)">
        <rect width="138" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">RUNTIME DESIGN</text>
        <text x="10" y="28" fill="#00E599" font-size="10.5" font-weight="700" class="mono theme-emerald-fill">BARE NODE 20</text>
      </g>
      <g transform="translate(146, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">LATENCY PROFILE</text>
        <text x="10" y="28" fill="#00F2FE" font-size="10.5" font-weight="700" class="mono theme-cyan-fill">&lt; 1MS CACHE READ</text>
      </g>
      <g transform="translate(298, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">RELATIONAL RIGOR</text>
        <text x="10" y="28" fill="#FF8C00" font-size="10.5" font-weight="700" class="mono theme-amber-fill">39 SQL TABLES</text>
      </g>
    </g>

    <!-- Benchmark Load-Test Box -->
    <g transform="translate(0, 122)">
      <rect width="442" height="34" rx="3" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <text x="12" y="16" fill="#94A3B8" font-size="8" font-weight="700" letter-spacing="0.1em" class="mono theme-text-body">BENCHMARK PERFORMANCE VERIFIED:</text>
      <text x="12" y="27" fill="#F8FAFC" font-size="9" font-weight="600" class="mono theme-text-head">
        100,000 SYNTHETIC RESPONSES · SUB-12MS WEBHOOK ROUTING · ZERO-TRUST EICAR
      </text>
    </g>

    <!-- Stack Footnote -->
    <text x="0" y="180" fill="#475569" font-size="9" font-weight="500" class="mono theme-text-dim">
      ENGINE: Node.js 20 (node:http) · PostgreSQL 15 · Redis · BullMQ · Single-Writer Locks
    </text>
  </g>

  <!-- ==================== RIGHT COLUMN: DUAL-STORE CACHE & POSTGRES PIPELINE ==================== -->
  <g id="formspear-pipeline" transform="translate(500, 30)">
    <rect width="344" height="200" rx="4" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
    <text x="12" y="18" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">
      DUAL-STORE ARCHITECTURE // MEMORY &lt;-&gt; POSTGRES
    </text>

    <!-- Top In-Memory Cache Tier -->
    <g transform="translate(14, 32)">
      <rect width="316" height="42" rx="3" fill="#161B22" stroke="#00E599" stroke-width="1" class="theme-elevated theme-emerald-stroke" />
      <text x="12" y="17" fill="#00E599" font-size="9" font-weight="700" class="mono theme-emerald-fill">SYNCHRONOUS IN-MEMORY COLLECTION CACHE</text>
      <text x="12" y="32" fill="#F8FAFC" font-size="8" font-weight="500" class="mono theme-text-head">
        Guarantees &lt;1ms Read/Write Burst Latency // Single-Writer Queue
      </text>
    </g>

    <!-- Async Sync Pipe -->
    <g transform="translate(172, 74)">
      <line x1="0" y1="0" x2="0" y2="24" stroke="#00E599" stroke-width="1.5" class="flow-sync theme-emerald-stroke" />
      <text x="8" y="14" fill="#94A3B8" font-size="7.5" font-weight="600" class="mono theme-text-body">ASYNC DIFF (ADVISORY LOCKS)</text>
    </g>

    <!-- Bottom Relational Database Tier -->
    <g transform="translate(14, 98)">
      <rect width="316" height="52" rx="3" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <text x="12" y="18" fill="#F8FAFC" font-size="9" font-weight="700" class="mono theme-text-head">POSTGRESQL RELATIONAL GROUND TRUTH</text>
      <text x="12" y="32" fill="#94A3B8" font-size="7.5" font-weight="500" class="mono theme-text-body">
        39 Normalized Tables · 13 Partial &amp; Compound Indexes · Zero Framework Bloat
      </text>
      <text x="12" y="44" fill="#00F2FE" font-size="7.5" font-weight="600" class="mono theme-cyan-fill">
        SUB-12MS DISPATCH: WHATSAPP · SLACK · HMAC WEBHOOKS
      </text>
    </g>

    <!-- Status Readout -->
    <g transform="translate(14, 160)">
      <rect width="316" height="26" rx="2" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <circle cx="12" cy="13" r="3" fill="#00E599" class="theme-emerald-fill" />
      <text x="22" y="17" fill="#F8FAFC" font-size="8" font-weight="600" class="mono theme-text-head">
        QUARANTINE PIPELINE: ZERO-TRUST EICAR PASS // REVISION STACKS: READY
      </text>
    </g>
  </g>
</svg>"""
    return svg

def generate_product_xanalgo():
    """Generates assets/profile/product_xanalgo.svg (880x260)"""
    w, h = 880, 260
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="xaBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080B10" />
      <stop offset="60%" stop-color="#0D1117" />
      <stop offset="100%" stop-color="#06080D" />
    </linearGradient>
  </defs>

  <style>
{SHARED_CSS}
    .flow-trade {{ stroke-dasharray: 4 6; animation: dashStream 2s linear infinite; }}
  </style>

  <!-- Canvas Surface -->
  <rect width="{w}" height="{h}" rx="6" fill="url(#xaBg)" class="theme-bg" />
  <rect width="{w}" height="{h}" rx="6" fill="none" stroke="#21262D" stroke-width="1.2" class="theme-border" />
  <line x1="0" y1="0" x2="{w}" y2="0" stroke="#A855F7" stroke-width="2" class="theme-violet-stroke" />

  <!-- Corner Crosshairs -->
  <g stroke="#30363D" stroke-width="0.8" opacity="0.7" class="theme-border-accent">
    <path d="M 10 14 L 18 14 M 14 10 L 14 18" />
    <path d="M {w - 18} 14 L {w - 10} 14 M {w - 14} 10 L {w - 14} 18" />
    <path d="M 10 {h - 14} L 18 {h - 14} M 14 {h - 18} L 14 {h - 10}" />
    <path d="M {w - 18} {h - 14} L {w - 10} {h - 14} M {w - 14} {h - 18} L {w - 14} {h - 10}" />
  </g>

  <!-- ==================== LEFT COLUMN: EDITORIAL SPECS ==================== -->
  <g transform="translate(36, 32)">
    <g transform="translate(0, 0)">
      <circle cx="4" cy="4" r="3.5" fill="#A855F7" class="theme-violet-fill" />
      <text x="14" y="7" fill="#A855F7" font-size="9" font-weight="700" letter-spacing="0.14em" class="mono theme-violet-fill">SYSTEM 07 // QUANTITATIVE EXECUTION</text>
    </g>

    <!-- Main Title -->
    <text x="0" y="32" fill="#F8FAFC" font-size="22" font-weight="800" letter-spacing="0.02em" class="sans theme-text-head">
      XENALGO: DETERMINISTIC NSE TRADING
    </text>
    <text x="0" y="48" fill="#94A3B8" font-size="11" font-weight="500" class="sans theme-text-body">
      Guarded Algorithmic Swing Execution with Pre-Flight Risk Veto Layer
    </text>

    <!-- 3 Telemetry Spec Chips -->
    <g transform="translate(0, 68)">
      <g transform="translate(0, 0)">
        <rect width="138" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">SAFETY ARCHITECTURE</text>
        <text x="10" y="28" fill="#A855F7" font-size="10.5" font-weight="700" class="mono theme-violet-fill">RISK VETO LAYER</text>
      </g>
      <g transform="translate(146, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">STATE MUTATION</text>
        <text x="10" y="28" fill="#00E599" font-size="10.5" font-weight="700" class="mono theme-emerald-fill">FILLS ARE TRUTH</text>
      </g>
      <g transform="translate(298, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">REGULATORY GOVERNOR</text>
        <text x="10" y="28" fill="#FF8C00" font-size="10.5" font-weight="700" class="mono theme-amber-fill">SEBI 2 ORD/SEC</text>
      </g>
    </g>

    <!-- Chaos Invariant Box -->
    <g transform="translate(0, 122)">
      <rect width="442" height="34" rx="3" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <text x="12" y="16" fill="#94A3B8" font-size="8" font-weight="700" letter-spacing="0.1em" class="mono theme-text-body">CHAOS HARDENING &amp; RECONCILIATION:</text>
      <text x="12" y="27" fill="#F8FAFC" font-size="9" font-weight="600" class="mono theme-text-head">
        REPLAYABLE SQLITE EVENT JOURNAL · CRASH RESILIENT · BROKER DRIFT REPAIR
      </text>
    </g>

    <!-- Stack Footnote -->
    <text x="0" y="180" fill="#475569" font-size="9" font-weight="500" class="mono theme-text-dim">
      INTEGRATION: Python 3.12 · Fyers API v3 · SQLite Journal · Hard Rate Governor
    </text>
  </g>

  <!-- ==================== RIGHT COLUMN: RISK PIPELINE & TELEMETRY ==================== -->
  <g id="xanalgo-hud" transform="translate(500, 30)">
    <rect width="344" height="200" rx="4" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
    <text x="12" y="18" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">
      ORDER EXECUTION VETO PIPELINE // 0 SPECULATIVE FILLS
    </text>

    <!-- Pipeline Stages -->
    <g transform="translate(14, 34)">
      <!-- Stage 1: Signal -->
      <rect x="0" y="0" width="68" height="32" rx="2" fill="#161B22" stroke="#A855F7" stroke-width="0.8" class="theme-elevated theme-violet-stroke" />
      <text x="34" y="15" fill="#F8FAFC" font-size="7.5" font-weight="600" text-anchor="middle" class="mono theme-text-head">Algorithmic</text>
      <text x="34" y="25" fill="#A855F7" font-size="7.5" font-weight="700" text-anchor="middle" class="mono theme-violet-fill">Signal</text>

      <line x1="68" y1="16" x2="80" y2="16" stroke="#A855F7" stroke-width="1" class="theme-violet-stroke" />

      <!-- Stage 2: RiskEngine -->
      <rect x="80" y="0" width="84" height="32" rx="2" fill="#161B22" stroke="#FF8C00" stroke-width="0.8" class="theme-elevated theme-amber-stroke" />
      <text x="122" y="15" fill="#F8FAFC" font-size="7.5" font-weight="600" text-anchor="middle" class="mono theme-text-head">RiskEngine</text>
      <text x="122" y="25" fill="#FF8C00" font-size="7.5" font-weight="700" text-anchor="middle" class="mono theme-amber-fill">check() VETO</text>

      <line x1="164" y1="16" x2="176" y2="16" stroke="#FF8C00" stroke-width="1" class="theme-amber-stroke" />

      <!-- Stage 3: Rate Governor -->
      <rect x="176" y="0" width="66" height="32" rx="2" fill="#161B22" stroke="#00F2FE" stroke-width="0.8" class="theme-elevated theme-cyan-stroke" />
      <text x="209" y="15" fill="#F8FAFC" font-size="7.5" font-weight="600" text-anchor="middle" class="mono theme-text-head">SEBI Rate</text>
      <text x="209" y="25" fill="#00F2FE" font-size="7.5" font-weight="700" text-anchor="middle" class="mono theme-cyan-fill">Governor</text>

      <line x1="242" y1="16" x2="254" y2="16" stroke="#00F2FE" stroke-width="1" class="theme-cyan-stroke" />

      <!-- Stage 4: Broker Socket -->
      <rect x="254" y="0" width="64" height="32" rx="2" fill="#161B22" stroke="#00E599" stroke-width="0.8" class="theme-elevated theme-emerald-stroke" />
      <text x="286" y="15" fill="#F8FAFC" font-size="7.5" font-weight="600" text-anchor="middle" class="mono theme-text-head">Broker</text>
      <text x="286" y="25" fill="#00E599" font-size="7.5" font-weight="700" text-anchor="middle" class="mono theme-emerald-fill">Socket</text>
    </g>

    <!-- Synthetic Candlestick Strip -->
    <g transform="translate(14, 82)">
      <rect width="316" height="64" rx="3" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <!-- Candlesticks -->
      <line x1="40" y1="12" x2="40" y2="52" stroke="#00E599" stroke-width="1" />
      <rect x="36" y="20" width="8" height="24" fill="#00E599" />
      <line x1="80" y1="18" x2="80" y2="58" stroke="#FF5555" stroke-width="1" />
      <rect x="76" y="28" width="8" height="18" fill="#FF5555" />
      <line x1="120" y1="8" x2="120" y2="48" stroke="#00E599" stroke-width="1" />
      <rect x="116" y="14" width="8" height="26" fill="#00E599" />
      <line x1="160" y1="14" x2="160" y2="50" stroke="#00E599" stroke-width="1" />
      <rect x="156" y="20" width="8" height="20" fill="#00E599" />
      <line x1="200" y1="10" x2="200" y2="46" stroke="#00E599" stroke-width="1" />
      <rect x="196" y="16" width="8" height="22" fill="#00E599" />

      <!-- Execution Marker -->
      <circle cx="200" cy="16" r="4" fill="#00F2FE" />
      <text x="210" y="20" fill="#00F2FE" font-size="7.5" font-weight="700" class="mono theme-cyan-fill">BUY_FILL @ 24,180.50</text>
    </g>

    <!-- State Journal Footer -->
    <g transform="translate(14, 158)">
      <rect width="316" height="26" rx="2" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <circle cx="12" cy="13" r="3" fill="#A855F7" class="theme-violet-fill" />
      <text x="22" y="17" fill="#F8FAFC" font-size="8" font-weight="600" class="mono theme-text-head">
        REPLAY JOURNAL: 1,420 AUDITED EVENTS // DRIFT: 0.00%
      </text>
    </g>
  </g>
</svg>"""
    return svg

def generate_product_candy_drop():
    """Generates assets/profile/product_candy_drop.svg (880x260)"""
    w, h = 880, 260
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="candyBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080B10" />
      <stop offset="60%" stop-color="#0D1117" />
      <stop offset="100%" stop-color="#05070B" />
    </linearGradient>
  </defs>

  <style>
{SHARED_CSS}
    .pulse-arcade {{ animation: pulseGlow 1.8s ease-in-out infinite; }}
  </style>

  <!-- Canvas Surface -->
  <rect width="{w}" height="{h}" rx="6" fill="url(#candyBg)" class="theme-bg" />
  <rect width="{w}" height="{h}" rx="6" fill="none" stroke="#21262D" stroke-width="1.2" class="theme-border" />
  <line x1="0" y1="0" x2="{w}" y2="0" stroke="#FF8C00" stroke-width="2" class="theme-amber-stroke" />

  <!-- Corner Crosshairs -->
  <g stroke="#30363D" stroke-width="0.8" opacity="0.7" class="theme-border-accent">
    <path d="M 10 14 L 18 14 M 14 10 L 14 18" />
    <path d="M {w - 18} 14 L {w - 10} 14 M {w - 14} 10 L {w - 14} 18" />
    <path d="M 10 {h - 14} L 18 {h - 14} M 14 {h - 18} L 14 {h - 10}" />
    <path d="M {w - 18} {h - 14} L {w - 10} {h - 14} M {w - 14} {h - 18} L {w - 14} {h - 10}" />
  </g>

  <!-- ==================== LEFT COLUMN: EDITORIAL SPECS ==================== -->
  <g transform="translate(36, 32)">
    <g transform="translate(0, 0)">
      <circle cx="4" cy="4" r="3.5" fill="#FF8C00" class="theme-amber-fill" />
      <text x="14" y="7" fill="#FF8C00" font-size="9" font-weight="700" letter-spacing="0.14em" class="mono theme-amber-fill">SYSTEM 08 // PURE WEB STANDARDS &amp; GRAPHICS</text>
    </g>

    <!-- Main Title -->
    <text x="0" y="32" fill="#F8FAFC" font-size="22" font-weight="800" letter-spacing="0.02em" class="sans theme-text-head">
      CANDY ARCADE: 100 PLAYABLE GAMES
    </text>
    <text x="0" y="48" fill="#94A3B8" font-size="11" font-weight="500" class="sans theme-text-body">
      Zero-Dependency HTML5 Canvas 2D Engine with Procedural Web Audio Synth
    </text>

    <!-- 3 Telemetry Spec Chips -->
    <g transform="translate(0, 68)">
      <g transform="translate(0, 0)">
        <rect width="138" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">BUNDLE OVERHEAD</text>
        <text x="10" y="28" fill="#00E599" font-size="10.5" font-weight="700" class="mono theme-emerald-fill">0 KB LIBRARIES</text>
      </g>
      <g transform="translate(146, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">AUDIO RUNTIME</text>
        <text x="10" y="28" fill="#00F2FE" font-size="10.5" font-weight="700" class="mono theme-cyan-fill">PROCEDURAL SYNTH</text>
      </g>
      <g transform="translate(298, 0)">
        <rect width="144" height="38" rx="3" fill="#0D1117" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />
        <text x="10" y="15" fill="#475569" font-size="7.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-dim">FRAMERATE BUDGET</text>
        <text x="10" y="28" fill="#FF8C00" font-size="10.5" font-weight="700" class="mono theme-amber-fill">60 FPS CANVAS</text>
      </g>
    </g>

    <!-- Longevity Manifesto Box -->
    <g transform="translate(0, 122)">
      <rect width="442" height="34" rx="3" fill="#161B22" stroke="#21262D" stroke-width="0.8" class="theme-elevated theme-border" />
      <text x="12" y="16" fill="#94A3B8" font-size="8" font-weight="700" letter-spacing="0.1em" class="mono theme-text-body">SOFTWARE LONGEVITY MANIFESTO:</text>
      <text x="12" y="27" fill="#F8FAFC" font-size="9" font-weight="600" class="mono theme-text-head">
        100 GAMES · ZERO INSTALL · 0 EXTERNAL ASSETS · BUILT TO LAST DECADES
      </text>
    </g>

    <!-- Stack Footnote -->
    <text x="0" y="180" fill="#475569" font-size="9" font-weight="500" class="mono theme-text-dim">
      PURE STANDARDS: Vanilla JS · Canvas 2D Context · Web Audio API · UTC PRNG Seeded Dailies
    </text>
  </g>

  <!-- ==================== RIGHT COLUMN: RETRO CRT BEZEL & PARTICLE ENGINE ==================== -->
  <g id="candy-bezel" transform="translate(500, 26)">
    <!-- CRT Bezel -->
    <rect width="344" height="204" rx="8" fill="#05070A" stroke="#30363D" stroke-width="1.5" class="theme-border-accent" />
    <rect x="8" y="8" width="328" height="188" rx="4" fill="#0A0E14" stroke="#21262D" stroke-width="0.8" class="theme-card theme-border" />

    <!-- Scanline Simulation Grid -->
    <line x1="8" y1="40" x2="336" y2="40" stroke="#151926" stroke-width="0.5" class="theme-grid" />
    <line x1="8" y1="70" x2="336" y2="70" stroke="#151926" stroke-width="0.5" class="theme-grid" />
    <line x1="8" y1="100" x2="336" y2="100" stroke="#151926" stroke-width="0.5" class="theme-grid" />
    <line x1="8" y1="130" x2="336" y2="130" stroke="#151926" stroke-width="0.5" class="theme-grid" />
    <line x1="8" y1="160" x2="336" y2="160" stroke="#151926" stroke-width="0.5" class="theme-grid" />

    <!-- Top Bezel Telemetry -->
    <text x="20" y="24" fill="#00E599" font-size="8" font-weight="700" letter-spacing="0.12em" class="mono theme-emerald-fill">
      CANDY_ARCADE // VIRTUAL: 960x600 [DPR: 2X]
    </text>
    <text x="320" y="24" fill="#FF8C00" font-size="8" font-weight="700" text-anchor="end" class="mono theme-amber-fill">
      60.0 FPS
    </text>

    <!-- Kinetic Game Particles -->
    <g transform="translate(172, 100)">
      <!-- Paddle -->
      <rect x="-40" y="55" width="80" height="8" rx="2" fill="#00F2FE" class="theme-cyan-fill" />
      <!-- Ball -->
      <circle cx="12" cy="18" r="6" fill="#FF8C00" class="pulse-arcade theme-amber-fill" />
      <!-- Trail -->
      <circle cx="6" cy="26" r="4" fill="#FF8C00" opacity="0.6" class="theme-amber-fill" />
      <circle cx="0" cy="34" r="2.5" fill="#FF8C00" opacity="0.3" class="theme-amber-fill" />
      <!-- Bricks / Blocks -->
      <g stroke="#080B10" stroke-width="2">
        <rect x="-120" y="-55" width="36" height="12" rx="2" fill="#00E599" />
        <rect x="-80" y="-55" width="36" height="12" rx="2" fill="#00F2FE" />
        <rect x="-40" y="-55" width="36" height="12" rx="2" fill="#FF8C00" />
        <rect x="0" y="-55" width="36" height="12" rx="2" fill="#A855F7" />
        <rect x="40" y="-55" width="36" height="12" rx="2" fill="#00E599" />
        <rect x="80" y="-55" width="36" height="12" rx="2" fill="#00F2FE" />
      </g>
    </g>

    <!-- Web Audio Synthesizer Chip Status -->
    <g transform="translate(20, 168)">
      <rect width="304" height="20" rx="2" fill="#161B22" stroke="#21262D" stroke-width="0.6" class="theme-elevated theme-border" />
      <text x="152" y="13" fill="#94A3B8" font-size="7.5" font-weight="600" text-anchor="middle" class="mono theme-text-body">
        AUDIO: <tspan fill="#00F2FE" class="theme-cyan-fill">SQUARE / SAW CHIP SYNTH</tspan> · 0 EXTERNAL MP3/WAV
      </text>
    </g>
  </g>
</svg>"""
    return svg

def generate_divider_quantum():
    """Generates assets/profile/divider_quantum.svg (960x40)"""
    w, h = 960, 40
    cx, cy = 480, 20
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="divLaserGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#21262D" stop-opacity="0.1" />
      <stop offset="20%" stop-color="#21262D" stop-opacity="0.6" />
      <stop offset="40%" stop-color="#00F2FE" stop-opacity="0.9" />
      <stop offset="50%" stop-color="#F8FAFC" stop-opacity="1" />
      <stop offset="60%" stop-color="#FF8C00" stop-opacity="0.9" />
      <stop offset="80%" stop-color="#21262D" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#21262D" stop-opacity="0.1" />
    </linearGradient>
  </defs>

  <style>
{SHARED_CSS}
    .pulse-divider {{ animation: pulseGlow 2.4s ease-in-out infinite; transform-origin: {cx}px {cy}px; }}
    .dash-div {{ stroke-dasharray: 4 8; animation: dashStream 4s linear infinite; }}
  </style>

  <!-- Central Specular Laser Line -->
  <line x1="30" y1="{cy}" x2="{w - 30}" y2="{cy}" stroke="url(#divLaserGrad)" stroke-width="1.2" />
  <line x1="120" y1="{cy}" x2="{w - 120}" y2="{cy}" stroke="#00F2FE" stroke-width="0.8" opacity="0.6" class="dash-div theme-cyan-stroke" />

  <!-- Center Core Diamond & Reticle -->
  <g class="pulse-divider">
    <circle cx="{cx}" cy="{cy}" r="14" fill="#080B10" stroke="#21262D" stroke-width="1" class="theme-bg theme-border" />
    <polygon points="{cx},{cy - 6} {cx + 6},{cy} {cx},{cy + 6} {cx - 6},{cy}" fill="#FF8C00" class="theme-amber-fill" />
    <circle cx="{cx}" cy="{cy}" r="2" fill="#F8FAFC" class="theme-text-head" />
  </g>

  <!-- Cardinal Coordinates & Crosshairs -->
  <g stroke="#30363D" stroke-width="1" opacity="0.8" class="theme-border-accent">
    <!-- Left Crosshair -->
    <path d="M 60 {cy - 5} L 60 {cy + 5} M 55 {cy} L 65 {cy}" />
    <!-- Right Crosshair -->
    <path d="M {w - 60} {cy - 5} L {w - 60} {cy + 5} M {w - 65} {cy} L {w - 55} {cy}" />
  </g>

  <!-- Telemetry Micro-Labels -->
  <text x="75" y="{cy + 3}" fill="#475569" font-size="7" font-weight="600" letter-spacing="0.12em" class="mono theme-text-dim">
    SEC_NODE // INVARIANTS: PASS
  </text>
  <text x="{w - 75}" y="{cy + 3}" fill="#475569" font-size="7" font-weight="600" letter-spacing="0.12em" text-anchor="end" class="mono theme-text-dim">
    XOLVERLABS ATELIER // 2026
  </text>
</svg>"""
    return svg

def generate_footer_console():
    """Generates assets/profile/footer_console.svg (960x120)"""
    w, h = 960, 120
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="footerBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080B10" />
      <stop offset="50%" stop-color="#0D1117" />
      <stop offset="100%" stop-color="#06080D" />
    </linearGradient>
    <linearGradient id="footerHairline" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#21262D" stop-opacity="0.2" />
      <stop offset="50%" stop-color="#00F2FE" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#21262D" stop-opacity="0.2" />
    </linearGradient>
  </defs>

  <style>
{SHARED_CSS}
    .pulse-beacon {{ animation: pulseGlow 2.4s ease-in-out infinite; }}
  </style>

  <!-- Canvas Surface -->
  <rect width="{w}" height="{h}" rx="6" fill="url(#footerBg)" class="theme-bg" />
  <rect width="{w}" height="{h}" rx="6" fill="none" stroke="#21262D" stroke-width="1.2" class="theme-border" />
  <line x1="20" y1="1" x2="{w - 20}" y2="1" stroke="url(#footerHairline)" stroke-width="1.5" />

  <!-- Corner Precision Crosshairs -->
  <g stroke="#30363D" stroke-width="1" opacity="0.8" class="theme-border-accent">
    <path d="M 12 16 L 22 16 M 17 11 L 17 21" />
    <path d="M {w - 22} 16 L {w - 12} 16 M {w - 17} 11 L {w - 17} 21" />
    <path d="M 12 {h - 16} L 22 {h - 16} M 17 {h - 21} L 17 {h - 11}" />
    <path d="M {w - 22} {h - 16} L {w - 12} {h - 16} M {w - 17} {h - 21} L {w - 17} {h - 11}" />
  </g>

  <!-- Main Terminal Console Layout -->
  <g transform="translate(36, 26)">
    <!-- Header Row -->
    <g transform="translate(0, 0)">
      <circle cx="4" cy="4" r="3" fill="#00E599" class="pulse-beacon theme-emerald-fill" />
      <text x="14" y="7" fill="#00E599" font-size="9" font-weight="700" letter-spacing="0.16em" class="mono theme-emerald-fill">
        DIRECT TRANSMISSION CONSOLE // FREQUENCY OPEN
      </text>
      <text x="{w - 72}" y="7" fill="#475569" font-size="8.5" font-weight="600" letter-spacing="0.1em" text-anchor="end" class="mono theme-text-dim">
        LAT: 20.2961° N · LON: 85.8245° E · BHUBANESWAR, INDIA
      </text>
    </g>

    <!-- Primary Dispatch Strip -->
    <g transform="translate(0, 24)">
      <!-- Channel 1: Studio -->
      <g transform="translate(0, 0)">
        <text x="0" y="10" fill="#94A3B8" font-size="8.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-body">STUDIO ATELIER:</text>
        <text x="0" y="24" fill="#F8FAFC" font-size="11" font-weight="700" class="mono theme-text-head">XolverLabs (xolver.in)</text>
      </g>

      <!-- Channel 2: Founder Inbox -->
      <g transform="translate(240, 0)">
        <text x="0" y="10" fill="#94A3B8" font-size="8.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-body">FOUNDER DIRECT:</text>
        <text x="0" y="24" fill="#00F2FE" font-size="11" font-weight="700" class="mono theme-cyan-fill">subhamjena.j@gmail.com</text>
      </g>

      <!-- Channel 3: Systems Consulting -->
      <g transform="translate(520, 0)">
        <text x="0" y="10" fill="#94A3B8" font-size="8.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-body">SYSTEMS DISPATCH:</text>
        <text x="0" y="24" fill="#FF8C00" font-size="11" font-weight="700" class="mono theme-amber-fill">lawflow.india@gmail.com</text>
      </g>

      <!-- Channel 4: Identity -->
      <g transform="translate(740, 0)">
        <text x="0" y="10" fill="#94A3B8" font-size="8.5" font-weight="700" letter-spacing="0.08em" class="mono theme-text-body">GITHUB PROTOCOL:</text>
        <text x="0" y="24" fill="#00E599" font-size="11" font-weight="700" class="mono theme-emerald-fill">github.com/DecoyINDIA</text>
      </g>
    </g>

    <!-- Bottom Cryptographic Seal -->
    <g transform="translate(0, 72)">
      <line x1="0" y1="0" x2="{w - 72}" y2="0" stroke="#21262D" stroke-width="0.8" class="theme-border" />
      <text x="0" y="14" fill="#475569" font-size="8" font-weight="500" letter-spacing="0.1em" class="mono theme-text-dim">
        VERIFIED SOVEREIGN RECORD: 100% DETERMINISTIC ARCHITECTURES · ZERO THIRD-PARTY TELEMETRY · MIT / APACHE 2.0 LICENSED
      </text>
    </g>
  </g>
</svg>"""
    return svg

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    generators = [
        ("hero_signature.svg", generate_hero),
        ("systems_topology.svg", generate_systems_topology),
        ("product_vaani.svg", generate_product_vaani),
        ("product_octapdf.svg", generate_product_octapdf),
        ("product_bmd.svg", generate_product_bmd),
        ("product_settlr.svg", generate_product_settlr),
        ("product_sportshawk.svg", generate_product_sportshawk),
        ("product_formspear.svg", generate_product_formspear),
        ("product_xanalgo.svg", generate_product_xanalgo),
        ("product_candy_drop.svg", generate_product_candy_drop),
        ("divider_quantum.svg", generate_divider_quantum),
        ("footer_console.svg", generate_footer_console),
    ]

    print(f"Generating {len(generators)} production SVG assets in {OUTPUT_DIR}...")
    success_count = 0
    total_bytes = 0

    for filename, gen_fn in generators:
        filepath = os.path.join(OUTPUT_DIR, filename)
        content = gen_fn()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        size_kb = len(content.encode("utf-8")) / 1024
        total_bytes += len(content.encode("utf-8"))
        print(f"  [OK] {filename} ({size_kb:.2f} KB)")
        success_count += 1

    print(f"\\nSuccessfully generated {success_count}/{len(generators)} assets.")
    print(f"Total budget consumed: {total_bytes / 1024:.2f} KB across all assets.")

if __name__ == "__main__":
    main()
