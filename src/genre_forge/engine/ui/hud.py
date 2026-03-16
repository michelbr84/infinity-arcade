"""
hud.py — Componentes de HUD (Heads-Up Display) para jogos Pygame.

Exibe informações de jogo: score, vida, tempo, nível.
"""

from typing import Dict, List, Optional, Tuple

import pygame


class HUD:
    """
    HUD configurável para jogos Pygame.

    Uso:
        hud = HUD(screen_width=800)
        hud.add("Score", 0)
        hud.add("Vida", 3, color=(50, 200, 50))
        hud.add("Tempo", "00:00", position="top-right")

        # No update:
        hud.set("Score", self.score)
        hud.set("Tempo", f"{minutes:02d}:{seconds:02d}")

        # No render:
        hud.render(screen)
    """

    def __init__(
        self,
        screen_width: int = 800,
        screen_height: int = 600,
        font_size: int = 28,
        padding: int = 12,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.padding = padding
        self.font = pygame.font.Font(None, font_size)
        self._items: Dict[str, dict] = {}

    def add(
        self,
        label: str,
        value: any = 0,
        color: Tuple[int, int, int] = (255, 255, 255),
        position: str = "top-left",
    ) -> None:
        """
        Adiciona item ao HUD.

        Args:
            label: Rótulo do item
            value: Valor inicial
            color: Cor do texto (RGB)
            position: "top-left", "top-right", "top-center",
                      "bottom-left", "bottom-right", "bottom-center"
        """
        self._items[label] = {
            "value": value,
            "color": color,
            "position": position,
        }

    def set(self, label: str, value: any) -> None:
        """Atualiza o valor de um item do HUD."""
        if label in self._items:
            self._items[label]["value"] = value

    def get(self, label: str) -> any:
        """Retorna o valor atual de um item."""
        item = self._items.get(label)
        return item["value"] if item else None

    def render(self, screen: pygame.Surface) -> None:
        """Renderiza todos os itens do HUD."""
        # Agrupa items por posição
        positions: Dict[str, list] = {}
        for label, item in self._items.items():
            pos = item["position"]
            if pos not in positions:
                positions[pos] = []
            positions[pos].append((label, item))

        # Renderiza cada grupo
        for pos, items in positions.items():
            self._render_group(screen, pos, items)

    def _render_group(self, screen: pygame.Surface, position: str, items: list) -> None:
        """Renderiza um grupo de items em uma posição."""
        line_height = 28

        for i, (label, item) in enumerate(items):
            text = self.font.render(
                f"{label}: {item['value']}", True, item["color"]
            )
            text_rect = text.get_rect()

            # Calcula posição
            if "top" in position:
                y = self.padding + i * line_height
            else:
                y = self.screen_height - self.padding - (len(items) - i) * line_height

            if "left" in position:
                x = self.padding
            elif "right" in position:
                x = self.screen_width - text_rect.width - self.padding
            else:  # center
                x = (self.screen_width - text_rect.width) // 2

            screen.blit(text, (x, y))


class HealthBar:
    """
    Barra de vida horizontal.

    Uso:
        health_bar = HealthBar(x=10, y=40, max_hp=100)
        health_bar.update(player.hp)
        health_bar.render(screen)
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int = 200,
        height: int = 20,
        max_hp: int = 100,
        bg_color: Tuple[int, int, int] = (60, 60, 70),
        fill_color: Tuple[int, int, int] = (50, 200, 50),
        low_color: Tuple[int, int, int] = (220, 50, 50),
        border_color: Tuple[int, int, int] = (180, 180, 190),
        low_threshold: float = 0.3,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.low_color = low_color
        self.border_color = border_color
        self.low_threshold = low_threshold

    def update(self, hp: int) -> None:
        """Atualiza HP atual."""
        self.current_hp = max(0, min(hp, self.max_hp))

    def render(self, screen: pygame.Surface) -> None:
        """Renderiza a barra de vida."""
        # Background
        pygame.draw.rect(screen, self.bg_color, self.rect)

        # Fill
        if self.current_hp > 0:
            ratio = self.current_hp / self.max_hp
            fill_width = int(self.rect.width * ratio)
            fill_rect = pygame.Rect(
                self.rect.x, self.rect.y, fill_width, self.rect.height
            )
            color = self.low_color if ratio <= self.low_threshold else self.fill_color
            pygame.draw.rect(screen, color, fill_rect)

        # Border
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
