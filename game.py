import random
from typing import List
import pygame
import sys
from game.config.constants import CAR_HEIGHT, CAR_WIDTH, LANE_COUNT, PLAYER_HEIGHT, PLAYER_WIDTH, SPAWN_INTERVAL, WIDTH, HEIGHT,WHITE
from game.models.car import Car
from game.models.directions import Directions
from game.models.player import Player

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infinite Car Dodge")

clock = pygame.time.Clock()

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL)

cars:List[Car] = []
player:Player = Player()

def extract_game_state() -> List[float]:
    lst = []
    sorted_cars = sorted(cars, key=lambda c: c.y)
    for i in range(LANE_COUNT):
        if i < len(sorted_cars):
            lst.append(sorted_cars[i].x)
            lst.append(sorted_cars[i].y)
        else:
            lst.append(-1)
            lst.append(-1)
    lst.append(player.x)
    lst.append(player.y)
    return lst

def main():
    global cars,player
    print("Game starting…")
    running = True
    game_over = False
    CAR_SPAWN_PROB = 0.6
    start_ticks = pygame.time.get_ticks()
    survived_time = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over and event.type == SPAWN_EVENT:
                cars = list(filter(lambda c: c.is_on_screen(), cars))
                empty_lane = random.randint(0, LANE_COUNT - 1)
                for lane in range(LANE_COUNT):
                    if lane == empty_lane:
                        continue  # leave this lane empty
                    if random.random() < CAR_SPAWN_PROB:
                        cars.append(Car(lane))

            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Restart game state
                cars = []
                player = Player()
                game_over = False
                start_ticks = pygame.time.get_ticks()
                survived_time = 0

        if not game_over:
            action = get_human_action()
            if action=='right':
                player.move(Directions.RIGHT)
            elif action=='left':
                player.move(Directions.LEFT)

        # Game over logic
        if not game_over:
            for car in cars:
                RELAXED_LOWER_BOUND = 4
                if (car.y + CAR_HEIGHT > HEIGHT - PLAYER_HEIGHT and car.y + CAR_HEIGHT - HEIGHT < RELAXED_LOWER_BOUND) and car.x < player.x + PLAYER_WIDTH and car.x + CAR_WIDTH > player.x:
                    print("Game Over")
                    game_over = True
                    survived_time = (pygame.time.get_ticks() - start_ticks) // 1000

        WIN.fill(WHITE)
        for car in cars:
            car.move()
            car.draw(WIN)

        print(extract_game_state())
        # Draw lines from player to each car
        player_center = (player.x + PLAYER_WIDTH // 2, player.y + PLAYER_HEIGHT // 2)
        for car in cars:
            car_center = (car.x + CAR_WIDTH // 2, car.y + CAR_HEIGHT // 2)
            pygame.draw.line(WIN, (0, 255, 0), player_center, car_center, 2)
        player.draw(WIN)
        if game_over:
            font = pygame.font.SysFont(None, 60)
            text = font.render("GAME OVER", True, (255, 0, 0))
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            font_small = pygame.font.SysFont(None, 40)
            time_text = font_small.render(f"Time Survived: {survived_time} s", True, (0, 0, 0))
            WIN.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2 + text.get_height() // 2 + 10))
            time_text = font_small.render("Press space to continue", True, (0, 0, 0))
            WIN.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2 + text.get_height() // 2 + 30))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

def get_human_action():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        return "right"
    elif keys[pygame.K_LEFT]:
        return "left"
    return "stay"


if __name__ == "__main__":
    main()
