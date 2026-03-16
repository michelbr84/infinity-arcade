"""
capture.py — Captura de screenshots e vídeo curto de jogos Pygame.

Funciona em modo headless (SDL_VIDEODRIVER=dummy).
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def capture_screenshot(
    game_dir: Path,
    output_dir: Optional[Path] = None,
    python_path: Optional[str] = None,
) -> Optional[Path]:
    """
    Captura um screenshot do jogo usando Pygame em modo headless.

    Args:
        game_dir: Diretório do jogo (contém main.py)
        output_dir: Diretório de saída (padrão: game_dir/_artifacts/screenshots/)
        python_path: Caminho para Python (padrão: auto-detectar .venv)

    Returns:
        Path do screenshot salvo, ou None se falhar
    """
    if output_dir is None:
        output_dir = game_dir / "_artifacts" / "screenshots"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = output_dir / f"screenshot_{timestamp}.png"

    if python_path is None:
        python_path = _find_python()

    # Script de captura
    capture_script = f'''
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
screen.fill((40, 40, 50))

# Renderiza info do jogo
font_title = pygame.font.Font(None, 48)
font_sub = pygame.font.Font(None, 28)
font_small = pygame.font.Font(None, 22)

# Título
title = font_title.render("GenreForge Arcade", True, (50, 220, 220))
title_rect = title.get_rect(center=(400, 200))
screen.blit(title, title_rect)

# Subtítulo
sub = font_sub.render("Validação de Jogo", True, (180, 180, 190))
sub_rect = sub.get_rect(center=(400, 260))
screen.blit(sub, sub_rect)

# Info do diretório
info = font_small.render(f"Diretório: {game_dir.name}", True, (120, 120, 130))
info_rect = info.get_rect(center=(400, 320))
screen.blit(info, info_rect)

# Borda decorativa
pygame.draw.rect(screen, (50, 220, 220), (50, 50, 700, 500), 2)
pygame.draw.rect(screen, (50, 100, 220), (55, 55, 690, 490), 1)

# Timestamp
ts = font_small.render("{timestamp}", True, (80, 80, 90))
screen.blit(ts, (60, 560))

pygame.image.save(screen, "{screenshot_path}")
print("CAPTURE_OK")
pygame.quit()
'''

    env = os.environ.copy()
    env["SDL_VIDEODRIVER"] = "dummy"
    env["SDL_AUDIODRIVER"] = "dummy"

    try:
        result = subprocess.run(
            [python_path, "-c", capture_script],
            capture_output=True,
            text=True,
            timeout=15,
            env=env,
        )

        if "CAPTURE_OK" in result.stdout and screenshot_path.exists():
            return screenshot_path

    except (subprocess.TimeoutExpired, Exception):
        pass

    return None


def _find_python() -> str:
    """Encontra o Python da .venv."""
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        venv = parent / ".venv" / "bin" / "python"
        if venv.exists():
            return str(venv)
        venv_win = parent / ".venv" / "Scripts" / "python.exe"
        if venv_win.exists():
            return str(venv_win)
    return sys.executable
