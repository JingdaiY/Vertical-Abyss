# PROTOTYPE - NOT FOR PRODUCTION
# Question: Does the core loop of descend -> scavenge -> escape feel engaging?
# Date: 2026-04-07

# 60秒。门打开了。不要犹豫。
# The clock starts the moment the doors part.

import pygame
import math
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    FLOOR_TILE_SIZE, FLOOR_GRID_COLS, FLOOR_GRID_ROWS,
    GRID_ORIGIN_X, GRID_ORIGIN_Y,
    VISION_RADIUS,
    C_BLACK, C_DARK, C_TILE_FLOOR, C_TILE_WALL, C_TILE_EXIT,
    C_WHITE, C_LIGHT_GRAY, C_MID_GRAY, C_DARK_GRAY,
    C_RED, C_RED_BRIGHT, C_AMBER, C_GREEN,
    C_PLAYER,
    ITEMS,
    PANEL_X, PANEL_WIDTH,
    STATE_ELEVATOR, STATE_DEATH,
    FLOOR_TIME_LIMIT,
)
from src.player import Player
from src.inventory import Inventory
from src.timer import CountdownTimer
from src.floor_gen import FloorData, generate_floor
from src.ui.hud import (
    render_text, draw_timer_bar, draw_inventory_panel, Button
)

_TS = FLOOR_TILE_SIZE   # shorthand


