
# Matrix Screen Simulator

Matrix rain en pygame. Full-width katakana + ASCII sobre canvas negro con estela verde degradada.

## Requisitos

```bash
pip install pygame
```

## Uso

```bash
python main.py
```

### CLI flags

| Flag | Defecto | Descripción |
|------|---------|-------------|
| `--fullscreen` | — | Pantalla completa |
| `-W` | 800 | Ancho ventana |
| `-H` | 600 | Alto ventana |
| `--fps` | 30 | Frames por segundo |
| `--noise` | 1.0 | Multiplicador de spawn (0.0–2.0) |

## Controles

| Tecla | Acción |
|-------|--------|
| Cualquier tecla | Acelera gotas / "break free" |
| Escape | Salir |

## Notas

- **macOS only** — usa font del sistema `/System/Library/Fonts/AppleSDGothicNeo.ttc`
- No requiere conexión a internet
- Sin tests, sin linter, sin CI

## Repo

https://github.com/renrique92/matrix-screen
