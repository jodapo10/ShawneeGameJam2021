import pygame
from SimpleVector import Vector
from Globals import *
from Text import Text
from Button import Button
from Tilemap import Tilemap
from Camera import Camera
from Player import Player
from Enemy import Enemy, SoldierEnemy
from Item import Portal, Key, Door

banner = pygame.transform.scale(pygame.image.load("Assets/Images/Banner.png"), (600, 300))


class LevelManager:
    def __init__(self):
        self.num = 0
        self.settings = False

        # Menu Options
        self.buttonList = []
        self.holdButtonsList = []
        self.menuState = 'Main'
        self.textDict = {Text('welcome', [10, 10]): [None, None]}

        # Camera
        self.camera = Camera()

        # Entities
        self.player = Player()
        self.enemiesList = []
        self.itemsList = []

        # Tilemap
        self.tilemap = Tilemap("Assets/Tilemaps/Test_1.txt")
        self.blitRect = [0, 0, Globs.TILE_SIZE, Globs.TILE_SIZE]
        self.day = True
        self.loadLevel(0)

    def changeDay(self, forceDay=False):
        self.day ^= True
        if forceDay:
            self.day = True
        if self.day:
            self.blitRect = [0, 0, Globs.TILE_SIZE, Globs.TILE_SIZE]
        else:
            self.blitRect = [Globs.TILE_SIZE, 0, Globs.TILE_SIZE, Globs.TILE_SIZE]

    def loadLevel(self, number=0):
        self.num = number

        if self.num == 0:
            Globs.PAUSED = True
            self.player.hasControl = False
            self.buttonList = [Button([25, 350], [400, 100], 'NewGame', "new game", Text.Fonts[50]),
                               Button([25, 475], [400, 100], 'Settings', "settings", Text.Fonts[50]),
                               Button([690, 550], [100, 40], 'Quit', "quit", Text.Fonts[25])]

        if self.num == 1:
            # Reset all changed values
            self.changeDay(True)
            Globs.PAUSED = False
            self.player.hasControl = True
            self.player.setSpeed()
            self.textDict.clear()
            self.buttonList = []

            # Load Tilemap
            self.tilemap = Tilemap("Assets/Tilemaps/Tilemap_1.txt")

            # Set up Player and Camera
            self.player.setPosition(500, 800)
            self.camera.setOffset(Vector(500, 825), True)

            # Set up Entities
            self.enemiesList = []

            # Set up Items
            self.itemsList = [Portal([2735, 400], [100, 250], False),
                              Portal([2735, 700], [100, 350], True),
                              Key([3200, 700], [32, 32]),
                              Door([4550, 950], [50, 100])]

        elif self.num == 2:
            # Reset all changed values
            Globs.PAUSED = False
            self.player.hasControl = True
            self.player.setSpeed()
            self.textDict.clear()
            self.buttonList = []

            # Load Tilemap
            self.tilemap = Tilemap("Assets/Tilemaps/Tilemap_2.txt")

            # Set up Player and Camera
            self.player.setPosition(500, 450)
            self.camera.setOffset(Vector(500, 500), True)

            # Set up Entities
            self.enemiesList = [SoldierEnemy([900, 1700]), SoldierEnemy([2150, 1200])]

            # Set up Items
            self.itemsList = [Portal([400, 1000], [450, 100]),
                              Portal([3265, 1400], [185, 250], False),
                              Portal([1250, 1000], [125, 150]),
                              Portal([3265, 850], [185, 300], False),
                              Key([1500, 500], [32, 32]),
                              Door([1050, 500], [50, 100])]

        elif self.num == 3:
            self.textDict[Text('thanks for playing!', [10, 10])] = [None, None]
            self.loadLevel(0)

    def loadMenu(self, menuType='Paused'):
        """ :param menuType: 'Paused', 'Resume', 'Main', 'Settings', etc... """
        Globs.PAUSED = True
        self.textDict.clear()

        if menuType == 'Paused':
            self.menuState = 'Paused'
            self.buttonList = [Button([25, 25], [150, 50], 'Resume', 'resume:', Text.Fonts[25]),
                               Button([25, 100], [150, 50], 'Main', 'menu:', Text.Fonts[25])]

        elif menuType == 'Resume':
            self.buttonList.clear()
            Globs.PAUSED = False

        elif menuType == 'Settings':
            self.settings = True
            self.buttonList = [Button([25, 25], [150, 50], 'Back', 'back', Text.Fonts[25])]
            self.textDict = {Text('input:', [550, 10]): [Text.Fonts[50], None],
                             Text('del to quit', [550, 60]): [None, None],
                             Text('f11 fullscreen', [550, 80]): [None, None],
                             Text('a + d to move', [550, 100]): [None, None],
                             Text('space to jump', [550, 120]): [None, None],
                             Text('l-shift to sprint', [550, 140]): [None, None],
                             Text('e to use swap-form', [550, 160]): [None, None],
                             Text('click to act', [550, 180]): [None, None]}

        elif menuType == 'Main':
            self.settings = False
            self.menuState = 'Main'
            self.loadLevel(0)

    def update(self, event, keys, mouse):
        # Menu Options
        if Globs.PAUSED:
            for button in self.buttonList:
                button.update(event, mouse)
                if button.clicked:
                    if button.type == 'NewGame':
                        self.player = Player()
                        self.loadLevel(1)
                    if button.type == 'NextLevel':
                        self.loadLevel(self.num + 1)
                    elif button.type == 'Resume':
                        if self.player.lives <= 0:
                            self.loadLevel(self.num)
                            self.player.resetValues(8)
                        self.loadMenu('Resume')
                    elif button.type == 'Main':
                        self.loadLevel(0)
                        self.menuState = 'Main'
                        self.textDict.clear()
                    elif button.type == 'Settings':
                        self.loadMenu('Settings')
                    elif button.type == 'Back':
                        self.loadMenu(self.menuState)
                    elif button.type == 'Quit':
                        Globs.RUNNING = False

        # Gameplay Updates
        else:
            # Player
            self.player.update(event, keys, mouse, self)
            self.camera.update()

            # Entities
            removalList = []
            for enemy in self.enemiesList:
                enemy.update(self)
                if enemy.dead:
                    removalList.append(enemy)
            for enemy in removalList:
                self.enemiesList.remove(enemy)

            # Items
            removalList = []
            for item in self.itemsList:
                item.update(self)
                if item.collected:
                    removalList.append(item)
            for item in removalList:
                self.itemsList.remove(item)

    def render(self, surface):
        # Menus
        if Globs.PAUSED:
            # Background
            surface.fill(grey)

            # Buttons
            for button in self.buttonList:
                button.render(surface)

            # Text
            for textEntry in self.textDict:
                textEntry.render(surface, self.textDict.get(textEntry)[0], self.textDict.get(textEntry)[1])

            if self.num == 0 and not self.settings:
                surface.blit(banner, (100, 25))

        else:
            # Camera
            self.camera.render(surface, self)
