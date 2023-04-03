import pygame
pygame.init()

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Player:
    def __init__(self):
        self.x, self.y = SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2#X and Y positions that don't get rounded NOTE: THESE ARE THE TOP LEFT COORDINATES OF THE SURFACE
        self.SIZE = 40
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.Surface((self.SIZE, self.SIZE))
        self.sprite.image.fill((255, 0, 0))
        self.sprite.rect = self.sprite.image.get_rect()
        self.velocity = Vector2(0, 0)
        self.ACCELERATION = 1.5
        self.MAX_SPEED = 7
        self.DECELERATION = 1
    def update(self):
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
        #Increases the player's position by the velocity
        self.x += self.velocity.x
        self.y += self.velocity.y
        #Updates the sprite's position
        self.sprite.rect.x = self.x
        self.sprite.rect.y = self.y

SCREEN_SIZE = [800, 600]
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
player = Player()
running = True

while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
    screen.fill((0, 0, 0))
    player.update()
    screen.blit(player.sprite.image, player.sprite.rect)
    pygame.display.update()
    clock.tick(120)