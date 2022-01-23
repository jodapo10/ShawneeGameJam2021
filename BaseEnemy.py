import pygame
from random import randint
from SimpleVector import Vector
from Globals import *


class BaseEnemy:
    def __init__(self, positionVector):
        self.pos = Vector(positionVector)
        self.size = Vector(Globs.TILE_SIZE, Globs.TILE_SIZE)
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

        self.state = 'idle'

        self.spd = 0
        self.acc = 0.5 * Globs.dt
        self.maxSpd = 5
        self.YSpd = 0
        self.YAcc = Globs.GRAVITY
        self.maxYSpd = Globs.GRAVITY_MAX
        self.deltaPos = Vector(int(self.spd), int(self.YSpd))
        self.onGround = False

        self.direction = 1
        self.hurtboxOffset = Vector(30, 10)
        self.hurtboxSize = Vector(60, 70)
        self.hurtbox = None
        self.updateHurtbox()

        self.attackFrame = False

        self.actionTimer = 0
        self.setActionTimer = 5

        self.stunTimer = 0
        self.setStunTimer = 120

        self.lives = 4
        self.weakness = 1
        self.iFrames = 0
        self.setIFrames = 5
        self.dead = False

    def update(self, curLevel):

        self.makeChoice(curLevel)

        # Direction
        if curLevel.player.pos.x <= self.pos.x:
            self.direction = 1
        elif curLevel.player.pos.x >= self.pos.x + self.size.x:
            self.direction = 2

        # Gravity
        if not self.onGround:
            self.YSpd += self.YAcc * Globs.dt

        # Friction
        if self.state != 'moving':
            self.friction()

        # Timers
        if self.stunTimer > 0:
            self.stunTimer -= Globs.dt

        # Cap Speeds
        spdLimit = self.maxSpd
        if self.spd > spdLimit:
            self.spd = spdLimit
        elif self.spd < -spdLimit:
            self.spd = -spdLimit

        # Set Default Values
        self.onGround = False
        self.attackFrame = False

        # Test New Position --
        self.deltaPos = Vector(int(self.spd), int(self.YSpd))

        self.collision(curLevel, self.deltaPos)

        # Damage
        self.takeDamage(curLevel.player)
        if self.iFrames > 0:
            self.iFrames -= 0.5 * Globs.dt
        if self.lives <= 0:
            self.dead = True

        # Set Position
        self.pos += self.deltaPos
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.updateHurtbox()

    def makeChoice(self, curLevel):
        if self.actionTimer <= 0:
            self.setActionTimer = randint(180, 270) * Globs.dt
            self.actionTimer += self.setActionTimer
            choiceNum = randint(1, 3)

            if choiceNum == 1:
                # Move
                self.state = 'moving'
            elif choiceNum == 2:
                # Shield
                self.actionTimer -= 100
                self.state = 'defending'
            elif choiceNum == 3:
                # Sword
                self.state = 'attacking'
        else:
            self.actionTimer -= Globs.dt

        if self.state == 'moving' and self.stunTimer <= 0:
            if self.direction == 1:
                self.spd -= self.acc * Globs.dt
            else:
                self.spd += self.acc * Globs.dt
            if self.hitbox.colliderect(curLevel.player.hitbox):
                self.state = 'attacking'
                self.actionTimer = 0
        else:
            self.spd = 0

    def friction(self):
        # Set Friction
        friction = 0.5 * Globs.dt
        if self.onGround:
            friction = 2 * Globs.dt

        # Apply Friction
        if self.spd > friction:
            self.spd -= friction * self.acc
        elif self.spd < -friction:
            self.spd += friction * self.acc
        else:
            self.spd = 0

    def updateHurtbox(self):
        if self.direction == 1:
            self.hurtbox = pygame.Rect(self.pos.x - self.hurtboxOffset.x, self.pos.y - self.hurtboxOffset.y,
                                       self.hurtboxSize.x, self.hurtboxSize.y)
        elif self.direction == 2:
            self.hurtbox = pygame.Rect(self.pos.x + self.size.x - self.hurtboxOffset.x,
                                       self.pos.y - self.hurtboxOffset.y, self.hurtboxSize.x, self.hurtboxSize.y)

    def takeDamage(self, player):
        if player.state == 'attacking' and self.state != 'defending':
            if self.hitbox.colliderect(player.hurtbox):
                self.lives -= self.weakness
                self.iFrames = self.setIFrames
                self.stunTimer = self.setStunTimer
                self.state = 'defending'

                if player.pos.x < self.pos.x:
                    self.deltaPos.x += 15
                else:
                    self.deltaPos.x -= 15
                if not player.pos.y < self.pos.y:
                    self.deltaPos.y -= 15
        elif player.state == 'defending':
            if self.hitbox.colliderect(player.hurtbox):
                self.stunTimer = self.setStunTimer

    def collision(self, curLevel, deltaPos, tileSet=None):
        damage = False
        platformsList = curLevel.tilemap.collisionTiles

        camOffset = curLevel.camera.offset

        # Horizontal Collision
        testHitbox = pygame.Rect(self.pos.x + deltaPos.x, self.pos.y, self.size.x, self.size.y)
        for platform in platformsList:
            if abs((Vector(platform.x, platform.y) - self.pos).x) < 100:
                if testHitbox.colliderect(platform):
                    self.spd = 0

                    # Directional
                    if self.pos.x > platform.x:
                        deltaPos.x = platform.x - self.pos.x + platform.w
                        if damage:
                            deltaPos.x += 10
                    else:
                        deltaPos.x = platform.x - self.pos.x - self.size.x
                        if damage:
                            deltaPos.x -= 10

                    # Damage
                    if damage and self.iFrames <= 0:
                        self.lives -= self.weakness
                        self.iFrames = self.setIFrames

        # Vertical Collision
        testHitbox = pygame.Rect(self.pos.x, self.pos.y + deltaPos.y, self.size.x, self.size.y)
        for platform in platformsList:
            if abs((Vector(platform.x, platform.y) - self.pos).y) < 100:
                if testHitbox.colliderect(platform):
                    self.YSpd = 0

                    # Directional
                    if self.pos.y < platform.y:
                        deltaPos.y = platform.y - self.pos.y - self.size.y
                        self.onGround = True
                        if damage:
                            deltaPos.y -= 10
                    else:
                        deltaPos.y = platform.y - self.pos.y + self.size.y
                        self.onGround = False
                        if damage:
                            deltaPos.y += 10

                    # Damage
                    if damage and self.iFrames <= 0:
                        self.lives -= self.weakness
                        self.iFrames = self.setIFrames

    def render(self, surface, camOffset):
        if self.state == 'attacking':
            pygame.draw.rect(surface, white, [self.hurtbox.x + camOffset.x, self.hurtbox.y + camOffset.y,
                                              self.hurtbox.w, self.hurtbox.h], 2)

        tmp = pygame.Rect(self.pos.x + camOffset.x, self.pos.y + camOffset.y, self.size.x, self.size.y)
        color = orange
        if self.iFrames > 0:
            color = white
        pygame.draw.rect(surface, color, tmp, 0)

        if Globs.DEBUG_VISUALS:
            pygame.draw.circle(surface, white, self.pos + camOffset, 2, 0)
            pygame.draw.rect(surface, red, [self.hurtbox.x + camOffset.x, self.hurtbox.y + camOffset.y, self.hurtbox.w,
                                            self.hurtbox.h], 2)
