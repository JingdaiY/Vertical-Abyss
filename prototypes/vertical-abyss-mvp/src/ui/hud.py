# PROTOTYPE - NOT FOR PRODUCTION
# Question: Does the core loop of descend -> scavenge -> escape feel engaging?
# Date: 2026-04-07

# HUD是真相。数字不说谎。
# The HUD is truth. Numbers do not lie.

import pygame
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, C_WHITE, C_RED, C_RED_BRIGHT,
    C_DARK, C_PANEL_BG, C_MID_GRAY, C_LIGHT_GRAY, C_DARK_GRAY,
    C_TIMER_NORMAL, C_TIMER_URGENT, C_BUTTON_BG, C_BUTTON_HOVER,
    C_BUTTON_TEXT, C_BLACK, C_AMBER, C_GREEN, C_ORANGE,
)

# ─────────────────────────────────────────────────────────────────────────────
# Font helpers
# ─────────────────────────────────────────────────────────────────────────────
# IMPORTANT: Pygame's built-in fonts do not support CJK characters on most
# systems.  We try to find a system font that does.  If none is found, Chinese
# strings will render as boxes — the English fallback labels will still be
# visible.  On macOS, "PingFang SC" or "Hiragino Sans GB" usually work.
# On Linux, try "Noto Sans CJK SC" or "WenQuanYi Micro Hei".
# We store fonts here so we only load them once.

_font_cache: dict = {}


def _get_font(size: int, bold: bool = False) -> pygame.font.Font:
    key = (size, bold)
    if key not in _font_cache:
        # SysFont name lookup is unreliable for CJK on macOS — it silently falls
        # back to a Latin font and renders boxes at ~5px wide.
        # Load directly from known file paths instead; much more reliable.
        font_file_candidates = [
            "/System/Library/Fonts/Hiragino Sans GB.ttc",           # macOS
            "/System/Library/Fonts/PingFang.ttc",                   # macOS
            "/System/Library/Fonts/STHeiti Light.ttc",              # macOS
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",  # Linux
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",  # Linux alt
            "C:/Windows/Fonts/msyh.ttc",                            # Windows
        ]
        font = None
        for path in font_file_candidates:
            try:
                candidate = pygame.font.Font(path, size)
                test = candidate.render("废", True, (255, 255, 255))
                # A real CJK glyph at size 16+ should be at least size*0.5 wide
                if test.get_width() > size * 0.5:
                    font = candidate
                    break
            except Exception:
                continue
        if font is None:
            # 字体加载失败，退回英文字体。中文将显示为方块。
            # CJK font not found; Chinese will render as boxes.
            font = pygame.font.SysFont("monospace", size, bold=bold)
        _font_cache[key] = font
    return _font_cache[key]


def render_text(surface: pygame.Surface, text: str, x: int, y: int,
                size: int = 14, color=C_WHITE, bold: bool = False,
                center: bool = False):
    font = _get_font(size, bold)
    img  = font.render(text, True, color)
    if center:
        rect = img.get_rect(center=(x, y))
    else:
        rect = img.get_rect(topleft=(x, y))
    surface.blit(img, rect)
    return rect


# ─────────────────────────────────────────────────────────────────────────────
# Button
# ─────────────────────────────────────────────────────────────────────────────

class Button:
    """Simple clickable rectangle with hover state."""

    def __init__(self, x: int, y: int, w: int, h: int,
                 label_cn: str, label_en: str):
        self.rect     = pygame.Rect(x, y, w, h)
        self.label_cn = label_cn
        self.label_en = label_en
        self.hovered  = False

    def update(self, mouse_pos: tuple):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))

    def draw(self, surface: pygame.Surface):
        color = C_BUTTON_HOVER if self.hovered else C_BUTTON_BG
        pygame.draw.rect(surface, color, self.rect, border_radius=4)
        pygame.draw.rect(surface, C_LIGHT_GRAY, self.rect, 1, border_radius=4)

        cx = self.rect.centerx
        cy = self.rect.centery

        # Chinese label (top line)
        render_text(surface, self.label_cn, cx, cy - 9, size=14,
                    color=C_BUTTON_TEXT, center=True)
        # English label (bottom line, smaller)
        render_text(surface, self.label_en, cx, cy + 9, size=11,
                    color=(160, 180, 210), center=True)


# ─────────────────────────────────────────────────────────────────────────────
# Timer bar
# ─────────────────────────────────────────────────────────────────────────────

def draw_timer_bar(surface: pygame.Surface, seconds_left: int,
                   fraction: float, urgent: bool,
                   x: int, y: int, w: int, h: int):
    """
    秒针不会停下来。
    The second hand does not stop.
    """
    # Background track
    pygame.draw.rect(surface, C_DARK_GRAY, (x, y, w, h), border_radius=3)

    # Fill
    fill_w = max(0, int(w * fraction))
    color  = C_TIMER_URGENT if urgent else C_TIMER_NORMAL
    if fill_w > 0:
        pygame.draw.rect(surface, color, (x, y, fill_w, h), border_radius=3)

    # Border
    pygame.draw.rect(surface, C_MID_GRAY, (x, y, w, h), 1, border_radius=3)

    # Label
    label = f"TIMER: {seconds_left}s"
    render_text(surface, label, x + w // 2, y + h // 2,
                size=13, color=C_WHITE, bold=True, center=True)


# ─────────────────────────────────────────────────────────────────────────────
# Inventory panel
# ─────────────────────────────────────────────────────────────────────────────

def draw_inventory_panel(surface: pygame.Surface, lines: list[tuple[str, tuple]],
                         x: int, y: int, w: int, label: str = "INVENTORY"):
    """
    Render the inventory list on the right panel.
    lines: [(display_string, color), ...]
    """
    # Panel background
    panel_rect = pygame.Rect(x - 5, y - 5, w + 5, SCREEN_HEIGHT - y)
    pygame.draw.rect(surface, C_PANEL_BG, panel_rect)
    pygame.draw.line(surface, C_DARK_GRAY, (x - 5, y - 5), (x - 5, SCREEN_HEIGHT), 1)

    # Header
    render_text(surface, label, x, y, size=13, color=C_LIGHT_GRAY, bold=True)
    pygame.draw.line(surface, C_DARK_GRAY, (x, y + 18), (x + w, y + 18), 1)

    if not lines:
        render_text(surface, "(empty)", x, y + 26, size=12, color=C_MID_GRAY)
        return

    row_y = y + 26
    for text, color in lines:
        render_text(surface, text, x, row_y, size=13, color=color)
        row_y += 20
