#!/usr/bin/env python3
"""Render contribution heatmap SVG from fetched JSON data."""
import json
import os
import sys
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
CELL_SIZE = 13
CELL_GAP = 3
CELL_R = 2.5
WEEKS = 53
DAYS = 7
LABEL_W = 48
HEADER_H = 24
LEGEND_H = 30
STATS_H = 36
PAD = 16
CARD_BG = "#161b22"
CARD_STROKE = "#30363d"

SVG_W = LABEL_W + WEEKS * (CELL_SIZE + CELL_GAP) + 16 + PAD * 2
SVG_H = HEADER_H + DAYS * (CELL_SIZE + CELL_GAP) + LEGEND_H + STATS_H + 16 + PAD * 2

MONTH_LABELS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAY_LABELS = ["Mon", "", "Wed", "", "Fri", "", ""]

def build_heatmap(data_path: str = "data/contributions.json"):
    """Return (width, height, inner_svg_markup) — no outer <svg> wrapper."""
    with open(data_path) as f:
        data = json.load(f)

    days = data["days"]
    if not days:
        print("No days in data")
        sys.exit(1)

    # Build date->level map
    day_map = {d["date"]: d["level"] for d in days}

    # Find the Sunday on or before the earliest date, then group into weeks
    dates = sorted(day_map.keys())
    first = datetime.strptime(dates[0], "%Y-%m-%d")
    last = datetime.strptime(dates[-1], "%Y-%m-%d")

    # Go back to the Sunday of the first week
    start = first
    while start.weekday() != 6:  # Sunday
        start -= __import__('datetime').timedelta(days=1)

    # Build grid: list of weeks, each week is 7 days (Sun=0 .. Sat=6)
    weeks = []
    current = start
    while current <= last or len(weeks) < WEEKS:
        week = []
        for dow in range(7):
            d = current + __import__('datetime').timedelta(days=dow)
            if d > last and d > datetime.now():
                week.append(-1)
            else:
                ds = d.strftime("%Y-%m-%d")
                week.append(day_map.get(ds, 0))
        weeks.append(week)
        current += __import__('datetime').timedelta(days=7)
        if len(weeks) >= WEEKS:
            break

    # SVG
    svg = []
    svg.append(f'<rect width="{SVG_W}" height="{SVG_H}" rx="8" fill="{CARD_BG}" stroke="{CARD_STROKE}" stroke-width="1"/>')

    # Month labels
    prev_month = -1
    for wi in range(min(WEEKS, len(weeks))):
        first_day_offset = wi * 7
        d = start + __import__('datetime').timedelta(days=first_day_offset)
        m = d.month
        if m != prev_month:
            x = PAD + LABEL_W + wi * (CELL_SIZE + CELL_GAP)
            svg.append(f'<text x="{x}" y="{PAD + HEADER_H - 6}" font-family="Courier New, Courier, monospace" font-size="10" fill="#8b949e">{MONTH_LABELS[m]}</text>')
            prev_month = m

    # Day labels
    for di in range(DAYS):
        y = PAD + HEADER_H + di * (CELL_SIZE + CELL_GAP) + CELL_SIZE - 2
        if DAY_LABELS[di]:
            svg.append(f'<text x="{PAD}" y="{y}" font-family="Courier New, Courier, monospace" font-size="9" fill="#8b949e">{DAY_LABELS[di]}</text>')

    # Cells with SMIL staggered animation (GitHub-safe)
    cell_idx = 0
    for wi in range(min(WEEKS, len(weeks))):
        for di in range(DAYS):
            level = weeks[wi][di] if di < len(weeks[wi]) else -1
            if level < 0:
                continue
            color = PALETTE[min(level, len(PALETTE) - 1)]
            x = PAD + LABEL_W + wi * (CELL_SIZE + CELL_GAP)
            y = PAD + HEADER_H + di * (CELL_SIZE + CELL_GAP)
            delay = (wi * DAYS + di) * 0.003
            svg.append(f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="{CELL_R}" fill="{color}" opacity="0">')
            svg.append(f'  <animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.15s" fill="freeze"/>')
            svg.append(f'</rect>')
            cell_idx += 1

    # Legend
    ly = PAD + HEADER_H + DAYS * (CELL_SIZE + CELL_GAP) + 12
    svg.append(f'<text x="{PAD + LABEL_W}" y="{ly + 10}" font-family="Courier New, Courier, monospace" font-size="10" fill="#8b949e">Less</text>')
    for i, c in enumerate(PALETTE):
        lx = PAD + LABEL_W + 36 + i * (CELL_SIZE + CELL_GAP)
        svg.append(f'<rect x="{lx}" y="{ly}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="{CELL_R}" fill="{c}"/>')
    svg.append(f'<text x="{PAD + LABEL_W + 36 + len(PALETTE) * (CELL_SIZE + CELL_GAP) + 6}" y="{ly + 10}" font-family="Courier New, Courier, monospace" font-size="10" fill="#8b949e">More</text>')

    # Stats
    total = data.get("total", 0)
    sy = ly + LEGEND_H + 8
    svg.append(f'<text x="{PAD + LABEL_W}" y="{sy}" font-family="Courier New, Courier, monospace" font-size="11" fill="#8b949e">{total:,} contributions in the last year</text>')

    return SVG_W, SVG_H, '\n'.join(svg)

def render_heatmap(data_path: str = "data/contributions.json", output_path: str = "contrib-heatmap.svg"):
    svg_w, svg_h, inner = build_heatmap(data_path)
    full = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">\n{inner}\n</svg>'
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(full)
    print(f"Heatmap SVG saved to {output_path}")

if __name__ == "__main__":
    render_heatmap()
