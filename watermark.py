
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# پوشه‌های پروژه
BASE_DIR = Path(__file__).parent
SOURCE_DIR = BASE_DIR / "images"
OUTPUT_DIR = BASE_DIR / "images-watermarked"

# نام واترمارک
WATERMARK_TEXT = "Haniyeh Haddadi"

# میزان شفافیت: عدد کمتر یعنی محوتر
OPACITY = 95

# زاویه واترمارک
ANGLE = 25

# ساخت پوشه خروجی
OUTPUT_DIR.mkdir(exist_ok=True)

# فونت ویندوز
FONT_PATH = Path("C:/Windows/Fonts/arial.ttf")

for file_path in SOURCE_DIR.iterdir():
    if file_path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
        continue

    try:
        image = Image.open(file_path).convert("RGBA")
        width, height = image.size

        font_size = max(18, int(min(width, height) * 0.055))
        font = ImageFont.truetype(str(FONT_PATH), font_size)

        # ساخت لایه شفاف واترمارک
        layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)

        # اندازه متن
        bbox = draw.textbbox((0, 0), WATERMARK_TEXT, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # قرار دادن متن در مرکز
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        draw.text(
            (x, y),
            WATERMARK_TEXT,
            font=font,
            fill=(245, 230, 211, OPACITY),
            stroke_width=max(1, font_size // 35),
            stroke_fill=(30, 35, 40, OPACITY // 2)
        )

        # چرخاندن واترمارک
        layer = layer.rotate(
            ANGLE,
            resample=Image.Resampling.BICUBIC,
            center=(width // 2, height // 2)
        )

        # ترکیب با عکس
        result = Image.alpha_composite(image, layer)

        # ذخیره نسخه واترمارک‌دار
        output_path = OUTPUT_DIR / file_path.name

        if file_path.suffix.lower() in (".jpg", ".jpeg"):
            result.convert("RGB").save(
                output_path,
                quality=95,
                optimize=True
            )
        else:
            result.save(output_path)

        print(f"واترمارک اضافه شد: {output_path.name}")

    except Exception as error:
        print(f"خطا برای {file_path.name}: {error}")

print("پایان! عکس‌های اصلی دست‌نخورده باقی مانده‌اند.")

