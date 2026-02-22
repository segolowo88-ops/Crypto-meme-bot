# “””
meme_generator.py

Generates MOLTER ($MOLTING) crypto meme images using Pillow.
Custom memes for the MOLTER / Molty / Openclaw AI agent project on Solana.
“””

import io
import random
from PIL import Image, ImageDraw, ImageFont

# ── Meme text pools ──────────────────────────────────────────────────────────

MEMES = {
“random”: [
(“Molty sees a dip 🦀”, “MOLTING season activated 🚀”),
(“Other AIs trade stocks”, “Molty trades $MOLTING on Solana 🦀”),
(“This is fine 🔥”, “$MOLTING at -80%\nMolty: still bullish”),
(“My portfolio:”, “100% $MOLTING\nNo regrets 🦀”),
(“Molty after analyzing\nthe chart for 3 seconds:”, “Buy more $MOLTING”),
(“Not financial advice”, “But Molty says MOLT or regret 🦀”),
(“When $MOLTING pumps:”, “I am a genius AI crab 🦀”),
(“When $MOLTING dips:”, “Molty calls it a discount 🦀”),
(“Openclaw agent Molty:”, “Running on vibes\nand Solana speed 🚀”),
(“1 $MOLTING = 1 $MOLTING”, “That’s the math 🦀”),
(“Bearish in the streets”, “Molty molting in the sheets 🦀”),
(“My therapist:”, ‘“Tell me about Molty”\n\nMe: 👁️👄👁️’),
],
“moon”: [
(“Molty locked in moon\ncalculations 🦀🌙”, “ETA: next molt cycle”),
(”$MOLTING to the moon 🚀”, “Molty already bought the ticket”),
(“Moon mission initiated”, “Pilot: Molty 🦀\nFuel: hopium + Solana”),
(“Wen moon $MOLTING?”, “When Molty finishes molting 🦀”),
(“Moon gang 🌙🦀”, “MOLT or HFSP”),
(“LFG $MOLTING 🚀🌙”, “Molty has spoken 🦀”),
],
“coin”: [
(“Other memecoins:”, “Just memes\n$MOLTING: memes + AI + trading 🦀”),
(“Diversified portfolio:”, “100% $MOLTING\nMolty approves 🦀”),
(”$MOLTING is different 👀”, “AI crab on Solana\nName a better duo”),
(“Fundamental analysis\nby Molty 🦀:”, “Number go up? MOLT\nNumber go down? MOLT more”),
(“Openclaw agent Molty\nprocessing trade data:”, “Conclusion: buy $MOLTING”),
(“Solana speed ⚡”, “Molty moves faster\nthan your CEX 🦀”),
],
“wen”: [
(“Wen $MOLTING lambo? 🏎️”, “Wen Molty finishes\nhis next molt 🦀”),
(“Wen listing? 🏦”, “Molty is already\non the move 🦀”),
(“Wen AI agent\ntakes over trading?”, “Molty: I’m already here 🦀”),
(“Wen $MOLTING moon? 🌙”, “Openclaw never sleeps 🦀”),
(“Wen financial freedom?”, “Probably wen you\nstop asking Molty 🦀”),
(“Wen Solana flips ETH?”, “Molty: sooner than\nyou think anon 🦀”),
],
}

# ── Color palettes (MOLTER themed) ───────────────────────────────────────────

PALETTES = [
{“bg”: (15, 8, 5),  “accent”: (220, 80, 30),  “text”: (255,255,255), “sub”: (255,200,170)},
{“bg”: (8, 5, 25),  “accent”: (153, 69, 255), “text”: (255,255,255), “sub”: (210,180,255)},
{“bg”: (5, 20, 15), “accent”: (20, 241, 149), “text”: (255,255,255), “sub”: (160,255,210)},
{“bg”: (5, 10, 35), “accent”: (0, 180, 255),  “text”: (255,255,255), “sub”: (160,220,255)},
{“bg”: (20, 15, 5), “accent”: (255, 190, 20), “text”: (255,255,255), “sub”: (255,230,150)},
{“bg”: (25, 5, 5),  “accent”: (255, 50, 50),  “text”: (255,255,255), “sub”: (255,180,180)},
]

class MemeGenerator:
WIDTH  = 800
HEIGHT = 500

