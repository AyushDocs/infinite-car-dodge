from game.config.constants import CAR_HEIGHT, CAR_WIDTH, WIDTH,HEIGHT,PLAYER_HEIGHT,PLAYER_SPEED,PLAYER_WIDTH
import pygame

from game.models.directions import Directions



class Player:
    def __init__(self):
        self.x = WIDTH // 2 - PLAYER_WIDTH // 2 # center se thoda left
        self.y = HEIGHT - PLAYER_HEIGHT - 10 # 10 units above center top left corner of player
        self.speed = PLAYER_SPEED
        # Load placeholder sprite
        try:
            self.sprite = pygame.image.load("assets/player.png")
            self.sprite = pygame.transform.scale(self.sprite, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.sprite.set_colorkey((255,255,255))  # Set black as transparent color
        except Exception:
            self.sprite = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            self.sprite.fill((255, 0, 0))

    def move(self, direction:Directions):
        ##  <--
        if direction == Directions.LEFT and self.x - self.speed >= 0:
            self.x -= self.speed
        ## -->
        elif direction == Directions.RIGHT and self.x + self.speed + PLAYER_WIDTH <= WIDTH:
            self.x += self.speed

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))
	