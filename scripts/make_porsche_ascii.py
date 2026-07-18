#!/usr/bin/env python3
"""Convert data/porsche-source.gif into an animated, source-colored ASCII SVG."""
import os
import sys
from PIL import Image, ImageSequence

RAMP = " .:-=+*#%@"
WIDTH = 60
CELL_W = 7
CELL_H = 12
FRAME_STEP = 3  # sample every Nth gif frame to keep SVG size reasonable

def brightness_to_char(b: float) -> str:
    idx = int(b * (len(RAMP) - 1))
    return RAMP[min(idx, len(RAMP) - 1)]

def load_frames(path: str):
    im = Image.open(path)
    base = Image.new("RGBA", im.size, (13, 17, 23, 255))  # #0d1117 backdrop
    frames = []
    durations = []
    for frame in ImageSequence.Iterator(im):
        base.alpha_composite(frame.convert("RGBA"))
        frames.append(base.convert("RGB"))
        durations.append(frame.info.get("duration", 40))
    return frames, durations

def make_porsche_svg(input_path: str = "data/porsche-source.gif", output_path: str = "vaib-ascii.svg"):
    raw_frames, raw_durations = load_frames(input_path)
    raw_frames = raw_frames[::FRAME_STEP]
    raw_durations = raw_durations[::FRAME_STEP]
    total_dur = sum(raw_durations) / 1000.0
    num_frames = len(raw_frames)

    aspect = raw_frames[0].height / raw_frames[0].width
    height = int(WIDTH * aspect * (CELL_W / CELL_H))

    grids = []  # grids[frame][row][col] = (char, hexcolor)
    for img in raw_frames:
        small = img.resize((WIDTH, height), Image.LANCZOS)
        px = small.load()
        grid = []
        for row in range(height):
            line = []
            for col in range(WIDTH):
                r, g, b = px[col, row]
                lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
                ch = brightness_to_char(lum)
                line.append((ch, "#%02x%02x%02x" % (r, g, b)))
            grid.append(line)
        grids.append(grid)

    svg_w = WIDTH * CELL_W
    svg_h = height * CELL_H

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">')
    lines.append(f'<rect width="{svg_w}" height="{svg_h}" fill="#0d1117"/>')
    lines.append('<style>text { font-family: "Courier New", Courier, monospace; font-size: 11px; }</style>')

    keytimes = ";".join(f"{i/(num_frames-1):.4f}" for i in range(num_frames))

    for row in range(height):
        for col in range(WIDTH):
            ch0, color0 = grids[0][row][col]
            if all(grids[fi][row][col][0] == ' ' for fi in range(num_frames)):
                continue

            colors = ";".join(grids[fi][row][col][1] for fi in range(num_frames))
            glyph = ch0 if ch0 != ' ' else chr(160)

            x = col * CELL_W
            y = row * CELL_H + CELL_H - 2

            lines.append(f'<text x="{x}" y="{y}" fill="{color0}">{glyph}')
            lines.append(f'  <animate attributeName="fill" values="{colors}" keyTimes="{keytimes}" dur="{total_dur:.2f}s" repeatCount="indefinite"/>')
            lines.append('</text>')

    lines.append('</svg>')

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))
    fsize = os.path.getsize(output_path)
    print(f"Porsche ASCII SVG saved to {output_path} ({WIDTH}x{height}, {num_frames} frames, {fsize/1024:.0f}KB)")

if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "data/porsche-source.gif"
    make_porsche_svg(inp)
