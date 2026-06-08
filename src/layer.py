from __future__ import annotations
import pygame
import random
from dataclasses import dataclass
from typing import Any, Dict, List
from .render import (
    CHARACTERS, SCREEN_OFFSET, HEAD_COLOR,
    color_cache, bg_color_cache,
    get_font, get_texture,
)


@dataclass
class LayerConfig:
    min_size: int = 12
    max_size: int = 20
    min_vel: int = 3
    max_vel: int = 8
    alpha: int = 255
    spawn_rate: float = 1.0
    color_offset: int = 0


class Layer:
    config: LayerConfig
    characters: List[Dict[str, Any]]
    x_velocities: List[int]
    spawn_counter: float

    def __init__(self, config: LayerConfig, w: int) -> None:
        self.config = config
        self.characters = []
        num_part = round(w / config.max_size)
        self.x_velocities = [random.randint(config.min_vel, config.max_vel) for _ in range(num_part)]
        self.spawn_counter = 0.0

    def spawn(self, noise: float) -> None:
        cfg = self.config
        num_part = len(self.x_velocities)
        step = cfg.max_size
        self.spawn_counter += cfg.spawn_rate * noise
        while self.spawn_counter >= 1.0:
            self.spawn_counter -= 1.0
            rx = random.randint(0, num_part - 1)
            self.characters.append({
                "x": rx * step,
                "y": 0,
                "text": random.choice(CHARACTERS),
                "velocity": self.x_velocities[rx],
                "size": random.randint(cfg.min_size, cfg.max_size),
            })

    def update(self, h: int, speed: float = 1.0) -> None:
        for ch in self.characters:
            ch["y"] += ch["velocity"] * speed
        self.characters[:] = [c for c in self.characters if c["y"] <= h + SCREEN_OFFSET]

    def render(self, screen: pygame.Surface) -> None:
        cfg = self.config
        colors = color_cache if cfg.color_offset == 0 else bg_color_cache
        lc = len(colors)
        for ch in self.characters:
            vel = ch["velocity"]
            size = ch["size"]
            trail_len = int(min(lc, max(2, vel + 2)) if cfg.color_offset == 0 else min(lc, max(1, vel)))
            y = ch["y"]
            for i in range(trail_len):
                c = random.choice(CHARACTERS)
                if i == 0 and cfg.color_offset == 0:
                    font = get_font(size)
                    tex = font.render(c, True, HEAD_COLOR)
                else:
                    ci = (i - 1) if cfg.color_offset == 0 else i
                    tex = get_texture(c, size, ci, cfg.alpha)
                screen.blit(tex, (ch["x"], y))
                gap = max(1, size - i)
                y -= gap