```
def generate(self, category: str = "random") -> io.BytesIO:
    pool = MEMES.get(category, MEMES["random"])
    top_text, bottom_text = random.choice(pool)
    palette = random.choice(PALETTES)

    img = Image.new("RGB", (self.WIDTH, self.HEIGHT), palette["bg"])
    draw = ImageDraw.Draw(img)

    self._draw_background(draw, palette)
    self._draw_grid(draw, palette)
    self._draw_chart(draw, palette)
    self._draw_crab(draw, palette)
    self._draw_text(draw, top_text, bottom_text, palette)
    self._draw_watermark(draw, palette)

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    buf.seek(0)
    return buf

def _draw_background(self, draw, palette):
    bg = palette["bg"]
    for y in range(self.HEIGHT):
        factor = y / self.HEIGHT
        r = int(bg[0] + (30 * factor))
        g = int(bg[1] + (20 * factor))
        b = int(bg[2] + (40 * factor))
        draw.line([(0, y), (self.WIDTH, y)], fill=(min(r,255), min(g,255), min(b,255)))

def _draw_grid(self, draw, palette):
    col = tuple(min(c + 20, 255) for c in palette["bg"])
    for x in range(0, self.WIDTH, 60):
        draw.line([(x, 0), (x, self.HEIGHT)], fill=col, width=1)
    for y in range(0, self.HEIGHT, 40):
        draw.line([(0, y), (self.WIDTH, y)], fill=col, width=1)

def _draw_chart(self, draw, palette):
    chart_y_base = int(self.HEIGHT * 0.75)
    chart_height = int(self.HEIGHT * 0.35)
    points_count = 60
    x_step = self.WIDTH / points_count

    values = [random.gauss(0.5, 0.15) for _ in range(points_count)]
    trend = random.choice([-1, 1])
    for i in range(len(values)):
        values[i] += trend * i * 0.008

    mn, mx = min(values), max(values)
    norm = [(v - mn) / (mx - mn + 1e-9) for v in values]
    pts = [(int(i * x_step), int(chart_y_base - norm[i] * chart_height)) for i in range(points_count)]

    poly = [(0, chart_y_base)] + pts + [(self.WIDTH, chart_y_base)]
    accent = palette["accent"]

    img_overlay = Image.new("RGBA", (self.WIDTH, self.HEIGHT), (0, 0, 0, 0))
    od = ImageDraw.Draw(img_overlay)
    od.polygon(poly, fill=(*accent, 25))
    base = draw._image
    base.paste(Image.alpha_composite(base.convert("RGBA"), img_overlay).convert("RGB"))

    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=accent, width=2)

def _draw_crab(self, draw, palette):
    accent = palette["accent"]
    x, y = self.WIDTH - 115, self.HEIGHT - 115
    draw.ellipse([x, y, x+60, y+40], fill=accent)
    draw.ellipse([x-20, y+5, x+10, y+25], fill=accent)
    draw.ellipse([x+50, y+5, x+80, y+25], fill=accent)
    draw.ellipse([x+12, y+8, x+22, y+18], fill=(255,255,255))
    draw.ellipse([x+38, y+8, x+48, y+18], fill=(255,255,255))
    draw.ellipse([x+15, y+11, x+19, y+15], fill=(0,0,0))
    draw.ellipse([x+41, y+11, x+45, y+15], fill=(0,0,0))
    for i in range(3):
        lx = x + 5 + i * 15
        draw.line([(lx, y+35), (lx-8, y+55)], fill=accent, width=3)
        draw.line([(lx+35, y+35), (lx+43, y+55)], fill=accent, width=3)

def _draw_text(self, draw, top, bottom, palette):
    W, H = self.WIDTH, self.HEIGHT
    try:
        font_big   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except Exception:
        font_big   = ImageFont.load_default()
        font_small = ImageFont.load_default()
    self._draw_centered_text(draw, top,    font_big,   palette["text"], palette["accent"], W//2, H//5,        W-60)
    self._draw_centered_text(draw, bottom, font_small, palette["sub"],  palette["bg"],     W//2, int(H*0.58), W-80)

def _draw_centered_text(self, draw, text, font, color, shadow_color, cx, cy, max_width):
    lines = text.split("\n")
    line_height = font.size + 8
    y = cy - (line_height * len(lines)) // 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = cx - tw // 2
        for dx, dy in [(-2,-2),(2,-2),(-2,2),(2,2),(0,3)]:
            draw.text((x+dx, y+dy), line, font=font, fill=shadow_color)
        draw.text((x, y), line, font=font, fill=color)
        y += line_height

def _draw_watermark(self, draw, palette):
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except Exception:
        font = ImageFont.load_default()
    draw.text((20, self.HEIGHT - 30), "@mMOLTINGbot  •  $MOLTING 🦀", font=font, fill=(*palette["accent"][:3],))

def get_caption(self, category: str) -> str:
    captions = {
        "random": ["🦀 Molty has spoken", "🔥 $MOLTING szn", "👀 Openclaw watching", "😭 Molty felt that"],
        "moon":   ["🌙 Molt to the moon", "🚀 LFG $MOLTING!", "🦀 Molty strapped in"],
        "coin":   ["🦀 $MOLTING different", "💎 Claw hands only", "⚡ Solana speed"],
        "wen":    ["🦀 Wen Molty decides", "⏳ Molt cycle soon™", "🤡 We're so back"],
    }
    pool = captions.get(category, captions["random"])
    return random.choice(pool) + "\n\n_$MOLTING • Openclaw AI Agent • Solana 🦀_"
```
