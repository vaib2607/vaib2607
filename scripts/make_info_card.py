#!/usr/bin/env python3
"""Generate a neofetch-style info card SVG with SMIL animations (GitHub-safe)."""
import os

CARD_W = 490
CARD_H = 340
LINE_H = 28
DELAY_STEP = 0.15

def make_info_card(output_path: str = "info-card.svg"):
    lines_data = [
        ("os",      "macOS Sequoia"),
        ("editor",  "Neovim + VS Code"),
        ("lang",    "Swift / Python / TypeScript"),
        ("stack",   "React Native · SwiftUI · FastAPI"),
        ("shell",   "zsh + starship"),
        ("theme",   "GitHub Dark Dimmed"),
        ("now",     "Building cool stuff"),
        ("focus",   "iOS · Web · AI/ML"),
    ]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CARD_W} {CARD_H}" width="{CARD_W}" height="{CARD_H}">')
    svg.append(f'<rect width="{CARD_W}" height="{CARD_H}" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1"/>')

    # Title bar
    svg.append(f'<rect width="{CARD_W}" height="36" rx="8" fill="#21262d"/>')
    svg.append(f'<rect x="0" y="28" width="{CARD_W}" height="8" fill="#21262d"/>')
    svg.append(f'<circle cx="18" cy="18" r="5" fill="#ff5f57"/>')
    svg.append(f'<circle cx="36" cy="18" r="5" fill="#febc2e"/>')
    svg.append(f'<circle cx="54" cy="18" r="5" fill="#28c840"/>')
    svg.append(f'<text x="100" y="23" font-family="monospace" font-size="12" fill="#8b949e">vaib@github</text>')

    y = 64
    for i, (label, value) in enumerate(lines_data):
        delay = i * DELAY_STEP
        svg.append(f'<g opacity="0">')
        svg.append(f'  <animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.3s" fill="freeze"/>')
        svg.append(f'  <text x="24" y="{y}" font-family="monospace" font-size="13" fill="#58a6ff">{label}</text>')
        svg.append(f'  <text x="120" y="{y}" font-family="monospace" font-size="13" fill="#c9d1d9">{value}</text>')
        svg.append(f'</g>')
        y += LINE_H

    # Divider
    svg.append(f'<line x1="24" y1="{y - 8}" x2="{CARD_W - 24}" y2="{y - 8}" stroke="#30363d" stroke-width="1"/>')

    # ASCII art logo
    logo_y = y + 8
    ascii_logo = [
        "  __  __       ",
        " |  \\/  |__  _ _",
        " | |\\/| / _` | '_|",
        " |_|  |_\\__,_|_|  ",
    ]
    delay_logo = len(lines_data) * DELAY_STEP
    svg.append(f'<g opacity="0">')
    svg.append(f'  <animate attributeName="opacity" from="0" to="1" begin="{delay_logo}s" dur="0.3s" fill="freeze"/>')
    for j, row in enumerate(ascii_logo):
        svg.append(f'  <text x="24" y="{logo_y + j * 16}" font-family="monospace" font-size="11" fill="#58a6ff">{row}</text>')
    svg.append(f'</g>')

    svg.append('</svg>')

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(svg))
    print(f"Info card SVG saved to {output_path}")

if __name__ == "__main__":
    make_info_card()
