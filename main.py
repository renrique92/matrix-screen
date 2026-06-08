"""
MATRIX SCREEN SIMULATOR
Author: Rafael Sendrea
"""
import pygame
import random
import sys

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

DELAY = 0.05

font_cache = {}
color_cache = [pygame.Color(c) for c in GREENS]


def get_font(size):
    if size not in font_cache:
        font_cache[size] = pygame.font.Font(FONT_PATH, size)
    return font_cache[size]


def main():
    pygame.init()

    screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
    pygame.display.set_caption("Matrix Screen")
    clock = pygame.time.Clock()

    refresh(screen)

    characters = []

    num_part = round(CANVAS_WIDTH / PARTICLE_MAX_SIZE)

    x_velocities = []
    for i in range(num_part):
        x_velocities.append(random.randint(3, 8))

    key_pressed = False

    while not key_pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                key_pressed = True

        rand_x = random.randint(0, num_part - 1)

        character = {
            "x": rand_x * PARTICLE_MAX_SIZE,
            "y": 0,
            "text": random.choice(CHARACTERS),
            "velocity": x_velocities[rand_x],
            "size": random.randint(PARTICLE_MIN_SIZE, PARTICLE_MAX_SIZE)
        }
        characters.append(character)

        draw_characters(screen, characters)
        pygame.display.flip()
        clock.tick(20)
        refresh(screen)

    print("Breaking free from the matrix...")
    accelerate_all(characters)

    while len(characters) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_characters(screen, characters)
        pygame.display.flip()
        clock.tick(20)
        refresh(screen)

    print("You took the red pill!")
    pygame.quit()


def accelerate_all(characters):
    for char in characters:
        char["velocity"] = 10


def draw_characters(screen, characters):
    for character in characters:
        character["y"] += character["velocity"]

    characters[:] = [c for c in characters if c["y"] <= CANVAS_HEIGHT + SCREEN_OFFSET]

    for character in characters:
        print_character(screen, character)


def print_character(screen, character):
    font_obj = get_font(character["size"])
    for i in range(len(color_cache)):
        char = random.choice(CHARACTERS)
        text_surf = font_obj.render(char, True, color_cache[i])
        screen.blit(text_surf, (character["x"], character["y"] - (i * character["size"])))


def refresh(screen):
    screen.fill((0, 0, 0))


if __name__ == '__main__':
    main()
