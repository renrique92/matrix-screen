"""
MATRIX SCREEN SIMULATOR
Author: Rafael Sendrea
"""
import pygame
import random
import sys
import argparse
from typing import List, Dict, Any, Tuple

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
PARTICLE_MIN_SIZE = 10
PARTICLE_MAX_SIZE = 20

SCREEN_OFFSET = 150

CHARACTERS = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ0123456789ABCDEF@#$%&"
FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
GREENS = [
    "#66FF66",
    "#33FF33",
    "#00EE00",
    "#00DD00",
    "#009900",
    "#008000",
    "#005000",
    "#004000",
    "#001900"
]

TICK = 20

font_cache: Dict[int, pygame.font.Font] = {}
texture_cache: Dict[Tuple[str, int, int], pygame.Surface] = {}
color_cache: List[pygame.Color] = [pygame.Color(c) for c in GREENS]


def get_font(size: int) -> pygame.font.Font:
    if size not in font_cache:
        font_cache[size] = pygame.font.Font(FONT_PATH, size)
    return font_cache[size]


def get_texture(char: str, size: int, color_idx: int) -> pygame.Surface:
    key = (char, size, color_idx)
    if key not in texture_cache:
        font = get_font(size)
        texture_cache[key] = font.render(char, True, color_cache[color_idx])
    return texture_cache[key]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Matrix Screen Simulator")
    parser.add_argument("--fullscreen", action="store_true",
                        help="Fullscreen mode")
    parser.add_argument("-W", "--width", type=int, default=CANVAS_WIDTH,
                        help="Window width (default: %(default)s)")
    parser.add_argument("-H", "--height", type=int, default=CANVAS_HEIGHT,
                        help="Window height (default: %(default)s)")
    parser.add_argument("--fps", type=int, default=TICK,
                        help="Frames per second (default: %(default)s)")
    parser.add_argument("--noise", type=float, default=1.0,
                        help="Spawn rate multiplier 0.0-2.0 (default: %(default)s)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pygame.init()

    w = args.width
    h = args.height
    flags = pygame.FULLSCREEN if args.fullscreen else 0
    screen = pygame.display.set_mode((w, h), flags)
    pygame.display.set_caption("Matrix Screen")
    clock = pygame.time.Clock()

    refresh(screen)

    characters: List[Dict[str, Any]] = []

    num_part = round(w / PARTICLE_MAX_SIZE)

    x_velocities: List[int] = []
    for _ in range(num_part):
        x_velocities.append(random.randint(3, 8))

    run_loop(screen, clock, characters, x_velocities, spawn=True,
             spawn_rate=args.noise, fps=args.fps)

    print("Breaking free from the matrix...")
    accelerate_all(characters)

    run_loop(screen, clock, characters, x_velocities, spawn=False, fps=args.fps)

    print("You took the red pill!")
    pygame.quit()


def accelerate_all(characters: List[Dict[str, Any]]) -> None:
    for char in characters:
        char["velocity"] = 10


def run_loop(screen: pygame.Surface, clock: pygame.time.Clock,
             characters: List[Dict[str, Any]], x_velocities: List[int],
             spawn: bool, spawn_rate: float = 1.0, fps: int = 20) -> None:
    w = screen.get_width()
    h = screen.get_height()
    num_part = round(w / PARTICLE_MAX_SIZE)
    spawn_counter = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

        if spawn:
            spawn_counter += spawn_rate
            while spawn_counter >= 1.0:
                spawn_counter -= 1.0
                rand_x = random.randint(0, num_part - 1)
                character: Dict[str, Any] = {
                    "x": rand_x * PARTICLE_MAX_SIZE,
                    "y": 0,
                    "text": random.choice(CHARACTERS),
                    "velocity": x_velocities[rand_x],
                    "size": random.randint(PARTICLE_MIN_SIZE, PARTICLE_MAX_SIZE)
                }
                characters.append(character)

        update(characters, h)
        render(screen, characters)
        pygame.display.flip()
        clock.tick(fps)
        refresh(screen)


def update(characters: List[Dict[str, Any]], h: int) -> None:
    for character in characters:
        character["y"] += character["velocity"]
    characters[:] = [c for c in characters if c["y"] <= h + SCREEN_OFFSET]


def render(screen: pygame.Surface, characters: List[Dict[str, Any]]) -> None:
    for character in characters:
        print_character(screen, character)


def print_character(screen: pygame.Surface, character: Dict[str, Any]) -> None:
    size = character["size"]
    for i in range(len(color_cache)):
        char = random.choice(CHARACTERS)
        tex = get_texture(char, size, i)
        screen.blit(tex, (character["x"], character["y"] - (i * size)))


def refresh(screen: pygame.Surface) -> None:
    screen.fill((0, 0, 0))


if __name__ == '__main__':
    main()
