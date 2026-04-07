# 游戏常量 (Game Constants)

> **Status**: In Design
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: All four pillars (constants are the tuning layer beneath every pillar)

## Overview

游戏常量（`src/core/constants.gd`）是全游戏所有可调数值的唯一权威来源。它是一个无实例、无逻辑的纯数据文件——不包含任何运行时状态，只提供 `const` 声明。所有系统从这里读取数值，不在各自的脚本中硬编码魔法数字。玩家永远不会直接"看见"这个系统，但它决定了游戏的每一分压力感：计时器有多紧迫，视野有多狭窄，背包有多满。

*Game Constants (`src/core/constants.gd`) is the single authoritative source for every tunable value in the game. It is a pure data file with no runtime state — only `const` declarations. All systems read from here; nothing is hardcoded elsewhere. Players never see this system directly, but it controls every ounce of pressure: how tight the timer is, how narrow the vision, how quickly the backpack fills.*

## Player Fantasy

这是一个"你不应该注意到的系统"。当游戏感觉紧张而公平，当 60 秒刚好够拿到两件物资再跑回去，当视野恰好足够让你知道出口在哪却看不到角落里有什么——这就是游戏常量正在工作的证明。

对设计师而言，这个系统服务于 **Pillar 1（压迫即乐趣）**：每一个数值都是一个"压力旋钮"，调高让玩家更绝望，调低让玩家更从容。找到那个让玩家说出"刚好来得及"而不是"根本不可能"的数值组合，是这个系统存在的全部意义。

*This is a "system you should never notice." When the game feels tense and fair — when 60 seconds is just enough to grab two items and sprint back, when vision is just wide enough to see the exit but not the corners — that's game constants doing their job. For designers, this system serves Pillar 1 (Pressure IS the Game): every value is a pressure dial. The goal is finding the combination where players say "just made it" instead of "never had a chance."*

## Detailed Design

### Core Rules

1. **单一来源原则**：所有常量定义在 `src/core/constants.gd`，使用 `class_name Constants`。其他脚本通过 `Constants.CONSTANT_NAME` 访问，不在本地重新定义或硬编码任何数值。

2. **只读，无运行时修改**：所有条目使用 GDScript `const`，不使用 `var`。运行时可变数值（如 DDA 调整后的计时器时长）由各自系统计算并存储，常量只提供基准值。

3. **按功能分组，附注释**：文件按功能分块，每块前有分组注释：
   ```
   # ─── CATEGORY NAME ───────────────────
   const CONSTANT_NAME: type = value  # 简短说明
   ```

**完整常量定义（初始值）：**

```gdscript
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
const EXIT_ZONE_WIDTH: int       = 2      # tiles wide (exit zone spans one edge)

# ─── ELEVATOR HUB ─────────────────────────────────────────
const ELEVATOR_COLS: int      = 2
const ELEVATOR_ROWS: int      = 2
const ELEVATOR_TILE_SIZE: int = 96        # larger tiles for the intimate hub feel

# ─── PLAYER ───────────────────────────────────────────────
const PLAYER_SPEED: float              = 150.0  # px/s
const PLAYER_COLLISION_RADIUS: float   = 14.0   # px (half-size of player hitbox square)
const PLAYER_INTERACTION_RADIUS: float = 56.0   # px (~1.2 tiles; must be within to interact)
const PLAYER_MAX_HP: int               = 5      # max health; each point = one hazard tile step

# ─── FOG OF WAR ───────────────────────────────────────────
const FOG_VISION_RADIUS: int    = 3     # tiles (Chebyshev distance from player)
const FOG_EXPLORED_ALPHA: float = 0.55  # 0=transparent, 1=solid black; explored-but-not-visible

# ─── TIMER ────────────────────────────────────────────────
const TIMER_BASE_DURATION: float    = 60.0  # seconds (before DDA adjustment)
const TIMER_URGENCY_THRESHOLD: float = 15.0 # seconds remaining → red/urgent visual mode
const TIMER_MINIMUM: float          = 20.0  # DDA can never push timer below this value

# ─── INVENTORY ────────────────────────────────────────────
const INVENTORY_MAX_CAPACITY: int = 20  # max items a player can carry per run

# ─── DDA BASELINE (formula lives in difficulty-tracker GDD) ─────────────
const DDA_BASE_VARIANCE: float = 0.20  # ±20% from base difficulty per floor

# ─── DEATH ────────────────────────────────────────────────
const DEATH_SCREEN_DURATION: float = 3.0  # seconds before "try again" button appears
```

### States and Transitions

N/A — 游戏常量是无状态的纯配置文件，不存在状态机。

### Interactions with Other Systems

**单向只读**：每个下游系统读取 `Constants.*`；常量文件本身不调用任何其他系统，不持有任何引用。

