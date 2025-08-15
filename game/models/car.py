
import pygame
from game.config.constants import CAR_HEIGHT, CAR_SPEED, CAR_WIDTH, HEIGHT, LANE_WIDTH


class Car:
    def __init__(self, lane):
        self.x = lane * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2
        self.y = -CAR_HEIGHT
        self.speed = CAR_SPEED
        # Load car sprite from assets
        try:
            self.sprite = pygame.image.load("assets/car.png")
            self.sprite = pygame.transform.scale(self.sprite, (CAR_WIDTH, CAR_HEIGHT))
        except Exception:
            self.sprite = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
            self.sprite.fill((255, 0, 0))

    def move(self):
        self.y += self.speed

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def is_on_screen(self):
        return self.y <  HEIGHT
