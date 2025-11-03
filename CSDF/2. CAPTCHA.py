from captcha.image import ImageCaptcha
import random
import string
import os
import sys
import webbrowser

WIDTH = 220
HEIGHT = 80
CHARS = string.ascii_uppercase + string.digits
LENGTH = 6

def random_text(length=LENGTH):
    return "".join(random.choice(CHARS) for _ in range(length))

if __name__ == "__main__":
    code = random_text()
    image = ImageCaptcha(width=WIDTH, height=HEIGHT)
    img = image.generate_image(code)
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