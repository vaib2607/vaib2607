#!/usr/bin/env python3
"""Convert a prepped grayscale photo into a self-typing monochrome ASCII SVG."""
import sys
import os
import numpy as np
from PIL import Image

RAMP = " .`:-=+*cs#%@"
WIDTH = 100
CELL_W = 7
CELL_H = 14
ANIM_DELAY_PER_ROW = 0.03

def brightness_to_char(b: float) -> str:
    idx = int(b * (len(RAMP) - 1))
    return RAMP[min(idx, len(RAMP) - 1)]

def make_ascii_svg(input_path: str, output_path: str = "vaib-ascii.svg"):
    img = Image.open(input_path).convert("L")
    w, h = img.size
    aspect = h / w
    height = int(WIDTH * aspect * (CELL_W / CELL_H))
    img = img.resize((WIDTH, height), Image.LANCZOS)
    pixels = np.array(img, dtype=float) / 255.0

    svg_w = WIDTH * CELL_W
    svg_h = height * CELL_H

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">')
    lines.append(f'<rect width="{svg_w}" height="{svg_h}" fill="#0d1117"/>')
    lines.append('<style>text { font-family: "Courier New", Courier, monospace; font-size: 13px; fill: #8b949e; }</style>')

    for row_idx in range(height):
        delay = row_idx * ANIM_DELAY_PER_ROW
        y = row_idx * CELL_H + CELL_H - 2
        chars = []
        for col_idx in range(WIDTH):
            b = 1.0 - pixels[row_idx, col_idx]
            ch = brightness_to_char(b)
            x = col_idx * CELL_W
            if ch != ' ':
                chars.append(f'<text x="{x}" y="{y}">{ch}</text>')
        if chars:
            row_content = ''.join(chars)
            lines.append(f'<g opacity="0">')
            lines.append(f'  <animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.3s" fill="freeze"/>')
            lines.append(f'  {row_content}')
            lines.append(f'</g>')

    lines.append('</svg>')

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))
    print(f"ASCII SVG saved to {output_path}")

if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "data/source-prepped.png"
    make_ascii_svg(inp)
