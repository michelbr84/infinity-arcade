"""
input_map.py — Mapeamento configurável de input para ações de jogo.

Permite definir ações de jogo (ex.: "move_left", "shoot") e mapear teclas/mouse.
"""

from typing import Callable, Dict, List, Optional, Set

import pygame


class InputMap:
    """
    Mapeamento de teclas/mouse para ações de jogo.

    Uso:
        inputs = InputMap()
        inputs.bind("move_left", [pygame.K_a, pygame.K_LEFT])
        inputs.bind("move_right", [pygame.K_d, pygame.K_RIGHT])
        inputs.bind("shoot", [pygame.K_SPACE])

        # No update:
        if inputs.is_held("move_left"):
            player.x -= speed * dt
        if inputs.is_pressed("shoot"):
            player.shoot()

        # No loop de eventos:
        inputs.process_event(event)

        # No final do frame:
        inputs.end_frame()
    """

    def __init__(self):
        self._bindings: Dict[str, List[int]] = {}
        self._held_keys: Set[int] = set()
        self._pressed_keys: Set[int] = set()
        self._released_keys: Set[int] = set()
        self._mouse_pos = (0, 0)
        self._mouse_buttons: Set[int] = set()
        self._mouse_pressed: Set[int] = set()

    def bind(self, action: str, keys: List[int]) -> None:
        """
        Vincula uma ação a uma ou mais teclas.

        Args:
            action: Nome da ação (ex.: "move_left", "shoot")
            keys: Lista de pygame key constants
        """
        self._bindings[action] = keys

    def unbind(self, action: str) -> None:
        """Remove vinculação de uma ação."""
        self._bindings.pop(action, None)

    def process_event(self, event: pygame.event.Event) -> None:
        """
        Processa um evento pygame para atualizar estado do input.
        Chamar para cada evento no loop de eventos.
        """
        if event.type == pygame.KEYDOWN:
            self._held_keys.add(event.key)
            self._pressed_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            self._held_keys.discard(event.key)
            self._released_keys.add(event.key)
        elif event.type == pygame.MOUSEMOTION:
            self._mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._mouse_buttons.add(event.button)
            self._mouse_pressed.add(event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._mouse_buttons.discard(event.button)

    def is_held(self, action: str) -> bool:
        """Retorna True se alguma tecla da ação está sendo mantida pressionada."""
        keys = self._bindings.get(action, [])
        return any(k in self._held_keys for k in keys)

    def is_pressed(self, action: str) -> bool:
        """Retorna True se alguma tecla da ação foi pressionada NESTE frame."""
        keys = self._bindings.get(action, [])
        return any(k in self._pressed_keys for k in keys)

    def is_released(self, action: str) -> bool:
        """Retorna True se alguma tecla da ação foi solta NESTE frame."""
        keys = self._bindings.get(action, [])
        return any(k in self._released_keys for k in keys)

    def get_axis(self, negative_action: str, positive_action: str) -> float:
        """
        Retorna -1, 0 ou 1 com base em duas ações opostas.

        Útil para movimento:
            dx = inputs.get_axis("move_left", "move_right")
            dy = inputs.get_axis("move_up", "move_down")
        """
        value = 0.0
        if self.is_held(negative_action):
            value -= 1.0
        if self.is_held(positive_action):
            value += 1.0
        return value

    @property
    def mouse_pos(self) -> tuple:
        """Posição atual do mouse."""
        return self._mouse_pos

    def is_mouse_held(self, button: int = 1) -> bool:
        """Retorna True se botão do mouse está pressionado (1=esq, 2=meio, 3=dir)."""
        return button in self._mouse_buttons

    def is_mouse_pressed(self, button: int = 1) -> bool:
        """Retorna True se botão do mouse foi clicado NESTE frame."""
        return button in self._mouse_pressed

    def end_frame(self) -> None:
        """Limpa estados de frame único. Chamar no final de cada frame."""
        self._pressed_keys.clear()
        self._released_keys.clear()
        self._mouse_pressed.clear()

    def get_movement_vector(
        self,
        left: str = "move_left",
        right: str = "move_right",
        up: str = "move_up",
        down: str = "move_down",
    ) -> tuple:
        """
        Retorna vetor de movimento normalizado (dx, dy).

        Retorna tupla (dx, dy) onde cada componente é -1, 0 ou 1.
        """
        dx = self.get_axis(left, right)
        dy = self.get_axis(up, down)
        return (dx, dy)


def create_default_input_map() -> InputMap:
    """
    Cria InputMap com bindings padrão WASD + Setas + SPACE.

    Retorna InputMap configurado com:
        - move_left, move_right, move_up, move_down (WASD + setas)
        - action / shoot (SPACE)
        - interact (E)
        - inventory (I)
    """
    inputs = InputMap()

    # Movimento
    inputs.bind("move_left", [pygame.K_a, pygame.K_LEFT])
    inputs.bind("move_right", [pygame.K_d, pygame.K_RIGHT])
    inputs.bind("move_up", [pygame.K_w, pygame.K_UP])
    inputs.bind("move_down", [pygame.K_s, pygame.K_DOWN])

    # Ações
    inputs.bind("action", [pygame.K_SPACE])
    inputs.bind("shoot", [pygame.K_SPACE])
    inputs.bind("interact", [pygame.K_e])
    inputs.bind("inventory", [pygame.K_i])

    return inputs