class FloorScene:
    """
    The scavenging floor. This is the dangerous part.
    时间在流逝。找到你需要的，然后离开。
    Time flows. Find what you need and leave.
    """

    def __init__(self, inventory: Inventory, floor_number: int):
        self.inventory    = inventory
        self.floor_number = floor_number
        self.floor_data   = generate_floor(floor_number)
        self.timer        = CountdownTimer(FLOOR_TIME_LIMIT)

        # Player spawns near the exit (top of grid, row 1 col 1)
        spawn_px = GRID_ORIGIN_X + 1 * _TS + _TS // 2
        spawn_py = GRID_ORIGIN_Y + 1 * _TS + _TS // 2
        self.player = Player(spawn_px, spawn_py)

        # HUD hint for nearby items
        self._item_nearby: str | None = None  # item_key if player is adjacent
        self._near_exit   = False

        # Fade-in overlay (door opening animation — lights come up)
        self._fade_alpha  = 255
        self._fading_in   = True
        self._overlay     = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._overlay.fill(C_BLACK)

        # Pre-render fog overlay (64×64 reusable surface)
        self._fog_full = pygame.Surface((_TS, _TS))
        self._fog_full.fill(C_BLACK)
        self._fog_dim  = pygame.Surface((_TS, _TS))
        self._fog_dim.fill(C_BLACK)
        self._fog_dim.set_alpha(140)

        self._done = False  # True when scene should transition out

    # ── Public API ─────────────────────────────────────────────────────────────

    def on_enter(self):
        self.timer.start()
        self._fading_in  = True
        self._fade_alpha = 255
        self._done       = False
        # Update fog visibility from spawn point
        self._update_fog(1, 1)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        # E key — pick up nearby item
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if self._item_nearby is not None:
                col, row = self.player.tile_pos(_TS, GRID_ORIGIN_X, GRID_ORIGIN_Y)
                # Check adjacent tiles for items
                picked = self._try_pick_item(col, row)
                if picked:
                    self.inventory.add(picked)
        return None

    def update(self, dt: float, keys) -> str | None:
        # Fade in animation
        if self._fading_in:
            self._fade_alpha -= 8
            if self._fade_alpha <= 0:
                self._fade_alpha = 0
                self._fading_in  = False

        if self._done:
            return None  # Handled by game.py after a delay

        # Player movement
        self.player.handle_input_floor(
            keys,
            self.floor_data.walls,
            _TS,
            GRID_ORIGIN_X, GRID_ORIGIN_Y,
            FLOOR_GRID_COLS, FLOOR_GRID_ROWS,
        )

        # Update fog of war
        col, row = self.player.tile_pos(_TS, GRID_ORIGIN_X, GRID_ORIGIN_Y)
        self._update_fog(col, row)

        # Detect nearby items (for E-key prompt)
        self._item_nearby = self._find_nearby_item(col, row)

        # Detect exit
        self._near_exit = (col, row) in self.floor_data.exit_tiles
        if self._near_exit:
            self.timer.stop()
            return STATE_ELEVATOR

        # Timer tick
        self.timer.tick(dt)
        if self.timer.is_expired():
            return STATE_DEATH

        return None

    def draw(self, surface: pygame.Surface):
        surface.fill(C_DARK)
        self._draw_top_bar(surface)
        self._draw_grid(surface)
        self._draw_fog(surface)
        self.player.draw(surface)
        self._draw_right_panel(surface)
        self._draw_pickup_hint(surface)

        # Fade overlay (door opening / closing)
        if self._fade_alpha > 0:
            self._overlay.set_alpha(self._fade_alpha)
            surface.blit(self._overlay, (0, 0))

    # ── Fog of war ─────────────────────────────────────────────────────────────

    def _update_fog(self, player_col: int, player_row: int):
        """
        Mark tiles within VISION_RADIUS as revealed.
        Uses squared distance for speed — no sqrt needed.
        """
        fd = self.floor_data
        r2 = VISION_RADIUS * VISION_RADIUS
        for row in range(FLOOR_GRID_ROWS):
            for col in range(FLOOR_GRID_COLS):
                d2 = (col - player_col) ** 2 + (row - player_row) ** 2
                if d2 <= r2:
                    fd.revealed[row][col] = True

    def _is_visible(self, col: int, row: int, player_col: int, player_row: int) -> bool:
        d2 = (col - player_col) ** 2 + (row - player_row) ** 2
        return d2 <= VISION_RADIUS * VISION_RADIUS

    # ── Drawing helpers ────────────────────────────────────────────────────────

    def _draw_top_bar(self, surface: pygame.Surface):
        # Background strip
        pygame.draw.rect(surface, (12, 12, 18), (0, 0, SCREEN_WIDTH, GRID_ORIGIN_Y - 2))
        pygame.draw.line(surface, C_DARK_GRAY, (0, GRID_ORIGIN_Y - 2), (SCREEN_WIDTH, GRID_ORIGIN_Y - 2), 1)

        env = self.floor_data.environment
        # Floor label
        render_text(surface, f"B-{self.floor_number}",
                    GRID_ORIGIN_X + 4, 8, size=14, color=C_AMBER, bold=True)

        # Timer bar — centred in the top bar, above the grid
        bar_w = 200
        bar_x = GRID_ORIGIN_X + (FLOOR_GRID_COLS * _TS - bar_w) // 2
        bar_y = 10
        draw_timer_bar(surface,
                       self.timer.seconds_left(),
                       self.timer.fraction_remaining(),
                       self.timer.is_urgent(),
                       bar_x, bar_y, bar_w, 26)

        # Environment name (right side of bar)
        render_text(surface, env["name_cn"],
                    bar_x + bar_w + 12, 8, size=13, color=C_LIGHT_GRAY)
        render_text(surface, env["name_en"],
                    bar_x + bar_w + 12, 24, size=10, color=C_MID_GRAY)

    def _draw_grid(self, surface: pygame.Surface):
        fd   = self.floor_data
        env  = fd.environment
        pcol, prow = self.player.tile_pos(_TS, GRID_ORIGIN_X, GRID_ORIGIN_Y)
        tint = env.get("floor_tint", (35, 35, 45))

        for row in range(FLOOR_GRID_ROWS):
            for col in range(FLOOR_GRID_COLS):
                x = GRID_ORIGIN_X + col * _TS
                y = GRID_ORIGIN_Y + row * _TS
                rect = pygame.Rect(x, y, _TS - 1, _TS - 1)

                tile_key = (col, row)

                if tile_key in fd.walls:
                    base_color = C_TILE_WALL
                elif tile_key in fd.exit_tiles:
                    base_color = C_TILE_EXIT
                else:
                    base_color = tint

                pygame.draw.rect(surface, base_color, rect)

                # Item dot on tile (only if revealed)
                if fd.revealed[row][col] and tile_key in fd.items:
                    item_key = fd.items[tile_key]
                    _, _, item_color = ITEMS[item_key]
                    center_x = x + _TS // 2
                    center_y = y + _TS // 2
                    pygame.draw.circle(surface, item_color,
                                       (center_x, center_y), 6)
                    pygame.draw.circle(surface, C_WHITE,
                                       (center_x, center_y), 6, 1)

                # Exit zone marker arrows
                if tile_key in fd.exit_tiles:
                    self._draw_exit_marker(surface, x, y)

                # Subtle grid line
                pygame.draw.rect(surface, (col * 2 % 10 + 25, 25, 30), rect, 1)

    def _draw_exit_marker(self, surface: pygame.Surface, x: int, y: int):
        """Draw a simple upward arrow on exit tiles."""
        cx = x + _TS // 2
        cy = y + _TS // 2
        pts = [
            (cx,       cy - 10),
            (cx - 7,   cy + 4),
            (cx - 3,   cy + 4),
            (cx - 3,   cy + 10),
            (cx + 3,   cy + 10),
            (cx + 3,   cy + 4),
            (cx + 7,   cy + 4),
        ]
        pygame.draw.polygon(surface, (80, 200, 80), pts)

    def _draw_fog(self, surface: pygame.Surface):
        """
        Overlay fog of war:
        - Unrevealed: full black tile
        - Revealed but not currently visible: dark semi-transparent overlay
        """
        fd = self.floor_data
        pcol, prow = self.player.tile_pos(_TS, GRID_ORIGIN_X, GRID_ORIGIN_Y)

        for row in range(FLOOR_GRID_ROWS):
            for col in range(FLOOR_GRID_COLS):
                x = GRID_ORIGIN_X + col * _TS
                y = GRID_ORIGIN_Y + row * _TS

                if not fd.revealed[row][col]:
                    # Never seen — pure black
                    pygame.draw.rect(surface, C_BLACK, (x, y, _TS - 1, _TS - 1))
                elif not self._is_visible(col, row, pcol, prow):
                    # Seen but not currently lit — dim overlay
                    dim_surf = pygame.Surface((_TS - 1, _TS - 1), pygame.SRCALPHA)
                    dim_surf.fill((0, 0, 0, 140))
                    surface.blit(dim_surf, (x, y))

    def _draw_right_panel(self, surface: pygame.Surface):
        inv_lines = self.inventory.display_lines()
        draw_inventory_panel(surface, inv_lines,
                             PANEL_X, GRID_ORIGIN_Y,
                             PANEL_WIDTH,
                             label="INVENTORY")

        # Controls hint
        hint_y = GRID_ORIGIN_Y + FLOOR_GRID_ROWS * _TS - 60
        render_text(surface, "[E] Pick Up", PANEL_X, hint_y, size=12, color=C_MID_GRAY)
        render_text(surface, "Return to Exit", PANEL_X, hint_y + 18, size=12, color=C_MID_GRAY)
        render_text(surface, "(top-left tiles)", PANEL_X, hint_y + 34, size=11, color=C_DARK_GRAY)

        # Atmosphere description
        env = self.floor_data.environment
        desc_y = SCREEN_HEIGHT - 95
        render_text(surface, env["desc_cn"],
                    PANEL_X, desc_y, size=11, color=(90, 90, 105))
        # Wrap English desc at ~30 chars
        desc_en = env["desc_en"]
        words   = desc_en.split()
        line    = ""
        en_y    = desc_y + 32
        for word in words:
            test = line + word + " "
            if len(test) > 30:
                render_text(surface, line.strip(), PANEL_X, en_y, size=10, color=(65, 65, 80))
                en_y += 14
                line  = word + " "
            else:
                line = test
        if line.strip():
            render_text(surface, line.strip(), PANEL_X, en_y, size=10, color=(65, 65, 80))

    def _draw_pickup_hint(self, surface: pygame.Surface):
        if self._item_nearby:
            _, name_en, color = ITEMS[self._item_nearby]
            name_cn = ITEMS[self._item_nearby][0]
            msg = f"[E]  {name_cn}  {name_en}"
            render_text(surface, msg,
                        GRID_ORIGIN_X + FLOOR_GRID_COLS * _TS // 2,
                        GRID_ORIGIN_Y + FLOOR_GRID_ROWS * _TS + 8,
                        size=13, color=color, bold=True, center=True)

        if self._near_exit:
            render_text(surface, "— EXIT —  Returning...",
                        GRID_ORIGIN_X + FLOOR_GRID_COLS * _TS // 2,
                        GRID_ORIGIN_Y + FLOOR_GRID_ROWS * _TS + 8,
                        size=13, color=C_GREEN, bold=True, center=True)

    # ── Item interaction ───────────────────────────────────────────────────────

    def _find_nearby_item(self, player_col: int, player_row: int) -> str | None:
        """Return item key if there's an item on the player's current tile or adjacent."""
        fd = self.floor_data
        for dc in range(-1, 2):
            for dr in range(-1, 2):
                tile = (player_col + dc, player_row + dr)
                if tile in fd.items:
                    return fd.items[tile]
        return None

    def _try_pick_item(self, player_col: int, player_row: int) -> str | None:
        """
        Pick up an item on or adjacent to the player tile.
        Returns the item key if picked, None otherwise.
        """
        fd = self.floor_data
        for dc in range(-1, 2):
            for dr in range(-1, 2):
                tile = (player_col + dc, player_row + dr)
                if tile in fd.items:
                    key = fd.items.pop(tile)
                    return key
        return None
