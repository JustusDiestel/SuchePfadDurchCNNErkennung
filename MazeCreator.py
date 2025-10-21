from PIL import Image, ImageDraw
import random

bildBreite = 400
feldSeitenlänge = 20
mauerBlöcke = 0.3

breitenBlöcke = int(bildBreite/feldSeitenlänge)
höhenBlöcke = int(bildBreite/feldSeitenlänge)

def createRandomMaze():
    img = Image.new("RGB", (bildBreite, bildBreite), "white")
    draw = ImageDraw.Draw(img)
    anzMauern = 0
    anzBlöcke = bildBreite * bildBreite / feldSeitenlänge ** 2
    for x in range(breitenBlöcke):
        for y in range(höhenBlöcke):
            if random.random() > 0.7:
                if mauerBlöcke > anzMauern/anzBlöcke:
                    x0, y0 = x * breitenBlöcke, y *breitenBlöcke
                    pixel = img.getpixel((x0, y0))
                    if pixel != (0,0,0):
                        draw.rectangle([x0, y0, x0 + feldSeitenlänge, y0 + feldSeitenlänge], fill="black")
    return img

def createStartAndEnd(img):
    weißeBlöcke = []
    for x in range(breitenBlöcke):
        for y in range(höhenBlöcke):
            x0, y0 = x * feldSeitenlänge, y * feldSeitenlänge
            pixel = img.getpixel((x0, y0))
            if pixel != (0, 0, 0):
                weißeBlöcke.append((x, y))
    start = random.choice(weißeBlöcke)
    weißeBlöcke.remove(start)
    end = random.choice(weißeBlöcke)
    draw = ImageDraw.Draw(img)

    #mrin Start ist grün und das Ziel ist rot
    sx, sy = start[0] * feldSeitenlänge, start[1] * feldSeitenlänge
    ex, ey = end[0] * feldSeitenlänge, end[1] * feldSeitenlänge

    draw.rectangle([sx, sy, sx + feldSeitenlänge, sy + feldSeitenlänge], fill="green")
    draw.rectangle([ex, ey, ex + feldSeitenlänge, ey + feldSeitenlänge], fill="red")

    return img
