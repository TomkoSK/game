import pygame
import random
import math
import time
pygame.init()

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class Player(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.x, self.y = SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2#X and Y positions that don't get rounded NOTE: THESE ARE THE TOP LEFT COORDINATES OF THE PLAYER RECT
        self.lastFrameX, self.lastFrameY = 0, 0
        self.SIZE = 40
        self.image = pygame.Surface((self.SIZE, self.SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.velocity = Vector2(0, 0)
        self.ACCELERATION = 1.5
        self.maxSpeed = 4
        self.DECELERATION = 1
    def move(self):
        keys = pygame.key.get_pressed()
        #Decelerates or sets velocity to 0 if the velocity is less than the deceleration value
        if(abs(self.velocity.x) < self.DECELERATION):
            self.velocity.x = 0
        else:#Decreases the deceleration if it's higher than 0
            if(self.velocity.x > 0):
                self.velocity.x -= self.DECELERATION
            elif(self.velocity.x < 0):
                self.velocity.x += self.DECELERATION
        if(abs(self.velocity.y) < self.DECELERATION):
            self.velocity.y = 0
        else:
            if(self.velocity.y > 0):
                self.velocity.y -= self.DECELERATION
            elif(self.velocity.y < 0):
                self.velocity.y += self.DECELERATION
        #Accelerates based on input
        if(keys[pygame.K_a]):
            self.velocity.x -= self.ACCELERATION
        if(keys[pygame.K_d]):
            self.velocity.x += self.ACCELERATION
        if(keys[pygame.K_s]):
            self.velocity.y += self.ACCELERATION
        if(keys[pygame.K_w]):
            self.velocity.y -= self.ACCELERATION
        #Decreases the player's velocity if it's above the max
        if(abs(self.velocity.x) > self.maxSpeed):
            if(self.velocity.x > 0):
                self.velocity.x = self.maxSpeed
            elif(self.velocity.x < 0):
                self.velocity.x = -self.maxSpeed
        if(abs(self.velocity.y) > self.maxSpeed):
            if(self.velocity.y > 0):
                self.velocity.y = self.maxSpeed
            elif(self.velocity.y < 0):
                self.velocity.y = -self.maxSpeed
        #Detects collision
        collideRectX = self.rect.copy()
        #Simulates moving the rectangle by the velocity, if it crashes into a wall the velocity is decreased to stop at the wall
        collideRectX.x += self.velocity.x
        for sprite in walls:
            if(collideRectX.colliderect(sprite.rect)):
                if(self.velocity.x > 0):
                    self.velocity.x = sprite.rect.left - self.rect.right
                elif(self.velocity.x < 0):
                    self.velocity.x = sprite.rect.right - self.rect.left
        collideRectY = self.rect.copy()
        #Same thing but for the Y axis
        collideRectY.y += self.velocity.y
        for sprite in walls:
            if(collideRectY.colliderect(sprite.rect)):
                if(self.velocity.y > 0):
                    self.velocity.y = sprite.rect.top - self.rect.bottom
                elif(self.velocity.y < 0):
                    self.velocity.y = sprite.rect.bottom - self.rect.top
        #Increases the player's position by the velocity
        self.x += self.velocity.x
        self.y += self.velocity.y
        #Updates the sprite's position
        self.rect.x = self.x
        self.rect.y = self.y
    def update(self):
        self.move()

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, xSize, ySize):
        super().__init__()
        self.image = pygame.Surface((xSize, ySize))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y  
    def setY(self, y):
        self.rect.y = y

class StaminaBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.length = 380
        self.height = 30
        self.image = pygame.Surface((self.length, self.height))
        self.edgeColor = (100,100,100)
        self.edgeWidth = 3
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_SIZE[0]-390
        self.rect.y = 10
        self.value = 380
    def setValue(self, value):
        self.rect.value = value
    def update(self):
        self.image.fill((255,0,0))
        pygame.draw.rect(self.image, (0,255,0), (0, 0, self.value, self.height))
        pygame.draw.rect(self.image, self.edgeColor, (0, 0, self.length, self.edgeWidth))
        pygame.draw.rect(self.image, self.edgeColor, (0, self.height-self.edgeWidth, 480, self.edgeWidth))
        pygame.draw.rect(self.image, self.edgeColor, (0, 0, self.edgeWidth, self.height))
        pygame.draw.rect(self.image, self.edgeColor, (self.length-self.edgeWidth, 0, self.edgeWidth, self.height))

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.birthTime = time.time()
        self.speed = 15
        self.size = 20
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.x, self.y = player.rect.center[0], player.rect.center[1]#Urounded x and y for accuracy with decimals
        self.rect.center = (self.x, self.y)
        mousePos = pygame.mouse.get_pos()
        offsets = getCameraOffsets()
        playerPosOnScreen = (player.rect.center[0]+offsets[0], player.rect.center[1]+offsets[1]+offsets[2])
        angle = math.atan2(mousePos[1] - playerPosOnScreen[1], mousePos[0] - playerPosOnScreen[0])
        self.velocity = Vector2(math.cos(angle)*self.speed, math.sin(angle)*self.speed)
    def update(self):
        if(time.time()-self.birthTime > 3):#If the bullet somehow exists for more than 3 seconds it disappears
            self.kill()
        for sprite in walls:#If bullet collides with wall it disappears
            if(self.rect.colliderect(sprite.rect)):
                self.kill()
        self.x += self.velocity.x
        self.y += self.velocity.y
        self.rect.center = (self.x, self.y)

def updateScreen():
    screen.fill((0, 0, 0))
    offsets = getCameraOffsets()
    for sprite in allSprites:
        screen.blit(sprite.image, (sprite.rect.x+offsets[0], sprite.rect.y+offsets[1]+offsets[2]))
    screen.blit(staminaBar.image, staminaBar.rect)
    pygame.display.flip()

def getCameraOffsets():#These offsets are the offsets that are added to the rect value when drawing sprites on screen to make it look like a camera follows the player around
    #Gets the offset based on cursor position
    cursorOffsetY = (CENTER[1]-pygame.mouse.get_pos()[1])/3
    cursorOffsetX = (CENTER[0]-pygame.mouse.get_pos()[0])/9
    #Gets the camera offset on the Y axis based on player's position
    offsetY = CENTER[1]-player.rect.y
    return [cursorOffsetX, cursorOffsetY, offsetY]

screen = pygame.display.set_mode((900, 900))
SCREEN_SIZE = screen.get_size()
CENTER = [SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2]
SHOT_COOLDOWN = 0.3
shootTime = 0
clock = pygame.time.Clock()
allSprites = pygame.sprite.Group()
walls = pygame.sprite.Group()


player = Player()
allSprites.add(player)
staminaBar = StaminaBar()#Stamina bar isn't added to allSprites so its position on the screen isn't moved because of the camera
sideWallsWidth = SCREEN_SIZE[0]-800
sideWalls = [Wall(SCREEN_SIZE[0]-sideWallsWidth/2, -SCREEN_SIZE[1]/2, 1000, SCREEN_SIZE[1]*2), Wall(sideWallsWidth/2-1000, -SCREEN_SIZE[1]/2, 1000, SCREEN_SIZE[1]*2)]#NOTE: *2 is just a magic number, the wall is a bit longer than the screen so the player can't see the end of it
for wall in sideWalls:
    allSprites.add(wall)
    walls.add(wall)
for y in range(0, -450000, -225):
    wall = Wall(random.randint(0, 500), y, random.randint(80, 300), 36)
    walls.add(wall)
    allSprites.add(wall)
running = True

while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        elif(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            if(time.time() - shootTime > SHOT_COOLDOWN):
                shootTime = time.time()
                bullet = Bullet()
                allSprites.add(bullet)
        #Changes max movespeed when shift is pressed and releases
        elif(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_LSHIFT and staminaBar.value > 0):
                player.maxSpeed = 6
        elif(event.type == pygame.KEYUP):
            if(event.key == pygame.K_LSHIFT):
                player.maxSpeed = 4
    #Decreases stamina bar if player is holding shift
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_LSHIFT]):
        if(staminaBar.value - 1.5 > 0):
            staminaBar.value -= 1.5
        else:
            staminaBar.value = 0
            #if stamina bar reaches 0 move speed goes back down
            if(player.maxSpeed == 6):
                player.maxSpeed = 4
    else:
        if(staminaBar.value + 0.7 <= staminaBar.length):
            staminaBar.value += 0.7
        else:
            staminaBar.value = staminaBar.length
    #Moves the side walls so the player cannot go over them
    for wall in sideWalls:
        wall.setY(player.rect.y - SCREEN_SIZE[1]/2*2)#NOTE: *2 is just a magic number, the wall is a bit longer than the screen so the player can't see the end of it
    #Updates all sprites
    allSprites.update()
    staminaBar.update()
    #Updates the screen
    updateScreen()
    clock.tick(120)