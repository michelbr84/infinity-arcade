"""
core_loop.py — Game loop base com delta time e hooks de ciclo de vida.

Fornece a classe GameBase que todo jogo deve herdar.
Padrão: handle_events → update → render por frame.
"""

import sys
from typing import Optional

import pygame


# Cores padrão do projeto
class Colors:
    """Paleta de cores padrão do GenreForge Arcade."""
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
    ORANGE = (240, 150, 30)


class GameBase:
    """
    Classe base para jogos Pygame com game loop padrão.

    Hooks de ciclo de vida (override nas subclasses):
        on_init()      — chamado após pygame.init()
        on_event(event) — chamado para cada evento pygame
        on_update(dt)  — chamado a cada frame (dt em segundos)
        on_render(screen) — chamado a cada frame para desenhar
        on_quit()      — chamado antes de encerrar

    Uso:
        class MeuJogo(GameBase):
            def on_init(self):
                self.player = Player(400, 300)

            def on_update(self, dt):
                self.player.update(dt)

            def on_render(self, screen):
                self.player.draw(screen)

        MeuJogo(title="Meu Jogo").run()
    """

    def __init__(
        self,
        title: str = "GenreForge Arcade",
        width: int = 800,
        height: int = 600,
        fps: int = 60,
        bg_color: tuple = Colors.DARK_GRAY,
    ):
        """
        Inicializa o jogo.

        Args:
            title: Título da janela
            width: Largura da tela em pixels
            height: Altura da tela em pixels
            fps: Frames por segundo alvo
            bg_color: Cor de fundo (RGB tuple)
        """
        pygame.init()

        self.width = width
        self.height = height
        self.fps = fps
        self.bg_color = bg_color
        self.title = title

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        # Fontes padrão
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)

        # Estado do jogo
        self.score = 0
        self.game_over = False
        self.game_won = False

        # Delta time atual
        self.dt = 0.0
        self.total_time = 0.0

        # Hook de inicialização
        self.on_init()

    def on_init(self) -> None:
        """Override: inicialização customizada do jogo."""
        pass

    def on_event(self, event: pygame.event.Event) -> None:
        """Override: processar evento individual."""
        pass

    def on_update(self, dt: float) -> None:
        """Override: lógica de atualização (dt em segundos)."""
        pass

    def on_render(self, screen: pygame.Surface) -> None:
        """Override: renderizar elementos na tela."""
        pass

    def on_quit(self) -> None:
        """Override: cleanup antes de encerrar."""
        pass

    def handle_events(self) -> None:
        """Processa eventos do pygame (QUIT, ESC, e delega ao hook)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_r and (self.game_over or self.game_won):
                    self.restart()

            # Delega ao hook do usuário
            self.on_event(event)

    def restart(self) -> None:
        """Reinicia o estado do jogo."""
        self.score = 0
        self.game_over = False
        self.game_won = False
        self.total_time = 0.0
        self.on_init()

    def update(self, dt: float) -> None:
        """Atualiza lógica do jogo se não pausado/game over."""
        if self.paused or self.game_over or self.game_won:
            return

        self.total_time += dt
        self.on_update(dt)

    def render(self) -> None:
        """Renderiza o frame completo."""
        self.screen.fill(self.bg_color)

        # Renderiza conteúdo do jogo
        self.on_render(self.screen)

        # Overlay de estados especiais
        if self.game_over:
            self._render_game_over()
        elif self.game_won:
            self._render_victory()
        elif self.paused:
            self._render_pause()

        pygame.display.flip()

    def render_hud(
        self,
        items: dict[str, str | int | float],
        position: str = "top-left",
        color: tuple = Colors.WHITE,
    ) -> None:
        """
        Renderiza HUD com pares chave:valor.

        Args:
            items: Dicionário de labels e valores
            position: "top-left", "top-right", "bottom-left", "bottom-right"
            color: Cor do texto
        """
        padding = 10
        line_height = 25

        if "top" in position:
            y_start = padding
        else:
            y_start = self.height - padding - (len(items) * line_height)

        for i, (label, value) in enumerate(items.items()):
            text = self.font_medium.render(f"{label}: {value}", True, color)

            if "left" in position:
                x = padding
            else:
                x = self.width - text.get_width() - padding

            self.screen.blit(text, (x, y_start + i * line_height))

    def _render_game_over(self) -> None:
        """Renderiza overlay de Game Over."""
        # Fundo semi-transparente
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Texto
        text = self.font_large.render("GAME OVER", True, Colors.RED)
        rect = text.get_rect(center=(self.width // 2, self.height // 2 - 40))
        self.screen.blit(text, rect)

        score_text = self.font_medium.render(
            f"Score Final: {self.score}", True, Colors.WHITE
        )
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
        self.screen.blit(score_text, score_rect)

        restart = self.font_small.render(
            "R = Reiniciar  |  ESC = Sair", True, Colors.LIGHT_GRAY
        )
        restart_rect = restart.get_rect(center=(self.width // 2, self.height // 2 + 60))
        self.screen.blit(restart, restart_rect)

    def _render_victory(self) -> None:
        """Renderiza overlay de Vitória."""
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        text = self.font_large.render("VITÓRIA!", True, Colors.GREEN)
        rect = text.get_rect(center=(self.width // 2, self.height // 2 - 40))
        self.screen.blit(text, rect)

        score_text = self.font_medium.render(
            f"Score Final: {self.score}", True, Colors.WHITE
        )
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
        self.screen.blit(score_text, score_rect)

        restart = self.font_small.render(
            "R = Jogar de novo  |  ESC = Sair", True, Colors.LIGHT_GRAY
        )
        restart_rect = restart.get_rect(center=(self.width // 2, self.height // 2 + 60))
        self.screen.blit(restart, restart_rect)

    def _render_pause(self) -> None:
        """Renderiza overlay de Pausa."""
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self.screen.blit(overlay, (0, 0))

        text = self.font_large.render("PAUSA", True, Colors.YELLOW)
        rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, rect)

        hint = self.font_small.render("P = Continuar", True, Colors.LIGHT_GRAY)
        hint_rect = hint.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(hint, hint_rect)

    def run(self) -> None:
        """Loop principal do jogo."""
        while self.running:
            self.dt = self.clock.tick(self.fps) / 1000.0
            self.handle_events()
            self.update(self.dt)
            self.render()

        self.on_quit()
        pygame.quit()
        sys.exit()
