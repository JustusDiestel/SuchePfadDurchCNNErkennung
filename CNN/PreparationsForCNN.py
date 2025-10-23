import numpy as np
'''Brauch ich eigentlich garnicht '''
def maze_to_grid(img, feldgröße=20):
    width, height = img.size
    blöcke_x = width // feldgröße
    blöcke_y = height // feldgröße

    grid = np.zeros((blöcke_y, blöcke_x), dtype=np.float32)
    print(grid)

    for y in range(blöcke_y):
        for x in range(blöcke_x):
            # Mittelpunkt jedes Blocks bestimmen
            px = x * feldgröße + feldgröße // 2
            py = y * feldgröße + feldgröße // 2
            r, g, b = img.getpixel((px, py))

            if (r, g, b) == (0, 0, 0):
                grid[y, x] = 0.0  # Wand
            elif (r, g, b) == (0, 255, 0):
                grid[y, x] = 2.0  # Start
            elif (r, g, b) == (255, 0, 0):
                grid[y, x] = 3.0  # Ziel
            else:
                grid[y, x] = 1.0  # frei
    return grid


