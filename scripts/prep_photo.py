#!/usr/bin/env python3
"""Prep a photo for ASCII conversion: grayscale, contrast boost, white background."""
import sys
import numpy as np
from PIL import Image, ImageEnhance

def prep_photo(input_path: str, output_path: str = "data/source-prepped.png"):
    img = Image.open(input_path).convert("L")

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.8)

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)

    img.save(output_path)
    print(f"Prepped photo saved to {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <input-image>")
        sys.exit(1)
    prep_photo(sys.argv[1])
