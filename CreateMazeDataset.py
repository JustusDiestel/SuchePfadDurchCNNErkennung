import MazeCreator
import os
from PIL import Image



def createDataset(bildBreite, feldSeitenlänge, mauerBlöcke, breitenBlöcke, höhenBlöcke, anzahl):
    os.makedirs("MazesDatensatz", exist_ok=True)
    for x in range(anzahl):
        img = MazeCreator.createRandomMaze(bildBreite, feldSeitenlänge, mauerBlöcke, breitenBlöcke, höhenBlöcke)
        img, start, end, weißeBlöcke = MazeCreator.createStartAndEnd(img, feldSeitenlänge, breitenBlöcke, höhenBlöcke)
        dateiname = os.path.join("MazesDatensatz", f"{x}.png")
        img.save(dateiname)



if __name__ == "__main__":
    bildBreite = 400
    feldSeitenlänge = 20
    mauerBlöcke = 0.3

    breitenBlöcke = int(bildBreite / feldSeitenlänge)
    höhenBlöcke = int(bildBreite / feldSeitenlänge)
    anzahl = 100

    createDataset(bildBreite, feldSeitenlänge, mauerBlöcke, breitenBlöcke, höhenBlöcke, anzahl)

