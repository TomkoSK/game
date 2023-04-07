import pygame
import random
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
        self.MAX_SPEED = 5
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
        if(abs(self.velocity.x) > self.MAX_SPEED):
            if(self.velocity.x > 0):
                self.velocity.x = self.MAX_SPEED
            elif(self.velocity.x < 0):
                self.velocity.x = -self.MAX_SPEED
        if(abs(self.velocity.y) > self.MAX_SPEED):
            if(self.velocity.y > 0):
                self.velocity.y = self.MAX_SPEED
            elif(self.velocity.y < 0):
                self.velocity.y = -self.MAX_SPEED
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

def updateScreen():
    screen.fill((0, 0, 0))
    offsets = getCameraOffsets()
    for sprite in allSprites:
        screen.blit(sprite.image, (sprite.rect.x+offsets[0], sprite.rect.y+offsets[1]+offsets[2]))
    pygame.display.flip()

def getCameraOffsets():#These offsets are the offsets that are added to the rect value when drawing sprites on screen to make it look like a camera follows the player around
    #Gets the offset based on cursor position
    cursorOffsetY = (CENTER[1]-pygame.mouse.get_pos()[1])/3
    cursorOffsetX = (CENTER[0]-pygame.mouse.get_pos()[0])/9
    #Gets the camera offset on the Y axis based on player's position
    offsetY = CENTER[1]-player.rect.y
    return [cursorOffsetX, cursorOffsetY, offsetY]

SCREEN_SIZE = [900, 720]
CENTER = [SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2]
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
allSprites = pygame.sprite.Group()
walls = pygame.sprite.Group()

player = Player()
allSprites.add(player)
sideWalls = [Wall(SCREEN_SIZE[0]-50, -SCREEN_SIZE[1]/2, 500, SCREEN_SIZE[1]*2), Wall(-450, -SCREEN_SIZE[1]/2, 500, SCREEN_SIZE[1]*2)]#NOTE: *1.2 is just a magic number, the wall is a bit longer than the screen so the player can't see the end of it
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
    #Moves the side walls so the player cannot go over them
    for wall in sideWalls:
        wall.setY(player.rect.y - SCREEN_SIZE[1]/2*2)#NOTE: *1.2 is just a magic number, the wall is a bit longer than the screen so the player can't see the end of it
    allSprites.update()
    updateScreen()
    clock.tick(120)