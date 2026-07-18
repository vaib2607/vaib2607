#!/usr/bin/env python3
"""Generate a clean Porsche 911 (992) ASCII art SVG."""
import os

CELL_W = 6
CELL_H = 11

# Clean Porsche 911 side profile - 992 generation
ASCII_ART = [
    "                                                                                     ",
    "                          .------.                                                   ",
    "                     .---'        '---.                                              ",
    "                  .-'    __________    '-.                                           ",
    "               .-'    .-'          '-.    '-.                                        ",
    "            .-'     .'                '.     '-.                                     ",
    "         .-'      .'                    '.      '-.                                  ",
    "        /      .'                        '.       \\                                 ",
    "       /     .'                            '.      \\                                ",
    "      |    .'          ____------____          '.   |                               ",
    "      |  .'         .-'              '-.         '. |                               ",
    "      |.'          /                    \\          '.|                               ",
    "      ||          |    _____________     |          ||                               ",
    "      ||          |   |           |     |          ||                               ",
    "      ||          |   |  O     O  |     |          ||                               ",
    "      ||          |   |           |     |          ||                               ",
    "      ||     ___  |   |___________|  ___|     ___  ||                               ",
    "      ||    /   \\ |                  |   \\    /   \\ ||                               ",
    "      ||   |  O  ||                  || O  |  |  O  ||                               ",
    "      ||    \\___/  \\                /  \\___/   \\___/  ||                               ",
    "      ''----------'\\______________/'----------''                                 ",
    "                                                                                     ",
    "    ___________            ___________                                               ",
    "   /           \\          /           \\                                              ",
    "  |  ___   ___  |        |  ___   ___  |                                            ",
    "  | |   | |   | |        | |   | |   | |                                            ",
    "  | |___| |___| |        | |___| |___| |                                            ",
    "   \\___________/          \\___________/                                             ",
    "                                                                                     ",
]

def make_porsche_svg(output_path: str = "vaib-ascii.svg"):
    height = len(ASCII_ART)
    width = max(len(row) for row in ASCII_ART)
    svg_w = width * CELL_W
    svg_h = height * CELL_H

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">')
    lines.append(f'<rect width="{svg_w}" height="{svg_h}" fill="#0d1117"/>')
    lines.append('<style>text { font-family: "Courier New", Courier, monospace; font-size: 12px; fill: #8b949e; }</style>')

    for row_idx, row in enumerate(ASCII_ART):
        delay = row_idx * 0.04
        y = row_idx * CELL_H + CELL_H - 2
        chars = []
        for col_idx, ch in enumerate(row):
            if ch == ' ':
                continue
            x = col_idx * CELL_W
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
    print(f"Porsche 911 ASCII SVG saved to {output_path}")

if __name__ == "__main__":
    make_porsche_svg()
