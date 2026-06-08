from __future__ import annotations
import pygame
from typing import Dict, List, Tuple

FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
CHARACTERS = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ0123456789ABCDEF@#$%&"
SCREEN_OFFSET = 150

THEMES: Dict[str, List[str]] = {
    "classic": ["#66FF66", "#33FF33", "#00EE00", "#00DD00", "#009900", "#008000", "#005000", "#004000", "#001900"],
    "amber": ["#FFB000", "#E0A000", "#C08000", "#A06000", "#805000", "#604000", "#403000", "#302000", "#201000"],
    "cyan": ["#AAFFFF", "#66FFEE", "#33FFDD", "#00FFCC", "#00CC99", "#009966", "#006633", "#004422", "#002211"],
    "ice": ["#FFFFFF", "#CCFFFF", "#99FFFF", "#66FFFF", "#33CCCC", "#009999", "#006666", "#004444", "#002222"],
}

font_cache: Dict[int, pygame.font.Font] = {}
texture_cache: Dict[Tuple[str, int, int, int], pygame.Surface] = {}
color_cache: List[pygame.Color] = [pygame.Color(c) for c in THEMES["classic"]]
bg_color_cache: List[pygame.Color] = [pygame.Color(c) for c in THEMES["classic"][-4:]]

current_theme_name: str = "classic"
HEAD_COLOR = pygame.Color("#FFFFFF")


def set_theme(name: str) -> None:
    global color_cache, bg_color_cache, current_theme_name
    colors = THEMES[name]
    color_cache = [pygame.Color(c) for c in colors]
    bg_color_cache = [pygame.Color(c) for c in colors[-4:]]
    texture_cache.clear()
    from .effects import clear_caches
    clear_caches()
    current_theme_name = name


def get_font(size: int) -> pygame.font.Font:
    if size not in font_cache:
        font_cache[size] = pygame.font.Font(FONT_PATH, size)
    return font_cache[size]


def get_texture(char: str, size: int, color_idx: int, alpha: int = 255) -> pygame.Surface:
    key = (char, size, color_idx, alpha)
    if key not in texture_cache:
        font = get_font(size)
        col = color_cache[color_idx] if alpha == 255 else bg_color_cache[color_idx]
        tex = font.render(char, True, col)
        if alpha < 255:
            tex.set_alpha(alpha)
        texture_cache[key] = tex
    return texture_cache[key]


def refresh(screen: pygame.Surface) -> None:
    screen.fill((0, 0, 0))
