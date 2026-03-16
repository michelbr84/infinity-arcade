#!/usr/bin/env python3
"""
generate_game.py — Gera um projeto de jogo Pygame a partir de gênero e parâmetros.

Uso:
    python generate_game.py --genre shooter --name "space-invader" --pitch "Nave espacial contra aliens"
    python generate_game.py --genre puzzle --name "box-push" --pitch "Puzzle de empurrar caixas"
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def get_project_root() -> Path:
    """Retorna o diretório raiz do projeto."""
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent.parent.parent.parent


def slugify(text: str) -> str:
    """Converte texto em slug URL-safe."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


VALID_GENRES = [
    "action", "adventure", "rpg", "shooter", "strategy",
    "puzzle", "racing", "sports", "simulation", "sandbox",
]

GENRE_DESCRIPTIONS = {
    "action": "Jogo de ação com movimento, combate e colisões",
    "adventure": "Exploração, gatilhos e puzzles com narrativa",
    "rpg": "Progressão, itens e combate por turnos ou action-lite",
    "shooter": "Tiro, spawn de inimigos, score e power-ups",
    "strategy": "Grid, turnos, ações por unidade e AI simples",
    "puzzle": "Regras determinísticas, checagem de vitória e níveis",
    "racing": "Física simplificada, pista e contagem de voltas/tempo",
    "sports": "Regras de partida simples, placar e rounds",
    "simulation": "Ticks de tempo, agentes e UI de inspeção",
    "sandbox": "Mundo editável, inventário e loop criativo",
}


def create_blueprint(genre: str, name: str, pitch: str) -> dict:
    """Cria o blueprint (game.json) do jogo."""
    return {
        "name": name,
        "slug": slugify(name),
        "genre": genre,
        "pitch": pitch,
        "description": GENRE_DESCRIPTIONS.get(genre, ""),
        "version": "0.1.0",
        "created_at": datetime.now().isoformat(),
        "config": {
            "resolution": [800, 600],
            "fps": 60,
            "title": name.replace("-", " ").title(),
            "fullscreen": False,
        },
        "controls": {
            "quit": "ESC",
            "movement": "WASD or Arrow Keys",
            "action": "SPACE",
        },
        "rules": {
            "pygame_only": True,
            "no_external_assets": True,
            "must_have_hud": True,
            "must_have_win_lose": True,
            "must_handle_quit": True,
        },
    }


def create_readme(blueprint: dict) -> str:
    """Gera o README.md do jogo."""
    return f"""# {blueprint['config']['title']}

> {blueprint['pitch']}

## Gênero
**{blueprint['genre'].title()}** — {blueprint['description']}

## Como Jogar

```bash
# Ativar ambiente virtual
source .venv/bin/activate  # Linux/macOS
# .venv\\Scripts\\activate   # Windows

# Rodar o jogo
python main.py
```

## Controles
- **{blueprint['controls']['movement']}** — Movimento
- **{blueprint['controls']['action']}** — Ação principal
- **{blueprint['controls']['quit']}** — Sair

## Configuração
- Resolução: {blueprint['config']['resolution'][0]}×{blueprint['config']['resolution'][1]}
- FPS: {blueprint['config']['fps']}

## Gerado por
GenreForge Arcade — Pygame Genre Forge Skill
Data: {blueprint['created_at'][:10]}
"""


