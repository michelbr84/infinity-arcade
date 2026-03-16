"""
effects.py — Efeitos visuais simples para jogos Pygame.

Sistema de partículas e efeitos de flash/shake.
"""

import math
import random
from typing import List, Optional, Tuple

import pygame


class Particle:
    """Uma partícula individual."""

    __slots__ = ("x", "y", "vx", "vy", "color", "size", "life", "max_life", "gravity")

    def __init__(
        self,
        x: float,
        y: float,
        vx: float,
        vy: float,
        color: Tuple[int, int, int],
        size: float = 3,
        life: float = 1.0,
        gravity: float = 0,
    ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life
        self.gravity = gravity

    @property
    def alive(self) -> bool:
        return self.life > 0

    def update(self, dt: float) -> None:
        """Atualiza posição e vida."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt
        self.life -= dt

    def render(self, screen: pygame.Surface) -> None:
        """Renderiza a partícula com fade-out."""
        if not self.alive:
            return

        alpha = max(0, self.life / self.max_life)
        current_size = max(1, int(self.size * alpha))

        # Cor com fade
        r = min(255, int(self.color[0] * alpha))
        g = min(255, int(self.color[1] * alpha))
        b = min(255, int(self.color[2] * alpha))

        pygame.draw.circle(
            screen, (r, g, b),
            (int(self.x), int(self.y)),
            current_size,
        )


class ParticleEmitter:
    """
    Emissor de partículas para explosões, trails, etc.

    Uso:
        emitter = ParticleEmitter()

        # Explosão
        emitter.emit_burst(x=400, y=300, count=20, color=(255, 100, 0))

        # No loop:
        emitter.update(dt)
        emitter.render(screen)
    """

    def __init__(self, max_particles: int = 500):
        self.particles: List[Particle] = []
        self.max_particles = max_particles

    def emit_burst(
        self,
        x: float,
        y: float,
        count: int = 15,
        color: Tuple[int, int, int] = (255, 200, 50),
        speed_range: Tuple[float, float] = (50, 200),
        size_range: Tuple[float, float] = (2, 5),
        life_range: Tuple[float, float] = (0.3, 1.0),
        gravity: float = 100,
    ) -> None:
        """
        Emite uma explosão de partículas.

        Args:
            x, y: Posição central da emissão
            count: Número de partículas
            color: Cor base (será variada levemente)
            speed_range: Velocidade mín/máx
            size_range: Tamanho mín/máx
            life_range: Vida mín/máx em segundos
            gravity: Aceleração para baixo
        """
        for _ in range(min(count, self.max_particles - len(self.particles))):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*speed_range)

            # Variação de cor
            r = min(255, max(0, color[0] + random.randint(-30, 30)))
            g = min(255, max(0, color[1] + random.randint(-30, 30)))
            b = min(255, max(0, color[2] + random.randint(-30, 30)))

            particle = Particle(
                x=x,
                y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                color=(r, g, b),
                size=random.uniform(*size_range),
                life=random.uniform(*life_range),
                gravity=gravity,
            )
            self.particles.append(particle)

    def emit_trail(
        self,
        x: float,
        y: float,
        dx: float = 0,
        dy: float = 0,
        color: Tuple[int, int, int] = (100, 200, 255),
        count: int = 2,
    ) -> None:
        """Emite partículas de trail (rastro) na direção oposta ao movimento."""
        for _ in range(count):
            spread = 30
            particle = Particle(
                x=x + random.uniform(-3, 3),
                y=y + random.uniform(-3, 3),
                vx=-dx * 0.3 + random.uniform(-spread, spread),
                vy=-dy * 0.3 + random.uniform(-spread, spread),
                color=color,
                size=random.uniform(1, 3),
                life=random.uniform(0.1, 0.4),
                gravity=0,
            )
            self.particles.append(particle)

    def update(self, dt: float) -> None:
        """Atualiza e remove partículas mortas."""
        for p in self.particles:
            p.update(dt)

        self.particles = [p for p in self.particles if p.alive]

    def render(self, screen: pygame.Surface) -> None:
        """Renderiza todas as partículas."""
        for p in self.particles:
            p.render(screen)

    def clear(self) -> None:
        """Remove todas as partículas."""
        self.particles.clear()

    @property
    def count(self) -> int:
        """Número de partículas ativas."""
        return len(self.particles)


class ScreenShake:
    """
    Efeito de screen shake (tremor de tela).

    Uso:
        shake = ScreenShake()
        shake.trigger(intensity=8, duration=0.3)

        # No render:
        offset_x, offset_y = shake.get_offset()
        screen.blit(game_surface, (offset_x, offset_y))
        shake.update(dt)
    """

    def __init__(self):
        self.intensity = 0
        self.duration = 0
        self.timer = 0

    def trigger(self, intensity: float = 5, duration: float = 0.2) -> None:
        """Inicia o efeito de shake."""
        self.intensity = intensity
        self.duration = duration
        self.timer = duration

    def update(self, dt: float) -> None:
        """Atualiza o timer do shake."""
        if self.timer > 0:
            self.timer -= dt

    def get_offset(self) -> Tuple[int, int]:
        """Retorna offset (x, y) para aplicar à tela."""
        if self.timer <= 0:
            return (0, 0)

        progress = self.timer / self.duration
        current_intensity = self.intensity * progress

        return (
            int(random.uniform(-current_intensity, current_intensity)),
            int(random.uniform(-current_intensity, current_intensity)),
        )

    @property
    def active(self) -> bool:
        return self.timer > 0
