import pygame
from Globals import *
from LevelManager import LevelManager


class GameLoop:
    def __init__(self):
        self.Running = True
        self.Clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(Globs.WINDOW_SIZE, pygame.SCALED)
        pygame.display.set_caption("Duality")

        # Current Level
        self.curLevel = LevelManager()

    def Update(self):
        # Time
        Globs.dt = self.Clock.tick(Globs.FPS) / 1000
        # Set_FPS(dt)

        # Get Input
        event = pygame.event.poll()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse

        # Quit
        if not Globs.RUNNING:
            self.Running = False
        if event.type == pygame.QUIT:
            self.Running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                self.Running = False

            if event.key == pygame.K_ESCAPE:
                if self.curLevel.num == 0:
                    self.Running = False
                elif not Globs.PAUSED:
                    self.curLevel.loadMenu('Paused')
                else:
                    self.curLevel.loadMenu('Resume')

            # Window Resize
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

        # Current Level
        self.curLevel.update(event, keys, mouse)

    def Render(self):
        # Background
        self.window.fill(blue)

        # Current Level
        self.curLevel.render(self.window)

        # Flip Surface
        pygame.display.flip()
