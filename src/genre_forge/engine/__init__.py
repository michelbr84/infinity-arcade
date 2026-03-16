"""Engine Layer — componentes reutilizáveis para jogos Pygame."""

from genre_forge.engine.core_loop import GameBase
from genre_forge.engine.math2d import Vector2D
from genre_forge.engine.collision import check_aabb, check_circle, check_groups
from genre_forge.engine.input_map import InputMap
from genre_forge.engine.scene_manager import SceneManager, Scene

__all__ = [
    "GameBase",
    "Vector2D",
    "check_aabb",
    "check_circle",
    "check_groups",
    "InputMap",
    "SceneManager",
    "Scene",
]
