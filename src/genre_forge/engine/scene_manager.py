"""
scene_manager.py — Gerenciador de cenas (stack-based) para jogos Pygame.

Permite navegar entre cenas: menu, gameplay, pause, game over, etc.
"""

from typing import Any, Dict, List, Optional

import pygame


class Scene:
    """
    Classe base para cenas do jogo.

    Override os métodos de ciclo de vida:
        on_enter(data) — ao entrar na cena
        on_exit() — ao sair da cena
        on_event(event) — processar evento
        on_update(dt) — lógica (dt em segundos)
        on_render(screen) — desenhar
    """

    def __init__(self, manager: "SceneManager"):
        self.manager = manager
        self.active = False

    def on_enter(self, data: Optional[Dict[str, Any]] = None) -> None:
        """Chamado quando a cena se torna ativa."""
        self.active = True

    def on_exit(self) -> None:
        """Chamado quando a cena é removida ou substituída."""
        self.active = False

    def on_pause(self) -> None:
        """Chamado quando outra cena é empilhada sobre esta."""
        pass

    def on_resume(self) -> None:
        """Chamado quando a cena acima é removida e esta volta ao topo."""
        pass

    def on_event(self, event: pygame.event.Event) -> None:
        """Processar evento pygame."""
        pass

    def on_update(self, dt: float) -> None:
        """Atualizar lógica (dt em segundos)."""
        pass

    def on_render(self, screen: pygame.Surface) -> None:
        """Renderizar na tela."""
        pass


class SceneManager:
    """
    Gerenciador de cenas com stack (pilha).

    Suporta:
        push(scene) — empilha nova cena
        pop() — remove cena do topo
        replace(scene) — substitui cena do topo
        current — cena ativa (topo da pilha)

    Uso:
        manager = SceneManager()
        manager.register("menu", MenuScene)
        manager.register("game", GameplayScene)
        manager.register("pause", PauseScene)

        manager.push("menu")

        # No game loop:
        manager.handle_event(event)
        manager.update(dt)
        manager.render(screen)
    """

    def __init__(self):
        self._scenes: Dict[str, type] = {}
        self._stack: List[Scene] = []

    def register(self, name: str, scene_class: type) -> None:
        """
        Registra uma classe de cena com um nome.

        Args:
            name: Nome identificador da cena
            scene_class: Classe que herda de Scene
        """
        self._scenes[name] = scene_class

    @property
    def current(self) -> Optional[Scene]:
        """Retorna a cena ativa (topo da pilha)."""
        return self._stack[-1] if self._stack else None

    @property
    def is_empty(self) -> bool:
        """Retorna True se não há cenas na pilha."""
        return len(self._stack) == 0

    def push(self, name: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Empilha uma nova cena.

        A cena anterior recebe on_pause().
        A nova cena recebe on_enter(data).
        """
        if name not in self._scenes:
            raise ValueError(f"Cena '{name}' não registrada. "
                             f"Disponíveis: {list(self._scenes.keys())}")

        # Pausa a cena atual
        if self._stack:
            self._stack[-1].on_pause()

        # Cria e empilha nova cena
        scene = self._scenes[name](self)
        self._stack.append(scene)
        scene.on_enter(data)

    def pop(self) -> Optional[Scene]:
        """
        Remove a cena do topo.

        A cena removida recebe on_exit().
        A cena abaixo (se existir) recebe on_resume().
        """
        if not self._stack:
            return None

        scene = self._stack.pop()
        scene.on_exit()

        if self._stack:
            self._stack[-1].on_resume()

        return scene

    def replace(self, name: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Substitui a cena do topo por uma nova.

        A cena antiga recebe on_exit().
        A nova cena recebe on_enter(data).
        """
        if self._stack:
            self._stack.pop().on_exit()

        scene = self._scenes[name](self)
        self._stack.append(scene)
        scene.on_enter(data)

    def clear(self) -> None:
        """Remove todas as cenas da pilha."""
        while self._stack:
            self._stack.pop().on_exit()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Delega evento para a cena ativa."""
        if self.current:
            self.current.on_event(event)

    def update(self, dt: float) -> None:
        """Atualiza a cena ativa."""
        if self.current:
            self.current.on_update(dt)

    def render(self, screen: pygame.Surface) -> None:
        """Renderiza a cena ativa (e opcionalmente as abaixo)."""
        if self.current:
            self.current.on_render(screen)
