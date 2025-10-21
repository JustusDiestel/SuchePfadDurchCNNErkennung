from sympy.integrals.heurisch import heurisch
from PIL import Image, ImageDraw
import MazeCreator
import AStarAlgo

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from CNN import HeuristikNN, MazeDataset

import AStarAlgoCNN
from MazeCreator import returnWeißeBlöcke
from CreateMazeDataset import maze_to_grid

bildBreite = 20*20
feldSeitenlänge = 20
mauerBlöcke = 0.3

breitenBlöcke = int(bildBreite/feldSeitenlänge)
höhenBlöcke = int(bildBreite/feldSeitenlänge)



if __name__ == "__main__":
    mc = MazeCreator.createRandomMaze(bildBreite, feldSeitenlänge, mauerBlöcke, breitenBlöcke, höhenBlöcke)
    mc, start, end, weißeBlöcke = MazeCreator.createStartAndEnd(mc, feldSeitenlänge, breitenBlöcke, höhenBlöcke)
    #img.show()

    heuristic = AStarAlgo.distributeHeuristic(mc, start, end, bildBreite, feldSeitenlänge, mauerBlöcke, breitenBlöcke, höhenBlöcke, weißeBlöcke)
    aPath = AStarAlgo.doAStarAlgo(start, end, weißeBlöcke, heuristic)
    #print(aPath)

    aPathDrawing = ImageDraw.Draw(mc)
    for p in aPath[1:-1]:
        aPathDrawing.rectangle([p[0]*feldSeitenlänge, p[1]*feldSeitenlänge, p[0]*feldSeitenlänge + feldSeitenlänge,p[1]*feldSeitenlänge + feldSeitenlänge], fill="orange")

    mc.show()


    dataset = MazeDataset("dataset.csv")
    loader = DataLoader(dataset, batch_size=16, shuffle=True)

    model = HeuristikNN()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(10):
        total_loss = 0
        for x, y in loader:
            optimizer.zero_grad()
            output = model(x)
            loss = criterion(output.squeeze(), y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1} | Loss: {total_loss:.4f}")

    torch.save(model.state_dict(), "cnn_heuristik.pth")

    # Maze vorbereiten
    grid = maze_to_grid(mc, feldSeitenlänge)
    weißeBlöcke = [(x, y) for y in range(len(grid)) for x in range(len(grid)) if grid[y, x] != 0]

    # Modell laden
    model = HeuristikNN()
    model.load_state_dict(torch.load("cnn_heuristik.pth"))
    model.eval()

    # CNN-basierten Pfad berechnen
    aPath_cnn = AStarAlgoCNN.doAStarAlgoCNN(start, end, weißeBlöcke, grid, model)

    # Pfad einzeichnen
    draw = ImageDraw.Draw(mc)
    if aPath_cnn:
        for p in aPath_cnn[1:-1]:
            draw.rectangle(
                [p[0] * feldSeitenlänge, p[1] * feldSeitenlänge,
                 p[0] * feldSeitenlänge + feldSeitenlänge,
                 p[1] * feldSeitenlänge + feldSeitenlänge],
                fill="blue"
            )
    else:
        print("⚠️ Kein CNN-Pfad gefunden.")

    mc.show()