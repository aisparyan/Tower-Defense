'''
Using framework from Lukas Peraza
https://github.com/LBPeraza/Pygame-Asteroids/blob/master/game.py
'''

# Main game file that you run the game from
# This file also draws ALL User Interface in the game
import pygame
import pygame_textinput
import math
import time
import random
import sys
import ast
import os

from pygamegame import PygameGame
from enemies import Enemy, Air, Tank, Fast, Slow, Normal
from button import Button
from characters import Character, baseSoldier, Bullet, Sniper, Heavy
from player import Fortress, Player
from map import Map


class Game(PygameGame):
    def init(self):
        self.enemies = []
        self.enemyQueue = []
        self.enemiesKilled = 0
        self.enemiesSpawned = 0
        self.characters = []

        self.soldier = baseSoldier(self.width - self.width // 6 + 25, 25, "soldier1")
        self.sniper = Sniper(self.width - self.width // 6 + 25, 125, "sniper")
        self.heavy = Heavy(self.width - self.width // 6 + 25, 225, "heavy")

        self.width = 1200
        self.height = 800

        self.woodImg = pygame.image.load("assets/wood.jpg")

        self.gameOver = False
        self.roundOver = False
        self.wave = 0
        self.time = 0
        self.drag = False
        self.upgradeMenu = False
        self.currChar = None
        self.currRad = None

        self.idleCount = 0
        self.offsetX = 0
        self.offsetY = 0

        self.score = 0
        self.bullets = []
        self.wonGame = False

        self.backButton = Button((234, 124, 112), 25, self.height - 150, 200, 50, "Back")

        self.mode = "startScreenMode"

        self.seed = None

        self.levelEdit = Map()

        self.FreePlayMap = Map()

        self.LoadedLevelMap = Map()

        self.map = Map()

        self.isPaused = False



        self.characterTypes = []
        self.fortress = Fortress(300)
        self.player = Player()
        self.debugOn = False

        self.userInput = None

        self.editor = Button((255, 255, 255), self.width // 2 - 150, self.height // 2 - 200, 300, 100, "Level Editor")
        self.LoadLevel = Button((255, 255, 255), self.width // 2 - 150, self.height // 2, 300, 100, "Load Levels")
        self.Generate = Button((255, 255, 255), self.width // 2 - 150, self.height // 2 + 200, 300, 100, "Generate")

        self.saveSlot2 = "---Empty---"
        self.saveSlot3 = "---Empty---"
        self.saveSlot4 = "---Empty---"
        self.saveSlot5 = "---Empty---"

        if os.path.exists("Levels/Level1.txt"):
            self.saveSlot1 = "Level 1"
        else:
            self.saveSlot1 = "Empty"
        if os.path.exists("Levels/Level2.txt"):
            self.saveSlot2 = "Level 2"
        else:
            self.saveSlot2 = "Empty"
        if os.path.exists("Levels/Level3.txt"):
            self.saveSlot3 = "Level 3"
        else:
            self.saveSlot3 = "Empty"
        if os.path.exists("Levels/Level4.txt"):
            self.saveSlot4 = "Level 4"
        else:
            self.saveSlot4 = "Empty"
        if os.path.exists("Levels/Level5.txt"):
            self.saveSlot5 = "Level 5"
        else:
            self.saveSlot5 = "Empty"

        self.darkBG = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.darkBG, (0, 0, 0, 150), (0, 0, self.width, self.height))
        self.roundRecap = Button(((29, 209, 161)), self.width//2 - 500, self.height//2 - 300, 1000, 600)


        self.inputText = ""


    def keyPressed(self, code, mod):

        grass = 0
        path = 1
        water = 2
        beginningNode = 3
        endingNode = 4

        if code == pygame.K_r:
            self.mode = "startScreenMode"



        if self.mode == "startScreenMode":
            if code == pygame.K_s:
                self.map.generatePath()
                self.map.generateWater()
                self.mode = "gameMode"


        if self.mode == "gameMode" or self.mode == "startScreenMode/FreeMode/FreePlay":
            if code == pygame.K_n:
                self.roundOver = True
                self.enemies = []

            if code == pygame.K_d:
                self.debugOn = not self.debugOn

            if code == pygame.K_ESCAPE:
                self.isPaused = not self.isPaused

        if self.mode == "startScreenMode/FreeMode/LevelEditor":
            if code == pygame.K_c:
                print('cleared!')
                self.levelEdit.userCreatedPath = []
                self.levelEdit.grid = [[0] * 10 for n in range(8)]
            if code == pygame.K_q:
                print(self.levelEdit.isMapLegal())
            try:
                if code == pygame.K_s:
                    if self.levelEdit.isMapLegal():
                        self.mode = "startScreenMode/FreeMode/SaveLevels"
                        print("legal")
                    else:
                        print("not legal")
            except:
                pass

            if code == pygame.K_b:
                self.levelEdit.blockType = beginningNode
                self.fortress.levelEditorMode = False

            if code == pygame.K_e:
                self.fortress.levelEditorMode = True
                self.levelEdit.blockType = endingNode
                print(self.fortress.endNode)

            if code == pygame.K_1:
                self.fortress.levelEditorMode = False

                self.levelEdit.blockType = path
            if code == pygame.K_2:
                self.fortress.levelEditorMode = False

                self.levelEdit.blockType = water
            if code == pygame.K_3:
                self.fortress.levelEditorMode = False

                self.levelEdit.blockType = grass

            if code == pygame.K_l:
                if self.levelEdit.isMapLegal():
                    grid = ast.literal_eval(self.FreePlayMap.loadLevel("Level1.txt"))
                    self.FreePlayMap = Map(None, grid)
                    self.FreePlayMap.userCreatedPath = self.levelEdit.userCreatedPath
                    print(self.FreePlayMap.grid)
                    self.fortress.levelEditorMode = True
                    self.mode = "startScreenMode/FreeMode/FreePlay"

        if self.mode == "startScreenMode/FreeMode/GenerateSeeds":
            # https://gamedev.stackexchange.com/questions/138938/how-to-only-allow-letters-to-be-pressed-on-in-pygame
            press = pygame.key.get_pressed()
            for i in range(pygame.K_1, pygame.K_9 + 1):
                if press[i] == True:
                    name = pygame.key.name(i)
                    self.inputText += str(name)
                    self.seed = self.inputText


            if code == pygame.K_RETURN:
                self.FreePlayMap.seed = self.seed
                self.FreePlayMap.generatePath()
                self.FreePlayMap.generateWater()
                Map.centerCellList = self.FreePlayMap.centerCellList
                self.FreePlayMap.generated = True
                self.mode = "startScreenMode/FreeMode/FreePlay" # prob create a new mode and draw it again,
            if code == pygame.K_BACKSPACE:
                self.inputText = self.inputText[:-1]

    def mousePressed(self, x, y):
        pos = pygame.mouse.get_pos()


        if self.backButton.isOver(pos):
            self.mode ="startScreenMode"

        if self.mode == "startScreenMode/FreeMode":
            if self.editor.isOver(pos):
                self.mode = "startScreenMode/FreeMode/LevelEditor"
            if self.LoadLevel.isOver(pos):
                self.mode = "startScreenMode/FreeMode/LoadLevels"
            if self.Generate.isOver(pos):
                self.mode = "startScreenMode/FreeMode/GenerateSeeds"

        '''
        if self.mode == "startScreenMode/FreeMode":
            if x > 0 and x < 500 and y > 0 and y < 500:
                print("YYET")
                self.seed = self.userInput
                self.levelEdit.generatePath()
                self.mode = "startScreenMode/FreeMode/FreePlay"
        '''
        print(x // 100, y // 100)
        '''
        if self.map.grid[y // self.map.width][x // self.map.width] == 1:
            self.map.grid[y // self.map.width][x // self.map.width] = 0
        elif self.map.grid[y // self.map.width][x // self.map.width] == 0:
            self.map.grid[y // self.map.width][x // self.map.width] = 1
        '''

        if self.mode == "startScreenMode/FreeMode/LevelEditor":

            if self.levelEdit.blockType != None:
                self.levelEdit.grid[y//100][x//100] = self.levelEdit.blockType
                if self.levelEdit.blockType == 1:
                    if (x//100, y//100) not in self.levelEdit.userCreatedPath:
                        self.levelEdit.userCreatedPath.append((x//100, y//100))

                if self.fortress.levelEditorMode:
                    self.fortress.endNode = self.levelEdit.endNode()
                    self.fortress.levelEditorMode = False

        if self.mode == "startScreenMode/FreeMode/SaveLevels":

            if self.save1.isOver(pos):
                self.levelEdit.saveLevel("Level1.txt")
                self.saveSlot1 = "Level1"
                self.mode = "startScreenMode"

            if self.save2.isOver(pos):
                self.levelEdit.saveLevel("Level2.txt")
                self.mode = "startScreenMode"
                self.saveSlot2 = "Level2"

            if self.save3.isOver(pos):
                self.levelEdit.saveLevel("Level3.txt")
                self.mode = "startScreenMode"
                self.saveSlot3 = "Level3"

            if self.save4.isOver(pos):
                self.levelEdit.saveLevel("Level4.txt")
                self.mode = "startScreenMode"
                self.saveSlot4 = "Level4"

            if self.save5.isOver(pos):
                self.levelEdit.saveLevel("Level5.txt")
                self.mode = "startScreenMode"
                self.saveSlot5 = "Level5"





        if self.mode == "gameMode" or self.mode == "startScreenMode/FreeMode/FreePlay":
            if self.wonGame:
                if self.menuScreen.isOver(pos):
                    pygame.quit()
            # Check if clicked in bounds of character in sidebar
            if x > self.width - self.width // 6 + 25 and \
                x < self.width - self.width // 6 + 175 and \
                y > 25 and y < 100 and self.player.money >= 150:
                print('clicked!')
                self.player.money -= 150

                # Create instance of character
                self.currChar = baseSoldier(self.width - self.width // 6 + 25, 25, 'soldier1')
                self.characters.append(self.currChar)

                # Allow drag character
                self.drag = True
                self.currChar.selected = True
                self.offsetX = self.currChar.x - x
                self.offsetY = self.currChar.y - y

            # SNIPER
            if x > self.width - self.width // 6 + 25 and \
                x < self.width - self.width // 6 + 175 and \
                y > 130 and y < 180 and self.player.money >= 550:
                print('clicked!')
                self.player.money -= 550

                # Create instance of character
                self.currChar = Sniper(self.width - self.width // 6 + 25, 25, 'sniper')
                self.characters.append(self.currChar)

                # Allow drag character
                self.drag = True
                self.currChar.selected = True
                self.offsetX = self.currChar.x - x
                self.offsetY = self.currChar.y - 200 + y

            # HEAVY
            if x > self.width - self.width // 6 + 25 and \
                x < self.width - self.width // 6 + 175 and \
                y > 230 and y < 280 and self.player.money >= 300:
                print('clicked!')
                self.player.money -= 300

                # Create instance of character
                self.currChar = Heavy(self.width - self.width // 6 + 25, 25, 'heavy')
                self.characters.append(self.currChar)

                # Allow drag character
                self.drag = True
                self.currChar.selected = True
                self.offsetX = self.currChar.x - x
                self.offsetY = self.currChar.y + 200 - y
            if self.RepairTower.isOver(pos):
                if self.fortress.currentHealth == 100:
                    pass
                else:
                    current = self.fortress.currentHealth
                    self.fortress.currentHealth += 100
                    if self.fortress.currentHealth > 100:
                        self.fortress.currentHealth = current
                    else:
                        self.player.money -= 1000
            '''
            # DEBUG WEIRD UPGRADE MENUS and fix selection on sidebar character aka self.soldier
            for character in self.characters:
                if x < character.x + 64 and y < character.y + 54 and x > character.x and y > character.y \
                        or x > self.width - self.width //6 and y > 0 and x < 1200 and y < 400:
                    character.selected = True
                else:
                    character.selected = False
                if character.upgrade1Clicked(x, y):
                    print('upgrade CLicked!')
            '''

    def mouseReleased(self, x, y):
        pos = pygame.mouse.get_pos()

        if self.mode == "gameMode":

            if self.roundOver == True and len(self.enemies) == 0:
                if self.nextRound.isOver(pos):
                    self.wave += 1
                    if self.map.waterDifficulty < 5:
                        pass
                    else:
                        self.map.waterDifficulty = int(self.map.waterDifficulty / 2)
                    self.map.generateWater()
                    self.roundOver = False

        if self.mode == "startScreenMode":
            if self.Campaign.isOver(pos):
                self.map.generatePath()
                self.map.generateWater()
                self.mode = "gameMode"
            if self.FreeMode.isOver(pos):
                self.mode = "startScreenMode/FreeMode"

        posX, posY = x // 100, y // 100
        if self.mode == "gameMode" or self.mode == "startScreenMode/FreeMode/FreePlay":
            # Release character
            self.drag = False
            # Fixes NoneType error
            if self.currChar == None:
                pass
            else:
                self.currChar.selected = False
            # Reset for next selection
            self.currChar = None
            self.offsetX = 0
            self.offsetY = 0

        if self.isPaused:
            if self.resumeButton.isOver(pos):
                self.isPaused = not self.isPaused
            if self.menuScreen.isOver(pos):
                pygame.quit()
            if self.quit.isOver(pos):
                pygame.quit()

        if self.mode == "startScreenMode/FreeMode/LoadLevels":
            if self.save1.isOver(pos):
                if self.saveSlot1 == "Empty": pass
                else:
                    grid = ast.literal_eval(self.FreePlayMap.loadLevel("Level1.txt"))[0]
                    path = ast.literal_eval(self.FreePlayMap.loadLevel("Level1.txt"))[1]
                    self.FreePlayMap.grid = grid
                    self.FreePlayMap.userCreatedPath = path
                    self.fortress.levelEditorMode = True
                    self.mode = "startScreenMode/FreeMode/FreePlay"

            if self.save2.isOver(pos):
                if self.saveSlot2 == "Empty": pass
                else:
                    grid = ast.literal_eval(self.FreePlayMap.loadLevel("Level2.txt"))[0]
                    path = ast.literal_eval(self.FreePlayMap.loadLevel("Level2.txt"))[1]
                    self.FreePlayMap.grid = grid
                    self.FreePlayMap.userCreatedPath = path
                    self.fortress.levelEditorMode = True
                    self.mode = "startScreenMode/FreeMode/FreePlay"

            if self.save3.isOver(pos):
                if self.saveSlot3 == "Empty": pass
                else:
                    grid = ast.literal_eval(self.FreePlayMap.loadLevel("Level3.txt"))[0]
                    path = ast.literal_eval(self.FreePlayMap.loadLevel("Level3.txt"))[1]
                    self.FreePlayMap.grid = grid
                    self.FreePlayMap.userCreatedPath = path
                    self.fortress.levelEditorMode = True
                    self.mode = "startScreenMode/FreeMode/FreePlay"

            if self.save4.isOver(pos):
                if self.saveSlot4 == "Empty": pass
                else:
                    grid = ast.literal_eval(self.FreePlayMap.loadLevel("Level4.txt"))[0]
                    path = ast.literal_eval(self.FreePlayMap.loadLevel("Level4.txt"))[1]
                    self.FreePlayMap.grid = grid
                    self.FreePlayMap.userCreatedPath = path
                    self.fortress.levelEditorMode = True
                    self.mode = "startScreenMode/FreeMode/FreePlay"

            if self.save5.isOver(pos):
                if self.saveSlot5 == "Empty": pass
                else:
                    grid = ast.literal_eval(self.FreePlayMap.loadLevel("Level5.txt"))[0]
                    path = ast.literal_eval(self.FreePlayMap.loadLevel("Level5.txt"))[1]
                    self.FreePlayMap.grid = grid
                    self.FreePlayMap.userCreatedPath = path
                    self.fortress.levelEditorMode = True
                    self.mode = "startScreenMode/FreeMode/FreePlay"

    def mouseDrag(self, x, y):
        if self.mode == "gameMode" or self.mode == "startScreenMode/FreeMode/FreePlay":
            posX, posY = x // 100, y // 100
            # Allow character to move if dragged
            if self.drag == True:
                # Adjust location of image by offset
                self.currChar.x = x + self.offsetX
                self.currChar.y = y + self.offsetY
                self.currChar.cx = x + self.offsetX //4 +12
                self.currChar.cy = y + self.offsetY //4 - 2
            if self.currChar == None:
                pass
            else:
                if self.mode == "gameMode":

                    if (posX, posY) in self.map.waterTiles():

                        self.currChar.inWater = True
                    else:
                        self.currChar.inWater = False
                else:
                    if (posX, posY) in self.FreePlayMap.waterTiles():
                        self.currChar.inWater = True
                    else:
                        self.currChar.inWater = False

    def mouseMotion(self, x, y):
        pos = pygame.mouse.get_pos()
        if self.backButton.isOver(pos):
            self.backButton.color = (204, 94, 82)
        else:
            self.backButton.color = (234, 124, 112)


    def checkCharacterTypes(self):
        for character in self.characters:
            self.characterTypes.append(character.type)


    def timerFired(self, dt):
        print(self.isPaused)
        self.time += 1

        if self.isPaused:
            pass
        elif self.wonGame:
            pass
        else:
            '''
            if self.mode == "startScreenMode/FreeMode":
                events = pygame.event.get()
                textinput.update(events)
                if textinput.update(events):
                    self.userInput = textinput.get_text()
            '''
            if self.mode == "gameMode" or self.mode == "startScreenMode/FreeMode/FreePlay":

                if self.mode == "gameMode":
                    yValue = __import__("map").Map.yValue
                else:
                    self.fortress.endNode = self.FreePlayMap.endNode()
                    if self.FreePlayMap.generated:
                        yValue = __import__("map").Map.yValue
                    else:
                        Enemy.wasMapCreated = True
                        Map.yValue = self.FreePlayMap.startNode()[1]
                        yValue = self.FreePlayMap.startNode()[1]
                    width = 100
                    cellCenter = 50
                    newCenter = []
                    if len(self.FreePlayMap.userCreatedPath) != 0:
                        for coord in self.FreePlayMap.userCreatedPath:
                            newCenter.append(((coord[0] * width) + cellCenter, (coord[1] * width) + cellCenter))
                        Map.centerCellList = newCenter
                    print(self.FreePlayMap.centerCellList)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.debugOn:
                    print(mouse_x, mouse_y)

                # Spawn enemies
                if self.wave > -1:
                    spawnDelay = 0
                elif self.wave > 2:
                    spawnDelay = 60
                elif self.wave > 5:
                    spawnDelay = 180
                elif self.wave > 9:
                    self.wonGame = True
                if self.roundOver:
                    pass
                else:
                    if self.time % 240 - spawnDelay == 0:
                        self.enemies.append(Fast(1050, yValue * 100 + 50, 15))
                        self.enemiesSpawned += 1
                    if self.time % 120 - spawnDelay == 0:
                        self.enemies.append(Slow(1050, yValue * 100 + 50, 15))
                        self.enemiesSpawned += 1
                    if self.time % 60 == 0:
                        self.enemies.append(Normal(1050, yValue * 100 + 50, 15))
                        self.enemiesSpawned += 1

                    if self.enemiesSpawned == (self.wave + 1)* 10:
                        self.roundOver = True

                if self.wave > 4:
                    if self.time % 50 == 0:
                        self.enemies.append(Tank(1050, yValue * 100 + 50, 15))
                        self.enemiesSpawned += 1

                if self.wave > 2:
                    if self.time % 60 == 0:
                        self.enemies.append(Air(1050, yValue * 100 + 50, 15))
                        self.enemiesSpawned += 1

                # Update enemies
                for enemy in self.enemies:
                    enemy.enemyPathing()
                    enemy.check()
                    enemy.move()
                    enemy.updateDir()
                    if enemy.currentHealth <= 0:
                        self.enemies.remove(enemy)
                        self.enemiesKilled += 1
                        self.player.money += enemy.value
                        self.score += enemy.value * 5
                    if enemy.currPoint == len(enemy.centerCellList) - 1:
                        self.enemies.remove(enemy)
                        if self.fortress.currentHealth >= 0:
                            self.fortress.currentHealth -= enemy.damage
                            if self.fortress.currentHealth <= 0:
                                self.mode = "gameOverMode"

                # Loop through characters and enemies and
                # check if in range, then adjust angle and fire

                for character in self.characters:
                    if self.debugOn:
                        character.rotate(mouse_x, mouse_y)

                    for enemy in self.enemies:
                        if character.distance(enemy.x, enemy.y) < character.radius:


                            # add to queue
                            # while enemy still in range and alive, attack that enemy
                            # check if list not empty
                            # else not dead or out of range, remove from queue

                            # character.attack(enemy)  always attack first enemy until dead

                            print(character.inRange)

                            if character.canAttack(enemy) and self.drag == False:
                                self.currAttack = enemy
                                character.rotate(enemy.x, enemy.y)
                                if self.time % 10 == 0:
                                    self.bullets.append(character.shoot(enemy))

                for character in self.characters:
                    if self.mode == "gameMode":
                        water = self.map.waterTiles()
                    else:
                        water = self.FreePlayMap.waterTiles()
                    if (character.x//100, character.y//100) in water and self.drag == False:
                        self.characters.remove(character)
                        self.player.money += character.cost





                # Loop through bullets and move them
                # also delete if offscreen
                for bullet in self.bullets:
                    bullet.move()
                    if bullet.offscreen(self.width, self.height):
                        self.bullets.remove(bullet)

                # Loop through bullets and enemies
                # check for collision
                for character in self.characters:
                    for bullet in self.bullets:
                        for enemy in self.enemies:
                            if bullet.collision(enemy.x, enemy.y, 40) and enemy.enemyType == "Ground":
                                try:
                                    self.bullets.remove(bullet)
                                except:
                                    pass



                # Update characters
                for character in self.characters:
                    if character.selected == True and self.drag == False and character.x < self.width - self.width // 6 + 25:
                        self.upgradeMenu = True
                    if character.selected == False:
                        character.update()


    def redrawAll(self, screen):

        if self.mode == "gameOverMode":
            pygame.draw.rect(screen, (255, 107, 107), (0, 0, 1200, 800))

            self.gameOverScreen = Button((254, 202, 87), self.width // 2 - 150, self.height // 2 - 200, 300, 100, "Game Over!")
            self.Restart = Button((254, 202, 87), self.width // 2 - 150, self.height // 2, 300, 100, "Press 'r' to restart")
            self.SeedDisplay = Button((254, 202, 87), self.width // 2 - 150, self.height // 2 + 200, 300, 100, "Seed: " + str(self.seed))

            self.gameOverScreen.draw(screen)
            self.Restart.draw(screen)
            self.SeedDisplay.draw(screen)


        if self.mode == "startScreenMode":
            # Draws background
            pygame.draw.rect(screen, (29, 209, 161), (0, 0, 1200, 800))
            self.Campaign = Button((254, 202, 87), self.width//2 - 150, self.height//2 - 200, 300, 100, "Campaign")
            self.FreeMode = Button((254, 202, 87), self.width//2 - 150, self.height//2, 300, 100, "Free Play")


            screen.blit(self.displayText("Tower Defense", 54, (0, 0, 0)), (self.width//2 - 135, self.height//2 - 300))

            self.Campaign.draw(screen, (0, 0, 0))
            self.FreeMode.draw(screen, (0, 0, 0))



        if self.mode == "startScreenMode/FreeMode":
            pygame.draw.rect(screen, (254, 202, 87), (0, 0, 1200, 800))

            screen.blit(self.displayText("Tower Defense", 54, (0, 0, 0)),
                        (self.width // 2 - 135, self.height // 2 - 300))

            self.editor.draw(screen, (0, 0, 0))
            self.LoadLevel.draw(screen, (0, 0, 0))
            self.Generate.draw(screen, (0, 0, 0))

            self.backButton.draw(screen)


        if self.mode == "startScreenMode/FreeMode/LevelEditor":
            pygame.draw.rect(screen, (155, 215, 255), (0, 0, 1200, 800))


            sand = Button((254, 202, 87), self.width - 200, 100, 200, 50, "Press '1' for sand")
            sand.draw(screen)

            water = Button((254, 202, 87), self.width - 200, 200, 200, 50, "Press '2' for water")
            water.draw(screen)


            start = Button((254, 202, 87), self.width - 200, 300, 200, 50, "'b' for start node")
            start.draw(screen)

            end = Button((254, 202, 87), self.width - 200, 400, 200, 50, "'e' for end node")
            end.draw(screen)

            self.levelEdit.drawLevelEditor(screen)



            self.backButton.x = self.width - self.backButton.width
            self.backButton.draw(screen)

        if self.mode == "startScreenMode/FreeMode/SaveLevels":
            pygame.draw.rect(screen, (123, 87, 85), (0, 0, 1200, 800))

            self.save1 = Button((10, 189, 227), self.width // 2 - 150, self.height // 2 - 375, 300, 100, self.saveSlot1)
            self.save2 = Button((10, 189, 227), self.width // 2 - 150, self.height // 2 - 225, 300, 100, self.saveSlot2)
            self.save3 = Button((10, 189, 227), self.width // 2 - 150, self.height // 2 - 75, 300, 100, self.saveSlot3)
            self.save4 = Button((10, 189, 227), self.width // 2 - 150, self.height // 2 + 75, 300, 100, self.saveSlot4)
            self.save5 = Button((10, 189, 227), self.width // 2 - 150, self.height // 2 + 225, 300, 100, self.saveSlot5)

            self.save1.draw(screen, (0, 0, 0))
            self.save2.draw(screen, (0, 0, 0))
            self.save3.draw(screen, (0, 0, 0))
            self.save4.draw(screen, (0, 0, 0))
            self.save5.draw(screen, (0, 0, 0))

            self.backButton.draw(screen, (0, 0, 0))

        if self.mode == "startScreenMode/FreeMode/LoadLevels":

            pygame.draw.rect(screen, (84, 160, 255), (0, 0, 1200, 800))

            self.save1 = Button((255, 255, 255), self.width // 2 - 150, self.height // 2 - 375, 300, 100, self.saveSlot1)
            self.save2 = Button((255, 255, 255), self.width // 2 - 150, self.height // 2 - 225, 300, 100, self.saveSlot2)
            self.save3 = Button((255, 255, 255), self.width // 2 - 150, self.height // 2 - 75, 300, 100, self.saveSlot3)
            self.save4 = Button((255, 255, 255), self.width // 2 - 150, self.height // 2 + 75, 300, 100, self.saveSlot4)
            self.save5 = Button((255, 255, 255), self.width // 2 - 150, self.height // 2 + 225, 300, 100, self.saveSlot5)

            self.save1.draw(screen, (0, 0, 0))
            self.save2.draw(screen, (0, 0, 0))
            self.save3.draw(screen, (0, 0, 0))
            self.save4.draw(screen, (0, 0, 0))
            self.save5.draw(screen, (0, 0, 0))

            self.backButton.draw(screen, (0, 0, 0))

        if self.mode == "startScreenMode/FreeMode/GenerateSeeds":
            pygame.draw.rect(screen, (255, 159, 243), (0, 0, 1200, 800))
            self.inputBox = Button((255, 255, 255), self.width//2 - 250, self.height//2 - 100, 500, 100, self.inputText)
            self.inputBox.draw(screen, (0, 0, 0))

            self.backButton.draw(screen, (0, 0, 0))



        if self.mode == "gameMode":

            self.map.draw(screen)

            # Draw all enemies
            for enemy in self.enemies:
                enemy.draw(screen)
                enemy.drawHealth(screen)


            #pygame.draw.rect(screen, (213, 123, 0), (self.width - self.width // 6 + 25, 25, 150, 150))



            # Draw all bullets
            for bullet in self.bullets:
                bullet.draw(screen)

            # Draw sidebar
            self.woodImg = pygame.transform.scale(self.woodImg, (1200, 800))
            screen.blit(self.woodImg, (self.width - self.width // 6, 0,
                                       400, 400))

            # Draws sidebar characters
            self.soldier.draw(screen)
            self.sniper.draw(screen)
            self.heavy.draw(screen)

            costSoldier = Button((0, 210, 211), self.width - 100, 25, self.width, 60, "150")
            cost1 = self.displayText("$150", 36, (0, 0, 0))
            costSoldier.draw(screen)
            screen.blit(cost1, (self.width - 75, 45))


            costSniper = Button((0, 210, 211), self.width - 100, 130, self.width, 60, "550")
            costSniper.draw(screen)
            cost2 = self.displayText("$350", 36, (0, 0, 0))
            screen.blit(cost2, (self.width - 75, 150))


            costHeavy = Button((0, 210, 211), self.width - 100, 230, self.width, 60, "300")
            costHeavy.draw(screen)
            cost3 = self.displayText("$550", 36, (0, 0, 0))
            screen.blit(cost3, (self.width - 75, 250))

            self.RepairTower = Button((0, 210, 211), self.width - 200, self.height - 300, 200, 60, "Repair Tower $1000")
            self.RepairTower.draw(screen)

            # Draw all characters
            for character in self.characters:
                character.draw(screen)
                if self.debugOn: character.drawDebug(screen)
            # Draw upgrade menu
            if self.upgradeMenu == True:
                for character in self.characters:
                    if character.selected == True and self.drag == False:
                        character.upgradeMenu(screen)

            self.fortress.drawHealth(screen)
            self.fortress.draw(screen)

            screen.blit(self.displayText("Money: $" + str(self.player.money), 54, (255, 255, 255)),
                        (25, self.height - 150, 100 + self.fortress.startingHealth, 15))

            if self.roundOver and len(self.enemies) == 0:
                screen.blit(self.darkBG, (0, 0))
                self.roundRecap.draw(screen)
                roundRecap = self.displayText("Round Recap", 84, (255, 255, 255))
                screen.blit(roundRecap, ((self.width//2 + 1000) // 4, self.height//2 - 275))

                highScore = self.displayText("High Score: " + str(self.score), 84, (255, 255, 255))
                screen.blit(highScore, ((self.width // 2 + 1000) // 4, self.height // 2 - 175))

                enemiesKilled = self.displayText("Enemies Killed: " + str(self.enemiesKilled), 84, (255, 255, 255))
                screen.blit(enemiesKilled, ((self.width // 2 + 1000) // 4 - 75, self.height // 2 - 75))

                seed = self.displayText("Seed: " + str(self.map.seed), 84, (255, 255, 255))
                screen.blit(seed, ((self.width // 2 + 1000) // 8, self.height // 2 + 25))

                self.nextRound = Button((254, 202, 87), (self.width//2 + 1000) // 4, self.height//2 + 150, 400, 100, "Next Round")
                self.nextRound.draw(screen)

            if self.wonGame:
                screen.blit(self.darkBG, (0, 0))
                self.roundRecap.draw(screen)
                roundRecap = self.displayText("Round Recap", 84, (255, 255, 255))
                screen.blit(roundRecap, ((self.width // 2 + 1000) // 4, self.height // 2 - 275))

                highScore = self.displayText("High Score: " + str(self.score), 84, (255, 255, 255))
                screen.blit(highScore, ((self.width // 2 + 1000) // 4, self.height // 2 - 175))

                enemiesKilled = self.displayText("Enemies Killed: " + str(self.enemiesKilled), 84, (255, 255, 255))
                screen.blit(enemiesKilled, ((self.width // 2 + 1000) // 4 - 75, self.height // 2 - 75))

                seed = self.displayText("Seed: " + str(self.map.seed), 84, (255, 255, 255))
                screen.blit(seed, ((self.width // 2 + 1000) // 8, self.height // 2 + 25))

                self.menuScreen = Button((254, 202, 87), (self.width // 2 + 1000) // 4, self.height // 2 + 150, 400, 100, "Exit")
                self.menuScreen.draw(screen)

            if self.isPaused:
                screen.blit(self.darkBG, (0, 0))
                self.roundRecap.draw(screen)
                pauseMenu = self.displayText("Tower Defense", 84, (255, 255, 255))
                screen.blit(pauseMenu, ((self.width//2 + 1000) // 4, self.height//2 - 275))

                self.resumeButton = Button((254, 202, 87), (self.width//2 + 1000) // 4 + 50, self.height//2 - 100, 325, 75, "Resume Game")
                self.resumeButton.draw(screen, (0, 0, 0))

                self.menuScreen = Button((254, 202, 87), (self.width//2 + 1000) // 4 + 50, self.height//2, 325, 75, "Exit")
                self.menuScreen.draw(screen, (0, 0, 0))

                self.quit = Button((254, 202, 87), (self.width//2 + 1000) // 4 + 50, self.height//2 + 100, 325, 75, "Quit Game")
                self.quit.draw(screen, (0, 0, 0))



        if self.mode == "startScreenMode/FreeMode/FreePlay":

            self.FreePlayMap.draw(screen)

            # Draw all enemies
            for enemy in self.enemies:
                enemy.draw(screen)
                enemy.drawHealth(screen)


            # Draw all bullets
            for bullet in self.bullets:
                bullet.draw(screen)

            # Draw sidebar
            self.woodImg = pygame.transform.scale(self.woodImg, (1200, 800))
            screen.blit(self.woodImg, (self.width - self.width // 6, 0,
                                       400, 400))
            # Draws sidebar characters
            self.soldier.draw(screen)
            self.sniper.draw(screen)
            self.heavy.draw(screen)

            costSoldier = Button((0, 210, 211), self.width - 100, 25, self.width, 60, "150")
            cost1 = self.displayText("$150", 36, (0, 0, 0))
            costSoldier.draw(screen)
            screen.blit(cost1, (self.width - 75, 45))

            costSniper = Button((0, 210, 211), self.width - 100, 130, self.width, 60, "550")
            costSniper.draw(screen)
            cost2 = self.displayText("$350", 36, (0, 0, 0))
            screen.blit(cost2, (self.width - 75, 150))

            costHeavy = Button((0, 210, 211), self.width - 100, 230, self.width, 60, "300")
            costHeavy.draw(screen)
            cost3 = self.displayText("$550", 36, (0, 0, 0))
            screen.blit(cost3, (self.width - 75, 250))

            self.RepairTower = Button((0, 210, 211), self.width - 200, self.height - 300, 200, 60, "Repair Tower $1000")
            self.RepairTower.draw(screen)

            # Draw all characters
            for character in self.characters:
                character.draw(screen)
                if self.debugOn: character.drawDebug(screen)
            # Draw upgrade menu
            if self.upgradeMenu == True:
                for character in self.characters:
                    if character.selected == True and self.drag == False:
                        character.upgradeMenu(screen)

            self.fortress.drawHealth(screen)
            self.fortress.draw(screen)

            screen.blit(self.displayText("Money: $" + str(self.player.money), 54, (255, 255, 255)),
                        (25, self.height - 150, 100 + self.fortress.startingHealth, 15))

            if self.roundOver and len(self.enemies) == 0:
                screen.blit(self.darkBG, (0, 0))
                self.roundRecap.draw(screen)
                roundRecap = self.displayText("Round Recap", 84, (255, 255, 255))
                screen.blit(roundRecap, ((self.width // 2 + 1000) // 4, self.height // 2 - 275))

                highScore = self.displayText("High Score: " + str(self.score), 84, (255, 255, 255))
                screen.blit(highScore, ((self.width // 2 + 1000) // 4, self.height // 2 - 175))

                enemiesKilled = self.displayText("Enemies Killed: " + str(self.enemiesKilled), 84, (255, 255, 255))
                screen.blit(enemiesKilled, ((self.width // 2 + 1000) // 4 - 75, self.height // 2 - 75))

                seed = self.displayText("Seed: " + str(self.map.seed), 84, (255, 255, 255))
                screen.blit(seed, ((self.width // 2 + 1000) // 8, self.height // 2 + 25))

                self.nextRound = Button((254, 202, 87), (self.width // 2 + 1000) // 4, self.height // 2 + 150, 400, 100,
                                        "Next Round")
                self.nextRound.draw(screen)

            if self.wonGame:
                screen.blit(self.darkBG, (0, 0))
                self.roundRecap.draw(screen)
                roundRecap = self.displayText("Round Recap", 84, (255, 255, 255))
                screen.blit(roundRecap, ((self.width // 2 + 1000) // 4, self.height // 2 - 275))

                highScore = self.displayText("High Score: " + str(self.score), 84, (255, 255, 255))
                screen.blit(highScore, ((self.width // 2 + 1000) // 4, self.height // 2 - 175))

                enemiesKilled = self.displayText("Enemies Killed: " + str(self.enemiesKilled), 84, (255, 255, 255))
                screen.blit(enemiesKilled, ((self.width // 2 + 1000) // 4 - 75, self.height // 2 - 75))

                seed = self.displayText("Seed: " + str(self.map.seed), 84, (255, 255, 255))
                screen.blit(seed, ((self.width // 2 + 1000) // 8, self.height // 2 + 25))

                self.menuScreen = Button((254, 202, 87), (self.width // 2 + 1000) // 4, self.height // 2 + 150, 400, 100, "Exit")
                self.menuScreen.draw(screen)


            if self.isPaused:
                screen.blit(self.darkBG, (0, 0))
                self.roundRecap.draw(screen)
                pauseMenu = self.displayText("Tower Defense", 84, (255, 255, 255))
                screen.blit(pauseMenu, ((self.width//2 + 1000) // 4, self.height//2 - 275))

                self.resumeButton = Button((254, 202, 87), (self.width//2 + 1000) // 4 + 50, self.height//2 - 100, 325, 75, "Resume Game")
                self.resumeButton.draw(screen, (0, 0, 0))

                self.menuScreen = Button((254, 202, 87), (self.width//2 + 1000) // 4 + 50, self.height//2, 325, 75, "Exit")
                self.menuScreen.draw(screen, (0, 0, 0))

                self.quit = Button((254, 202, 87), (self.width//2 + 1000) // 4 + 50, self.height//2 + 100, 325, 75, "Quit Game")
                self.quit.draw(screen, (0, 0, 0))

Game(1200, 800).run()
