from __future__ import annotations
import random
import pygame
from typing import Any, Callable, Dict, List
from .layer import Layer
from .render import CHARACTERS, color_cache, get_font

GLOW_SCALE = 4
GLOW_ALPHA = 80

glow_cache: Dict[tuple, pygame.Surface] = {}
particle_tex_cache: Dict[int, pygame.Surface] = {}


def clear_caches() -> None:
    glow_cache.clear()
    particle_tex_cache.clear()


def get_glow_texture(char: str, size: int, color_idx: int) -> pygame.Surface:
    key = (char, size, color_idx)
    if key not in glow_cache:
        font = get_font(max(1, size // GLOW_SCALE))
        col = color_cache[color_idx]
        glow_cache[key] = font.render(char, True, col)
    return glow_cache[key]


def render_glow(surf: pygame.Surface, characters: List[Dict[str, Any]],
                w: int, h: int) -> None:
    gs = GLOW_SCALE
    for ch in characters:
        size = max(1, ch["size"] // gs)
        vel = ch["velocity"]
        trail_len = min(len(color_cache), max(2, vel + 2))
        y = ch["y"] // gs
        x = ch["x"] // gs
        for i in range(trail_len):
            c = random.choice(CHARACTERS)
            tex = get_glow_texture(c, size, 0 if i == 0 else i - 1)
            surf.blit(tex, (x, y))
            gap = max(1, size - i)
            y -= gap


def update_particles(particles: List[Dict[str, Any]]) -> None:
    dt = 0.016
    for p in particles:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 2 * dt
        p["life"] -= dt * 2
    particles[:] = [p for p in particles if p["life"] > 0]


def render_particles(screen: pygame.Surface, particles: List[Dict[str, Any]],
                     clock: pygame.time.Clock) -> None:
    for p in particles:
        size = p["size"]
        if size not in particle_tex_cache:
            font = get_font(size)
            col = color_cache[0]
            particle_tex_cache[size] = font.render(random.choice(CHARACTERS), True, col)
        tex = particle_tex_cache[size].copy()
        alpha = max(0, min(255, int(p["life"] * 255)))
        tex.set_alpha(alpha)
        screen.blit(tex, (p["x"], p["y"]))


def draw_stats(screen: pygame.Surface, clock: pygame.time.Clock,
               drop_count: int, paused: bool = False,
               speed: float = 1.0) -> None:
    font = pygame.font.Font(None, 14)
    status = " PAUSED" if paused else ""
    text = f"FPS: {clock.get_fps():.0f} | Drops: {drop_count} | Speed: {speed:.1f}{status}"
    surf = font.render(text, True, pygame.Color("#666666"))
    screen.blit(surf, (4, 4))


def build_pipeline(glow: bool, glow_surf: Any,
                   fg_layer: Layer | None, w: int, h: int,
                   scanlines: bool, scanline_surf: Any,
                   show_stats: bool, clock: pygame.time.Clock,
                   paused_ref: List[bool],
                   speed_ref: List[float]) -> List[Callable[[pygame.Surface], None]]:
    pipe: List[Callable[[pygame.Surface], None]] = []
    if glow and glow_surf and fg_layer:
        def apply_glow(screen: pygame.Surface) -> None:
            glow_surf.fill((0, 0, 0))
            render_glow(glow_surf, fg_layer.characters, w, h)
            scaled = pygame.transform.scale(glow_surf, (w, h))
            scaled.set_alpha(GLOW_ALPHA)
            screen.blit(scaled, (0, 0), special_flags=pygame.BLEND_ADD)
        pipe.append(apply_glow)
    if scanlines and scanline_surf:
        def apply_scanlines(screen: pygame.Surface) -> None:
            screen.blit(scanline_surf, (0, 0))
        pipe.append(apply_scanlines)
    if show_stats:
        fg = fg_layer
        def apply_stats(screen: pygame.Surface) -> None:
            n = len(fg.characters) if fg else 0
            draw_stats(screen, clock, n, paused_ref[0], speed_ref[0])
        pipe.append(apply_stats)
    return pipe
