"""
meme_generator.py
=================
Generates crypto meme images using Pillow (no external APIs needed).
All memes are procedurally generated — no image files required.
"""

import io
import random
import math
import textwrap
from PIL import Image, ImageDraw, ImageFont

# ── Meme text pools ──────────────────────────────────────────────────────────

MEMES = {
    "random": [
        ("This is fine 🔥", "Crypto market at -80%"),
        ("They told me to\nsell the top", "I bought more instead"),
        ("My portfolio be like:", "📉📉📉📉📉"),
        ("Diamond hands 💎🙌", "Paper hands 📄🤚"),
        ("Me explaining crypto\nto my parents", "stonks 📈"),
        ("Not financial advice", "But seriously... buy the dip"),
        ("When the chart goes up:", "I'm a genius investor"),
        ("When the chart goes down:", "It's just a correction"),
        ("HODL", "Hold On for Dear Life"),
        ("1 BTC = 1 BTC", "That's it. That's the meme."),
        ("Bearish in the streets\nBullish in the sheets", "WAGMI 🚀"),
        ("My therapist:", '"Tell me about your portfolio"\n\nMe: 👁️👄👁️'),
    ],
    "moon": [
        ("We're going to the moon! 🌙", "NASA: We're not affiliated"),
        ("To the moon 🚀", "Sir, this is a Wendy's"),
        ("Moon mission initiated", "ETA: undefined\nFuel: hopium"),
        ("When Lambo?", "When moon?\nWhen McDonald's?"),
        ("Moon gang 🌙", "WAGMI or HFSP"),
        ("LFG 🚀🌙", "Strap in, anon"),
    ],
    "coin": [
        ("Buy high, sell low", "Instructions unclear"),
        ("Diversified portfolio:", "100% memecoins"),
        ("This coin is different 👀", "They always say this"),
        ("When the devs rugpull:", "Should've bought BTC"),
        ("Fundamental analysis:", "Number go up? Buy\nNumber go down? Buy more"),
        ("My coin vs Bitcoin:", "Same chart, more hopium"),
    ],
    "wen": [
        ("Wen lambo? 🏎️", "When you stop asking"),
        ("Wen moon?", "Astronomers hate him"),
        ("Wen lambo:", "Sir your portfolio is -95%"),
        ("Wen listing? 🏦", "Wen airdrop? Wen anything?"),
        ("Wen lambo 🏎️", "Current status: still on bicycle"),
        ("Wen financial freedom?", "Probably wen I stop buying dips"),
    ],
}

# ── Color palettes ────────────────────────────────────────────────────────────

PALETTES = [
    {"bg": (10, 10, 30), "accent": (247, 147, 26), "text": (255, 255, 255), "sub": (200, 200, 200)},
    {"bg": (5, 30, 15), "accent": (0, 230, 100), "text": (255, 255, 255), "sub": (180, 240, 180)},
    {"bg": (30, 5, 5), "accent": (255, 60, 60), "text": (255, 255, 255), "sub": (240, 180, 180)},
    {"bg": (5, 10, 40), "accent": (60, 140, 255), "text": (255, 255, 255), "sub": (180, 200, 255)},
    {"bg": (20, 5, 35), "accent": (180, 60, 255), "text": (255, 255, 255), "sub": (220, 180, 255)},
    {"bg": (25, 20, 5), "accent": (255, 200, 30), "text": (255, 255, 255), "sub": (240, 220, 150)},
]


