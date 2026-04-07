# PROTOTYPE - NOT FOR PRODUCTION
# Question: Does the core loop of descend -> scavenge -> escape feel engaging?
# Date: 2026-04-07

# 所有数字都是谎言，直到你真正感受到它们。
# All numbers are lies until you feel them.

# ── Display ────────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS           = 60
TITLE         = "垂直深渊 | Vertical Abyss"

# ── Tile sizes ─────────────────────────────────────────────────────────────────
FLOOR_TILE_SIZE    = 48   # Each tile on a scavenging floor
ELEVATOR_TILE_SIZE = 96   # Larger tiles — the elevator is intimate, close

# ── Grid dimensions ───────────────────────────────────────────────────────────
FLOOR_GRID_COLS = 10
FLOOR_GRID_ROWS = 10

ELEVATOR_GRID_COLS = 2
ELEVATOR_GRID_ROWS = 2

# ── Player ─────────────────────────────────────────────────────────────────────
PLAYER_SPEED      = 2     # px per frame — fast enough to feel urgent
PLAYER_SIZE       = 20    # Visual radius of the player circle
VISION_RADIUS     = 3     # Tiles revealed around the player at any moment

# ── Timer ─────────────────────────────────────────────────────────────────────
# 60秒。门打开了。不要犹豫。
# The clock starts the moment the doors part.
FLOOR_TIME_LIMIT  = 60    # seconds

# ── Floor generation ──────────────────────────────────────────────────────────
WALL_CHANCE       = 0.30  # 30% of open tiles become rubble
ITEM_COUNT_MIN    = 5
ITEM_COUNT_MAX    = 8
DEATH_ITEM_LOSS   = 3     # Items stripped from inventory on time-out

# ── Inventory ─────────────────────────────────────────────────────────────────
INVENTORY_MAX     = 20

# ── Layout: Floor scene panel split ───────────────────────────────────────────
GRID_ORIGIN_X     = 10    # Left edge of the 10×10 grid
GRID_ORIGIN_Y     = 50    # Below the top bar
PANEL_X           = GRID_ORIGIN_X + FLOOR_GRID_COLS * FLOOR_TILE_SIZE + 10  # Right panel start
PANEL_WIDTH       = SCREEN_WIDTH - PANEL_X - 5

# ── Colors (palette) ──────────────────────────────────────────────────────────
# 深渊的颜色。没有一种是明亮的。
# The colors of the abyss. None of them are bright.
C_BLACK        = (0,   0,   0)
C_DARK         = (15,  15,  20)
C_DARK_GRAY    = (40,  40,  50)
C_MID_GRAY     = (80,  80,  95)
C_LIGHT_GRAY   = (160, 160, 175)
C_WHITE        = (220, 220, 230)
C_RED          = (200, 50,  50)
C_RED_BRIGHT   = (240, 80,  80)
C_GREEN        = (60,  180, 80)
C_AMBER        = (210, 160, 50)
C_ORANGE       = (220, 110, 40)
C_BLUE         = (60,  100, 200)
C_PANEL_BG     = (18,  18,  25)
C_TILE_FLOOR   = (35,  35,  45)
C_TILE_WALL    = (55,  55,  70)
C_TILE_EXIT    = (30,  80,  30)
C_PLAYER       = (200, 200, 255)
C_TIMER_NORMAL = (200, 200, 50)
C_TIMER_URGENT = (220, 50,  50)  # When < 15 s remain
C_ELEVATOR_BG  = (20,  20,  30)
C_ELEVATOR_TILE= (45,  45,  60)
C_BUTTON_BG    = (40,  80,  120)
C_BUTTON_HOVER = (60,  110, 160)
C_BUTTON_TEXT  = (210, 230, 255)
C_FOG_DIM      = (0,   0,   0,  140)  # RGBA — semi-transparent fog

# ── Item definitions ──────────────────────────────────────────────────────────
# Each item: (display_name_cn, display_name_en, color)
ITEMS = {
    "scrap":   ("废铁",   "Scrap Metal",    C_LIGHT_GRAY),
    "food":    ("罐头",   "Canned Food",    C_AMBER),
    "battery": ("旧电池", "Old Battery",    C_GREEN),
    "medkit":  ("急救包", "First Aid Kit",  C_RED),
    "fuel":    ("燃料桶", "Fuel Canister",  C_ORANGE),
}

# ── Floor environments ────────────────────────────────────────────────────────
# 每一层都有自己的气味，自己的声音，自己的危险。
# Every floor has its own smell, its own sound, its own danger.
ENVIRONMENTS = [
    {
        "name_cn": "办公室废墟",
        "name_en": "Office Ruins",
        "desc_cn": "荧光灯管嘶嘶作响，文件在风中腐烂。这里曾有人活着。",
        "desc_en": "Fluorescent tubes hiss. Documents rot in a wind with no source. People lived here once.",
        "floor_tint": (35, 35, 42),
    },
    {
        "name_cn": "地下停车场",
        "name_en": "Underground Parking",
        "desc_cn": "锈蚀的车壳挡住了出路。黑暗在角落里积聚，像水一样。",
        "desc_en": "Rusted car shells block every path. Darkness pools in corners like standing water.",
        "floor_tint": (28, 28, 35),
    },
    {
        "name_cn": "医院走廊",
        "name_en": "Hospital Corridor",
        "desc_cn": "气味早已消散，但脚步声回响得太响了。快走。",
        "desc_en": "The smell is long gone, but your footsteps echo too loudly. Move.",
        "floor_tint": (38, 35, 38),
    },
    {
        "name_cn": "仓储区",
        "name_en": "Storage Area",
        "desc_cn": "货架倒塌，物资散落其中。没有时间贪心。",
        "desc_en": "Shelves collapsed, supplies scattered across them. No time to be greedy.",
        "floor_tint": (32, 30, 25),
    },
    {
        "name_cn": "机械室",
        "name_en": "Machine Room",
        "desc_cn": "管道嘎嘎作响，好像这座楼还在喘气。也许它是。",
        "desc_en": "Pipes groan as if the building is still breathing. Maybe it is.",
        "floor_tint": (25, 30, 32),
    },
]

# ── Game states ───────────────────────────────────────────────────────────────
STATE_ELEVATOR = "elevator"
STATE_DESCEND  = "descend"   # Brief door-close animation
STATE_FLOOR    = "floor"
STATE_DEATH    = "death"
STATE_ASCEND   = "ascend"    # Brief door-open animation back in elevator
