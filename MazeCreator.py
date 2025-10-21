from PIL import Image, ImageDraw
import random



def createRandomMaze(bildBreite, feldSeitenlänge, mauerBlöcke, breitenBlöcke, höhenBlöcke):
    realiverWandanteil = 0.7#random.random()
    img = Image.new("RGB", (bildBreite, bildBreite), "white")
    draw = ImageDraw.Draw(img)
    anzMauern = 0
    anzBlöcke = bildBreite * bildBreite / feldSeitenlänge ** 2
    for x in range(breitenBlöcke):
        for y in range(höhenBlöcke):
            if random.random() >realiverWandanteil :
                if mauerBlöcke > anzMauern/anzBlöcke:
                    x0, y0 = x * feldSeitenlänge, y * feldSeitenlänge
                    pixel = img.getpixel((x0+1, y0+1))
                    if pixel != (0,0,0):
                        draw.rectangle([x0, y0, x0 + feldSeitenlänge, y0 + feldSeitenlänge], fill="black")
    #img.show()
    return img

def createStartAndEnd(img, feldSeitenlänge, breitenBlöcke, höhenBlöcke):
    weißeBlöcke = returnWeißeBlöcke(img, feldSeitenlänge, breitenBlöcke, höhenBlöcke)
    start = random.choice(weißeBlöcke)
    weißeBlöcke.remove(start)
    end = random.choice(weißeBlöcke)
    draw = ImageDraw.Draw(img)
    print(len(weißeBlöcke))

    #mrin Start ist grün und das Ziel ist rot
    sx, sy = start[0] * feldSeitenlänge, start[1] * feldSeitenlänge
    ex, ey = end[0] * feldSeitenlänge, end[1] * feldSeitenlänge

    draw.rectangle([sx, sy, sx + feldSeitenlänge, sy + feldSeitenlänge], fill="green")
    draw.rectangle([ex, ey, ex + feldSeitenlänge, ey + feldSeitenlänge], fill="red")
    #img.show()
    return img, start, end, weißeBlöcke

def returnWeißeBlöcke(img, feldSeitenlänge, breitenBlöcke, höhenBlöcke):
    weißeBlöcke = []
    draw = ImageDraw.Draw(img)
    for x in range(breitenBlöcke):
        for y in range(höhenBlöcke):
            x0, y0 = x * feldSeitenlänge, y * feldSeitenlänge
            px = x0 + feldSeitenlänge // 2
            py = y0 + feldSeitenlänge // 2
            pixel = img.getpixel((px, py))

            if pixel != (0,0,0):
                weißeBlöcke.append((x, y))
                # zur Kontrolle einzeichnen:
                draw.rectangle([x0, y0, x0 + feldSeitenlänge, y0 + feldSeitenlänge])
    #img.show()
    return weißeBlöcke