import pygame
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
        #Handles collision
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

SCREEN_SIZE = [1280, 720]
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
allSprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
player = Player()
allSprites.add(player)
wall = Wall(100, 100, 600, 100)
walls.add(wall)
allSprites.add(wall)
running = True

while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
    screen.fill((0, 0, 0))
    allSprites.update()
    for sprite in allSprites:
        screen.blit(sprite.image, sprite.rect)
    pygame.display.update()
    clock.tick(120)