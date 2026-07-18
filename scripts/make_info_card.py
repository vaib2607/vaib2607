#!/usr/bin/env python3
"""Generate a neofetch-style info card SVG with SMIL animations (GitHub-safe)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from theme import THEMES

CARD_W = 600
CARD_H = 300
LINE_H = 28
DELAY_STEP = 0.15

def build_info_card(theme: dict = THEMES["dark"]):
    """Return (width, height, inner_svg_markup) — no outer <svg> wrapper."""
    lines_data = [
        ("os",       "macOS Sequoia (14 tabs deep, send help)"),
        ("editor",   "Neovim + VS Code, no I will not pick one"),
        ("lang",     "Swift / Python / TypeScript, feral polyglot"),
        ("stack",    "React Native · SwiftUI · FastAPI go brrr"),
        ("shell",    "zsh + starship, prompt more decorated than me"),
        ("theme",    "GitHub Dark Dimmed, my eyes said thanks"),
        ("now",      "vibe coding at 2am, it's fine, it's shipped"),
        ("focus",    "iOS · Web · AI/ML, brain has 47 open tabs too"),
    ]

    svg = []
    svg.append(f'<rect width="{CARD_W}" height="{CARD_H}" rx="8" fill="{theme["card_bg"]}" stroke="{theme["card_stroke"]}" stroke-width="1"/>')

    # Title bar
    svg.append(f'<rect width="{CARD_W}" height="36" rx="8" fill="{theme["title_bar"]}"/>')
    svg.append(f'<rect x="0" y="28" width="{CARD_W}" height="8" fill="{theme["title_bar"]}"/>')
    svg.append(f'<circle cx="18" cy="18" r="5" fill="#ff5f57"/>')
    svg.append(f'<circle cx="36" cy="18" r="5" fill="#febc2e"/>')
    svg.append(f'<circle cx="54" cy="18" r="5" fill="#28c840"/>')
    svg.append(f'<text x="100" y="23" font-family="monospace" font-size="12" fill="{theme["text_dim"]}">vaib@github</text>')

    y = 64
    for i, (label, value) in enumerate(lines_data):
        delay = i * DELAY_STEP
        svg.append(f'<g opacity="0">')
        svg.append(f'  <animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.3s" fill="freeze"/>')
        svg.append(f'  <text x="24" y="{y}" font-family="monospace" font-size="13" fill="{theme["text_label"]}">{label}</text>')
        svg.append(f'  <text x="120" y="{y}" font-family="monospace" font-size="13" fill="{theme["text_main"]}">{value}</text>')
        svg.append(f'</g>')
        y += LINE_H

    return CARD_W, CARD_H, '\n'.join(svg)

def make_info_card(output_path: str = "info-card.svg"):
    card_w, card_h, inner = build_info_card()
    full = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {card_w} {card_h}" width="{card_w}" height="{card_h}">\n{inner}\n</svg>'
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(full)
    print(f"Info card SVG saved to {output_path}")

if __name__ == "__main__":
    make_info_card()
