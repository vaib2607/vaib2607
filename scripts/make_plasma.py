#!/usr/bin/env python3
"""Generate an animated ASCII plasma effect SVG using SMIL animations."""
import os
import math

CHARSET = " .,:;+*?%S#@"
WIDTH = 80
HEIGHT = 25
CELL_W = 7
CELL_H = 12

# Sunset palette
PALETTE = [
    "#1a0a2e", "#2d1b4e", "#4a1942", "#6b1d3b",
    "#8b2252", "#a02858", "#c4384f", "#d94f3a",
    "#e87030", "#f09040", "#f5b060", "#ffd080",
]

def plasma_value(x, y, t):
    v1 = math.sin(x * 0.12 + t)
    v2 = math.sin(y * 0.18 + t * 0.7)
    v3 = math.sin((x + y) * 0.09 + t * 0.5)
    v4 = math.sin(math.sqrt(x * x + y * y) * 0.14 + t * 0.3)
    return (v1 + v2 + v3 + v4) / 4.0

def make_plasma_svg(output_path: str = "plasma.svg"):
    svg_w = WIDTH * CELL_W
    svg_h = HEIGHT * CELL_H

    num_frames = 4
    total_dur = 2.4

    # Pre-compute all frames
    all_frames = []
    for fi in range(num_frames):
        t = fi * (2 * math.pi / num_frames)
        grid = []
        for row in range(HEIGHT):
            line = []
            for col in range(WIDTH):
                v = plasma_value(col, row, t)
                v = (v + 1) / 2.0
                ci = int(v * (len(PALETTE) - 1))
                ci = max(0, min(ci, len(PALETTE) - 1))
                line.append(PALETTE[ci])
            grid.append(line)
        all_frames.append(grid)

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">')
    lines.append(f'<rect width="{svg_w}" height="{svg_h}" fill="#0a0a1a"/>')
    lines.append('<style>text { font-family: "Courier New", Courier, monospace; font-size: 10px; }</style>')

    keytimes = ";".join([f"{i/(num_frames-1):.2f}" for i in range(num_frames)])

    for row in range(HEIGHT):
        for col in range(WIDTH):
            x = col * CELL_W
            y = row * CELL_H + CELL_H - 1

            v0 = plasma_value(col, row, 0)
            v0 = (v0 + 1) / 2.0
            char_idx = int(v0 * (len(CHARSET) - 1))
            ch = CHARSET[max(0, min(char_idx, len(CHARSET) - 1))]
            ch = ch.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

            colors = ";".join([all_frames[fi][row][col] for fi in range(num_frames)])

            lines.append(f'<text x="{x}" y="{y}" fill="{all_frames[0][row][col]}">{ch}')
            lines.append(f'<animate attributeName="fill" values="{colors}" keyTimes="{keytimes}" dur="{total_dur}s" repeatCount="indefinite"/></text>')

    lines.append('</svg>')

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))
    fsize = os.path.getsize(output_path)
    print(f"Plasma SVG saved to {output_path} ({WIDTH}x{HEIGHT}, {fsize/1024:.0f}KB)")

if __name__ == "__main__":
    make_plasma_svg()
