import pygame
from SimpleVector import Vector
from Text import Text
from Globals import *


class Button:
    def __init__(self, posVector, sizeVector, effect=None, textString=None, font=None, color=black, bColor=white, hColor=white, hbColor=black):
        self.pos = Vector(posVector)
        self.size = Vector(sizeVector)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

        self.highlighted = False
        self.clicked = False
        self.color = color
        self.bColor = bColor
        self.hColor = hColor
        self.hbColor = hbColor

        self.type = effect
        self.text = Text(textString, self.pos + Vector(5, 10), 0, white)
        self.font = font

    def update(self, event, mouse):
        mouseX, mouseY = mouse.get_pos()
        self.highlighted = False
        self.clicked = False

        if self.rect.collidepoint(mouseX, mouseY):
            self.highlighted = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = True

    def render(self, surface):
        if not self.highlighted:
            pygame.draw.rect(surface, self.color, self.rect, 0)
            pygame.draw.rect(surface, self.bColor, self.rect, 2)
            if self.text is not None:
                self.text.updateColor(white)
        else:
            pygame.draw.rect(surface, self.hColor, self.rect, 0)
            pygame.draw.rect(surface, self.hbColor, self.rect, 2)
            if self.text is not None:
                self.text.updateColor(black)

        if self.text is not None:
            self.text.render(surface, self.font)
