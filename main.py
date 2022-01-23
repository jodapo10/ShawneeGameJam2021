import pygame
from GameLoop import GameLoop
from Globals import Globs

pygame.init()

Globs.MONITOR_SIZE = [pygame.display.Info().current_w, pygame.display.Info().current_h]
GL = GameLoop()

""" 
Didn't quite get as far as I wanted. I'll be back next year.
 - JdP
"""

while GL.Running:
    GL.Update()
    GL.Render()

pygame.quit()
