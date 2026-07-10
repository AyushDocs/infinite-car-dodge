import random
from typing import List, Optional
import pygame
import gymnasium as gym
import numpy as np
from ai.agent import RandomAgent
from game.config.constants import (
    CAR_HEIGHT, CAR_WIDTH, LANE_COUNT, LANE_WIDTH,
    PLAYER_HEIGHT, PLAYER_WIDTH, SPAWN_INTERVAL, WIDTH, HEIGHT, WHITE,
    CAR_SPEED, PLAYER_SPEED,
)
from game.models.car import Car
from game.models.directions import Directions
from game.models.player import Player

ACTIONS = ["left", "right", "stay"]
ACTION_TO_DIR = {"left": Directions.LEFT, "right": Directions.RIGHT}

BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
DARK = (30, 30, 30)
DARK_GRAY = (50, 50, 50)
GRAY = (180, 180, 180)


def extract_game_state(cars, player) -> List[float]:
    lane_cars = {i: [] for i in range(LANE_COUNT)}
    for c in cars:
        lane_idx = int(c.x // LANE_WIDTH)
        if 0 <= lane_idx < LANE_COUNT:
            lane_cars[lane_idx].append(c)
    player_y = player.y
    lst = []
    for i in range(LANE_COUNT):
        lane_cars[i].sort(key=lambda c: c.y, reverse=True)
        nearest = lane_cars[i][-1] if lane_cars[i] else None
        if nearest:
            dist_y = player_y - nearest.y
            lst.append(dist_y / HEIGHT)
        else:
            lst.append(1.0)
    player_lane = player.x // LANE_WIDTH
    lst.append(player_lane / LANE_COUNT)
    return lst


class CarDodgeGame:
    DIFFICULTY_RAMP_FRAMES = 1800

    def __init__(self, render: bool = False):
        self.render_enabled = render
        self.win: Optional[pygame.Surface] = None
        self.clock: Optional[pygame.time.Clock] = None
        self.font: Optional[pygame.font.Font] = None
        self.cars: List[Car] = []
        self.player: Optional[Player] = None
        self.game_over = False
        self.survived_frames = 0
        self.base_car_speed = CAR_SPEED
        self.base_spawn_interval = 90
        self.car_spawn_prob = 0.6
        self.steps_since_last_spawn = 0

        if self.render_enabled:
            pygame.init()
            self.win = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Infinite Car Dodge")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont("monospace", 20, bold=True)
            self.big_font = pygame.font.SysFont("monospace", 36, bold=True)

    @property
    def difficulty(self) -> float:
        return min(1.0, self.survived_frames / self.DIFFICULTY_RAMP_FRAMES)

    @property
    def car_speed(self) -> float:
        return self.base_car_speed + self.difficulty * 4

    @property
    def spawn_interval(self) -> int:
        return max(30, int(self.base_spawn_interval * (1 - self.difficulty * 0.5)))

    @property
    def spawn_prob(self) -> float:
        return min(0.9, self.car_spawn_prob + self.difficulty * 0.25)

    def reset(self):
        self.cars = []
        self.player = Player()
        self.game_over = False
        self.survived_frames = 0
        self.steps_since_last_spawn = 0
        return np.array(extract_game_state(self.cars, self.player), dtype=np.float32)

    def _despawn_offscreen(self):
        self.cars = [c for c in self.cars if c.is_on_screen()]

    def _spawn_wave(self):
        self._despawn_offscreen()
        empty_lane = random.randint(0, LANE_COUNT - 1)
        for lane in range(LANE_COUNT):
            if lane == empty_lane:
                continue
            if random.random() < self.spawn_prob:
                car = Car(lane)
                car.speed = self.car_speed
                self.cars.append(car)

    def _check_collision(self):
        for car in self.cars:
            if (car.x < self.player.x + PLAYER_WIDTH
                and car.x + CAR_WIDTH > self.player.x
                and car.y < self.player.y + PLAYER_HEIGHT
                and car.y + CAR_HEIGHT > self.player.y):
                return True
        return False

    def _step_physics(self):
        self.steps_since_last_spawn += 1
        if self.steps_since_last_spawn >= self.spawn_interval:
            self._spawn_wave()
            self.steps_since_last_spawn = 0
        for car in self.cars:
            car.speed = self.car_speed
            car.move()

    def step(self, action: str):
        if self.game_over:
            obs = np.array(extract_game_state(self.cars, self.player), dtype=np.float32)
            return obs, 0.0, True, False, {}

        prev_player_x = self.player.x
        if action in ACTION_TO_DIR:
            self.player.move(ACTION_TO_DIR[action])

        self._step_physics()

        collision = self._check_collision()
        self.survived_frames += 1

        lives_reward = 0.1 + self.difficulty * 0.15

        player_lane = int(self.player.x // LANE_WIDTH)
        closest_frame_y = HEIGHT
        for c in self.cars:
            if int(c.x // LANE_WIDTH) == player_lane:
                if c.y > 0 and c.y < closest_frame_y:
                    closest_frame_y = c.y
        if closest_frame_y < HEIGHT:
            danger = max(0, 1.0 - (self.player.y - closest_frame_y) / HEIGHT)
            danger_penalty = -danger * (0.5 + self.difficulty * 0.5)
        else:
            danger_penalty = 0.0

        near_miss = 0.0
        for c in self.cars:
            dx = abs(c.x - self.player.x)
            dy = abs(c.y - self.player.y)
            if dy < 80 and dx < CAR_WIDTH * 1.5:
                near_miss += 0.3

        step_reward = lives_reward + danger_penalty + near_miss
        if collision:
            self.game_over = True
            step_reward = -10.0 - self.survived_frames * 0.01

        if self.render_enabled:
            self._render_frame()

        obs = np.array(extract_game_state(self.cars, self.player), dtype=np.float32)
        return obs, step_reward, collision, False, {}

    def _render_frame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
                self.game_over = False
                self.reset()
                return

        self.win.fill(DARK_GRAY)

        for i in range(LANE_COUNT):
            x = i * LANE_WIDTH
            pygame.draw.line(self.win, (100, 100, 100), (x, 0), (x, HEIGHT), 1)

        for car in self.cars:
            car.draw(self.win)

        self.player.draw(self.win)

        score_text = self.font.render(f"Score: {self.survived_frames // 60}s", True, WHITE)
        diff_text = self.font.render(f"Speed: {self.car_speed:.1f}", True, WHITE)
        self.win.blit(score_text, (10, 10))
        self.win.blit(diff_text, (10, 35))

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(160)
            overlay.fill(BLACK)
            self.win.blit(overlay, (0, 0))

            go_text = self.big_font.render("GAME OVER", True, RED)
            score_label = self.font.render(f"Score: {self.survived_frames // 60}s", True, WHITE)
            restart_label = self.font.render("Press R to restart", True, GRAY)
            go_rect = go_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
            score_rect = score_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
            restart_rect = restart_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.win.blit(go_text, go_rect)
            self.win.blit(score_label, score_rect)
            self.win.blit(restart_label, restart_rect)

        pygame.display.flip()
        self.clock.tick(60)

    def close(self):
        if self.render_enabled:
            pygame.quit()


class CarDodgeEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(self, render_mode: Optional[str] = None):
        super().__init__()
        self.render_mode = render_mode
        self.game = CarDodgeGame(render=(render_mode == "human"))

        self.observation_space = gym.spaces.Box(
            low=-1.0, high=1.0,
            shape=(LANE_COUNT + 1,),
            dtype=np.float32,
        )
        self.action_space = gym.spaces.Discrete(3)

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed, options=options)
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        obs = self.game.reset()
        return obs, {}

    def step(self, action_idx: int):
        action = ACTIONS[action_idx]
        obs, reward, terminated, truncated, info = self.game.step(action)
        return obs, reward, terminated or truncated, False, info

    def render(self):
        if self.render_mode == "human":
            return
        raise NotImplementedError("Only human render mode is supported")

    def close(self):
        self.game.close()


def main(action_getter):
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Infinite Car Dodge")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 20, bold=True)
    big_font = pygame.font.SysFont("monospace", 36, bold=True)
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, SPAWN_INTERVAL)
    cars: List[Car] = []
    player = Player()
    game_over = False
    survived_frames = 0
    steps_since_last_spawn = 0
    running = True
    diff = 0.0
    base_spawn_interval = 90

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                cars = []
                player = Player()
                game_over = False
                survived_frames = 0
                steps_since_last_spawn = 0
                diff = 0.0
            if not game_over and event.type == spawn_event:
                cars = [c for c in cars if c.is_on_screen()]
                empty_lane = random.randint(0, LANE_COUNT - 1)
                spawn_prob = min(0.9, 0.6 + diff * 0.25)
                for lane in range(LANE_COUNT):
                    if lane == empty_lane:
                        continue
                    if random.random() < spawn_prob:
                        car = Car(lane)
                        car.speed = 4 + diff * 4
                        cars.append(car)

        if not game_over:
            action = action_getter(cars, player)
            if action == "right":
                player.move(Directions.RIGHT)
            elif action == "left":
                player.move(Directions.LEFT)

            steps_since_last_spawn += 1
            spawn_interval = max(30, int(base_spawn_interval * (1 - diff * 0.5)))
            if steps_since_last_spawn >= spawn_interval:
                steps_since_last_spawn = 0
                cars = [c for c in cars if c.is_on_screen()]
                empty_lane = random.randint(0, LANE_COUNT - 1)
                spawn_prob = min(0.9, 0.6 + diff * 0.25)
                for lane in range(LANE_COUNT):
                    if lane == empty_lane:
                        continue
                    if random.random() < spawn_prob:
                        car = Car(lane)
                        car.speed = 4 + diff * 4
                        cars.append(car)

        if not game_over:
            for car in cars:
                car.speed = 4 + diff * 4
                car.move()
                if (car.x < player.x + PLAYER_WIDTH
                    and car.x + CAR_WIDTH > player.x
                    and car.y < player.y + PLAYER_HEIGHT
                    and car.y + CAR_HEIGHT > player.y):
                    game_over = True

            survived_frames += 1
            diff = min(1.0, survived_frames / 1800)

        win.fill(DARK_GRAY)
        for i in range(LANE_COUNT):
            x = i * LANE_WIDTH
            pygame.draw.line(win, (100, 100, 100), (x, 0), (x, HEIGHT), 1)
        for car in cars:
            car.draw(win)
        player.draw(win)

        score_text = font.render(f"Score: {survived_frames // 60}s", True, WHITE)
        diff_text = font.render(f"Speed: {4 + diff * 4:.1f}", True, WHITE)
        win.blit(score_text, (10, 10))
        win.blit(diff_text, (10, 35))

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(160)
            overlay.fill(BLACK)
            win.blit(overlay, (0, 0))
            go_text = big_font.render("GAME OVER", True, RED)
            score_label = font.render(f"Score: {survived_frames // 60}s", True, WHITE)
            restart_label = font.render("Press R to restart", True, GRAY)
            win.blit(go_text, go_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
            win.blit(score_label, score_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))
            win.blit(restart_label, restart_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def get_human_action(cars, player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        return "right"
    elif keys[pygame.K_LEFT]:
        return "left"
    return "stay"


def get_ai_action(cars, player):
    return RandomAgent().act(["left", "right", "stay"])


if __name__ == "__main__":
    main(get_ai_action)