def create_main_stub(blueprint: dict) -> str:
    """Gera um main.py stub básico para o gênero."""
    title = blueprint["config"]["title"]
    width, height = blueprint["config"]["resolution"]
    fps = blueprint["config"]["fps"]
    genre = blueprint["genre"]

    return f'''#!/usr/bin/env python3
"""
{title} — Jogo de {genre} gerado pelo GenreForge Arcade.

{blueprint["pitch"]}
"""

import sys
import math
import random
import pygame

# --- Constantes ---
SCREEN_WIDTH = {width}
SCREEN_HEIGHT = {height}
FPS = {fps}
TITLE = "{title}"

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 100, 220)
YELLOW = (240, 220, 50)
CYAN = (50, 220, 220)
MAGENTA = (220, 50, 220)
DARK_GRAY = (40, 40, 50)
LIGHT_GRAY = (180, 180, 190)


class Game:
    """Classe principal do jogo."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)

        # TODO: Inicializar entidades do gênero "{genre}"
        self._init_game()

    def _init_game(self):
        """Inicializa estado do jogo. Override para cada gênero."""
        pass

    def handle_events(self):
        """Processa eventos do pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self._init_game()
                    self.score = 0
                    self.game_over = False

    def update(self, dt: float):
        """Atualiza lógica do jogo. dt em segundos."""
        if self.game_over:
            return
        # TODO: Lógica de atualização do gênero "{genre}"

    def render(self):
        """Renderiza o frame atual."""
        self.screen.fill(DARK_GRAY)

        if self.game_over:
            self._render_game_over()
        else:
            # TODO: Renderizar entidades do gênero "{genre}"
            self._render_placeholder()

        # HUD sempre visível
        self._render_hud()

        pygame.display.flip()

    def _render_placeholder(self):
        """Placeholder visual — substituir com lógica do gênero."""
        # Texto central
        text = self.font.render(
            f"Gênero: {genre.upper()} — Implemente a lógica aqui!",
            True, CYAN
        )
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)

    def _render_hud(self):
        """Renderiza HUD mínimo: score."""
        score_text = self.font.render(f"Score: {{self.score}}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def _render_game_over(self):
        """Renderiza tela de game over."""
        text = self.font_large.render("GAME OVER", True, RED)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(text, rect)

        score_text = self.font.render(f"Score Final: {{self.score}}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(score_text, score_rect)

        restart = self.font.render("Pressione R para reiniciar ou ESC para sair", True, LIGHT_GRAY)
        restart_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(restart, restart_rect)

    def run(self):
        """Loop principal do jogo."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time em segundos
            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()
        sys.exit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
'''


def generate_game(genre: str, name: str, pitch: str) -> Path:
    """Gera o projeto completo do jogo."""
    project_root = get_project_root()
    slug = slugify(name)
    game_dir = project_root / "generated_games" / slug

    # Cria estrutura de diretórios
    game_dir.mkdir(parents=True, exist_ok=True)
    (game_dir / "_artifacts" / "screenshots").mkdir(parents=True, exist_ok=True)
    (game_dir / "_artifacts" / "video").mkdir(parents=True, exist_ok=True)

    # Gera blueprint
    blueprint = create_blueprint(genre, name, pitch)
    with open(game_dir / "game.json", "w", encoding="utf-8") as f:
        json.dump(blueprint, f, indent=2, ensure_ascii=False)

    # Gera README
    readme = create_readme(blueprint)
    with open(game_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    # Gera main.py
    main_code = create_main_stub(blueprint)
    with open(game_dir / "main.py", "w", encoding="utf-8") as f:
        f.write(main_code)

    return game_dir


def main():
    parser = argparse.ArgumentParser(
        description="GenreForge Arcade — Gerador de jogos Pygame por gênero"
    )
    parser.add_argument(
        "--genre", required=True, choices=VALID_GENRES,
        help="Gênero do jogo"
    )
    parser.add_argument(
        "--name", required=True,
        help="Nome do jogo (será convertido em slug)"
    )
    parser.add_argument(
        "--pitch", default="",
        help="Descrição/pitch curto do jogo"
    )

    args = parser.parse_args()

    print(f"\n🎮 Gerando jogo '{args.name}' (gênero: {args.genre})...\n")

    game_dir = generate_game(args.genre, args.name, args.pitch)

    print(f"✅ Jogo gerado em: {game_dir}")
    print(f"   - main.py:   {game_dir / 'main.py'}")
    print(f"   - game.json: {game_dir / 'game.json'}")
    print(f"   - README.md: {game_dir / 'README.md'}")
    print(f"\n▶️  Para jogar: python {game_dir / 'main.py'}\n")


if __name__ == "__main__":
    main()
