from __future__ import annotations
import json
import pygame
import random
import sys
import argparse
from math import cos, sin
from typing import Any, Dict, List
from .render import (
    set_theme, refresh, THEMES, current_theme_name,
)
from .layer import Layer, LayerConfig
from .effects import (
    build_pipeline, update_particles, render_particles, GLOW_SCALE,
)

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

TICK = 30

CONFIG_PATH = "config.json"


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Matrix Screen Simulator")
    parser.add_argument("--fullscreen", action="store_true", default=None,
                        help="Fullscreen mode")
    parser.add_argument("-W", "--width", type=int, default=None,
                        help="Window width")
    parser.add_argument("-H", "--height", type=int, default=None,
                        help="Window height")
    parser.add_argument("--fps", type=int, default=None,
                        help="Frames per second")
    parser.add_argument("--noise", type=float, default=None,
                        help="Spawn rate multiplier 0.0-2.0")
    parser.add_argument("--show-stats", action="store_true", default=None,
                        help="Show FPS and drop count overlay")
    parser.add_argument("--glow", action="store_true", default=None,
                        help="Enable neon glow effect (bloom)")
    parser.add_argument("--theme", type=str, default=None,
                        choices=list(THEMES.keys()),
                        help="Color theme")
    parser.add_argument("--scanlines", action="store_true", default=None,
                        help="Enable CRT scanline effect")
    parser.add_argument("--config", type=str, default=None,
                        help="Load config from JSON file")
    return parser.parse_args(argv)


def load_config(path: str) -> Dict[str, Any]:
    with open(path) as f:
        return json.load(f)


def merge_cfg(args: argparse.Namespace, cfg: Dict[str, Any]) -> Dict[str, Any]:
    cli = vars(args)
    result: Dict[str, Any] = {}
    result["width"] = cli.get("width") or cfg.get("width", CANVAS_WIDTH)
    result["height"] = cli.get("height") or cfg.get("height", CANVAS_HEIGHT)
    result["fps"] = cli.get("fps") or cfg.get("fps", TICK)
    result["noise"] = cli.get("noise") or cfg.get("noise", 1.0)
    result["theme"] = cli.get("theme") or cfg.get("theme", "classic")
    result["fullscreen"] = cli.get("fullscreen") if cli.get("fullscreen") is not None else cfg.get("fullscreen", False)
    result["show_stats"] = cli.get("show_stats") if cli.get("show_stats") is not None else cfg.get("show_stats", False)
    result["glow"] = cli.get("glow") if cli.get("glow") is not None else cfg.get("glow", False)
    result["scanlines"] = cli.get("scanlines") if cli.get("scanlines") is not None else cfg.get("scanlines", False)
    result["layers"] = cfg.get("layers")
    return result


def make_layers(raw: List[Dict[str, Any]] | None, w: int) -> List[Layer]:
    if raw:
        return [Layer(LayerConfig(**lc), w) for lc in raw]
    return [
        Layer(LayerConfig(min_size=8, max_size=12, min_vel=1, max_vel=3,
                          alpha=40, spawn_rate=0.3, color_offset=4), w),
        Layer(LayerConfig(), w),
    ]


