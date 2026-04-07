# PROTOTYPE - NOT FOR PRODUCTION
# Question: Does the core loop of descend -> scavenge -> escape feel engaging?
# Date: 2026-04-07

# 电梯是唯一安全的地方。也许是。
# The elevator is the only safe place. Maybe.

import pygame
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    ELEVATOR_TILE_SIZE, ELEVATOR_GRID_COLS, ELEVATOR_GRID_ROWS,
    GRID_ORIGIN_X, GRID_ORIGIN_Y,
    C_BLACK, C_DARK, C_ELEVATOR_BG, C_ELEVATOR_TILE,
    C_WHITE, C_LIGHT_GRAY, C_MID_GRAY, C_DARK_GRAY,
    C_RED, C_RED_BRIGHT, C_AMBER,
    PANEL_X, PANEL_WIDTH,
    STATE_DESCEND,
)
from src.player import Player
from src.inventory import Inventory
from src.ui.hud import render_text, Button, draw_inventory_panel


# Elevator grid origin — placed left-centre of screen
_EL_ORIGIN_X = 30
_EL_ORIGIN_Y = 120
_EL_WIDTH    = ELEVATOR_GRID_COLS * ELEVATOR_TILE_SIZE   # 192
_EL_HEIGHT   = ELEVATOR_GRID_ROWS * ELEVATOR_TILE_SIZE   # 192


