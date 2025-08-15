import random
from typing import List
import pygame
import sys
from ai.agent import RandomAgent
from game.config.constants import CAR_HEIGHT, CAR_WIDTH, LANE_COUNT, PLAYER_HEIGHT, PLAYER_WIDTH, SPAWN_INTERVAL, WIDTH, HEIGHT,WHITE
from game.models.car import Car
from game.models.directions import Directions
from game.models.player import Player


def extract_game_state(cars,player) -> List[float]:
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

def main(action_getter):
    pygame.init()

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Infinite Car Dodge")

    clock = pygame.time.Clock()

    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL)

    cars:List[Car] = []
    player:Player = Player()
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

            # Removed space-to-continue and restart logic

        if not game_over:
            action = action_getter(cars,player)
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
                    running = False
                    survived_time = (pygame.time.get_ticks() - start_ticks) // 1000
                    pygame.quit()
                    return survived_time

        WIN.fill(WHITE)
        for car in cars:
            car.move()
            car.draw(WIN)

        print(extract_game_state(cars,player))
        # Draw lines from player to each car
        player_center = (player.x + PLAYER_WIDTH // 2, player.y + PLAYER_HEIGHT // 2)
        for car in cars:
            car_center = (car.x + CAR_WIDTH // 2, car.y + CAR_HEIGHT // 2)
            pygame.draw.line(WIN, (0, 255, 0), player_center, car_center, 2)
        player.draw(WIN)
    # Removed game over label and restart prompt since game closes immediately
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def get_human_action(cars,player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        return "right"
    elif keys[pygame.K_LEFT]:
        return "left"
    return "stay"

def get_ai_action(cars,player):
    agent = RandomAgent()
    return agent.act(extract_game_state(cars,player))


if __name__ == "__main__":
    main(get_ai_action)
