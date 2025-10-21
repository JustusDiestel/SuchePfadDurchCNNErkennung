'''NUR CHAT WEIL ICH BIN MÜDE'''

import torch
from heapq import heappush, heappop
from CNN import HeuristikNN
import numpy as np


# 🧠 Hilfsfunktion: CNN-Heuristik für ein Feld berechnen
def cnn_heuristic(model, grid, pos, end):
    # Kopie des Grids erzeugen, mit markiertem Ziel (optional)
    g_copy = np.copy(grid)
    g_copy[end[1], end[0]] = 3.0
    g_copy[pos[1], pos[0]] = 2.0

    tensor = torch.tensor(g_copy).unsqueeze(0).unsqueeze(0).float()
    with torch.no_grad():
        h_val = model(tensor).item()
    return h_val


# 🧩 A*-Algorithmus mit CNN-Heuristik
def doAStarAlgoCNN(start, end, weißeBlöcke, grid, model):
    open_set = []
    heappush(open_set, (0, start))

    came_from = {}
    laufAufwand = {w: float('inf') for w in weißeBlöcke}
    laufAufwand[start] = 0

    while open_set:
        _, current = heappop(open_set)

        if current == end:
            return reconstruct_path(came_from, current)

        x, y = current
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        neighbors = [n for n in neighbors if n in weißeBlöcke]

        for neighbor in neighbors:
            neuerLaufaufwand = laufAufwand[current] + 1

            if neuerLaufaufwand < laufAufwand[neighbor]:
                laufAufwand[neighbor] = neuerLaufaufwand
                came_from[neighbor] = current

                # 💡 CNN-Heuristik berechnen
                h = cnn_heuristic(model, grid, neighbor, end)
                f_score = neuerLaufaufwand + h
                heappush(open_set, (f_score, neighbor))

    return None


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]