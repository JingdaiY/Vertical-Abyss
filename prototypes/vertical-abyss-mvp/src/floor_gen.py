# PROTOTYPE - NOT FOR PRODUCTION
# Question: Does the core loop of descend -> scavenge -> escape feel engaging?
# Date: 2026-04-07

# 每一层都是随机的。每一层都是相同的恐惧。
# Every floor is random. Every floor is the same fear.

import random
from src.constants import (
    FLOOR_GRID_COLS, FLOOR_GRID_ROWS,
    WALL_CHANCE, ITEM_COUNT_MIN, ITEM_COUNT_MAX,
    ITEMS, ENVIRONMENTS,
)


class FloorData:
    """
    Pure data class. No pygame, no rendering — just the floor state.
    """

    def __init__(self):
        self.cols       = FLOOR_GRID_COLS
        self.rows       = FLOOR_GRID_ROWS
        self.walls:  set[tuple[int,int]]  = set()
        self.items:  dict[tuple[int,int], str] = {}  # (col,row) -> item_key
        self.exit_tiles: set[tuple[int,int]] = set()
        self.environment: dict = {}

        # Fog of war — revealed[row][col]
        # False = never seen, True = seen at least once
        self.revealed: list[list[bool]] = [
            [False] * self.cols for _ in range(self.rows)
        ]


def generate_floor(floor_number: int) -> FloorData:
    """
    生成一个新的随机楼层。
    Generate a new random floor.

    Rules:
    - Entry / exit is the top row (row 0).  Player spawns on row 1.
    - Walls are randomly placed, never on exit tiles or player spawn.
    - Items are scattered on open non-exit tiles.
    """
    fd = FloorData()
    fd.environment = random.choice(ENVIRONMENTS)

    cols, rows = fd.cols, fd.rows

    # ── Exit tiles (top edge, row 0) ──────────────────────────────────────────
    # 出口永远在上方。也许这有什么含义。
    # The exit is always above. Maybe that means something.
    exit_cols = [0, 1, 2]  # Left three tiles of top row are the exit zone
    for c in exit_cols:
        fd.exit_tiles.add((c, 0))

    # ── Spawn region (player enters from top, row 1) ──────────────────────────
    spawn_protected = {(c, 0) for c in range(cols)} | {(c, 1) for c in exit_cols}

    # ── Walls ─────────────────────────────────────────────────────────────────
    for row in range(rows):
        for col in range(cols):
            if (col, row) in spawn_protected:
                continue
            if random.random() < WALL_CHANCE:
                fd.walls.add((col, row))

    # ── Items ─────────────────────────────────────────────────────────────────
    # 物资散落在废墟中。有些人曾经需要这些东西。
    # Supplies scattered in the ruin. Someone needed these once.
    item_count = random.randint(ITEM_COUNT_MIN, ITEM_COUNT_MAX)
    item_keys  = list(ITEMS.keys())
    open_tiles = [
        (c, r)
        for r in range(rows)
        for c in range(cols)
        if (c, r) not in fd.walls
        and (c, r) not in fd.exit_tiles
        and (c, r) != (1, 1)  # Don't place item on exact spawn point
    ]
    random.shuffle(open_tiles)
    for i in range(min(item_count, len(open_tiles))):
        tile = open_tiles[i]
        fd.items[tile] = random.choice(item_keys)

    # ── Connectivity check (flood fill from spawn) ────────────────────────────
    # We don't guarantee full connectivity in this prototype — just make sure
    # the spawn and exit are reachable from each other.  If not, clear a path.
    spawn = (1, 1)
    _ensure_path(fd, spawn, list(fd.exit_tiles)[0])

    return fd


def _ensure_path(fd: FloorData, start: tuple, end: tuple):
    """
    Carve a guaranteed corridor between start and end using a simple L-shaped
    path. This is brute-force prototype logic — it's not elegant and that's fine.
    """
    sc, sr = start
    ec, er = end

    # Walk column first, then row
    c = sc
    while c != ec:
        fd.walls.discard((c, sr))
        c += 1 if ec > sc else -1

    r = sr
    while r != er:
        fd.walls.discard((ec, r))
        r += 1 if er > sr else -1
