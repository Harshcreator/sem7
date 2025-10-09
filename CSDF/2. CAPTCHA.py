import random
import string
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import webbrowser

WIDTH = 220
HEIGHT = 80
CHARS = string.ascii_uppercase + string.digits
LENGTH = 6
FONT_SIZE = 40

def random_text(length=LENGTH):
    return "".join(random.choice(CHARS) for _ in range(length))

def load_font(size=FONT_SIZE):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 
        "C:\\Windows\\Fonts\\arial.ttf",                       
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def generate_captcha(text):
    img = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = load_font()

    for _ in range(8):
        x0 = random.randint(0, WIDTH)
        y0 = random.randint(0, HEIGHT)
        x1 = x0 + random.randint(30, 120)
        y1 = y0 + random.randint(10, 60)
        color = tuple(random.randint(200, 255) for _ in range(3))
        draw.rectangle([x0, y0, x1, y1], fill=color)

    char_x = 10
    for ch in text:
        y = random.randint(5, 20)
        angle = random.uniform(-25, 25)
        ch_img = Image.new("RGBA", (FONT_SIZE+10, FONT_SIZE+10), (0,0,0,0))
        ch_draw = ImageDraw.Draw(ch_img)
        ch_draw.text((5, 0), ch, font=font, fill=(0,0,0))
        ch_img = ch_img.rotate(angle, resample=Image.BICUBIC, expand=1)
        img.paste(ch_img, (char_x, y), ch_img)
        char_x += FONT_SIZE - 6 + random.randint(-4, 6)

    for _ in range(6):
        x1 = random.randint(0, WIDTH)
        y1 = random.randint(0, HEIGHT)
        x2 = random.randint(0, WIDTH)
        y2 = random.randint(0, HEIGHT)
        draw.line([(x1,y1),(x2,y2)], fill=tuple(random.randint(0,120) for _ in range(3)), width=random.randint(1,3))

    for _ in range(200):
        x = random.randint(0, WIDTH-1)
        y = random.randint(0, HEIGHT-1)
        draw.point((x,y), fill=tuple(random.randint(0,200) for _ in range(3)))

    img = img.filter(ImageFilter.SMOOTH)
    return img

if __name__ == "__main__":
    code = random_text()
    img = generate_captcha(code)
    out_file = "captcha.png"
    img.save(out_file)
    print(f"CAPTCHA image saved to: {out_file}")

    try:
        if sys.platform.startswith("linux"):
            os.system(f"xdg-open {out_file}")
        elif sys.platform.startswith("win"):
            os.startfile(out_file)
        else:
            webbrowser.open("file://" + os.path.abspath(out_file))
    except Exception:
        pass

    user_input = input("Enter CAPTCHA: ").strip()
    if user_input.upper() == code:
        print("Verified — input matches CAPTCHA.")
    else:
        print("Not verified — input does NOT match.")
        print("Actual CAPTCHA was:", code)