| 下游系统 | 读取的常量 | 说明 |
|---------|-----------|------|
| 玩家实体 | `PLAYER_SPEED`, `PLAYER_COLLISION_RADIUS`, `PLAYER_INTERACTION_RADIUS` | 移动和交互基准值 |
| 楼层生成器 | `TILE_SIZE`, `FLOOR_COLS`, `FLOOR_ROWS`, `FLOOR_WALL_DENSITY`, `FLOOR_ITEM_COUNT_*`, `EXIT_ZONE_WIDTH` | 生成网格和物品 |
| 雾效状态 | `FOG_VISION_RADIUS`, `FOG_EXPLORED_ALPHA` | 视野半径和渲染透明度 |
| 计时器系统 | `TIMER_BASE_DURATION`, `TIMER_URGENCY_THRESHOLD`, `TIMER_MINIMUM` | 倒计时逻辑 |
| 背包系统 | `INVENTORY_MAX_CAPACITY` | 容量上限 |
| 难度追踪器/DDA | `TIMER_BASE_DURATION`, `DDA_BASE_VARIANCE` | DDA 公式的输入基准 |
| 死亡系统 | `DEATH_SCREEN_DURATION` | 死亡界面停留时长 |
| 电梯中枢场景 | `ELEVATOR_COLS`, `ELEVATOR_ROWS`, `ELEVATOR_TILE_SIZE` | 中枢空间大小 |

## Formulas

游戏常量不定义公式——它是公式变量的**输入端**，不是公式本身。以下公式将在各自系统 GDD 中详细定义，此处仅记录引用关系：

| 公式 | 所在 GDD | 引用的常量 |
|------|---------|-----------|
| DDA 计时器计算 | 难度追踪器/DDA GDD | `TIMER_BASE_DURATION`, `TIMER_MINIMUM` |
| 雾效视野范围 | 雾效状态 GDD | `FOG_VISION_RADIUS` |
| 楼层物品数量 | 楼层生成器 GDD | `FLOOR_ITEM_COUNT_MIN`, `FLOOR_ITEM_COUNT_MAX` |
| 楼层墙壁生成 | 楼层生成器 GDD | `FLOOR_WALL_DENSITY`, `FLOOR_COLS`, `FLOOR_ROWS` |
| DDA 难度波动 | 难度追踪器/DDA GDD | `DDA_BASE_VARIANCE` |

**预期引用方式（GDScript）：**
```gdscript
# ✅ 正确
var item_count: int = randi_range(Constants.FLOOR_ITEM_COUNT_MIN, Constants.FLOOR_ITEM_COUNT_MAX)

# ❌ 禁止
var item_count: int = randi_range(3, 8)  # 魔法数字
```

## Edge Cases

| 场景 | 预期行为 | 理由 |
|------|---------|------|
| `TIMER_BASE_DURATION` < `TIMER_MINIMUM` | 计时器系统运行时警告，使用 `TIMER_MINIMUM` 作为实际值 | 防止 DDA 产生物理上无法通关的楼层 |
| `FLOOR_ITEM_COUNT_MIN` > `FLOOR_ITEM_COUNT_MAX` | 开发模式断言失败（立即崩溃暴露错误）；发布模式自动 swap 两值 | 配置错误应在开发期尽早发现 |
| `FOG_VISION_RADIUS` = 0 | 玩家完全看不见地图——合法但极端，不用于默认 | 保留为未来高难模式可选配置 |
| `FLOOR_WALL_DENSITY` ≥ 0.60 | 楼层生成器可能无法保证出口可达，需重新生成；常量注释标注安全上限 ≤ 0.50 | 超过此密度时连通性算法压力过大 |
| `INVENTORY_MAX_CAPACITY` < 1 | 视为设计错误；常量注释标注最小值 = 1 | 容量为 0 导致游戏无法进行，无设计意义 |
| `DDA_BASE_VARIANCE` > 0.50 | 游戏感觉随机而非有规律；常量注释标注推荐上限 ≤ 0.35 | 超过 ±50% 波动时玩家无法建立难度预期，违反 Pillar 4（每次死亡都值得）|

## Dependencies

