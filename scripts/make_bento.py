#!/usr/bin/env python3
"""Composite the porsche/heatmap/info-card tiles into one pixel-exact bento SVG.

Single static image so GitHub's markdown-in-HTML paragraph parsing can't
introduce stray gaps the way an HTML <table> of separate <img> tags does.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from make_porsche_ascii import build_porsche
from render_heatmap_svg import build_heatmap
from make_info_card import build_info_card

TILE_PAD = 8       # gap between a tile's outer shell and its inner card
OUTER_PAD = 24     # margin around the whole composite
GAP = 24           # gap between tiles
RIGHT_W = 400      # display width of the right-column tiles' inner content
SHELL_BG = "#1c2128"
SHELL_STROKE = "#30363d"
SHELL_RX = 20

MOTD_LINES = [
    "yo — this is the github. it has an ascii car and a heatmap because why not.",
    "",
    "I build stuff for iOS, web, and whatever shiny thing hijacks my attention next.",
    "currently down an AI/ML + open source rabbit hole, ask me about it, I will not stop talking.",
    "",
    "if you made it this far — hi. let's build something unhinged together.",
]
MOTD_LINE_H = 26
MOTD_PAD = 28

def shell(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{SHELL_RX}" fill="{SHELL_BG}" stroke="{SHELL_STROKE}" stroke-width="1"/>'

def nested(x, y, disp_w, disp_h, orig_w, orig_h, inner):
    return (
        f'<svg x="{x}" y="{y}" width="{disp_w:.2f}" height="{disp_h:.2f}" '
        f'viewBox="0 0 {orig_w} {orig_h}">{inner}</svg>'
    )

def make_bento(output_path: str = "bento.svg"):
    hero_w, hero_h, hero_inner = build_porsche()
    heat_w, heat_h, heat_inner = build_heatmap()
    info_w, info_h, info_inner = build_info_card()

    heat_disp_h = heat_h * RIGHT_W / heat_w
    info_disp_h = info_h * RIGHT_W / info_w

    # Hero's inner content height is solved so both columns land flush,
    # top and bottom, with zero slack — no centering hacks needed.
    hero_disp_h = heat_disp_h + GAP + info_disp_h + TILE_PAD * 2
    hero_disp_w = hero_disp_h * hero_w / hero_h

    hero_tile_w = hero_disp_w + TILE_PAD * 2
    hero_tile_h = hero_disp_h + TILE_PAD * 2
    right_tile_w = RIGHT_W + TILE_PAD * 2
    heat_tile_h = heat_disp_h + TILE_PAD * 2
    info_tile_h = info_disp_h + TILE_PAD * 2
    right_col_h = heat_tile_h + GAP + info_tile_h

    row1_w = hero_tile_w + GAP + right_tile_w
    row1_h = max(hero_tile_h, right_col_h)

    motd_h = MOTD_PAD * 2 + len(MOTD_LINES) * MOTD_LINE_H

    svg_w = OUTER_PAD * 2 + row1_w
    svg_h = OUTER_PAD * 3 + row1_h + motd_h

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w:.2f} {svg_h:.2f}" width="{svg_w:.0f}" height="{svg_h:.0f}">')
    parts.append(f'<rect width="{svg_w:.2f}" height="{svg_h:.2f}" fill="#0d1117"/>')

    # Hero tile — left
    hx, hy = OUTER_PAD, OUTER_PAD
    parts.append(shell(hx, hy, hero_tile_w, hero_tile_h))
    parts.append(nested(hx + TILE_PAD, hy + TILE_PAD, hero_disp_w, hero_disp_h, hero_w, hero_h, hero_inner))

    # Right column
    rx = OUTER_PAD + hero_tile_w + GAP
    ry = OUTER_PAD
    parts.append(shell(rx, ry, right_tile_w, heat_tile_h))
    parts.append(nested(rx + TILE_PAD, ry + TILE_PAD, RIGHT_W, heat_disp_h, heat_w, heat_h, heat_inner))

    ry2 = ry + heat_tile_h + GAP
    parts.append(shell(rx, ry2, right_tile_w, info_tile_h))
    parts.append(nested(rx + TILE_PAD, ry2 + TILE_PAD, RIGHT_W, info_disp_h, info_w, info_h, info_inner))

    # motd — full-width row, playful copy, same shell as everything else
    my = OUTER_PAD * 2 + row1_h
    parts.append(shell(OUTER_PAD, my, row1_w, motd_h))
    cx = OUTER_PAD + row1_w / 2
    ty = my + MOTD_PAD + 14
    for line in MOTD_LINES:
        if line:
            parts.append(
                f'<text x="{cx:.2f}" y="{ty}" text-anchor="middle" '
                f'font-family="Courier New, Courier, monospace" font-size="14" fill="#c9d1d9">{line}</text>'
            )
        ty += MOTD_LINE_H

    parts.append('</svg>')

    with open(output_path, 'w') as f:
        f.write('\n'.join(parts))
    fsize = os.path.getsize(output_path)
    print(f"Bento SVG saved to {output_path} ({svg_w:.0f}x{svg_h:.0f}, {fsize/1024:.0f}KB)")

if __name__ == "__main__":
    make_bento()
