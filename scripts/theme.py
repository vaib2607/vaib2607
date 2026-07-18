#!/usr/bin/env python3
"""Shared color themes for the bento tiles — dark mirrors GitHub Dark Dimmed, light mirrors GitHub Light."""

THEMES = {
    "dark": dict(
        bg="#0d1117",
        card_bg="#161b22",
        card_stroke="#30363d",
        shell_bg="#1c2128",
        shell_stroke="#30363d",
        title_bar="#21262d",
        text_dim="#8b949e",
        text_main="#c9d1d9",
        text_label="#58a6ff",
        heat_palette=["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"],
    ),
    "light": dict(
        bg="#ffffff",
        card_bg="#f6f8fa",
        card_stroke="#d0d7de",
        shell_bg="#eef1f4",
        shell_stroke="#d0d7de",
        title_bar="#eaeef2",
        text_dim="#57606a",
        text_main="#24292f",
        text_label="#0969da",
        heat_palette=["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"],
    ),
}
