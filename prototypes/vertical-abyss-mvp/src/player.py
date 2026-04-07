# PROTOTYPE - NOT FOR PRODUCTION
# Question: Does the core loop of descend -> scavenge -> escape feel engaging?
# Date: 2026-04-07

# 你只是一个点在黑暗中移动。但你是唯一移动的点。
# You are just a dot moving through darkness. But you are the only dot that moves.

import pygame
from src.constants import (
    PLAYER_SPEED, PLAYER_SIZE,
    FLOOR_TILE_SIZE, ELEVATOR_TILE_SIZE,
    FLOOR_GRID_COLS, FLOOR_GRID_ROWS,
    ELEVATOR_GRID_COLS, ELEVATOR_GRID_ROWS,
    GRID_ORIGIN_X, GRID_ORIGIN_Y,
    C_PLAYER,
)


class Player:
    """
    Pixel-position player entity. Knows nothing about game state — it just
    moves, collides, and reports its tile position.
    """

    def __init__(self, pixel_x: float, pixel_y: float):
        self.x = float(pixel_x)
        self.y = float(pixel_y)
        self.size = PLAYER_SIZE  # collision / draw radius

    # ── Movement ───────────────────────────────────────────────────────────────

    def handle_input_floor(self, keys, walls: set[tuple[int, int]], tile_size: int,
                           origin_x: int, origin_y: int, cols: int, rows: int):
        """
        Move on a floor grid. Walls is a set of (col, row) tuples that block movement.
        简单的AABB碰撞——快速，够用。
        Simple AABB collision — fast, good enough.
        """
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy -= PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy += PLAYER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += PLAYER_SPEED

        if dx != 0 and dy != 0:
            # Diagonal — normalise so speed doesn't compound.
            factor = PLAYER_SPEED / (PLAYER_SPEED * 1.4142)
            dx = int(dx * factor) or dx // abs(dx)
            dy = int(dy * factor) or dy // abs(dy)

        self._move_axis(dx, 0, walls, tile_size, origin_x, origin_y, cols, rows)
        self._move_axis(0, dy, walls, tile_size, origin_x, origin_y, cols, rows)

    def handle_input_elevator(self, keys):
        """
        Move freely within the 2×2 elevator room.
        The elevator is small — the bounds are tight. That is intentional.
        """
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy -= PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy += PLAYER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += PLAYER_SPEED

        # Constrain to 2×2 elevator grid (pixel bounds)
        min_x = GRID_ORIGIN_X + self.size
        max_x = GRID_ORIGIN_X + ELEVATOR_GRID_COLS * ELEVATOR_TILE_SIZE - self.size
        min_y = GRID_ORIGIN_Y + self.size
        max_y = GRID_ORIGIN_Y + ELEVATOR_GRID_ROWS * ELEVATOR_TILE_SIZE - self.size

        self.x = max(min_x, min(max_x, self.x + dx))
        self.y = max(min_y, min(max_y, self.y + dy))

    # ── Collision helper ───────────────────────────────────────────────────────

    def _move_axis(self, dx: int, dy: int, walls: set, tile_size: int,
                   origin_x: int, origin_y: int, cols: int, rows: int):
        """Attempt movement along one axis, revert if it enters a wall tile."""
        new_x = self.x + dx
        new_y = self.y + dy

        # Hard bounds — don't walk off the grid.
        half = self.size
        new_x = max(origin_x + half, min(origin_x + cols * tile_size - half, new_x))
        new_y = max(origin_y + half, min(origin_y + rows * tile_size - half, new_y))

        # Check each corner of the player square for wall collision.
        offsets = [(-half+1, -half+1), (half-1, -half+1),
                   (-half+1,  half-1), (half-1,  half-1)]
        blocked = False
        for ox, oy in offsets:
            px = new_x + ox
            py = new_y + oy
            col = int((px - origin_x) // tile_size)
            row = int((py - origin_y) // tile_size)
            if (col, row) in walls:
                blocked = True
                break

        if not blocked:
            self.x = new_x
            self.y = new_y

    # ── Tile position ──────────────────────────────────────────────────────────

    def tile_pos(self, tile_size: int, origin_x: int, origin_y: int) -> tuple[int, int]:
        """Return (col, row) of the tile the player centre occupies."""
        col = int((self.x - origin_x) // tile_size)
        row = int((self.y - origin_y) // tile_size)
        return col, row

    # ── Draw ───────────────────────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface):
        # Outer glow ring — barely visible, just enough to feel alive.
        pygame.draw.circle(surface, (80, 80, 140), (int(self.x), int(self.y)), self.size + 3)
        # Body
        pygame.draw.circle(surface, C_PLAYER, (int(self.x), int(self.y)), self.size)
        # Inner highlight
        pygame.draw.circle(surface, (230, 230, 255), (int(self.x) - 3, int(self.y) - 3), 5)
