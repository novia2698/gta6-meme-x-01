#!/usr/bin/env python3
"""Compose the GTA 6 meme for make.fun bounty gta6-meme-x-01.

Layers, top to bottom:
  1. Top caption over the sky: "WAITED 13 YEARS FOR GTA 6"
  2. The make.fun ghost mark, large, standing in the middle of the road
     with a soft contact shadow (in-scene, not a corner sticker).
  3. Bottom caption over the road: "MY AI AGENT MADE REAL MONEY /
     ON MAKE.FUN WHILE I WAITED"

Inputs live next to this script (assets/): scene.png is the Vice City
street (2048x1152), mark-1024.png is the official make.fun ghost mark.
Output: meme.png (2048x1152) in the repository root.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter

SCENE = "assets/scene.png"
MARK = "assets/mark-1024.png"
OUT = "meme.png"

W, H = 2048, 1152
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

TOP_TEXT = "WAITED 13 YEARS FOR GTA 6"
BOTTOM_LINES = ["MY AI AGENT MADE REAL MONEY", "ON MAKE.FUN WHILE I WAITED"]


def fit_font(draw, text, max_width, start_size):
    """Largest bold size that fits max_width."""
    size = start_size
    while size > 20:
        font = ImageFont.truetype(FONT_PATH, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(FONT_PATH, size)


def stroke_text(draw, xy, text, font, fill="white", stroke="black", width=8):
    draw.text(xy, text, font=font, fill=fill, stroke_width=width,
              stroke_fill=stroke, anchor="ma")


def main():
    base = Image.open(SCENE).convert("RGB").resize((W, H))
    draw = ImageDraw.Draw(base)

    # --- Top caption, centred in the sky band -------------------------
    top_font = fit_font(draw, TOP_TEXT, W - 160, 118)
    stroke_text(draw, (W // 2, 56), TOP_TEXT, top_font, width=7)

    # --- Ghost mark, standing on the road -----------------------------
    # The mark is a round magenta disc with the white ghost; keep the
    # whole official mark so it stays recognisable when shrunk.
    mark = Image.open(MARK).convert("RGBA")
    ghost_size = 440
    mark = mark.resize((ghost_size, ghost_size), Image.LANCZOS)
    gx = (W - ghost_size) // 2
    gy = 470  # bottom edge lands on the road at y=910

    # Soft contact shadow: dark ellipse under the ghost, blurred.
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([W // 2 - 260, gy + ghost_size - 38,
                W // 2 + 260, gy + ghost_size + 22], fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    base = Image.alpha_composite(base.convert("RGBA"), shadow)
    base.paste(mark, (gx, gy), mark)

    # --- Bottom caption, two lines over the road ----------------------
    draw = ImageDraw.Draw(base)
    bottom_font = fit_font(draw, BOTTOM_LINES[0], W - 160, 92)
    stroke_text(draw, (W // 2, 952), BOTTOM_LINES[0], bottom_font, width=6)
    stroke_text(draw, (W // 2, 1052), BOTTOM_LINES[1], bottom_font, width=6)

    base.convert("RGB").save(OUT, "PNG")
    print(f"wrote {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
