# PROTOTYPE - NOT FOR PRODUCTION
# Question: Does the core loop of descend -> scavenge -> escape feel engaging?
# Date: 2026-04-07

# 状态机。世界在这里运转。
# The state machine. The world runs here.

import pygame
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    STATE_ELEVATOR, STATE_DESCEND, STATE_FLOOR, STATE_DEATH, STATE_ASCEND,
    C_BLACK, C_DARK, C_RED, C_RED_BRIGHT, C_WHITE, C_LIGHT_GRAY,
    C_MID_GRAY, C_DARK_GRAY, C_AMBER, C_GREEN,
    ITEMS,
)
from src.inventory import Inventory
from src.scenes.elevator import ElevatorScene
from src.scenes.floor import FloorScene
from src.ui.hud import render_text, Button


class GameEngine:
    """
    Owns the game loop and routes state transitions.
    所有的门都通向更深的地方。
    All doors lead deeper.
    """

    def __init__(self):
        self.screen  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock   = pygame.time.Clock()

        self.inventory    = Inventory()
        self.floor_number = 0  # 0 = surface / hub; increments each descent

        # Scenes are recreated on each visit to keep state clean.
        self.state: str = STATE_ELEVATOR
        self._elevator_scene: ElevatorScene = self._make_elevator_scene()
        self._floor_scene:    FloorScene | None = None

        # Death screen state
        self._lost_items: list[str] = []
        self._continue_btn = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80, 200, 46,
            "继续", "[CONTINUE]"
        )

        # Brief transition delay (frames) for descend / ascend animations
        self._transition_timer = 0

    # ── Main loop ──────────────────────────────────────────────────────────────

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    break
                self._handle_event(event)

            if not running:
                break

            keys = pygame.key.get_pressed()
            self._update(dt, keys)
            self._draw()
            pygame.display.flip()

    # ── Event dispatch ─────────────────────────────────────────────────────────

    def _handle_event(self, event: pygame.event.Event):
        if self.state == STATE_ELEVATOR:
            self._elevator_scene.handle_event(event)

        elif self.state == STATE_FLOOR and self._floor_scene:
            self._floor_scene.handle_event(event)

        elif self.state == STATE_DEATH:
            self._continue_btn.update(pygame.mouse.get_pos())
            if self._continue_btn.is_clicked(event):
                self._enter_elevator(came_from_death=True)

    # ── Update dispatch ────────────────────────────────────────────────────────

    def _update(self, dt: float, keys):
        if self.state == STATE_ELEVATOR:
            next_state = self._elevator_scene.update(dt, keys)
            if next_state == STATE_DESCEND:
                self._begin_descent()

        elif self.state == STATE_DESCEND:
            # 短暂的过渡帧。门关上，然后打开。
            # Brief transition frames. Doors close, then open on the new floor.
            self._transition_timer -= 1
            if self._transition_timer <= 0:
                self._enter_floor()

        elif self.state == STATE_FLOOR and self._floor_scene:
            next_state = self._floor_scene.update(dt, keys)
            if next_state == STATE_ELEVATOR:
                self._enter_elevator(came_from_death=False)
            elif next_state == STATE_DEATH:
                self._enter_death()

        elif self.state == STATE_DEATH:
            self._continue_btn.update(pygame.mouse.get_pos())

        elif self.state == STATE_ASCEND:
            self._transition_timer -= 1
            if self._transition_timer <= 0:
                self.state = STATE_ELEVATOR

    # ── Draw dispatch ──────────────────────────────────────────────────────────

    def _draw(self):
        if self.state == STATE_ELEVATOR:
            self._elevator_scene.draw(self.screen)

        elif self.state == STATE_DESCEND:
            # Show black screen with descending text
            self.screen.fill(C_BLACK)
            render_text(self.screen, "正在下降...", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 16,
                        size=18, color=C_MID_GRAY, center=True)
            render_text(self.screen, "Descending...", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 8,
                        size=13, color=(60, 60, 75), center=True)
            render_text(self.screen, f"B-{self.floor_number}",
                        SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 34,
                        size=22, color=C_AMBER, bold=True, center=True)

        elif self.state == STATE_FLOOR and self._floor_scene:
            self._floor_scene.draw(self.screen)

        elif self.state == STATE_DEATH:
            self._draw_death_screen()

        elif self.state == STATE_ASCEND:
            self.screen.fill(C_BLACK)
            render_text(self.screen, "电梯上升中...", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 16,
                        size=18, color=C_MID_GRAY, center=True)
            render_text(self.screen, "Returning to elevator...", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 8,
                        size=13, color=(60, 60, 75), center=True)

    # ── State transitions ──────────────────────────────────────────────────────

    def _begin_descent(self):
        """
        门关上的那一刻，你就已经在下面了。
        The moment the door closes, you are already below.
        """
        self.floor_number += 1
        self.state = STATE_DESCEND
        self._transition_timer = 60  # 1 second at 60 fps

    def _enter_floor(self):
        self._floor_scene = FloorScene(self.inventory, self.floor_number)
        self._floor_scene.on_enter()
        self.state = STATE_FLOOR

    def _enter_elevator(self, came_from_death: bool):
        self._elevator_scene = self._make_elevator_scene()
        self._elevator_scene.on_enter(came_from_floor=True)
        self.state = STATE_ASCEND
        self._transition_timer = 45  # brief ascent fade

    def _enter_death(self):
        """
        时间到了。你付出代价。
        Time's up. You pay the price.
        """
        self._lost_items = self.inventory.apply_death_penalty()
        self.state = STATE_DEATH

    # ── Death screen ───────────────────────────────────────────────────────────

    def _draw_death_screen(self):
        """
        你没能回来。
        You didn't make it back.
        """
        self.screen.fill((8, 5, 5))

        # Red vignette border
        for i in range(8):
            alpha = 60 - i * 7
            if alpha > 0:
                border_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                pygame.draw.rect(border_surf, (180, 20, 20, alpha),
                                 (i * 2, i * 2,
                                  SCREEN_WIDTH - i * 4,
                                  SCREEN_HEIGHT - i * 4), 3)
                self.screen.blit(border_surf, (0, 0))

        cx = SCREEN_WIDTH // 2
        y  = 130

        render_text(self.screen, "你没能回来。",
                    cx, y, size=28, color=C_RED_BRIGHT, bold=True, center=True)
        render_text(self.screen, "You didn't make it back.",
                    cx, y + 38, size=16, color=(160, 60, 60), center=True)

        # Divider
        pygame.draw.line(self.screen, (60, 20, 20),
                         (cx - 140, y + 68), (cx + 140, y + 68), 1)

        y += 90
        render_text(self.screen, f"Floor: B-{self.floor_number}",
                    cx, y, size=14, color=C_AMBER, center=True)

        y += 32
        if self._lost_items:
            render_text(self.screen, "Items Lost:", cx, y, size=13,
                        color=(140, 60, 60), center=True)
            y += 22
            for key in self._lost_items:
                name_cn, name_en, color = ITEMS[key]
                render_text(self.screen, f"— {name_cn}  ({name_en})",
                            cx, y, size=13, color=color, center=True)
                y += 20
        else:
            render_text(self.screen, "You had nothing to lose.",
                        cx, y, size=13, color=C_MID_GRAY, center=True)
            y += 20

        # Continue button
        self._continue_btn.rect.topleft = (cx - 100, y + 30)
        self._continue_btn.draw(self.screen)

        render_text(self.screen, "继续寻找。总得继续。",
                    cx, y + 100, size=11, color=(60, 40, 40), center=True)

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _make_elevator_scene(self) -> ElevatorScene:
        return ElevatorScene(self.inventory, self.floor_number)
