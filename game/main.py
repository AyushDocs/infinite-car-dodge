import pygame
import sys
from game.config.constants import WIDTH, HEIGHT,WHITE

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infinite Car Dodge")

clock = pygame.time.Clock()

def main():
    print("Game starting…")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        WIN.fill(WHITE)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
