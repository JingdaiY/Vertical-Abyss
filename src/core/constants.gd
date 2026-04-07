class_name Constants

# ─── DISPLAY ──────────────────────────────────────────────
const SCREEN_WIDTH: int   = 800
const SCREEN_HEIGHT: int  = 600
const TARGET_FPS: int     = 60

# ─── FLOOR GRID ───────────────────────────────────────────
const TILE_SIZE: int             = 48     # px per tile
const FLOOR_COLS: int            = 10     # grid width in tiles
const FLOOR_ROWS: int            = 10     # grid height in tiles
const FLOOR_WALL_DENSITY: float  = 0.30   # proportion of non-exit tiles that are walls
const FLOOR_ITEM_COUNT_MIN: int  = 3      # minimum items spawned per floor
const FLOOR_ITEM_COUNT_MAX: int  = 8      # maximum items spawned per floor
const EXIT_ZONE_WIDTH: int       = 2      # tiles wide (exit zone spans top edge)

# ─── ELEVATOR HUB ─────────────────────────────────────────
const ELEVATOR_COLS: int      = 2
const ELEVATOR_ROWS: int      = 2
const ELEVATOR_TILE_SIZE: int = 96        # larger tiles for the intimate hub feel

# ─── PLAYER ───────────────────────────────────────────────
const PLAYER_SPEED: float              = 150.0  # px/s
const PLAYER_COLLISION_RADIUS: float   = 14.0   # px
const PLAYER_INTERACTION_RADIUS: float = 56.0   # px (~1.2 tiles)
const PLAYER_MAX_HP: int               = 5      # max health; each point = one hazard step

# ─── FOG OF WAR ───────────────────────────────────────────
const FOG_VISION_RADIUS: int    = 3     # tiles (Chebyshev distance from player)
const FOG_EXPLORED_ALPHA: float = 0.55  # 0=transparent, 1=solid; explored-but-not-visible

# ─── TIMER ────────────────────────────────────────────────
const TIMER_BASE_DURATION: float     = 60.0   # seconds (before DDA adjustment)
const TIMER_URGENCY_THRESHOLD: float = 15.0   # seconds remaining → urgent visual mode
const TIMER_MINIMUM: float           = 20.0   # DDA can never push timer below this

# ─── INVENTORY ────────────────────────────────────────────
const INVENTORY_MAX_CAPACITY: int = 20  # max total items per run

# ─── DDA BASELINE ─────────────────────────────────────────
const DDA_BASE_VARIANCE: float = 0.20  # ±20% from base difficulty per floor

# ─── DEATH ────────────────────────────────────────────────
const DEATH_SCREEN_DURATION: float = 3.0  # seconds before returning to elevator
