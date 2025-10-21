from PIL import Image
from heapq import heappush, heappop

def distributeHeuristic(img, start, end, bildBreite, feldSeitenlänge, mauerBlöcke, breitenBlöcke, höhenBlöcke, weißeBlöcke):
    heuristic = {}
    for w in weißeBlöcke:
        heuristic[w] = abs(end[0] - w[0]) + abs(end[1] - w[1])
    return heuristic



def doAStarAlgo(start, end, weißeBlöcke, heuristic):
    open_set = []
    heappush(open_set, (0, start))  # (f(n), node)

    came_from = {}
    laufAufwand = {w: float('inf') for w in weißeBlöcke}
    laufAufwand[start] = 0

    while open_set:
        _, current = heappop(open_set)

        if current == end:
            return reconstruct_path(came_from, current)


        x, y = current
        neighbors = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
        neighbors = [n for n in neighbors if n in weißeBlöcke]

        for neighbor in neighbors:
            neuerLaufaufwandZuNachbarn = laufAufwand[current] + 1
            if neuerLaufaufwandZuNachbarn < laufAufwand[neighbor]: #neue günstigere Pfade aktualieseren
                came_from[neighbor] = current
                laufAufwand[neighbor] = neuerLaufaufwandZuNachbarn
                f_score = neuerLaufaufwandZuNachbarn + heuristic[neighbor]
                heappush(open_set, (f_score, neighbor))

    return None  #kein Pfad


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]  # Pfad umdrehen





