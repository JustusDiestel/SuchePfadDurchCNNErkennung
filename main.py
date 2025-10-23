from PIL import ImageDraw
import MazeCreator
import AStarAlgo

import torch
from CNN.CNN import HeuristikNN
import AStarAlgoCNN
from torchvision import transforms

bildBreite = 20*20
feldSeitenlänge = 20
mauerBlöcke = 0.3

breitenBlöcke = int(bildBreite/feldSeitenlänge)
höhenBlöcke = int(bildBreite/feldSeitenlänge)



if __name__ == "__main__":
    #Hier werden random Mazes erstellt und wir merken uns das Bild, den Startpunkt, den Endpunkt, und welche Blöcke keine Mauer sind
    img = MazeCreator.createRandomMaze(bildBreite, feldSeitenlänge, mauerBlöcke, breitenBlöcke, höhenBlöcke)
    img, start, end, weißeBlöcke = MazeCreator.createStartAndEnd(img, feldSeitenlänge, breitenBlöcke, höhenBlöcke)
    #img.show()

    #Wir bestimmen die Heuristic der Felder mittels Manhatten Metrik
    heuristic = AStarAlgo.distributeHeuristic(img, start, end, bildBreite, feldSeitenlänge, mauerBlöcke, breitenBlöcke, höhenBlöcke, weißeBlöcke)

    #Wir ermitteln den schnellsten Weg mittels A* und zeichnen ihn ein
    aPath = AStarAlgo.doAStarAlgo(start, end, weißeBlöcke, heuristic)
    aPathDrawing = ImageDraw.Draw(img)
    for p in aPath[1:-1]:
        aPathDrawing.rectangle([p[0]*feldSeitenlänge, p[1]*feldSeitenlänge, p[0]*feldSeitenlänge + feldSeitenlänge,p[1]*feldSeitenlänge + feldSeitenlänge], fill="orange")

    img.show()




    # Modell laden
    model = HeuristikNN()
    model.load_state_dict(torch.load("CreateMazesAndTrainCNN/cnn_heuristik.pth"))
    model.eval()

    # Bild als Tensor vorbereiten (Grayscale, Resize, ToTensor)
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((bildBreite, bildBreite)),
        transforms.ToTensor()
    ])
    img_tensor = transform(img)

    # CNN Pfad berechnen
    aPath_cnn = AStarAlgoCNN.doAStarAlgoCNN(start, end, model, img_tensor)

    # Pfad einzeichnen
    draw = ImageDraw.Draw(img)
    if aPath_cnn:
        for p in aPath_cnn[1:-1]:
            draw.rectangle(
                [p[0] * feldSeitenlänge, p[1] * feldSeitenlänge,
                 p[0] * feldSeitenlänge + feldSeitenlänge,
                 p[1] * feldSeitenlänge + feldSeitenlänge],
                fill="blue"
            )
    else:
        print("gibt keinen")

    img.show()