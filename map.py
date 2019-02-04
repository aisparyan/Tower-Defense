import pygame
import math
import random
from pygamegame import PygameGame
import sys
import copy
import ast

# This file contains the classes for the Maps in game
# Contains algorithm that generates paths for campaign mode
# generates water near paths to make progressive rounds much harder to play
# Level Editor
# Finds the path that the user has created
# Allows the user to input a seed to play maps that their friends had given them
class Map(object):

    yValue = random.choice([n for n in range(7)])
    coords = []
    centerCellList = []

    def __init__(self, seed = None, grid = []):

        if grid == []:
            self.grid = [[0] * 10 for n in range(8)]
        else:
            self.grid = grid

        self.width = 100

        self.moves = ["moveLeft", "moveDown", "moveUp"]

        self.grassIMG = pygame.image.load("assets/grass.jpg")
        self.grassIMG = pygame.transform.scale(self.grassIMG, (100, 100))

        self.sandIMG = pygame.image.load("assets/sand.jpg")
        self.sandIMG = pygame.transform.scale(self.sandIMG, (100, 100))

        self.waterIMG = pygame.image.load("assets/water.jpg")
        self.waterIMG = pygame.transform.scale(self.waterIMG, (100, 100))


        self.startingX = (9 * 100) + 50
        self.startingY = (self.yValue * 100) + 50

        self.waterDifficulty = 100

        self.seed = seed

        self.userCreatedPath = []
        self.loadedLevelName = None

        # For level editor
        self.blockType = None
        self.water = set()

        self.generated = False


    def generatePath(self):
        # https://stackoverflow.com/questions/5012560/how-to-query-seed-used-by-random-random
        # used this thread to improve my seed generation, otherwise error with generation
        if self.seed == None:
            seed = random.randrange(sys.maxsize)
            rng = random.Random(seed)
            rng.seed(seed)
            self.seed = seed
        else:
            random.seed(self.seed)


        width = 100
        cellCenter = 50
        # Pick start node
        Map.yValue = random.choice([n for n in range(7)])

        self.grid[Map.yValue][9] = 1
        currX, currY = 9, Map.yValue
        print(9, Map.yValue)

        # Move
        complete = False
        prevMove = None

        Map.coords.append((currX, currY))

        while not complete:

            if prevMove == None:
                currMove = "moveLeft"
            elif prevMove == "moveDown":
                currMove = random.choice(["moveLeft", "moveDown"])
            elif prevMove == "moveUp":
                currMove = random.choice(["moveLeft", "moveUp"])
            else:
                currMove = random.choice(self.moves)



            if currMove == "moveLeft":
                try:
                    if currX - 1 < 0:
                        currMove = random.choice(["moveDown", "moveUp"])
                    else:
                        self.grid[currY][currX - 1] = 1
                        currX, currY = currX - 1, currY
                        prevMove = currMove
                        Map.coords.append((currX, currY))


                except:
                    pass

            elif currMove == "moveDown":
                try:
                    self.grid[currY + 1][currX] = 1
                    currX, currY = currX, currY + 1
                    prevMove = currMove
                    Map.coords.append((currX, currY))


                except:
                    pass

            elif currMove == "moveUp":
                try:
                    if currY - 1 < 0:
                        currMove = "moveLeft"
                    else:
                        self.grid[currY - 1][currX] = 1
                        currX, currY = currX, currY - 1
                        prevMove = currMove
                        Map.coords.append((currX, currY))


                except:
                    pass

            for y in range(7):
                if self.grid[y][0] == 1:
                    complete = True


        print(Map.coords)

        for coord in Map.coords:
            Map.centerCellList.append(((coord[0] * width) + cellCenter, (coord[1] * width) + cellCenter))

        print(Map.centerCellList)


    def generateWater(self):
        if self.seed == None:
            seed = random.randrange(sys.maxsize)
            rng = random.Random(seed)
            rng.seed(seed)
            self.seed = seed
        else:
            random.seed(self.seed)
        if self.waterDifficulty < 15:
            self.waterDifficulty = 3
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == 1:

                    for move in [[0,1],[1,0],[-1,0],[0,-1]]:
                        try:
                            moveX = move[0]
                            moveY = move[1]
                            newX = moveX + row
                            newY = moveY + col
                            if self.grid[newX][newY] == 0:
                                rand = random.randint(1, self.waterDifficulty)
                                if rand == 1:
                                    self.grid[newX][newY] = 2
                        except:
                            pass


    def checkIfTileIsValid(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                try:
                    if self.grid[mouse_x // 100][mouse_y // 100] == 2 and PygameGame.drag == True:
                        return False
                except:
                    pass
        return True

    def isMapLegal(self):
        haveVisited = set()
        toVisit = []
        path = copy.deepcopy(self.userCreatedPath)
        currX, currY = None, None

        endX = path[-1][0]
        endY = path[-1][1]
        if (endX, endY) not in [(0, n) for n in range(8)]:
            return False

        startX = path[0][0]
        startY = path[0][1]
        if (startX, startY) not in [(9, n) for n in range(10)]:
            return False

        while len(path) != 0:
            if currX == currY == None:
                (currX, currY) = path.pop()
            (nextX, nextY) = path.pop()
            neighbors = set()
            for neighbor in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                x = neighbor[0]
                y = neighbor[1]
                neighborX = currX + x
                neighborY = currY + y
                neighbors.add((neighborX, neighborY))
            print(nextX, nextY)
            print(neighbors)
            if (nextX, nextY) in neighbors:
                currX, currY = nextX, nextY
            else:
                return False
        return True



    def draw(self, screen):


        x, y = 0, 0

        for row in self.grid:

            for col in row:
                if col == 1 or col == 3 or col == 4:
                    img = self.sandIMG
                elif col == 2:
                    img = self.waterIMG
                else:
                    img = self.grassIMG
                screen.blit(img, (x, y))
                x += self.width
            x = 0
            y += self.width

    def startNode(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == 3:
                    return col, row

        return -1, -1

    def waterTiles(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == 2 or self.grid[row][col] == 1:
                    self.water.add((col, row))
        return self.water

    def endNode(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == 4:
                    return col, row

        return -1, -1

    def drawLevelEditor(self, screen):

        x, y = 0, 0

        for row in self.grid:
            for col in row:
                if col == 1:
                    screen.blit(self.sandIMG, (x, y))
                elif col == 2:
                    screen.blit(self.waterIMG, (x, y))
                elif col == 0:
                    screen.blit(self.grassIMG, (x, y))
                elif col == 3:
                    pygame.draw.rect(screen, (0, 0, 255), (x, y, self.width, self.width))
                elif col == 4:
                    pygame.draw.rect(screen, (255, 0, 0), (x, y, self.width, self.width))


                x += self.width
            x = 0
            y += self.width

        x, y = 0, 0

        for row in self.grid:
            for col in row:
                pygame.draw.rect(screen, (0, 0, 0), (x, y, self.width, self.width), 1)
                x += self.width
            x = 0
            y += self.width


    def readFile(self, path):
        with open(path, "rt") as f:
            return f.read()

    def writeFile(self, path, contents):
        with open(path, "wt") as f:
            f.write(contents)

    def saveLevel(self, nameofLevel):
        saveLevel = str([self.grid, self.userCreatedPath])

        self.writeFile("Levels/" + str(nameofLevel), saveLevel)

    def loadLevel(self, nameofLevel):
        return self.readFile("Levels/" + str(nameofLevel))

