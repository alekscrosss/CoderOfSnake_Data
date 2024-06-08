from PIL import Image, ImageDraw, ImageFont
import datetime


def add_date_to_image(image_path: str, date: datetime.datetime):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text = date.strftime("%Y-%m-%d %H:%M:%S")

    draw.text((10, 10), text, font=font, fill="white")
    image.save(image_path)