class ElevatorScene:
    """
    The hub. Between floors. Breathe.
    你回来了。但你还会再下去。
    You came back. But you will descend again.
    """

    def __init__(self, inventory: Inventory, floor_number: int):
        self.inventory    = inventory
        self.floor_number = floor_number

        # Player spawns at the centre of the 2×2 elevator.
        spawn_x = _EL_ORIGIN_X + _EL_WIDTH  // 2
        spawn_y = _EL_ORIGIN_Y + _EL_HEIGHT // 2
        self.player = Player(spawn_x, spawn_y)

        # Descend button — big, prominent
        btn_x = SCREEN_WIDTH // 2 + 30
        btn_y = SCREEN_HEIGHT - 120
        self.descend_btn = Button(btn_x, btn_y, 220, 52,
                                  "下到下一层", "[DESCEND]")

        # Atmosphere text changes depending on floor number
        self._atmosphere = self._pick_atmosphere()

        # Door animation state
        self.door_closing  = False
        self.door_alpha    = 0    # 0 = transparent, 255 = fully closed (black)
        self._next_state   = None

        # Surface used for elevator door overlay
        self._overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    def _pick_atmosphere(self) -> str:
        lines = [
            "电梯门缓缓关闭。",
            "The motor hums. Going down.",
            "你听到了什么吗？",
            "B-" + str(self.floor_number) + "层。更深了。",
            "Don't think. Just move.",
            "回来的人越来越少。",
        ]
        import random
        return random.choice(lines)

    # ── Public API ─────────────────────────────────────────────────────────────

    def on_enter(self, came_from_floor: bool = False):
        """Called every time the scene becomes active."""
        self.door_closing = False
        self.door_alpha   = 0
        self._atmosphere  = self._pick_atmosphere()

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Return next state key or None."""
        self.descend_btn.update(pygame.mouse.get_pos())
        if self.descend_btn.is_clicked(event) and not self.door_closing:
            self._start_door_close()
        return None

    def update(self, dt: float, keys) -> str | None:
        """Return next state or None to stay."""
        if not self.door_closing:
            self.player.handle_input_elevator(keys)
        else:
            # Animate door closing
            self.door_alpha += 6
            if self.door_alpha >= 255:
                self.door_alpha = 255
                return STATE_DESCEND

        self.descend_btn.update(pygame.mouse.get_pos())
        return None

    def draw(self, surface: pygame.Surface):
        surface.fill(C_DARK)
        self._draw_title(surface)
        self._draw_elevator_room(surface)
        self._draw_right_panel(surface)
        self.player.draw(surface)
        self._draw_door_overlay(surface)

    # ── Private drawing ────────────────────────────────────────────────────────

    def _draw_title(self, surface: pygame.Surface):
        render_text(surface, "垂直深渊  |  VERTICAL ABYSS",
                    SCREEN_WIDTH // 2, 22,
                    size=20, color=C_LIGHT_GRAY, bold=True, center=True)
        pygame.draw.line(surface, C_DARK_GRAY,
                         (0, 42), (SCREEN_WIDTH, 42), 1)

    def _draw_elevator_room(self, surface: pygame.Surface):
        ox = _EL_ORIGIN_X
        oy = _EL_ORIGIN_Y
        ts = ELEVATOR_TILE_SIZE

        # Draw floor tiles
        for row in range(ELEVATOR_GRID_ROWS):
            for col in range(ELEVATOR_GRID_COLS):
                rect = pygame.Rect(ox + col * ts, oy + row * ts, ts - 1, ts - 1)
                pygame.draw.rect(surface, C_ELEVATOR_TILE, rect)
                pygame.draw.rect(surface, (55, 55, 72), rect, 1)

        # Room border
        room_rect = pygame.Rect(ox - 2, oy - 2, _EL_WIDTH + 4, _EL_HEIGHT + 4)
        pygame.draw.rect(surface, C_MID_GRAY, room_rect, 2)

        # Atmosphere label below room
        render_text(surface, self._atmosphere,
                    ox, oy + _EL_HEIGHT + 12,
                    size=12, color=(100, 100, 115))

        # "ELEVATOR" label above
        render_text(surface, "[ ELEVATOR ]",
                    ox + _EL_WIDTH // 2, oy - 18,
                    size=11, color=C_MID_GRAY, center=True)

    def _draw_right_panel(self, surface: pygame.Surface):
        panel_x = _EL_ORIGIN_X + _EL_WIDTH + 30
        panel_y = 55

        # Floor depth indicator
        render_text(surface, f"Floor: B-{self.floor_number}",
                    panel_x, panel_y, size=16, color=C_AMBER, bold=True)
        pygame.draw.line(surface, C_DARK_GRAY,
                         (panel_x, panel_y + 22),
                         (SCREEN_WIDTH - 10, panel_y + 22), 1)

        # Inventory
        inv_lines = self.inventory.display_lines()
        draw_inventory_panel(surface, inv_lines,
                             panel_x, panel_y + 32,
                             SCREEN_WIDTH - panel_x - 10,
                             label="INVENTORY")

        # Descend button
        self.descend_btn.draw(surface)

        # Hint text below button
        hint_y = self.descend_btn.rect.bottom + 10
        render_text(surface, "每一层都更深。",
                    self.descend_btn.rect.centerx, hint_y,
                    size=11, color=(80, 80, 95), center=True)
        render_text(surface, "Every floor goes deeper.",
                    self.descend_btn.rect.centerx, hint_y + 16,
                    size=10, color=(65, 65, 80), center=True)

    def _draw_door_overlay(self, surface: pygame.Surface):
        """Black fade simulating elevator doors sliding shut."""
        if self.door_alpha <= 0:
            return
        self._overlay.fill((0, 0, 0, 0))
        # Split-door effect: two rectangles closing from left and right
        half = SCREEN_WIDTH // 2
        alpha = min(255, self.door_alpha)
        # Left door panel
        pygame.draw.rect(self._overlay, (0, 0, 0, alpha),
                         (0, 0, half * alpha // 255, SCREEN_HEIGHT))
        # Right door panel
        right_w = half * alpha // 255
        pygame.draw.rect(self._overlay, (0, 0, 0, alpha),
                         (SCREEN_WIDTH - right_w, 0, right_w, SCREEN_HEIGHT))
        surface.blit(self._overlay, (0, 0))

    def _start_door_close(self):
        self.door_closing = True
        self.door_alpha   = 0
