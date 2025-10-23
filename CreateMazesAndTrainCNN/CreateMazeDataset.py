import MazeCreator
import os
from PIL import Image
import csv

from AStarAlgo import doAStarAlgo
from CNN.PreparationsForCNN import maze_to_grid
import numpy as np


def createDataset(bildBreite, feldSeitenlänge, mauerBlöcke, breitenBlöcke, höhenBlöcke, anzahl):
    os.makedirs("../Data/MazesDatensatz", exist_ok=True)
    daten = []
    for x in range(anzahl):
        img = MazeCreator.createRandomMaze(bildBreite, feldSeitenlänge, mauerBlöcke, breitenBlöcke, höhenBlöcke)
        img, start, end, weißeBlöcke = MazeCreator.createStartAndEnd(img, feldSeitenlänge, breitenBlöcke, höhenBlöcke)
        dateiname = os.path.join("../Data/MazesDatensatz", f"{x}.png")
        img.save(dateiname)
        daten.append((dateiname, start[0], start[1], end[0], end[1]))

    return daten

def create_csv_from_mazes(daten, csv_path="dataset.csv", feldgröße=20):
    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["maze", "start_x", "start_y", "end_x", "end_y", "path_length"])

        for path, sx, sy, ex, ey in daten:
            img = Image.open(path)
            grid = maze_to_grid(img, feldgröße=feldgröße)
            np.save(path.replace(".png", ".npy"), grid)

            weißeBlöcke = [(x, y) for y in range(20) for x in range(20) if grid[y, x] != 0]
            start_block = (sx // feldgröße, sy // feldgröße)
            end_block = (ex // feldgröße, ey // feldgröße)
            path_astar = doAStarAlgo(start_block, end_block, weißeBlöcke, {})
            path_length = len(path_astar) if path_astar else -1

            writer.writerow([path, sx, sy, ex, ey, path_length])




if __name__ == "__main__":
    bildBreite = 400
    feldSeitenlänge = 20
    mauerBlöcke = 0.3

    breitenBlöcke = int(bildBreite / feldSeitenlänge)
    höhenBlöcke = int(bildBreite / feldSeitenlänge)
    anzahl = 100

    daten = createDataset(bildBreite, feldSeitenlänge, mauerBlöcke, breitenBlöcke, höhenBlöcke, anzahl)
    create_csv_from_mazes(daten, "../Data/dataset.csv", feldgröße=20)