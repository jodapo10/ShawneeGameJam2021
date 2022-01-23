import pygame
from SimpleVector import Vector
from Globals import *
from Text import Text


class Player:
    ImageDict = {'Hearts':  pygame.transform.scale(pygame.image.load("Assets/Images/Health.png"), (152, 38)),
                 'Stamina': pygame.transform.scale(pygame.image.load("Assets/Images/StaminaOutline.png"), (160, 60)),
                 'FormSwapTimer': pygame.image.load("Assets/Images/FormSwapBar.png")}

    SwordWalkingAnimation = {1: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/KnightPlayer/sword_1.png"), (192, 96)),
                             2: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/KnightPlayer/sword_2.png"), (192, 96)),
                             3: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/KnightPlayer/sword_3.png"), (192, 96)),
                             4: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/KnightPlayer/sword_4.png"), (192, 96))}
    ShieldWalkingAnimation = {1: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/KnightPlayer/shield_1.png"), (192, 96)),
                              2: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/KnightPlayer/shield_2.png"), (192, 96)),
                              3: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/KnightPlayer/shield_3.png"), (192, 96)),
                              4: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/KnightPlayer/shield_4.png"), (192, 96))}
    SwordAttackAnimation = {1: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/KnightPlayer/swordAttack_1.png"), (192, 96)),
                            2: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/KnightPlayer/swordAttack_2.png"), (192, 96)),
                            3: pygame.transform.scale(pygame.image.load("Assets/Images/Animations/KnightPlayer/swordAttack_3.png"), (192, 96))}
    ShieldDefendingAnimation = {1: pygame.transform.scale(
        pygame.image.load("Assets/Images/Animations/KnightPlayer/shieldDefend.png"), (192, 96))}

    AttackDirectionDict = None

    def __init__(self):
        # Position
        self.pos = Vector(0, 0)
        self.size = Vector(64, 96)
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

        # Control
        self.hasControl = True
        self.state = 'idle'  # 'idle', 'moving', 'falling', etc ...

        # Movement
        self.spd = 0
        self.acc = 50 * Globs.dt
        self.maxSpd = 10
        self.maxSprint = 15
        self.maxSlow = 1
        self.YSpd = 0
        self.YAcc = Globs.GRAVITY * Globs.dt
        self.maxYSpd = Globs.GRAVITY_MAX
        self.jump = -17.5
        self.onGround = False

        self.direction = 2
        self.hurtbox = None
        self.center = Vector(400, 425)

        # Animation
        self.frame = 1
        self.currentAnimation = Player.SwordWalkingAnimation
        self.image = self.currentAnimation[self.frame]

        # Stamina
        self.maxStamina = 300
        self.stamina = self.maxStamina
        self.hasStamina = True
        self.setStaminaDrain = -5 * Globs.dt
        self.staminaDrain = 0

        # Form
        self.form = 'sword'  # 'sword', 'shield'
        self.swapFormTimer = 0
        self.setSwapFormTimer = 5
        self.attackCooldown = 0
        self.attackFrame = 0
        self.setAttackFrame = 30
        self.setAttackCooldown = 60

        # Health
        self.lives = 8
        self.weakness = 2
        self.iFrames = 0
        self.setIFrames = 10

        # Gameplay
        self.inventory = []

    def setPosition(self, x, y):
        self.pos = Vector(x, y)
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def setSpeed(self):
        self.spd = 0
        self.YSpd = 0

    def setAcc(self):
        self.acc = 50 * Globs.dt
        self.YAcc = Globs.GRAVITY * Globs.dt

    def resetValues(self, lives=None, items=None):
        if lives is not None:
            self.lives = lives
        if items is not None:
            self.inventory = items

    def update(self, event, keys, mouse, curLevel):
        if self.hasControl:
            self.setAcc()

            # Input
            if keys[pygame.K_a]:
                self.spd -= self.acc
                if self.state != 'defending':
                    self.state = 'moving'
                self.direction = 2
            if keys[pygame.K_d]:
                self.spd += self.acc
                if self.state != 'defending':
                    self.state = 'moving'
                self.direction = 1
            if keys[pygame.K_SPACE] and self.onGround:
                if int(self.stamina) >= 50:
                    self.staminaDrain += 50
                    self.YSpd += self.jump
                    self.onGround = False
            if keys[pygame.K_LSHIFT] and self.hasStamina:
                if keys[pygame.K_a] or keys[pygame.K_d]:
                    self.state = 'sprinting'
                    if self.onGround:
                        self.spd *= 2
                        self.stamina -= 100 * Globs.dt
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.swapFormTimer <= 0:
                        if self.form == 'sword':
                            self.form = 'shield'
                            self.swapFormTimer = self.setSwapFormTimer
                            self.weakness = 1
                        elif self.form == 'shield':
                            self.form = 'sword'
                            self.swapFormTimer = self.setSwapFormTimer
                            self.weakness = 2
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.form == 'sword':
                    if self.attackCooldown <= 0 and self.hasStamina:
                        self.state = 'attacking'
                        self.attackFrame = self.setAttackFrame
                        self.staminaDrain += 50
                        self.attackCooldown = self.setAttackCooldown
                elif self.form == 'shield':
                    if self.stamina > 0 and self.hasStamina:
                        self.state = 'defending'
            if event.type == pygame.MOUSEBUTTONUP:
                if self.state == 'defending':
                    self.state = 'idle'

        # Gravity
        if not self.onGround:
            self.YSpd += self.YAcc

        # Friction
        if self.state != 'moving' and self.state != 'sprinting':
            if not keys[pygame.K_a] and not keys[pygame.K_d]:
                self.friction()
                self.frame = 1

        # Cap Speeds
        if self.state == 'sprinting':
            spdLimit = self.maxSprint
        elif self.state == 'defending':
            spdLimit = self.maxSlow
        else:
            spdLimit = self.maxSpd
        if self.spd > spdLimit:
            self.spd = spdLimit
        elif self.spd < -spdLimit:
            self.spd = -spdLimit

        # Health
        if self.iFrames > 0:
            self.iFrames -= 10 * Globs.dt
        if self.lives <= 0:
            curLevel.loadMenu('Paused')
            curLevel.textDict[Text('you died', [400, 10])] = [Text.Fonts[50], None]

        self.updateStamina()

        self.updateForm()

        # Set Default Values
        if self.state != 'defending' and self.attackFrame <= 0:
            self.state = 'idle'
        if self.attackFrame > 0:
            self.attackFrame -= 70 * Globs.dt
        self.onGround = False

        self.attackCooldown -= 70 * Globs.dt

        # Test New Position --
        deltaPos = Vector(int(self.spd), int(self.YSpd))

        # Collision
        self.enemyCollision(curLevel, deltaPos)

        self.collision(curLevel, deltaPos, None)
        if self.state != 'defending':
            self.collision(curLevel, deltaPos, 'damage')

        if curLevel.day:
            self.collision(curLevel, deltaPos, 'day')
            if self.state != 'defending':
                self.collision(curLevel, deltaPos, 'dayDamage')
        else:
            self.collision(curLevel, deltaPos, 'night')
            if self.state != 'defending':
                self.collision(curLevel, deltaPos, 'nightDamage')

        # Set Position
        self.pos += deltaPos
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.updateHurtbox()

        # Update Camera
        curLevel.camera.setOffset(deltaPos)

        self.animate()

    def friction(self):
        # Set Friction
        friction = 50 * Globs.dt
        if self.onGround:
            friction = 75 * Globs.dt

        # Apply Friction
        if self.spd > friction:
            self.spd -= friction * self.acc
        elif self.spd < -friction:
            self.spd += friction * self.acc
        else:
            self.spd = 0

    def updateStamina(self):
        # Recharge
        if self.state == 'idle':
            self.stamina += 40 * Globs.dt
        elif self.state == 'defending':
            self.stamina -= 25 * Globs.dt
        elif self.state != 'sprinting':
            self.stamina += 20 * Globs.dt

        if self.state == 'defending' and not self.hasStamina:
            self.state = 'idle'

        # Drain
        if self.staminaDrain > 0:
            self.stamina += self.setStaminaDrain
            self.staminaDrain += self.setStaminaDrain

        # Min / Max
        if self.stamina > self.maxStamina:
            self.stamina = self.maxStamina
            self.hasStamina = True
        if self.stamina < 0:
            self.stamina = 0
            self.hasStamina = False

    def updateForm(self):
        if self.swapFormTimer > 0:
            self.swapFormTimer -= 2 * Globs.dt

    def updateDirection(self, mouse):
        """ Old. Used Mouse Position."""
        mPos = Vector(mouse.get_pos())

        # Check Left
        if mPos.x >= self.center.x:
            self.direction = 1
        else:
            self.direction = 2

    def updateHurtbox(self):
        if self.state == 'defending':
            self.hurtbox = self.hitbox
        else:
            if self.direction == 1:
                self.hurtbox = pygame.Rect(self.pos.x + self.size.x - 20, self.pos.y - 20, 70, 130)
            elif self.direction == 2:
                self.hurtbox = pygame.Rect(self.pos.x - 50, self.pos.y - 20, 70, 130)

    def collision(self, curLevel, deltaPos, tileSet=None):
        damage = False
        platformsList = []

        # Determine Tile Set
        if tileSet is None:
            platformsList = curLevel.tilemap.collisionTiles
        elif tileSet == 'damage':
            damage = True
            platformsList = curLevel.tilemap.damageTiles
        elif tileSet == 'day':
            platformsList = curLevel.tilemap.dayTiles
        elif tileSet == 'dayDamage':
            damage = True
            platformsList = curLevel.tilemap.dayDamageTiles
        elif tileSet == 'night':
            platformsList = curLevel.tilemap.nightTiles
        elif tileSet == 'nightDamage':
            damage = True
            platformsList = curLevel.tilemap.nightDamageTiles

        camOffset = curLevel.camera.offset

        # Horizontal Collision
        for platform in platformsList:
            if -2 * Globs.TILE_SIZE <= platform.x + camOffset.x < Globs.WINDOW_SIZE[0] + (2 * Globs.TILE_SIZE):
                testHitbox = pygame.Rect(self.pos.x + deltaPos.x, self.pos.y, self.size.x, self.size.y)
                if testHitbox.colliderect(platform):
                    self.spd = 0

                    # Directional
                    if self.pos.x > platform.x:
                        deltaPos.x = platform.x - self.pos.x + platform.w
                    else:
                        deltaPos.x = platform.x - self.pos.x - self.size.x

                    # Damage
                    if damage and self.iFrames <= 0:
                        self.lives -= self.weakness
                        self.iFrames = self.setIFrames

        # Vertical Collision
        for platform in platformsList:
            if not self.onGround:
                if -2 * Globs.TILE_SIZE <= platform.y + camOffset.y < Globs.WINDOW_SIZE[1] + (2 * Globs.TILE_SIZE):
                    testHitbox = pygame.Rect(self.pos.x, self.pos.y + deltaPos.y, self.size.x, self.size.y)
                    if testHitbox.colliderect(platform):
                        self.YSpd = 0

                        # Directional
                        if self.pos.y < platform.y:
                            deltaPos.y = platform.y - self.pos.y - self.size.y
                            self.onGround = True
                        else:
                            deltaPos.y = platform.y - self.pos.y + platform.h
                            self.onGround = False

                        # Damage
                        if damage and self.iFrames <= 0:
                            self.lives -= self.weakness
                            self.iFrames = self.setIFrames

    def enemyCollision(self, curLevel, deltaPos):
        camOffset = curLevel.camera.offset

        # Horizontal Collision
        testHitbox = pygame.Rect(self.pos.x + deltaPos.x, self.pos.y, self.size.x, self.size.y)
        for enemy in curLevel.enemiesList:
            if -2 * Globs.TILE_SIZE <= enemy.pos.x + camOffset.x < Globs.WINDOW_SIZE[0] + (2 * Globs.TILE_SIZE):
                if enemy.state == 'attacking':
                    if testHitbox.colliderect(enemy.hurtbox):
                        self.spd = 0
    
                        # Directional
                        if self.pos.x > enemy.hurtbox.x:
                            deltaPos.x = enemy.hurtbox.x - self.pos.x + enemy.hurtbox.w
                            deltaPos.x += 10
                        else:
                            deltaPos.x = enemy.hurtbox.x - self.pos.x - self.size.x
                            deltaPos.x -= 10

                        # Damage
                        if self.iFrames <= 0 and self.state != 'defending':
                            self.lives -= self.weakness
                            self.iFrames = self.setIFrames
                        elif self.state == 'defending':
                            self.staminaDrain += 1

        # Vertical Collision
        testHitbox = pygame.Rect(self.pos.x, self.pos.y + deltaPos.y, self.size.x, self.size.y)
        for enemy in curLevel.enemiesList:
            if -2 * Globs.TILE_SIZE <= enemy.pos.y + camOffset.y < Globs.WINDOW_SIZE[1] + (2 * Globs.TILE_SIZE):
                if enemy.state == 'attacking':
                    if testHitbox.colliderect(enemy.hurtbox):
                        self.YSpd = 0

                        ''''# Directional
                        if self.pos.y < tmpRect.y:
                            deltaPos.y = tmpRect.y - self.pos.y - tmpRect.h
                            deltaPos.y -= 10
                        else:
                            deltaPos.y = tmpRect.y - self.pos.y + self.size.y'''

                        # Damage
                        if self.iFrames <= 0 and self.state != 'defending':
                            self.lives -= self.weakness
                            self.iFrames = self.setIFrames
                        elif self.state == 'defending':
                            self.staminaDrain += 1

    def animate(self):
        if self.form == 'shield':
            if self.state == 'defending':
                self.currentAnimation = Player.ShieldDefendingAnimation
            else:
                self.currentAnimation = Player.ShieldWalkingAnimation
        elif self.form == 'sword':
            self.currentAnimation = Player.SwordWalkingAnimation

        self.frame += 6 * Globs.dt
        if self.frame >= len(self.currentAnimation) + 1:
            self.frame = 1
        self.image = self.currentAnimation[int(self.frame)]

        if self.state == 'attacking' or self.attackFrame > 0:
            self.currentAnimation = Player.SwordAttackAnimation
            self.image = self.currentAnimation[min(4 - int(self.attackFrame // 10), 3)]

    def render(self, surface, camOffset, timeIsDay=False):
        # Blit
        if self.direction == 2:
            self.image = pygame.transform.flip(self.image, True, False)
            surface.blit(self.image, (self.pos + camOffset - Vector(32, 0)).i, [96, 0, 96, self.size.y])
        else:
            surface.blit(self.image, (self.pos + camOffset).i, [0, 0, 96, self.size.y])

        # Hearts
        for i in range(self.lives):
            heartPos = i % 2
            if self.form == 'sword':
                if heartPos == 0:
                    surface.blit(Player.ImageDict['Hearts'], (10 + (i // 2) * 40, 10), (38, 0, 38, 38))
                else:
                    surface.blit(Player.ImageDict['Hearts'], (10 + (i // 2) * 40, 10), (0, 0, 38, 38))
            else:
                if heartPos == 0:
                    surface.blit(Player.ImageDict['Hearts'], (10 + (i // 2) * 40, 10), (114, 0, 38, 38))
                else:
                    surface.blit(Player.ImageDict['Hearts'], (10 + (i // 2) * 40, 10), (76, 0, 38, 38))

        # Stamina
        pygame.draw.rect(surface, grey, [15, 65, 150, 20], 0)
        pygame.draw.rect(surface, white, [15, 65, int(self.stamina / self.maxStamina * 150), 20], 0)
        if self.form == 'sword':
            if self.hasStamina:
                surface.blit(Player.ImageDict['Stamina'], (10, 60), (0, 0, 160, 30))
            else:
                surface.blit(Player.ImageDict['Stamina'], (10, 60), (0, 30, 160, 30))
        else:
            if self.hasStamina:
                surface.blit(Player.ImageDict['Stamina'], (10, 60), (0, 30, 160, 30))
            else:
                surface.blit(Player.ImageDict['Stamina'], (10, 60), (0, 0, 160, 30))

        # Form Swap
        pygame.draw.rect(surface, grey, [15, 100, 145, 35], 0)
        pygame.draw.rect(surface, white, [15, 100, 145 - int(self.swapFormTimer / self.setSwapFormTimer * 145), 35], 0)
        if self.form == 'sword':
            surface.blit(Player.ImageDict['FormSwapTimer'], (15, 100), (0, 0, 145, 35))
            text = Text('e: shield', (19, 110))
            text.render(surface)
        else:
            surface.blit(Player.ImageDict['FormSwapTimer'], (15, 100), (0, 35, 145, 35))
            text = Text('e: sword', (20, 110))
            text.render(surface)

        if Globs.DEBUG_VISUALS:
            # Hitbox
            tmp = pygame.Rect(self.pos.x + camOffset.x, self.pos.y + camOffset.y, self.size.x, self.size.y)
            color = black
            if self.form == 'sword':
                color = red
            elif self.form == 'shield':
                color = purple
            if self.iFrames > 0:
                color = white
            pygame.draw.rect(surface, color, tmp, 1)

            # Hurtbox
            pygame.draw.circle(surface, white, self.center.i, 3, 0)
            pygame.draw.rect(surface, red, [self.hurtbox.x + camOffset.x, self.hurtbox.y + camOffset.y, self.hurtbox.w,
                                            self.hurtbox.h], 2)

        if Globs.DEBUG_TEXT:
            print(self.pos)
