import pygame
import math
import random
from pygamegame import PygameGame
from map import Map

# This file contains the classes for the player and the fortress in the game

class Player(object):
    def __init__(self):
        self.money = 150

    def drawMoney(self, screen):
        moneyText = pygame_font.Font(None, 20)
        moneyText.render("Money: " + str(self.money), (255, 255, 255), (0, 0, 0))





class Fortress(object):
    def __init__(self, health):
        self.startingHealth = health
        self.currentHealth = health
        self.isGameOver = False

        self.width = 1200
        self.height = 800

        self.color = (0, 255, 0)

        self.levelEditorMode = False
        self.endNode = (-1, -1)

        self.gameImg = pygame.image.load("assets/fortress.png").convert_alpha()
        self.gameImg = pygame.transform.scale(self.gameImg, (100, 100))
        self.gameImg = pygame.transform.rotate(self.gameImg, 90)


    def health(self):
        return self.health

    def drawHealth(self, screen):
        healthBarWidth = 90 + self.startingHealth
        displayHealth = int((self.currentHealth / self.startingHealth) * healthBarWidth)

        if self.currentHealth <= 200:
            self.color = (255, 170, 12)
        if self.currentHealth <= 100:
            self.color = (255, 0, 0)

        pygame.draw.rect(screen, (0, 0, 0), (25, self.height - 100, 100 + self.startingHealth, 25))
        pygame.draw.rect(screen, self.color, (30, self.height - 95, displayHealth, 15))



    def draw(self, screen, levelEditorFinalNode = None):
        if self.levelEditorMode:
            x, y = self.endNode
        else:
            finalNode = __import__("map").Map.coords[-1]
            x, y = finalNode

        screen.blit(self.gameImg, (x * 100, y * 100))



