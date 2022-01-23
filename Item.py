import pygame
import pygame.gfxdraw
from random import randint
from SimpleVector import Vector
from Globals import *


class Item:
    def __init__(self, positionVector, sizeVector):
        self.pos = Vector(positionVector)
        self.size = Vector(sizeVector)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.collected = False

    def update(self, curLevel):
        pass

    def render(self, surface, camOffset):
        pass

    def renderDebug(self, surface, camOffset):
        if Globs.DEBUG_VISUALS:
            tmp = [self.pos.x + camOffset.x, self.pos.y + camOffset.y, self.size.x, self.size.y]
            pygame.draw.rect(surface, white, tmp, 1)


class Portal(Item):
    def __init__(self, positionVector, sizeVector, activeAtDay=True):
        super().__init__(positionVector, sizeVector)
        self.activeAtDay = activeAtDay
        self.active = False

        self.colorSwapTimer = 0
        self.setColorSwapTimer = 2
        self.color = portal_A

    def update(self, curLevel):
        self.active = False
        if curLevel.day == self.activeAtDay:
            self.active = True
            if curLevel.player.hitbox.colliderect(self.rect):
                curLevel.changeDay()

            if self.colorSwapTimer > 0:
                self.colorSwapTimer -= Globs.dt
            else:
                self.setColorSwapTimer = randint(1, 4) / 2
                self.colorSwapTimer = self.setColorSwapTimer
                if self.color == portal_A:
                    self.color = portal_B
                else:
                    self.color = portal_A

    def render(self, surface, camOffset):
        if self.active:
            tmp = [self.pos.x + camOffset.x, self.pos.y + camOffset.y, self.size.x, self.size.y]
            pygame.draw.rect(surface, purple, tmp, 0)
            pygame.gfxdraw.box(surface, tmp, self.color)


class Key(Item):
    def __init__(self, positionVector, sizeVector):
        super().__init__(positionVector, sizeVector)
        self.image = pygame.image.load("Assets/Images/Key.png")

    def update(self, curLevel):
        if curLevel.player.hitbox.colliderect(self.rect):
            self.collected = True
            curLevel.player.inventory.append('Key')

    def render(self, surface, camOffset):
        surface.blit(self.image, (self.pos + camOffset).i)


class Door(Item):
    def __init__(self, positionVector, sizeVector):
        super().__init__(positionVector, sizeVector)
        self.image = pygame.transform.scale(pygame.image.load("Assets/Images/Door.png"), (50, 100))

    def update(self, curLevel):
        if curLevel.player.hitbox.colliderect(self.rect):
            if 'Key' in curLevel.player.inventory:
                curLevel.loadLevel(curLevel.num + 1)

    def render(self, surface, camOffset):
        tmp = [self.pos.x + camOffset.x, self.pos.y + camOffset.y, self.size.x, self.size.y]
        pygame.draw.rect(surface, green, tmp, 0)

        surface.blit(self.image, (self.pos + camOffset).i)