class MemeGenerator:
    WIDTH  = 800
    HEIGHT = 500

    def generate(self, category: str = "random") -> io.BytesIO:
        pool = MEMES.get(category, MEMES["random"])
        top_text, bottom_text = random.choice(pool)
        palette = random.choice(PALETTES)

        img = Image.new("RGB", (self.WIDTH, self.HEIGHT), palette["bg"])
        draw = ImageDraw.Draw(img)

        self._draw_background(draw, palette)
        self._draw_grid(draw, palette)
        self._draw_chart(draw, palette)
        self._draw_text(draw, top_text, bottom_text, palette)
        self._draw_watermark(draw, palette)

        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        buf.seek(0)
        return buf

    def _draw_background(self, draw: ImageDraw.Draw, palette: dict):
        bg = palette["bg"]
        for y in range(self.HEIGHT):
            factor = y / self.HEIGHT
            r = int(bg[0] + (30 * factor))
            g = int(bg[1] + (20 * factor))
            b = int(bg[2] + (40 * factor))
            draw.line([(0, y), (self.WIDTH, y)], fill=(
                min(r, 255), min(g, 255), min(b, 255)
            ))

    def _draw_grid(self, draw: ImageDraw.Draw, palette: dict):
        col = tuple(min(c + 20, 255) for c in palette["bg"])
        for x in range(0, self.WIDTH, 60):
            draw.line([(x, 0), (x, self.HEIGHT)], fill=col, width=1)
        for y in range(0, self.HEIGHT, 40):
            draw.line([(0, y), (self.WIDTH, y)], fill=col, width=1)

    def _draw_chart(self, draw: ImageDraw.Draw, palette: dict):
        chart_y_base = int(self.HEIGHT * 0.75)
        chart_height  = int(self.HEIGHT * 0.35)
        points_count  = 60
        x_step = self.WIDTH / points_count

        values = [random.gauss(0.5, 0.15) for _ in range(points_count)]
        trend = random.choice([-1, 1])
        for i in range(len(values)):
            values[i] += trend * i * 0.008

        mn, mx = min(values), max(values)
        norm = [(v - mn) / (mx - mn + 1e-9) for v in values]

        pts = [
            (int(i * x_step), int(chart_y_base - norm[i] * chart_height))
            for i in range(points_count)
        ]

        poly = [(0, chart_y_base)] + pts + [(self.WIDTH, chart_y_base)]
        accent = palette["accent"]

        img_overlay = Image.new("RGBA", (self.WIDTH, self.HEIGHT), (0, 0, 0, 0))
        od = ImageDraw.Draw(img_overlay)
        od.polygon(poly, fill=(*accent, 25))
        base = draw._image
        base.paste(Image.alpha_composite(base.convert("RGBA"), img_overlay).convert("RGB"))

        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i + 1]], fill=accent, width=2)

    def _draw_text(self, draw: ImageDraw.Draw, top: str, bottom: str, palette: dict):
        W, H = self.WIDTH, self.HEIGHT

        try:
            font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        except Exception:
            font_big = ImageFont.load_default()
            font_small = ImageFont.load_default()

        self._draw_centered_text(draw, top, font_big, palette["text"], palette["accent"],
                                  W // 2, H // 5, W - 60)
        self._draw_centered_text(draw, bottom, font_small, palette["sub"], palette["bg"],
                                  W // 2, int(H * 0.58), W - 80)

    def _draw_centered_text(self, draw, text, font, color, shadow_color, cx, cy, max_width):
        lines = text.split("\n")
        line_height = font.size + 8
        total_h = line_height * len(lines)
        y = cy - total_h // 2

        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            x = cx - tw // 2
            for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, 3)]:
                draw.text((x + dx, y + dy), line, font=font, fill=shadow_color)
            draw.text((x, y), line, font=font, fill=color)
            y += line_height

    def _draw_watermark(self, draw: ImageDraw.Draw, palette: dict):
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        except Exception:
            font = ImageFont.load_default()
        text = "@CryptoMemeBot  •  WAGMI 🚀"
        draw.text((20, self.HEIGHT - 30), text, font=font, fill=(*palette["accent"][:3],))

    def get_caption(self, category: str) -> str:
        captions = {
            "random": ["😂 Crypto life", "🔥 This hits different", "👀 Too real", "😭 My portfolio rn"],
            "moon":   ["🌙 Moon gang assemble", "🚀 LFG!", "📈 Strap in anon"],
            "coin":   ["🪙 DYOR (but also buy)", "💎 Diamond hands only", "📉 Just a correction"],
            "wen":    ["🏎️ Wen lambo era", "⏳ Soon™", "🤡 We're so back"],
        }
        pool = captions.get(category, captions["random"])
        return random.choice(pool) + "\n\n_Not financial advice. WAGMI 🙌_"
