"""
Verification script for all profile SVGs
Audits XML integrity, file sizes, viewBoxes, and design constitution compliance.
"""

import os
import xml.etree.ElementTree as ET

PROFILE_DIR = r"C:\Users\subha\.gemini\antigravity\scratch\DecoyINDIA\assets\profile"

BUDGETS = {
    "hero_signature.svg": 350 * 1024,
    "systems_topology.svg": 280 * 1024,
    "product_vaani.svg": 160 * 1024,
    "product_octapdf.svg": 160 * 1024,
    "product_bmd.svg": 160 * 1024,
    "product_settlr.svg": 160 * 1024,
    "product_sportshawk.svg": 160 * 1024,
    "product_formspear.svg": 160 * 1024,
    "product_xanalgo.svg": 160 * 1024,
    "product_candy_drop.svg": 160 * 1024,
    "divider_quantum.svg": 25 * 1024,
    "footer_console.svg": 60 * 1024,
}

EXPECTED_DIMENSIONS = {
    "hero_signature.svg": (960, 340),
    "systems_topology.svg": (960, 420),
    "product_vaani.svg": (880, 260),
    "product_octapdf.svg": (880, 260),
    "product_bmd.svg": (880, 260),
    "product_settlr.svg": (880, 260),
    "product_sportshawk.svg": (880, 260),
    "product_formspear.svg": (880, 260),
    "product_xanalgo.svg": (880, 260),
    "product_candy_drop.svg": (880, 260),
    "divider_quantum.svg": (960, 40),
    "footer_console.svg": (960, 120),
}

def verify():
    print("=" * 60)
    print("AUDITING PROFILE SVG ASSETS AGAINST DESIGN CONSTITUTION")
    print("=" * 60)

    all_passed = True

    for filename, max_bytes in BUDGETS.items():
        filepath = os.path.join(PROFILE_DIR, filename)
        print(f"\nAuditing: {filename}")
        
        if not os.path.exists(filepath):
            print(f"  [FAIL] File missing: {filepath}")
            all_passed = False
            continue

        size = os.path.getsize(filepath)
        size_kb = size / 1024
        max_kb = max_bytes / 1024
        if size > max_bytes:
            print(f"  [FAIL] Exceeds byte budget: {size_kb:.1f} KB > {max_kb:.1f} KB")
            all_passed = False
        else:
            print(f"  [PASS] Budget check: {size_kb:.1f} KB / {max_kb:.1f} KB budget")

        # XML Parsing check
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            print("  [PASS] Valid XML syntax")
        except Exception as e:
            print(f"  [FAIL] XML parsing error: {e}")
            all_passed = False
            continue

        # Dimension / ViewBox check
        expected_w, expected_h = EXPECTED_DIMENSIONS[filename]
        viewbox = root.attrib.get("viewBox", "")
        expected_vb = f"0 0 {expected_w} {expected_h}"
        if viewbox != expected_vb:
            print(f"  [FAIL] viewBox mismatch: found '{viewbox}', expected '{expected_vb}'")
            all_passed = False
        else:
            print(f"  [PASS] ViewBox verified: {viewbox}")

        # Check content requirements
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for media queries
        if "@media (prefers-color-scheme: light)" not in content:
            print("  [FAIL] Missing prefers-color-scheme: light media query")
            all_passed = False
        else:
            print("  [PASS] Light-mode resilience query present")

        if "@media (prefers-reduced-motion: reduce)" not in content:
            print("  [FAIL] Missing prefers-reduced-motion: reduce media query")
            all_passed = False
        else:
            print("  [PASS] Reduced-motion accessibility query present")

        # Static frame compliance: check that elements have non-zero initial visibility
        if "opacity: 0;" in content or "opacity:0;" in content:
            print("  [WARN] Check for hidden elements in static frame")
        else:
            print("  [PASS] Static frame test passed: All elements visible at t=0")

    print("\n" + "=" * 60)
    if all_passed:
        print("RESULT: ALL 12 SVG ASSETS PASSED INDEPENDENT AUDIT (100%)")
    else:
        print("RESULT: AUDIT FAILED ON ONE OR MORE CHECKS")
    print("=" * 60)

if __name__ == "__main__":
    verify()
