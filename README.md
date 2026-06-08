
# Matrix Screen Simulator

Matrix rain en pygame. Full-width katakana + ASCII sobre canvas negro con estela degradada.

## Requisitos

```bash
pip install pygame
```

## Uso

```bash
python main.py
```

### CLI flags

| Flag | Valores | Defecto | Descripción |
|------|---------|---------|-------------|
| `--fullscreen` | — | off | Pantalla completa |
| `-W` | int | 800 | Ancho ventana |
| `-H` | int | 600 | Alto ventana |
| `--fps` | int (1–240) | 30 | Frames por segundo |
| `--noise` | float (0.0–2.0) | 1.0 | Multiplicador de spawn |
| `--theme` | `classic` \| `amber` \| `cyan` \| `ice` | classic | Tema de color |
| `--show-stats` | — | off | Muestra FPS y contador de gotas |
| `--glow` | — | off | Efecto neón bloom (sin shaders) |
| `--scanlines` | — | off | Líneas CRT superpuestas |
| `--config` | ruta a `.json` | `config.json` | JSON de configuración |

## Controles (runtime)

| Tecla | Acción |
|-------|--------|
| `c` | Ciclar tema (classic → amber → cyan → ice) |
| `p` | Pausa / reanuda |
| `+` / `=` | Aumentar noise (más gotas) |
| `-` / `_` | Reducir noise |
| `r` | Reset (limpia todas las gotas) |
| `Espacio` | Rain burst (20–30 gotas instantáneas) |
| `Escape` | Salir |
| Click | Explosión de partículas + empuja gotas cercanas |

## Config JSON

Si existe `config.json` en el directorio del script, se carga automáticamente.
Se puede especificar otra ruta con `--config`. Los flags CLI tienen prioridad.

```json
{
  "theme": "amber",
  "fps": 60,
  "noise": 0.8,
  "fullscreen": true,
  "show_stats": true,
  "glow": true,
  "scanlines": true,
  "layers": [
    {"min_size": 8, "max_size": 12, "min_vel": 1, "max_vel": 3, "alpha": 40, "spawn_rate": 0.3},
    {"min_size": 14, "max_size": 22, "min_vel": 4, "max_vel": 9, "alpha": 255, "spawn_rate": 1.0}
  ]
}
```

## Características

- **Background layer**: gotas lentas y tenues para profundidad
- **Cabeza blanca**: el carácter líder de cada gota es blanco brillante
- **Temas**: classic (verde Matrix), amber, cyan, ice
- **Glow**: bloom neón sin shaders (reescalado + BLEND_ADD)
- **Scanlines**: efecto CRT
- **Click explosion**: partículas al hacer clic + empuje lateral en gotas cercanas
- **FPS overlay**: estadísticas en pantalla con `--show-stats`
- **Arquitectura capas**: `Layer` / `LayerConfig` — extensible a N capas
- **Pipeline post-procesamiento**: efectos encadenables como `List[Callable]`
- **Persistencia**: configuración vía `config.json`

## Notas

- **macOS only** — usa font del sistema `/System/Library/Fonts/AppleSDGothicNeo.ttc`
- No requiere conexión a internet
- Sin tests, sin linter, sin CI

## Repo

https://github.com/renrique92/matrix-screen
