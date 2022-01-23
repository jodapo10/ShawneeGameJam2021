import pygame
from SimpleVector import Vector
from Globals import *


class Tile:
    def __init__(self, position, textureKey):
        self.pos = Vector(position)
        self.texKey = textureKey


class Tilemap:
    def __init__(self, fileName):
        self.mapSize = [0, 0]
        self.textures = {}
        self.hasCollision = []
        self.doesDamage = []
        self.tiles = []
        self.collisionTiles = []
        self.damageTiles = []

        # Day and Night Exclusives
        self.dayHasCollision = []
        self.dayDoesDamage = []
        self.nightHasCollision = []
        self.nightDoesDamage = []

        self.dayTiles = []
        self.nightTiles = []
        self.dayDamageTiles = []
        self.nightDamageTiles = []

        self.mapKey = self.tilemapFromFile(fileName)

        # Clear Unneeded Data
        self.hasCollision.clear()
        self.doesDamage.clear()
        self.dayHasCollision.clear()
        self.dayDoesDamage.clear()
        self.nightHasCollision.clear()
        self.nightDoesDamage.clear()

    def tilemapFromFile(self, fileName):
        readFile = open(fileName, "r")
        lines = readFile.readlines()
        readFile.close()
        mapString = ""
        for line in lines:
            line = line.strip()
            key, value = line.split("=")
            if key == "mapLine":
                mapString += value[1:-1]
                mapString += "\n"
            elif key == "loadTexture":
                textureKey, textureFileName, collision, damages = value.split(",")
                self.textures[textureKey] = pygame.transform.scale(pygame.image.load(textureFileName),
                                                                   (2 * Globs.TILE_SIZE, Globs.TILE_SIZE))
                # Determine if has Collision
                if collision == "True":
                    self.hasCollision.append(textureKey)
                elif collision == "Day":
                    self.dayHasCollision.append(textureKey)
                elif collision == "Night":
                    self.nightHasCollision.append(textureKey)

                # Determine if does Damage
                if damages == "True":
                    self.doesDamage.append(textureKey)
                elif damages == "Day":
                    self.dayDoesDamage.append(textureKey)
                elif damages == "Night":
                    self.nightDoesDamage.append(textureKey)

            elif key == "mapSize":
                w, h = value.split(",")
                self.mapSize = [int(w), int(h)]

        return self.tilemapFromString(mapString.strip())

    def tilemapFromString(self, tilemapString):
        localTilemap = []
        for i in range(self.mapSize[1]):
            localTilemap.append(["  "] * self.mapSize[0])
        lines = tilemapString.split("\n")
        row = 0
        for line in lines:
            for col in range(0, self.mapSize[0]):
                tmpKey = line[col * 2: col * 2 + 2]
                localTilemap[row][col] = tmpKey
                if tmpKey != "  " and tmpKey != '':
                    self.tiles.append(Tile([col * Globs.TILE_SIZE, row * Globs.TILE_SIZE], tmpKey))

                    # Collision Tiles
                    if tmpKey in self.hasCollision:
                        self.collisionTiles.append(
                            pygame.Rect(col * Globs.TILE_SIZE, row * Globs.TILE_SIZE, Globs.TILE_SIZE, Globs.TILE_SIZE))
                    elif tmpKey in self.dayHasCollision:
                        self.dayTiles.append(
                            pygame.Rect(col * Globs.TILE_SIZE, row * Globs.TILE_SIZE, Globs.TILE_SIZE, Globs.TILE_SIZE))
                    elif tmpKey in self.nightHasCollision:
                        self.nightTiles.append(
                            pygame.Rect(col * Globs.TILE_SIZE, row * Globs.TILE_SIZE, Globs.TILE_SIZE, Globs.TILE_SIZE))

                    # Damage Tiles
                    if tmpKey in self.doesDamage:
                        self.damageTiles.append(
                            pygame.Rect(col * Globs.TILE_SIZE, row * Globs.TILE_SIZE, Globs.TILE_SIZE, Globs.TILE_SIZE))
                    elif tmpKey in self.dayDoesDamage:
                        self.dayDamageTiles.append(
                            pygame.Rect(col * Globs.TILE_SIZE, row * Globs.TILE_SIZE, Globs.TILE_SIZE, Globs.TILE_SIZE))
                    elif tmpKey in self.nightDoesDamage:
                        self.nightDamageTiles.append(
                            pygame.Rect(col * Globs.TILE_SIZE, row * Globs.TILE_SIZE, Globs.TILE_SIZE, Globs.TILE_SIZE))
            row += 1

        return localTilemap

    def render(self, surface, camOffset, dayCycle=None):
        for tile in self.tiles:
            tmp = tile.pos + camOffset
            if -2 * Globs.TILE_SIZE <= tmp.x <= Globs.WINDOW_SIZE[0] + 2 * Globs.TILE_SIZE:
                if -2 * Globs.TILE_SIZE <= tmp.y <= Globs.WINDOW_SIZE[1] + 2 * Globs.TILE_SIZE:
                    surface.blit(self.textures[tile.texKey], tmp, dayCycle)
