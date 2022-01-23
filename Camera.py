import pygame
import pygame.gfxdraw
from random import randint
from SimpleVector import Vector
from Globals import *


class Camera:
    def __init__(self):
        self.offset = Vector(0, 0)
        self.rect = pygame.Rect(0, 0, Globs.WINDOW_SIZE[0], Globs.WINDOW_SIZE[1])

        self.skySwapTimer = 0
        self.setSkySwapTimer = 3
        self.secondSky = False

    def setOffset(self, deltaPos, clear=False):
        if clear:
            self.offset = Vector(375, 375)
        self.offset -= deltaPos

    def update(self):
        if self.skySwapTimer <= 0:
            self.skySwapTimer = self.setSkySwapTimer
            if randint(1, 2) == 2:
                self.secondSky ^= True
        self.skySwapTimer -= Globs.dt

    def render(self, surface, curLevel):
        # Set Clipping Rectangle
        surface.set_clip(self.rect)

        # Fill Background
        if curLevel.day:
            surface.fill(sky)
            if self.secondSky:
                pygame.gfxdraw.box(surface, (0, 0, Globs.WINDOW_SIZE[0], Globs.WINDOW_SIZE[1]), sky_B)
        else:
            surface.fill(nightSky)
            if self.secondSky:
                pygame.gfxdraw.box(surface, (0, 0, Globs.WINDOW_SIZE[0], Globs.WINDOW_SIZE[1]), nightSky_B)

        # Items
        for item in curLevel.itemsList:
            item.render(surface, self.offset)
            if Globs.DEBUG_VISUALS:
                item.renderDebug(surface, self.offset)

        # Current Level
        curLevel.tilemap.render(surface, self.offset, curLevel.blitRect)
        for enemy in curLevel.enemiesList:
            enemy.render(surface, self.offset)

        curLevel.player.render(surface, self.offset, curLevel.day)

        # Reset Clipping Rectangle
        surface.set_clip(None)
