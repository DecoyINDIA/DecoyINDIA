import os
import re

base_dir = r"C:\Users\subha\.gemini\antigravity\scratch\DecoyINDIA"
readme_path = os.path.join(base_dir, "README.md")

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

print("=== CHECKING IMAGE ASSETS ===")
img_srcs = re.findall(r'src=["\']([^"\']+)["\']', content)
all_imgs_ok = True
for src in sorted(set(img_srcs)):
    full_path = os.path.join(base_dir, src.replace("/", os.sep))
    exists = os.path.exists(full_path)
    size = os.path.getsize(full_path) if exists else 0
    print(f"  {src} -> exists: {exists} ({size:,} bytes)")
    if not exists:
        all_imgs_ok = False

print("\n=== CHECKING ANCHORS ===")
href_anchors = re.findall(r'href=["\']#([^"\']+)["\']', content)
ids = set(re.findall(r'id=["\']([^"\']+)["\']', content))
all_anchors_ok = True
for anchor in sorted(set(href_anchors)):
    found = anchor in ids
    print(f"  #{anchor} -> target found: {found}")
    if not found:
        all_anchors_ok = False

lines = content.splitlines()
bytes_len = len(content.encode("utf-8"))
print(f"\nTotal Lines: {len(lines)}")
print(f"Total Bytes: {bytes_len:,}")
print(f"ALL IMAGES OK: {all_imgs_ok}")
print(f"ALL ANCHORS OK: {all_anchors_ok}")
