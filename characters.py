import pygame
import math
import random
from pygamegame import PygameGame


# This file contains all the character classes that the player can place
# down in game in addition to the bullet class
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type


        self.greenCircle = pygame.image.load("assets/green-circle.png").convert_alpha()
        self.selected = False
        self.cx = x
        self.cy = y
        self.isGround = True
        self.inWater = False


        self.damage = 100
        self.currAttack = None

    def distance(self, otherX, otherY):
        return math.sqrt(((self.x - otherX)**2 + (self.y - otherY)**2))

    def canAttack(self, other):
        if self.isAntiAir and other.enemyType == "Air":
            return True
        if self.isGround and other.enemyType == "Ground":
            return True
        return False



class baseSoldier(Character):
    def __init__(self, x, y, type):
        super().__init__(x, y, type)
        self.type = "soldier1"
        self.radius = 200
        self.angle = 0
        self.cost = 150
        self.gameImgPath = "assets/soldier1.png"
        self.gameImg = pygame.image.load(self.gameImgPath).convert_alpha()
        self.gameImg = pygame.transform.scale(self.gameImg, (64, 54))
        self.ogImg = self.gameImg
        self.image = self.ogImg
        self.rect = self.image.get_rect()

        # Rounds per min
        self.shootSpeed = 50
        self.isAntiAir = False

        self.inRange = False
        self.damage = 100
        self.inWater = False
        self.circleSurface = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA, 32)

        pygame.draw.circle(self.circleSurface, (0, 255, 0, 100), (self.radius, self.radius), self.radius)

        self.circleSurfaceRED = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA, 32)

        pygame.draw.circle(self.circleSurfaceRED, (255, 0, 0, 100), (self.radius, self.radius), self.radius)


    def update(self):
        self.image = pygame.transform.rotate(self.ogImg, self.angle)

    # This thread helped me fix some issues with rotation, citing just in case
    # https://stackoverflow.com/questions/10645566/weird-shifting-when-using-pygame-transform-rotate
    def rotate(self, otherX, otherY):
        x = (otherX - (self.x + self.rect.width/2) ) + .0001
        y = (otherY - (self.y + self.rect.height/2) )
        self.angle = (180 / math.pi) * -math.atan2(y,x)
        self.image = pygame.transform.rotate(self.ogImg, int(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def upgradeMenu(self, screen):
        width = 1200
        edgeOfSidebar = width - width // 6

        # Upgrade Sidebar appears
        pygame.draw.rect(screen, (94, 144, 224), (edgeOfSidebar, 0,
                                   1200, 800))
        # Button Upgrade 1
        pygame.draw.rect(screen, (0, 0, 0), (edgeOfSidebar + 25, 90, 150, 85))

        # Button Upgrade 2
        pygame.draw.rect(screen, (255, 0, 0), (edgeOfSidebar + 25, 190, 150, 85))

        return True

    def upgrade1Clicked(self, mouseX, mouseY):
        width = 1200
        return mouseX > width - width // 6 + 25 and mouseY > 90 \
               and mouseX < width - width // 6 + 25 + 150 and mouseY < 90 + 85

    def draw(self, screen):
        if self.selected == True:

            if self.inWater:
                screen.blit(self.circleSurfaceRED, (self.cx - self.radius, self.cy - self.radius))
            else:
                screen.blit(self.circleSurface, (self.cx - self.radius, self.cy - self.radius))


        draw_rect = self.rect.move(self.x, self.y)
        screen.blit(self.image, draw_rect)

    def drawDebug(self, screen):
        debug_rect = self.rect.move(self.x, self.y)
        pygame.draw.rect(screen, (100, 0, 0), debug_rect, 1)

    def shoot(self, enemy):
        enemy.currentHealth -= self.damage
        x = self.x + self.rect.width // 2  # offset * math.cos(math.radians(self.angle))
        y = self.y + self.rect.height // 2  # offset * math.sin(math.radians(self.angle))
        return Bullet(x, y, self.angle, self.shootSpeed)

class Sniper(Character):
    def __init__(self, x, y, type):
        super().__init__(x, y, type)
        self.type = "sniper"
        self.radius = 600
        self.cost = 550
        self.angle = 0
        # Rounds per min
        self.shootSpeed = 100
        self.isGround = True
        self.isAntiAir = True
        self.gameImgPath = "assets/sniper.png"
        self.gameImg = pygame.image.load(self.gameImgPath).convert_alpha()
        self.gameImg = pygame.transform.scale(self.gameImg, (64, 54))
        self.ogImg = self.gameImg
        self.image = self.ogImg
        self.rect = self.image.get_rect()

        self.damage = 50
        self.inRange = False

        self.inWater = False

        self.circleSurface = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA, 32)

        pygame.draw.circle(self.circleSurface, (0, 255, 0, 100), (self.radius, self.radius), self.radius)

        self.circleSurfaceRED = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA, 32)

        pygame.draw.circle(self.circleSurfaceRED, (255, 0, 0, 100), (self.radius, self.radius), self.radius)

    def update(self):
        self.image = pygame.transform.rotate(self.ogImg, self.angle)

    # This thread helped me fix some issues with rotation, citing just in case
    # https://stackoverflow.com/questions/10645566/weird-shifting-when-using-pygame-transform-rotate
    def rotate(self, otherX, otherY):
        x = (otherX - (self.x + self.rect.width/2) ) + .0001
        y = (otherY - (self.y + self.rect.height/2) )
        self.angle = (180 / math.pi) * -math.atan2(y,x)
        self.image = pygame.transform.rotate(self.ogImg, int(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def upgradeMenu(self, screen):
        width = 1200
        edgeOfSidebar = width - width // 6

        # Upgrade Sidebar appears
        pygame.draw.rect(screen, (94, 144, 224), (edgeOfSidebar, 0,
                                   1200, 800))
        # Button Upgrade 1
        pygame.draw.rect(screen, (0, 0, 0), (edgeOfSidebar + 25, 90, 150, 85))

        # Button Upgrade 2
        pygame.draw.rect(screen, (255, 0, 0), (edgeOfSidebar + 25, 190, 150, 85))

        return True

    def upgrade1Clicked(self, mouseX, mouseY):
        width = 1200
        return mouseX > width - width // 6 + 25 and mouseY > 90 \
               and mouseX < width - width // 6 + 25 + 150 and mouseY < 90 + 85

    def draw(self, screen):
        if self.selected == True:
            #screen.blit(self.greenCircle, (self.cx - self.greenCircle.get_rect().width/2, self.cy - self.greenCircle.get_rect().height/2))

            if self.inWater:
                screen.blit(self.circleSurfaceRED, (self.cx - self.radius, self.cy - self.radius))
            else:
                screen.blit(self.circleSurface, (self.cx - self.radius, self.cy - self.radius))


        draw_rect = self.rect.move(self.x, self.y)
        screen.blit(self.image, draw_rect)

    def drawDebug(self, screen):
        debug_rect = self.rect.move(self.x, self.y)
        pygame.draw.rect(screen, (100, 0, 0), debug_rect, 1)


    def shoot(self, enemy):
        enemy.currentHealth -= self.damage
        x = self.x + self.rect.width // 2  # offset * math.cos(math.radians(self.angle))
        y = self.y + self.rect.height // 2  # offset * math.sin(math.radians(self.angle))
        return Bullet(x, y, self.angle, self.shootSpeed)


class Heavy(Character):
    def __init__(self, x, y, type):
        super().__init__(x, y, type)
        self.type = "heavy"
        self.radius = 100
        self.angle = 0
        self.cost = 350
        # Rounds per min
        self.shootSpeed = 40
        self.isGround = True
        self.isAntiAir = False
        self.gameImgPath = "assets/heavy.png"
        self.gameImg = pygame.image.load(self.gameImgPath).convert_alpha()
        self.gameImg = pygame.transform.scale(self.gameImg, (64, 54))
        self.ogImg = self.gameImg
        self.image = self.ogImg
        self.rect = self.image.get_rect()

        self.damage = 200

        self.inRange = False

        self.inWater = False

        self.circleSurface = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA, 32)

        pygame.draw.circle(self.circleSurface, (0, 255, 0, 100), (self.radius, self.radius), self.radius)

        self.circleSurfaceRED = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA, 32)

        pygame.draw.circle(self.circleSurfaceRED, (255, 0, 0, 100), (self.radius, self.radius), self.radius)

    def update(self):
        self.image = pygame.transform.rotate(self.ogImg, self.angle)

    # This thread helped me fix some issues with rotation, citing just in case
    # https://stackoverflow.com/questions/10645566/weird-shifting-when-using-pygame-transform-rotate
    def rotate(self, otherX, otherY):
        x = (otherX - (self.x + self.rect.width/2) ) + .0001
        y = (otherY - (self.y + self.rect.height/2) )
        self.angle = (180 / math.pi) * -math.atan2(y,x)
        self.image = pygame.transform.rotate(self.ogImg, int(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def upgradeMenu(self, screen):
        width = 1200
        edgeOfSidebar = width - width // 6

        # Upgrade Sidebar appears
        pygame.draw.rect(screen, (94, 144, 224), (edgeOfSidebar, 0,
                                   1200, 800))
        # Button Upgrade 1
        pygame.draw.rect(screen, (0, 0, 0), (edgeOfSidebar + 25, 90, 150, 85))

        # Button Upgrade 2
        pygame.draw.rect(screen, (255, 0, 0), (edgeOfSidebar + 25, 190, 150, 85))

        return True

    def upgrade1Clicked(self, mouseX, mouseY):
        width = 1200
        return mouseX > width - width // 6 + 25 and mouseY > 90 \
               and mouseX < width - width // 6 + 25 + 150 and mouseY < 90 + 85

    def draw(self, screen):
        if self.selected == True:
            if self.inWater:
                screen.blit(self.circleSurfaceRED, (self.cx - self.radius, self.cy - self.radius))
            else:
                screen.blit(self.circleSurface, (self.cx - self.radius, self.cy - self.radius))


        draw_rect = self.rect.move(self.x, self.y)
        screen.blit(self.image, draw_rect)

    def drawDebug(self, screen):
        debug_rect = self.rect.move(self.x, self.y)
        pygame.draw.rect(screen, (100, 0, 0), debug_rect, 1)

    def shoot(self, enemy):
        enemy.currentHealth -= self.damage
        x = self.x + self.rect.width // 2  # offset * math.cos(math.radians(self.angle))
        y = self.y + self.rect.height // 2  # offset * math.sin(math.radians(self.angle))
        return Bullet(x, y, self.angle, self.shootSpeed)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, cx, cy, angle, speed):
        self.cx = cx
        self.cy = cy
        self.radius = 3
        self.angle = angle
        self.speed = speed

        self.damage = 100

    # Check collision with enemies
    def collision(self, otherX, otherY, otherSize):
        dist =  ((self.cx - otherX) ** 2 + (self.cy - otherY) ** 2) ** .5
        return dist < otherSize

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.cx), int(self.cy)), self.radius)

    # Used from HW11
    def move(self):
        self.cx += math.cos(math.radians(self.angle)) * self.speed
        self.cy -= math.sin(math.radians(self.angle)) * self.speed

    # Used from HW11
    def offscreen(self, width, height):
        return (self.cx + self.radius <= 0 or self.cx - self.radius >= width) and \
               (self.cy + self.radius <= 0 or self.cy - self.radius >= height)
