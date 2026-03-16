"""
collision.py — Detecção de colisão 2D para jogos Pygame.

Suporta AABB (retângulos), círculos e grupos de sprites.
"""

import math
from typing import List, Optional, Tuple

import pygame


def check_aabb(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """
    Verifica colisão entre dois retângulos (AABB).

    Args:
        rect1: Primeiro retângulo
        rect2: Segundo retângulo

    Returns:
        True se houver colisão
    """
    return rect1.colliderect(rect2)


def check_circle(
    center1: Tuple[float, float],
    radius1: float,
    center2: Tuple[float, float],
    radius2: float,
) -> bool:
    """
    Verifica colisão entre dois círculos.

    Args:
        center1: Centro do primeiro círculo (x, y)
        radius1: Raio do primeiro círculo
        center2: Centro do segundo círculo (x, y)
        radius2: Raio do segundo círculo

    Returns:
        True se houver colisão
    """
    dx = center1[0] - center2[0]
    dy = center1[1] - center2[1]
    dist_sq = dx * dx + dy * dy
    min_dist = radius1 + radius2
    return dist_sq <= min_dist * min_dist


def check_circle_rect(
    circle_center: Tuple[float, float],
    circle_radius: float,
    rect: pygame.Rect,
) -> bool:
    """
    Verifica colisão entre um círculo e um retângulo.

    Args:
        circle_center: Centro do círculo (x, y)
        circle_radius: Raio do círculo
        rect: Retângulo

    Returns:
        True se houver colisão
    """
    # Ponto mais próximo do retângulo ao centro do círculo
    closest_x = max(rect.left, min(circle_center[0], rect.right))
    closest_y = max(rect.top, min(circle_center[1], rect.bottom))

    dx = circle_center[0] - closest_x
    dy = circle_center[1] - closest_y

    return (dx * dx + dy * dy) <= (circle_radius * circle_radius)


def check_point_rect(
    point: Tuple[float, float],
    rect: pygame.Rect,
) -> bool:
    """Verifica se um ponto está dentro de um retângulo."""
    return rect.collidepoint(int(point[0]), int(point[1]))


def check_point_circle(
    point: Tuple[float, float],
    center: Tuple[float, float],
    radius: float,
) -> bool:
    """Verifica se um ponto está dentro de um círculo."""
    dx = point[0] - center[0]
    dy = point[1] - center[1]
    return (dx * dx + dy * dy) <= (radius * radius)


def check_groups(
    group_a: List[pygame.sprite.Sprite],
    group_b: List[pygame.sprite.Sprite],
    use_circle: bool = False,
) -> List[Tuple[pygame.sprite.Sprite, pygame.sprite.Sprite]]:
    """
    Verifica colisões entre dois grupos de sprites.

    Args:
        group_a: Primeiro grupo de sprites
        group_b: Segundo grupo de sprites
        use_circle: Se True, usa colisão circular (requer atributo 'radius')

    Returns:
        Lista de pares (sprite_a, sprite_b) que colidiram
    """
    collisions = []

    for sprite_a in group_a:
        for sprite_b in group_b:
            if use_circle:
                # Colisão circular — sprites devem ter atributo 'radius'
                r_a = getattr(sprite_a, "radius", sprite_a.rect.width // 2)
                r_b = getattr(sprite_b, "radius", sprite_b.rect.width // 2)
                center_a = sprite_a.rect.center
                center_b = sprite_b.rect.center
                if check_circle(center_a, r_a, center_b, r_b):
                    collisions.append((sprite_a, sprite_b))
            else:
                # Colisão AABB
                if sprite_a.rect.colliderect(sprite_b.rect):
                    collisions.append((sprite_a, sprite_b))

    return collisions


def check_bounds(
    rect: pygame.Rect,
    screen_width: int,
    screen_height: int,
) -> dict:
    """
    Verifica se um rect está fora dos limites da tela.

    Returns:
        Dict com "left", "right", "top", "bottom" (True se fora)
    """
    return {
        "left": rect.left < 0,
        "right": rect.right > screen_width,
        "top": rect.top < 0,
        "bottom": rect.bottom > screen_height,
        "any": (
            rect.left < 0
            or rect.right > screen_width
            or rect.top < 0
            or rect.bottom > screen_height
        ),
    }


def clamp_to_bounds(
    rect: pygame.Rect,
    screen_width: int,
    screen_height: int,
) -> pygame.Rect:
    """Restringe o rect para ficar dentro dos limites da tela."""
    rect = rect.copy()
    if rect.left < 0:
        rect.left = 0
    if rect.right > screen_width:
        rect.right = screen_width
    if rect.top < 0:
        rect.top = 0
    if rect.bottom > screen_height:
        rect.bottom = screen_height
    return rect
