from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def generate_countdown_image(game_image_url, time_left_str):
    response = requests.get(game_image_url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")

    overlay = Image.new('RGBA', img.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font = ImageFont.load_default()

    text = f"⏳ ينتهي بعد: {time_left_str}"
    draw.rectangle([10, 10, 500, 70], fill=(255, 0, 0, 200))
    draw.text((20, 15), text, font=font, fill="white")

    out = Image.alpha_composite(img, overlay)

    bio = BytesIO()
    bio.name = 'deal.png'
    out.convert("RGB").save(bio, 'PNG')
    bio.seek(0)
    return bio
