import pygame
import random
from pygamegame import PygameGame
from map import Map

class Enemy(object):
    wasMapCreated = False

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.isAlive = True
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.halt = False
        self.size = size
        self.speed = 8
        self.direction = random.choice([ [1, 0], [0, 1] ])
        self.enemyType = "Ground"
        self.type = None
        self.value = 25
        self.damage = 50
        #self.path = "assets/" + self.type + ".png"
        #self.image = pygame.image.load(self.path).convert_alpha()
        #self.image = pygame.transform.scale(self.image, (50, 100))

        self.nextPoint = True
        self.currPoint = 0

        self.currX = None
        self.currY = None
        self.destX = 0
        self.destY = 0

        self.startingHealth = 200

        self.color = (0, 255, 0)

        self.currentHealth = self.startingHealth

    def updateDir(self):
        pass

    def rotate(self):
        pass

    def goTo(self, currX, currY, destX, destY):

        self.xDiff = destX - currX
        self.yDiff = destY - currY

        if self.yDiff == 0: # moving on x axis
            if self.x >= destX:
                self.halt = False
                self.moveLeft = True
                self.nextPoint = False

            if self.x < destX:
                self.halt = False
                self.moveRight = True
                self.nextPoint = False

        elif self.xDiff == 0: # moving on y axis
            if self.yDiff > 0: # y moving down on the screen
                if self.y <= destY:
                    self.halt = False
                    self.moveDown = True
                    self.nextPoint = False


            elif self.yDiff < 0: # y is moving up on the screen
                if self.y >= destY:
                    self.halt = False
                    self.moveUp = True
                    self.nextPoint = False


    def enemyPathing(self):
        if Enemy.wasMapCreated:
            self.centerCellList = Map.centerCellList
            self.yValue = Map.startNode
        self.centerCellList = __import__("map").Map.centerCellList
        self.yValue = __import__("map").Map.yValue

        if self.currX == self.currY == None:
            self.currX, self.currY = 1050, self.yValue * 100 + 50
        if self.nextPoint:
            print(self.centerCellList)
            point = self.centerCellList[self.currPoint]
            print("a" + str(self.currPoint))

            self.destX = point[0]
            self.destY = point[1]

            self.goTo(self.currX, self.currY, self.destX, self.destY)
            self.currX, self.currY = self.destX, self.destY






    def move(self):
        if self.moveLeft:
            self.x -= self.speed
        if self.moveRight:
            self.x += self.speed
        if self.moveDown:
            self.y += self.speed
        if self.moveUp:
            self.y -= self.speed
        if self.halt:
            self.x += 0
            self.y += 0

    def check(self):


        if self.xDiff < 0: # move Left

            if self.x < self.destX:
                self.moveLeft = False
                self.halt = True
                self.currPoint += 1
                self.nextPoint = True
        if self.xDiff > 0:
            if self.x > self.destX:
                self.moveRight = False
                self.halt = True
                self.currPoint += 1
                self.nextPoint = True

        if self.yDiff > 0:  # y moving down on the screen
            if self.y > self.destY:
                self.moveDown = False
                self.halt = True
                self.currPoint += 1
                self.nextPoint = True

        if self.yDiff < 0:
            if self.y < self.destY:
                self.moveUp = False
                self.halt = True
                self.currPoint += 1
                self.nextPoint = True

    def isOffScreen(self):
        if self.x < 0 or self.x > 1200 or self.y < 0 or self.y > 800:
            return True

    def draw(self, screen):
        draw_rect = self.rect.move(self.x - 25, self.y - 25)
        screen.blit(self.image, draw_rect)

    def drawHealth(self, screen):
        healthBarWidth = self.startingHealth // 4
        displayHealth = int((self.currentHealth / self.startingHealth) * healthBarWidth)

        if self.currentHealth <= 0:
            self.currentHealth = 0
        if self.currentHealth <= self.startingHealth // 2:
            self.color = (255, 170, 12)
        if self.currentHealth <= self.startingHealth // 3:
            self.color = (255, 0, 0)

        pygame.draw.rect(screen, (0, 0, 0), (self.x - healthBarWidth // 2, self.y - 24, healthBarWidth, 5))
        pygame.draw.rect(screen, self.color, (self.x - healthBarWidth // 2, self.y - 23, displayHealth, 2.5))

class Tank(Enemy):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.speed = 2
        self.startingHealth = 450
        self.enemyType = "Ground"
        self.gameImg = pygame.image.load("assets/tank.png").convert_alpha()
        self.gameImg = pygame.transform.scale(self.gameImg, (25, 50))
        self.ogImg = self.gameImg
        self.image = self.ogImg
        self.rect = self.image.get_rect()
        self.value = 200

        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.halt = False
        self.nextPoint = True
        self.currPoint = 0

        self.angle = 0

        self.color = (0, 255, 0)

        self.currentHealth = self.startingHealth

        self.currX = None
        self.currY = None
        self.destX = 0
        self.destY = 0



    def rotate(self):
        self.image = pygame.transform.rotate(self.image, self.angle)


    def updateDir(self):
        if self.moveLeft:
            self.angle = 90
            self.image = pygame.transform.rotate(self.ogImg, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        elif self.moveUp:
            self.angle = 0
            self.image = pygame.transform.rotate(self.ogImg, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        elif self.moveDown:
            self.angle = 180
            self.image = pygame.transform.rotate(self.ogImg, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)



class Fast(Enemy):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.isAlive = True
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.halt = False
        self.size = size
        self.speed = 15
        self.direction = random.choice([[1, 0], [0, 1]])
        self.enemyType = "Ground"
        self.type = None
        self.value = 50
        self.damage = 5


        self.nextPoint = True
        self.currPoint = 0

        self.currX = None
        self.currY = None
        self.destX = 0
        self.destY = 0

        self.startingHealth = 200

        self.color = (0, 255, 0)

        self.currentHealth = self.startingHealth

        self.gameImg = pygame.image.load("assets/bombfast.png").convert_alpha()
        self.gameImg = pygame.transform.scale(self.gameImg, (50, 50))
        self.ogImg = self.gameImg
        self.image = self.ogImg
        self.rect = self.image.get_rect()


class Slow(Enemy):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.isAlive = True
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.halt = False
        self.size = size
        self.speed = 3
        self.direction = random.choice([[1, 0], [0, 1]])
        self.enemyType = "Ground"
        self.type = None
        self.value = 5
        self.damage = 50


        self.nextPoint = True
        self.currPoint = 0

        self.currX = None
        self.currY = None
        self.destX = 0
        self.destY = 0

        self.startingHealth = 200

        self.color = (0, 255, 0)

        self.currentHealth = self.startingHealth

        self.gameImg = pygame.image.load("assets/bombslow.png").convert_alpha()
        self.gameImg = pygame.transform.scale(self.gameImg, (50, 50))
        self.ogImg = self.gameImg
        self.image = self.ogImg
        self.rect = self.image.get_rect()


class Normal(Enemy):
    def __init__(self, x, y, size):
        super().__init__(self, x, y)
        self.x = x
        self.y = y
        self.isAlive = True
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.halt = False
        self.size = size
        self.speed = 6
        self.direction = random.choice([[1, 0], [0, 1]])
        self.enemyType = "Ground"
        self.type = None
        self.value = 25
        self.damage = 10

        self.nextPoint = True
        self.currPoint = 0

        self.currX = None
        self.currY = None
        self.destX = 0
        self.destY = 0

        self.startingHealth = 200

        self.color = (0, 255, 0)

        self.currentHealth = self.startingHealth

        self.gameImg = pygame.image.load("assets/bomb.png").convert_alpha()
        self.gameImg = pygame.transform.scale(self.gameImg, (50, 50))
        self.ogImg = self.gameImg
        self.image = self.ogImg
        self.rect = self.image.get_rect()


class Air(Enemy):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self.speed = 5
        self.enemyType = "Air"
        self.damage = 25
        self.value = 150

        self.startingHealth = 200

        self.gameImg = pygame.image.load("assets/air.png").convert_alpha()
        self.gameImg = pygame.transform.scale(self.gameImg, (64, 64))
        self.ogImg = self.gameImg
        self.image = self.ogImg
        self.rect = self.image.get_rect()

        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.halt = False
        self.nextPoint = True
        self.currPoint = 0

        self.angle = 0

        self.color = (0, 255, 0)

        self.currentHealth = self.startingHealth

        self.currX = None
        self.currY = None
        self.destX = 0
        self.destY = 0

    def draw(self, screen):
        draw_rect = self.rect.move(self.x, self.y)
        screen.blit(self.image, draw_rect)

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, self.angle)


    def updateDir(self):
        if self.moveLeft:
            self.angle = 90
            self.image = pygame.transform.rotate(self.ogImg, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        elif self.moveUp:
            self.angle = 0
            self.image = pygame.transform.rotate(self.ogImg, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        elif self.moveDown:
            self.angle = 180
            self.image = pygame.transform.rotate(self.ogImg, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)


