import MazeCreator

if __name__ == "__main__":
    mc = MazeCreator.createRandomMaze()
    mc = MazeCreator.createStartAndEnd(mc)
    mc.show()
