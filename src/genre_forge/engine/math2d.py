"""
math2d.py — Utilitários matemáticos 2D para jogos Pygame.

Classe Vector2D e funções auxiliares de geometria.
"""

import math
from typing import Tuple


class Vector2D:
    """
    Vetor 2D simples com operações matemáticas.

    Uso:
        pos = Vector2D(100, 200)
        vel = Vector2D(1, 0).normalize() * 300
        pos += vel * dt
    """

    __slots__ = ("x", "y")

    def __init__(self, x: float = 0, y: float = 0):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self) -> str:
        return f"Vector2D({self.x:.2f}, {self.y:.2f})"

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: "Vector2D") -> "Vector2D":
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x - other.x, self.y - other.y)

    def __isub__(self, other: "Vector2D") -> "Vector2D":
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, scalar: float) -> "Vector2D":
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector2D":
        return self.__mul__(scalar)

    def __imul__(self, scalar: float) -> "Vector2D":
        self.x *= scalar
        self.y *= scalar
        return self

    def __truediv__(self, scalar: float) -> "Vector2D":
        if scalar == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / scalar, self.y / scalar)

    def __neg__(self) -> "Vector2D":
        return Vector2D(-self.x, -self.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return False
        return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9

    @property
    def length(self) -> float:
        """Magnitude do vetor."""
        return math.sqrt(self.x * self.x + self.y * self.y)

    @property
    def length_squared(self) -> float:
        """Magnitude ao quadrado (evita sqrt, mais rápido)."""
        return self.x * self.x + self.y * self.y

    def normalize(self) -> "Vector2D":
        """Retorna vetor unitário (mesma direção, magnitude 1)."""
        mag = self.length
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)

    def dot(self, other: "Vector2D") -> float:
        """Produto escalar."""
        return self.x * other.x + self.y * other.y

    def cross(self, other: "Vector2D") -> float:
        """Produto vetorial 2D (retorna escalar)."""
        return self.x * other.y - self.y * other.x

    def distance_to(self, other: "Vector2D") -> float:
        """Distância até outro vetor."""
        return (self - other).length

    def angle(self) -> float:
        """Ângulo do vetor em radianos."""
        return math.atan2(self.y, self.x)

    def angle_degrees(self) -> float:
        """Ângulo do vetor em graus."""
        return math.degrees(self.angle())

    def rotate(self, angle_rad: float) -> "Vector2D":
        """Rotaciona o vetor por um ângulo em radianos."""
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return Vector2D(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a,
        )

    def lerp(self, other: "Vector2D", t: float) -> "Vector2D":
        """Interpolação linear entre este vetor e outro."""
        t = max(0.0, min(1.0, t))
        return self + (other - self) * t

    def clamp(self, min_x: float, min_y: float, max_x: float, max_y: float) -> "Vector2D":
        """Restringe o vetor aos limites dados."""
        return Vector2D(
            max(min_x, min(self.x, max_x)),
            max(min_y, min(self.y, max_y)),
        )

    def to_tuple(self) -> Tuple[float, float]:
        """Converte para tupla (x, y)."""
        return (self.x, self.y)

    def to_int_tuple(self) -> Tuple[int, int]:
        """Converte para tupla de inteiros (para posições de pixel)."""
        return (int(self.x), int(self.y))

    def copy(self) -> "Vector2D":
        """Retorna cópia do vetor."""
        return Vector2D(self.x, self.y)

    @staticmethod
    def from_angle(angle_rad: float, magnitude: float = 1.0) -> "Vector2D":
        """Cria vetor a partir de ângulo e magnitude."""
        return Vector2D(
            math.cos(angle_rad) * magnitude,
            math.sin(angle_rad) * magnitude,
        )

    @staticmethod
    def random_unit() -> "Vector2D":
        """Retorna vetor unitário em direção aleatória."""
        import random
        angle = random.uniform(0, 2 * math.pi)
        return Vector2D.from_angle(angle)


# --- Funções auxiliares ---

def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Distância entre dois pontos (tuplas)."""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx * dx + dy * dy)


def lerp(a: float, b: float, t: float) -> float:
    """Interpolação linear entre dois valores."""
    return a + (b - a) * max(0.0, min(1.0, t))


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Restringe valor aos limites."""
    return max(min_val, min(value, max_val))


def angle_between(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Ângulo em radianos de p1 para p2."""
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])
