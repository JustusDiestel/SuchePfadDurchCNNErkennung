from sympy.integrals.heurisch import heurisch
from PIL import Image, ImageDraw
import MazeCreator
import AStarAlgo

bildBreite = 28*20
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