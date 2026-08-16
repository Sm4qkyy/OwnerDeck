from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent

MARK_SRC = Path(
    r"C:\Users\honey\AppData\Local\Temp\codex-clipboard-a8f1b2c5-2730-4c6a-90f8-a49bf0ca950e.jpg"
)
WORDMARK_SRC = Path(
    r"C:\Users\honey\AppData\Local\Temp\codex-clipboard-b7f5028a-01c4-44f3-b3af-1a466ccc627e.jpg"
)


def transparent_logo(src, out, pad_ratio):
    im = Image.open(src).convert("RGBA")
    gray = ImageOps.grayscale(im)
    alpha = gray.point(lambda p: max(0, min(255, int((248 - p) * 3.4))) if p < 248 else 0)
    bbox = alpha.getbbox()
    if not bbox:
        raise SystemExit(f"no logo found in {src}")

    x0, y0, x1, y1 = bbox
    pad = max(8, int(max(x1 - x0, y1 - y0) * pad_ratio))
    box = (
        max(0, x0 - pad),
        max(0, y0 - pad),
        min(im.width, x1 + pad),
        min(im.height, y1 + pad),
    )
    alpha = alpha.crop(box)
    logo = Image.new("RGBA", alpha.size, (0, 0, 0, 0))
    logo.putalpha(alpha)
    logo.save(out)
    return logo


def favicon(mask, color, out):
    size = 512
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    scale = min((size * 0.76) / mask.width, (size * 0.76) / mask.height)
    resized = mask.resize(
        (int(mask.width * scale), int(mask.height * scale)),
        Image.Resampling.LANCZOS,
    )
    image = Image.new("RGBA", resized.size, color)
    image.putalpha(resized.getchannel("A"))
    canvas.alpha_composite(
        image,
        ((size - resized.width) // 2, (size - resized.height) // 2),
    )
    canvas.save(out)


mark = transparent_logo(MARK_SRC, ROOT / "ownerdeck-mark-mask.png", 0.07)
wordmark = transparent_logo(WORDMARK_SRC, ROOT / "ownerdeck-wordmark-mask.png", 0.04)

favicon(mark, (0, 0, 0, 255), ROOT / "favicon.png")
favicon(mark, (255, 255, 255, 255), ROOT / "favicon-dark.png")

print(f"mark {mark.size[0]}x{mark.size[1]}")
print(f"wordmark {wordmark.size[0]}x{wordmark.size[1]}")