def run_loop(screen: pygame.Surface, clock: pygame.time.Clock,
             layers: List[Layer], spawn: bool,
             spawn_rate: float = 1.0, fps: int = 20,
             show_stats: bool = False,
             glow: bool = False, scanlines: bool = False) -> None:
    w = screen.get_width()
    h = screen.get_height()
    noise = spawn_rate
    speed = 1.0
    speed_ref = [speed]
    fg_layer = layers[-1] if layers else None
    paused_ref = [False]

    particles: List[Dict[str, Any]] = []

    glow_surf = None
    if glow:
        glow_surf = pygame.Surface((w // GLOW_SCALE, h // GLOW_SCALE))

    scanline_surf = None
    if scanlines:
        scanline_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        for sy in range(0, h, 2):
            scanline_surf.fill((0, 0, 0, 25), (0, sy, w, 1))

    pipeline = build_pipeline(glow, glow_surf, fg_layer, w, h,
                              scanlines, scanline_surf,
                              show_stats, clock, paused_ref, speed_ref)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and spawn:
                mx, my = event.pos
                for _ in range(random.randint(10, 20)):
                    angle = random.uniform(0, 2 * 3.14159)
                    speed = random.uniform(2, 6)
                    particles.append({
                        "x": mx,
                        "y": my,
                        "vx": cos(angle) * speed,
                        "vy": sin(angle) * speed,
                        "life": 1.0,
                        "size": random.randint(8, 14),
                    })
                if fg_layer:
                    for ch in fg_layer.characters:
                        dx = abs(ch["x"] - mx)
                        if dx < 60:
                            push = (60 - dx) / 60 * 4
                            ch["velocity"] = max(1, ch["velocity"] + random.uniform(1, push))
            if event.type == pygame.KEYDOWN:
                if not spawn:
                    return
                key = event.key
                if key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif key == pygame.K_p:
                    paused_ref[0] = not paused_ref[0]
                elif key == pygame.K_EQUALS or key == pygame.K_PLUS:
                    noise = min(2.0, noise + 0.2)
                elif key == pygame.K_MINUS or key == pygame.K_UNDERSCORE:
                    noise = max(0.0, noise - 0.2)
                elif key == pygame.K_UP:
                    speed = min(5.0, speed + 0.2)
                    speed_ref[0] = speed
                elif key == pygame.K_DOWN:
                    speed = max(0.0, speed - 0.2)
                    speed_ref[0] = speed
                elif key == pygame.K_r:
                    for lyr in layers:
                        lyr.characters.clear()
                elif key == pygame.K_c:
                    themes = list(THEMES.keys())
                    idx = (themes.index(current_theme_name) + 1) % len(themes)
                    set_theme(themes[idx])
                elif key == pygame.K_SPACE:
                    if fg_layer:
                        for _ in range(random.randint(20, 30)):
                            fg_layer.spawn(1.0)

        if paused_ref[0]:
            for lyr in layers:
                lyr.render(screen)
            render_particles(screen, particles, clock)
            for fn in pipeline:
                fn(screen)
            pygame.display.flip()
            clock.tick(fps)
            refresh(screen)
            continue

        update_particles(particles)
        for lyr in layers:
            if spawn:
                lyr.spawn(noise * speed)
            lyr.update(h, speed)
            lyr.render(screen)

        render_particles(screen, particles, clock)
        for fn in pipeline:
            fn(screen)
        pygame.display.flip()
        clock.tick(fps)
        refresh(screen)


def main() -> None:
    args = parse_args()
    cfg: Dict[str, Any] = {}
    config_src = args.config or CONFIG_PATH
    try:
        cfg = load_config(config_src)
    except FileNotFoundError:
        pass
    merged = merge_cfg(args, cfg)

    pygame.init()

    w = merged["width"]
    h = merged["height"]
    flags = pygame.FULLSCREEN if merged["fullscreen"] else 0
    screen = pygame.display.set_mode((w, h), flags)
    pygame.display.set_caption("Matrix Screen")
    clock = pygame.time.Clock()

    set_theme(merged["theme"])

    refresh(screen)

    layers = make_layers(merged.get("layers"), w)

    run_loop(screen, clock, layers, spawn=True, spawn_rate=merged["noise"],
             fps=merged["fps"], show_stats=merged["show_stats"],
             glow=merged["glow"], scanlines=merged["scanlines"])

    print("Breaking free from the matrix...")
    if layers:
        for ch in layers[-1].characters:
            ch["velocity"] = 10

    run_loop(screen, clock, layers, spawn=False, fps=merged["fps"],
             show_stats=merged["show_stats"],
             glow=merged["glow"], scanlines=merged["scanlines"])

    print("You took the red pill!")
    pygame.quit()


if __name__ == '__main__':
    main()
