'''NUR CHAT WEIL ICH BIN MÜDE'''

import torch
from heapq import heappush, heappop
import numpy as np


# 🧠 Hilfsfunktion: CNN-Heuristik für ein Feld aus der Heatmap berechnen
def cnn_heuristic(model, img_tensor, pos):
    with torch.no_grad():
        heatmap = model(img_tensor.unsqueeze(0))  # (1, H, W)
    h_val = heatmap.item()
    return h_val


# 🧩 A*-Algorithmus mit CNN-Heuristik
def doAStarAlgoCNN(start, end, model, img_tensor):
    height, width = img_tensor.shape[-2], img_tensor.shape[-1]
    open_set = []
    heappush(open_set, (0, start))

    came_from = {}
    laufAufwand = {start: 0}

    while open_set:
        _, current = heappop(open_set)

        if current == end:
            return reconstruct_path(came_from, current)

        x, y = current
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        # Nachbarn filtern – nur wenn Pixel hell ist (also kein Mauerblock)
        # nur helle Pixel (also keine Mauer) zulassen
        neighbors = [
            n for n in neighbors
            if 0 <= n[0] < width
               and 0 <= n[1] < height
               and img_tensor[0, n[1], n[0]] > 0.5  # 0 = schwarz (Mauer), 1 = weiß (Weg)
        ]

        for neighbor in neighbors:
            neuerLaufaufwand = laufAufwand.get(current, float('inf')) + 1

            if neuerLaufaufwand < laufAufwand.get(neighbor, float('inf')):
                laufAufwand[neighbor] = neuerLaufaufwand
                came_from[neighbor] = current

                # 💡 CNN-Heuristik berechnen
                h = cnn_heuristic(model, img_tensor, neighbor)
                f_score = neuerLaufaufwand + h
                heappush(open_set, (f_score, neighbor))

    return None


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]