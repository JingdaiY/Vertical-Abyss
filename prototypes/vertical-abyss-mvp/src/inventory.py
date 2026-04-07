# PROTOTYPE - NOT FOR PRODUCTION
# Question: Does the core loop of descend -> scavenge -> escape feel engaging?
# Date: 2026-04-07

# 你能带走的东西很少。你愿意放弃的东西更少。
# You can carry very little. You are willing to give up even less.

import random
from src.constants import ITEMS, INVENTORY_MAX, DEATH_ITEM_LOSS


class Inventory:
    """
    A flat list of item keys. Stacking is cosmetic only — the list may contain
    duplicates. We summarise them at render time.
    """

    def __init__(self):
        # 电梯是唯一安全的地方。也许是。
        # The elevator is the only safe place. Maybe.
        self.items: list[str] = []  # list of item keys, e.g. ["scrap", "food", "scrap"]

    # ── Mutation ───────────────────────────────────────────────────────────────

    def add(self, item_key: str) -> bool:
        """Add one item. Returns False if inventory is full."""
        if len(self.items) >= INVENTORY_MAX:
            return False
        self.items.append(item_key)
        return True

    def apply_death_penalty(self) -> list[str]:
        """
        时间到了。你付出代价。
        Time's up. You pay the price.
        Removes up to DEATH_ITEM_LOSS random items and returns their keys.
        """
        if not self.items:
            return []

        count = min(DEATH_ITEM_LOSS, len(self.items))
        lost = random.sample(self.items, count)
        for key in lost:
            self.items.remove(key)
        return lost

    # ── Query ──────────────────────────────────────────────────────────────────

    def is_full(self) -> bool:
        return len(self.items) >= INVENTORY_MAX

    def summarise(self) -> dict[str, int]:
        """Return {item_key: count} for display."""
        counts: dict[str, int] = {}
        for key in self.items:
            counts[key] = counts.get(key, 0) + 1
        return counts

    def total(self) -> int:
        return len(self.items)

    def display_lines(self) -> list[tuple[str, tuple]]:
        """
        Returns a list of (display_string, color) tuples for UI rendering.
        e.g. [("废铁 ×3", (160,160,175)), ("罐头 ×1", (210,160,50))]
        """
        lines = []
        for key, count in self.summarise().items():
            name_cn, _name_en, color = ITEMS[key]
            lines.append((f"{name_cn}  x{count}", color))
        return lines