| 系统 | 方向 | 依赖性质 |
|------|------|---------|
| （无上游依赖） | — | 根节点，无前置系统 |
| 玩家实体 | 玩家实体 → 此系统 | 硬依赖 — 读取 `PLAYER_SPEED`, `PLAYER_COLLISION_RADIUS`, `PLAYER_INTERACTION_RADIUS` |
| 背包系统 | 背包系统 → 此系统 | 硬依赖 — 读取 `INVENTORY_MAX_CAPACITY` |
| 计时器系统 | 计时器系统 → 此系统 | 硬依赖 — 读取 `TIMER_BASE_DURATION`, `TIMER_URGENCY_THRESHOLD`, `TIMER_MINIMUM` |
| 楼层生成器 | 楼层生成器 → 此系统 | 硬依赖 — 读取 `TILE_SIZE`, `FLOOR_COLS`, `FLOOR_ROWS`, `FLOOR_WALL_DENSITY`, `FLOOR_ITEM_COUNT_*`, `EXIT_ZONE_WIDTH` |
| 雾效状态 | 雾效状态 → 此系统 | 硬依赖 — 读取 `FOG_VISION_RADIUS`, `FOG_EXPLORED_ALPHA` |
| 难度追踪器/DDA | DDA → 此系统 | 硬依赖 — 读取 `TIMER_BASE_DURATION`, `DDA_BASE_VARIANCE` |
| 电梯中枢场景 | 电梯中枢场景 → 此系统 | 硬依赖 — 读取 `ELEVATOR_COLS`, `ELEVATOR_ROWS`, `ELEVATOR_TILE_SIZE` |
| 死亡系统 | 死亡系统 → 此系统 | 软依赖 — 读取 `DEATH_SCREEN_DURATION` |

## Tuning Knobs

| 参数 | 当前值 | 安全范围 | 调高效果 | 调低效果 |
|------|--------|---------|---------|---------|
| `TIMER_BASE_DURATION` | 60s | 30–120s | 玩家更从容，可拿更多物资，压迫感下降 | 更紧迫，可能无法拿到任何物资（< 30s 可能违反 Pillar 1 下限） |
| `TIMER_URGENCY_THRESHOLD` | 15s | 10–25s | 更长时间处于红色紧迫状态，可能造成视觉疲劳 | 紧迫提示来不及反应，玩家猝不及防 |
| `PLAYER_SPEED` | 150 px/s | 100–220 px/s | 地图感觉更小，决策节奏加快 | 地图感觉更大，返回出口的时间成本更高 |
| `FOG_VISION_RADIUS` | 3 tiles | 2–5 tiles | 玩家看得更远，安全感增加，压迫感下降 | 极度受限，容易迷路而非产生策略性压力 |
| `FOG_EXPLORED_ALPHA` | 0.55 | 0.35–0.75 | 已探索区域更暗，方向感更弱 | 已探索区域几乎透明，地图感觉清晰、压力减小 |
| `FLOOR_WALL_DENSITY` | 0.30 | 0.15–0.50 | 楼层更迷宫化，路线更长，时间压力更大（> 0.50 有楼层不可解风险） | 楼层太空旷，搜索行为变为简单直线冲刺 |
| `DDA_BASE_VARIANCE` | 0.20 (±20%) | 0.05–0.35 | 楼层难度更不可预测（> 0.35 开始感觉不公平） | 难度波动极小，楼层感觉雷同，失去惊喜感 |
| `INVENTORY_MAX_CAPACITY` | 20 | 5–30 | 贪婪策略更安全，压迫感下降 | 玩家被迫做取舍，每次拾取都是决策（< 5 可能让玩家感到被剥夺而非被考验） |

## Visual/Audio Requirements

N/A — 游戏常量是纯数据文件，无视觉或音频反馈。

## UI Requirements

N/A — 玩家不直接与游戏常量交互，无 UI 需求。

## Acceptance Criteria

- [ ] `Constants.TILE_SIZE` 等所有常量可从任意 GDScript 文件通过 `Constants.` 前缀访问，无需实例化任何节点
- [ ] `src/` 目录下无孤立的魔法数字（CI 检查：不允许出现未被常量引用的 `60`、`150`、`48`、`10`、`3`、`20` 等关键数值）
- [ ] `FLOOR_ITEM_COUNT_MIN` ≤ `FLOOR_ITEM_COUNT_MAX`——游戏启动时断言检查，违反时开发模式崩溃
- [ ] `TIMER_MINIMUM` 被计时器系统正确用作下限——单元测试：`DDA 输出不能将计时器推低至 TIMER_MINIMUM 以下`
- [ ] 修改任意常量值后，无需修改其他文件即可生效（无缓存、无复制值）
- [ ] `constants.gd` 文件解析耗时 < 1ms（纯静态数据，无运行时计算）

## Open Questions

| 问题 | 负责人 | 目标解决时间 | 解决方案 |
|------|-------|------------|---------|
| `PLAYER_SPEED` 的最终值是否需要在 Godot 原型中实测调整？ | 开发者 | Vertical Slice 原型阶段 | 实测感受后更新 |
| `SCREEN_WIDTH / HEIGHT` 是否应支持响应式 Web 布局（非固定 800×600）？ | 开发者 | Vertical Slice 阶段 | 若支持，改为动态读取视口尺寸，常量改为最小支持值 |
