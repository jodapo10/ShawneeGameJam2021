import pygame
from random import randint
from SimpleVector import Vector
from Globals import *


class Enemy:
    def __init__(self, positionVector):
        self.pos = Vector(positionVector)
        self.size = Vector(Globs.TILE_SIZE, Globs.TILE_SIZE)
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

        self.state = 'idle'
        self.form = 'sword'

        self.spd = 0
        self.acc = 10 * Globs.dt
        self.maxSpd = 5
        self.YSpd = 0
        self.YAcc = Globs.GRAVITY * Globs.dt
        self.maxYSpd = Globs.GRAVITY_MAX
        self.deltaPos = Vector(int(self.spd), int(self.YSpd))
        self.onGround = False

        # Hurtbox
        self.direction = 1
        self.hurtboxOffset = Vector(30, 10)
        self.hurtboxSize = Vector(60, 70)
        self.hurtbox = None
        self.updateHurtbox()

        # Attack
        self.attackCooldown = 0
        self.attackFrame = 0
        self.setAttackFrame = 30
        self.setAttackCooldown = 0.4
        self.attackingThisFrame = False

        # Timers
        self.actionTimer = 0
        self.setActionTimer = 5
        self.stunTimer = 0
        self.setStunTimer = 80

        # Animation
        self.frame = 1
        self.currentAnimation = None
        self.image = None

        # Health
        self.lives = 4
        self.maxLives = 4
        self.weakness = 1
        self.iFrames = 0
        self.setIFrames = 5
        self.dead = False

    def updateHurtbox(self):
        if self.direction == 1:
            self.hurtbox = pygame.Rect(self.pos.x - self.hurtboxOffset.x, self.pos.y - self.hurtboxOffset.y,
                                       self.hurtboxSize.x, self.hurtboxSize.y)
        elif self.direction == 2:
            self.hurtbox = pygame.Rect(self.pos.x + self.size.x - self.hurtboxOffset.x,
                                       self.pos.y - self.hurtboxOffset.y, self.hurtboxSize.x, self.hurtboxSize.y)

    def makeChoice(self, forceChoice=None):
        if self.actionTimer <= 0:
            self.setActionTimer = randint(180, 270) * Globs.dt
            self.actionTimer += self.setActionTimer
            if forceChoice is not None:
                choiceNum = forceChoice
            else:
                choiceNum = randint(1, 3)

            if Globs.DEBUG_VISUALS:
                print('Enemy choice is: ' + str(choiceNum))

            if choiceNum == 1:
                # Move
                self.state = 'moving'
            elif choiceNum == 2:
                # Shield
                self.form = 'sword'
                self.state = 'attacking'
            elif choiceNum == 3:
                # Sword
                self.form = 'shield'
                self.state = 'defending'
        else:
            self.actionTimer -= Globs.dt

    def update(self, curLevel):
        if abs((curLevel.player.pos - self.pos).x) <= Globs.WINDOW_SIZE[0] and abs(
                (curLevel.player.pos - self.pos).y) <= Globs.WINDOW_SIZE[1]:

            self.makeChoice()

            # Direction
            if curLevel.player.pos.x <= self.pos.x:
                self.direction = 1
            elif curLevel.player.pos.x >= self.pos.x + self.size.x:
                self.direction = 2

            # Gravity
            if not self.onGround:
                self.YSpd += self.YAcc
    
            # Set Default Values
            self.onGround = False
            self.attackingThisFrame = False

            if self.spd > self.maxSpd:
                self.spd = self.maxSpd

            # Test New Position --
            self.deltaPos = Vector(int(self.spd), int(self.YSpd))

            # Timers
            if self.stunTimer > 0:
                self.stunTimer -= 60 * Globs.dt

            # Damage
            self.takeDamage(curLevel.player)
            if self.iFrames > 0:
                self.iFrames -= 10 * Globs.dt
            if self.lives <= 0:
                self.dead = True

            # Update States
            if self.state == 'moving' and self.stunTimer <= 0:
                if self.direction == 1:
                    self.spd -= self.acc
                else:
                    self.spd += self.acc
            else:
                self.spd = 0

            # Collision
            self.collision(curLevel, self.deltaPos)

            # Set Position
            self.pos += self.deltaPos
            self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
            self.updateHurtbox()

    def takeDamage(self, player):
        if player.state == 'attacking':
            if self.hitbox.colliderect(player.hurtbox):
                if self.state != 'defending':
                    self.lives -= self.weakness
                    self.iFrames = self.setIFrames
                    self.stunTimer = self.setStunTimer
                    self.form = 'shield'
                    self.state = 'defending'

                if player.pos.x < self.pos.x:
                    self.deltaPos.x += 15
                else:
                    self.deltaPos.x -= 15
                if not player.pos.y < self.pos.y:
                    self.deltaPos.y -= 15
        elif player.state == 'defending':
            if self.hitbox.colliderect(player.hurtbox) or self.hurtbox.colliderect(player.hitbox):
                self.stunTimer = self.setStunTimer
                if player.pos.x > self.pos.x:
                    self.deltaPos.x -= 15
                else:
                    self.deltaPos.x += 15
                self.form = 'shield'
                self.state = 'defending'

    def collision(self, curLevel, deltaPos):
        platformsList = curLevel.tilemap.collisionTiles
        player = curLevel.player

        camOffset = curLevel.camera.offset

        # Horizontal Collision
        testHitbox = pygame.Rect(self.pos.x + deltaPos.x, self.pos.y, self.size.x, self.size.y)
        for platform in platformsList:
            if testHitbox.colliderect(platform):
                self.spd = 0

                # Directional
                if self.pos.x > platform.x:
                    deltaPos.x = platform.x - self.pos.x + platform.w
                else:
                    deltaPos.x = platform.x - self.pos.x - self.size.x

        if testHitbox.colliderect(player.hitbox) and self.state != 'defending':
            self.actionTimer = 0
            self.makeChoice(2)

        # Vertical Collision
        testHitbox = pygame.Rect(self.pos.x, self.pos.y + deltaPos.y, self.size.x, self.size.y)
        for platform in platformsList:
            if testHitbox.colliderect(platform):
                self.YSpd = 0

                # Directional
                if self.pos.y < platform.y:
                    deltaPos.y = platform.y - self.pos.y - self.size.y
                    self.onGround = True

                else:
                    deltaPos.y = platform.y - self.pos.y + self.size.y
                    self.onGround = False

    def animate(self):
        pass

    def render(self, surface, camOffset):
        if self.state == 'attacking':
            pygame.draw.rect(surface, white, [self.hurtbox.x + camOffset.x, self.hurtbox.y + camOffset.y,
                                              self.hurtbox.w, self.hurtbox.h], 2)

        tmp = pygame.Rect(self.pos.x + camOffset.x, self.pos.y + camOffset.y, self.size.x, self.size.y)
        color = orange
        if self.iFrames > 0:
            color = white
        pygame.draw.rect(surface, color, tmp, 0)

        self.renderDebug(surface, camOffset)

    def renderDebug(self, surface, camOffset):
        if Globs.DEBUG_VISUALS:
            pygame.draw.circle(surface, white, self.pos + camOffset, 2, 0)
            pygame.draw.rect(surface, red, [self.hurtbox.x + camOffset.x, self.hurtbox.y + camOffset.y, self.hurtbox.w,
                                            self.hurtbox.h], 2)

            tmp = pygame.Rect(self.pos.x + camOffset.x, self.pos.y + camOffset.y, self.size.x, self.size.y)
            color = purple
            if self.iFrames > 0:
                color = white
            pygame.draw.rect(surface, color, tmp, 0)


