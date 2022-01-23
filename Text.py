import pygame
from SimpleVector import Vector
from Globals import *


class Text:
    Fonts = {}

    def __init__(self, text, positionVector, size=16, color=black, highlight=None):
        # Class Variables
        if len(Text.Fonts) == 0:
            Text.Fonts[16] = pygame.font.Font("Assets\Fonts\Font_JdP.ttf", 16)
            Text.Fonts[25] = pygame.font.Font("Assets\Fonts\Font_JdP.ttf", 25)
            Text.Fonts[50] = pygame.font.Font("Assets\Fonts\Font_JdP.ttf", 50)
        self.text = str(text)
        self.pos = Vector(positionVector)
        self.size = size

        self.color = color
        self.background = highlight

    def updateText(self, text=None):
        if text is not None:
            self.text = str(text)

    def updateColor(self, color, background=None):
        self.color = color
        self.background = background

    def render(self, surface, font=None, rect=None):
        if font is not None:
            tmp = font.render(self.text, False, self.color, self.background)
        else:
            tmp = Text.Fonts[16].render(self.text, False, self.color, self.background)

        if rect is None:
            surface.blit(tmp, self.pos.i)
        else:
            surface.blit(tmp, rect, pygame.Rect(0, 0, rect.w, rect.h))

