"""Builds the va-sid logo: logo.svg (icon), logo.png (512 px) and banner.png (README).

The style follows the Visual Assembler / VA SID Studio icons: glowing light blue pixel
blocks on deep indigo. The mark is a SID chip (DIP package) with a sawtooth and a pulse wave.
Needs Pillow and Microsoft Edge (renders the SVG / HTML):
    python assets/make_logo.py
"""

import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ASSETS = Path(__file__).resolve().parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FONT = ASSETS / "C64_Pro_Mono-STYLE.woff2"

GRID = 40
BRIGHT = "#bdf0ff"
GLOW = "#5fc8ff"
MID = "#4a72f5"
DIM = "#26249e"


def chip_cells():
    """(x, y, kind) cells of the mark on the 40x40 grid."""
    cells = {}
    x0, x1, y0, y1 = 7, 32, 12, 27
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            edge = x in (x0, x1) or y in (y0, y1)
            cells[(x, y)] = "mid" if edge else "dim"
    # the notch on the left end
    for y in range(18, 22):
        cells.pop((x0, y), None)
        cells[(x0 + 1, y)] = "mid"
    # pins, top and bottom
    for x in range(9, 31, 3):
        for y in (9, 10, 11, 28, 29, 30):
            cells[(x, y)] = "mid"
            cells[(x + 1, y)] = "mid"
    # "SID" in 5-row pixel letters
    glyphs = {
        "S": [".###", "#...", ".##.", "...#", "###."],
        "I": ["###", ".#.", ".#.", ".#.", "###"],
        "D": ["###.", "#..#", "#..#", "#..#", "###."],
    }
    left = 13
    for letter in "SID":
        rows = glyphs[letter]
        for dy, row in enumerate(rows):
            for dx, bit in enumerate(row):
                if bit == "#":
                    cells[(left + dx, 14 + dy)] = "bright"
        left += len(rows[0]) + 1
    # below it a sawtooth, then a pulse
    for tooth in range(2):
        left = 10 + tooth * 5
        for step in range(5):
            cells[(left + step, 25 - step)] = "bright"
        for y in range(21, 26):
            cells[(left + 4, y)] = "bright"
    cells[(20, 25)] = "bright"
    for x in range(21, 30):
        cells[(x, 21 if x < 25 else 25)] = "bright"
    for y in range(21, 26):
        cells[(21, y)] = "bright"
        cells[(25, y)] = "bright"
    cells[(30, 25)] = "bright"
    return cells


def cell_rects(cells, kind, inset=0.08):
    size = 1 - 2 * inset
    return "\n".join(
        f'    <rect x="{x + inset:.2f}" y="{y + inset:.2f}" width="{size:.2f}" height="{size:.2f}" rx="0.12"/>'
        for (x, y), k in sorted(cells.items())
        if k == kind
    )


def logo_svg():
    cells = chip_cells()
    scan = "\n".join(
        f'    <rect x="0" y="{y / 4:.2f}" width="{GRID}" height="0.08"/>' for y in range(0, GRID * 4, 2)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GRID} {GRID}" width="512" height="512" role="img" aria-label="va-sid">
  <title>va-sid</title>
  <defs>
    <radialGradient id="bg" cx="50%" cy="42%" r="70%">
      <stop offset="0" stop-color="#2f22c4"/>
      <stop offset="0.65" stop-color="#1b1290"/>
      <stop offset="1" stop-color="#0c0650"/>
    </radialGradient>
    <linearGradient id="rim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#6f7dff" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#2a1fa0" stop-opacity="0.6"/>
    </linearGradient>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="0.9"/>
    </filter>
    <clipPath id="card"><rect x="1.5" y="1.5" width="37" height="37" rx="8"/></clipPath>
  </defs>
  <rect x="1.5" y="1.5" width="37" height="37" rx="8" fill="url(#bg)"/>
  <g clip-path="url(#card)" fill="#000" opacity="0.14">
{scan}
  </g>
  <rect x="1.75" y="1.75" width="36.5" height="36.5" rx="7.8" fill="none" stroke="url(#rim)" stroke-width="0.5"/>
  <g fill="{DIM}">
{cell_rects(cells, "dim")}
  </g>
  <g fill="{MID}" filter="url(#glow)" opacity="0.7">
{cell_rects(cells, "mid", 0)}
  </g>
  <g fill="{MID}">
{cell_rects(cells, "mid")}
  </g>
  <g fill="{GLOW}" filter="url(#glow)">
{cell_rects(cells, "bright", 0)}
  </g>
  <g fill="{BRIGHT}">
{cell_rects(cells, "bright")}
  </g>
</svg>
"""


def banner_html(logo: Path):
    return f"""<!doctype html><html><head><style>
@font-face {{ font-family: c64; src: url('{FONT.as_uri()}'); }}
html, body {{ margin: 0; width: 1280px; height: 320px; overflow: hidden; }}
body {{ display: flex; align-items: center; gap: 44px; padding: 0 64px; box-sizing: border-box;
  background: radial-gradient(ellipse at 30% 40%, #2a1fb8 0%, #160d7c 55%, #0a0548 100%); font-family: c64; }}
body::after {{ content: ""; position: fixed; inset: 0;
  background: repeating-linear-gradient(0deg, rgba(0,0,0,.16) 0 2px, transparent 2px 4px); }}
img {{ width: 240px; height: 240px; }}
h1 {{ margin: 0; font-size: 92px; font-weight: normal; color: {BRIGHT}; letter-spacing: 4px;
  text-shadow: 0 0 18px {GLOW}, 0 0 4px {GLOW}; }}
p {{ margin: 22px 0 0; font-size: 21px; line-height: 1.6; color: #8fa6ff; text-shadow: 0 0 8px #3b4fe0; }}
</style></head><body>
<img src="{logo.as_uri()}">
<div><h1>VA-SID</h1><p>C64 SID EMULATION IN RUST<br>VA SID CORE &middot; RESID &middot; 6510 / CIA / VIC-II</p></div>
</body></html>"""


def screenshot(html: Path, png: Path, width: int, height: int, transparent: bool):
    args = [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
            f"--window-size={width},{height}", f"--screenshot={png}"]
    if transparent:
        args.append("--default-background-color=00000000")
    subprocess.run(args + [html.as_uri()], check=True, capture_output=True, timeout=60)


def main():
    logo = ASSETS / "logo.svg"
    logo.write_text(logo_svg(), encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        page = tmp / "logo.html"
        page.write_text(
            "<!doctype html><html style='overflow:hidden'><body style='margin:0;background:transparent'>"
            f"<img src='{logo.as_uri()}' width='1024' height='1024' style='display:block'>",
            encoding="utf-8",
        )
        big = tmp / "logo.png"
        screenshot(page, big, 1024, 1024, True)
        Image.open(big).convert("RGBA").resize((512, 512), Image.LANCZOS).save(ASSETS / "logo.png")
        page = tmp / "banner.html"
        page.write_text(banner_html(logo), encoding="utf-8")
        screenshot(page, ASSETS / "banner.png", 1280, 320, False)


if __name__ == "__main__":
    main()
