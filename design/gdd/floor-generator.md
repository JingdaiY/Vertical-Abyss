# 楼层生成器 (Floor Generator)

> **Status**: Designed
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: Pillar 1（压迫即乐趣）

## Overview

楼层生成器在每次进入楼层时程序生成 10×10 的地图网格。保证出口可达，随机放置物品和危险地块。使用 `run.floor_seed` 保证同一 seed 生成同一地图。

## Player Fantasy

每层楼都不一样，但都是可以通过的。玩家永远不会因为"地图不公平"而死亡。

## Detailed Design

### Core Rules

生成步骤（按序执行）：

1. **初始化**：全部格设为 FLOOR（可行走）
2. **放置墙壁**：随机选取非出口格，按 `FLOOR_WALL_DENSITY(0.30)` 比例设为 WALL
3. **强制出口**：顶边（row 0）整行设为 EXIT_ZONE；中列（col 4-5）保证为 FLOOR
4. **连通性保证**：从玩家起点（row 9, col 5）到出口用 L 形走廊算法打通：先垂直走到 row 0，再水平走到 col 5。走廊格强制设为 FLOOR（覆盖墙壁）
5. **放置危险地块**：在可行走的非出口格中，按 `spawn_density(0.08)` 随机选取设为 HAZARD
6. **放置物品**：在可行走的非出口、非危险格中，随机选取 `randi_range(FLOOR_ITEM_COUNT_MIN, FLOOR_ITEM_COUNT_MAX)` 个格，每格放置一件物品（加权随机从物品数据库选取）
7. **玩家起点**：row 9, col 5，强制 FLOOR，不放物品和危险地块

### Tile 枚举

```gdscript
enum TileType { FLOOR, WALL, EXIT_ZONE, HAZARD }
```

### States and Transitions

N/A — 一次性生成，不存在持续状态。

### Interactions with Other Systems

| 系统 | 接口 |
|------|------|
| 游戏常量 | 读取 `TILE_SIZE`, `FLOOR_COLS`, `FLOOR_ROWS`, `FLOOR_WALL_DENSITY` 等 |
| 楼层内容数据 | 读取 `hazard_tiles`（类型和 `spawn_density`）、`item_weight_overrides` |
| 物品数据库 | 读取所有物品的 `spawn_weight` 构建加权池 |
| RunStateManager | 读取 `run.floor_seed` 初始化随机数生成器 |
| 雾效状态 | 楼层生成后调用 `fog.initialize()` |
| TileMapLayer | 将 TileType 数组渲染为 Godot TileMapLayer |

## Formulas

```
期望物品数 = (FLOOR_ITEM_COUNT_MIN + FLOOR_ITEM_COUNT_MAX) / 2 = 5.5
期望危险地块数 = FLOOR_COLS × FLOOR_ROWS × (1 - FLOOR_WALL_DENSITY) × spawn_density ≈ 5.6
P(item_i) = item_weight_i / Σ(all_weights)
```

## Edge Cases

| 场景 | 预期行为 |
|------|---------|
| 连通性算法覆盖过多墙壁 | 允许——走廊保证优先于墙壁密度 |
| 物品数量超过可用格子数 | 取 `min(requested, available_tiles)` |
| `floor_seed = 0` | 使用 0 作为合法种子值，允许 |

## Dependencies

| 系统 | 方向 | 性质 |
|------|------|------|
| 游戏常量 | 生成器 → 常量 | 硬依赖 |
| 楼层内容数据 | 生成器 → 楼层数据 | 硬依赖 |
| 物品数据库 | 生成器 → 物品数据库 | 硬依赖 |
| RunStateManager | 生成器 → RSM | 硬依赖（floor_seed） |

## Tuning Knobs

| 参数 | 当前值 | 安全范围 | 效果 |
|------|--------|---------|------|
| `FLOOR_WALL_DENSITY` | 0.30 | 0.15–0.50 | 越高越像迷宫 |
| `FLOOR_ITEM_COUNT_MIN/MAX` | 3–8 | 2–12 | 控制每层物资丰富度 |

## Visual/Audio Requirements

N/A — 生成数组数据，由 TileMapLayer 渲染。

## UI Requirements

N/A。

## Acceptance Criteria

- [ ] 同一 `floor_seed` 每次生成相同地图（确定性）
- [ ] 出口（row 0）始终可从起点（row 9, col 5）步行到达
- [ ] 出口区域无物品和危险地块
- [ ] 生成时间 < 50ms（Web 性能要求）

## Open Questions

- L 形走廊算法是否足够？Pygame 原型已验证可行，Godot 版需重新实现和测试。