class SoldierEnemy(Enemy):

    ShieldDefendingAnimation = {1: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/EnemyKnight/shielfDefend.png"), (144, 72))}
    ShieldWalkingAnimation = {1: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/EnemyKnight/shieldWalking_1.png"), (144, 72)),
                              2: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/EnemyKnight/shieldWalking_2.png"), (144, 72)),
                              3: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/EnemyKnight/shieldWalking_3.png"), (144, 72)),
                              4: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/EnemyKnight/shieldWalking_4.png"), (144, 72))}
    SwordWalkingAnimation = {1: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/EnemyKnight/swordWalking_1.png"), (144, 72)),
                             2: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/EnemyKnight/swordWalking_2.png"), (144, 72)),
                             3: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/EnemyKnight/swordWalking_3.png"), (144, 72)),
                             4: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/EnemyKnight/swordWalking_4.png"), (144, 72))}
    SwordAttackAnimation = {1: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/EnemyKnight/swordAttack_1.png"), (144, 72)),
                            2: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/EnemyKnight/swordAttack_2.png"), (144, 72)),
                            3: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/EnemyKnight/swordAttack_3.png"), (144, 72))}

    def __init__(self, positionVector):
        super().__init__(positionVector)

        self.size = Vector(48, 72)
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

        # New Hurtbox
        self.hurtboxOffset = Vector(30, 10)
        self.hurtboxSize = Vector(60, 70)
        self.updateHurtbox()

        # New Animation
        self.image = SoldierEnemy.ShieldDefendingAnimation[1]
        self.currentAnimation = None

        # Health
        self.lives = 4
        self.weakness = 1

    def update(self, curLevel):
        super(SoldierEnemy, self).update(curLevel)
        if self.state == 'moving':
            self.form = 'sword'
        self.animate()

    def animate(self):

        if self.state == 'defending':
            self.currentAnimation = SoldierEnemy.ShieldDefendingAnimation
        elif self.form == 'shield':
            self.currentAnimation = SoldierEnemy.ShieldWalkingAnimation
        elif self.form == 'sword':
            self.currentAnimation = SoldierEnemy.SwordWalkingAnimation

        self.frame += 6 * Globs.dt
        if self.frame >= len(self.currentAnimation) + 1:
            self.frame = 1
        self.image = self.currentAnimation[int(self.frame)]

        if self.state == 'attacking' or self.attackFrame > 0:
            self.currentAnimation = SoldierEnemy.SwordAttackAnimation
            self.image = self.currentAnimation[int(min(self.frame, 3))]

    def render(self, surface, camOffset):
        if self.state == 'attacking' and Globs.DEBUG_VISUALS:
            pygame.draw.rect(surface, white, [self.hurtbox.x + camOffset.x, self.hurtbox.y + camOffset.y,
                                              self.hurtbox.w, self.hurtbox.h], 2)

        # Blit
        if self.direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)
            surface.blit(self.image, (self.pos + camOffset - Vector(24, 0)).i, [72, 0, 72, self.size.y])
        else:
            surface.blit(self.image, (self.pos + camOffset).i, [0, 0, 72, self.size.y])

        # HP
        if self.lives < self.maxLives:
            pygame.draw.rect(surface, grey, (self.pos.x + camOffset.x, self.pos.y - 20 + camOffset.y, self.size.x, 10), 0)
            pygame.draw.rect(surface, white, [self.pos.x + camOffset.x, self.pos.y - 20 + camOffset.y,
                                              int(self.lives / self.maxLives * self.size.x), 10], 0)

        self.renderDebug(surface, camOffset)
