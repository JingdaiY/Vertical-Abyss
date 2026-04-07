# 雾效状态 (Fog of War State)

> **Status**: Designed
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: Pillar 1（压迫即乐趣）

## Overview

雾效状态维护楼层的 10×10 可见性网格，记录每格是 UNKNOWN / EXPLORED / VISIBLE。每次玩家移动后更新；雾效渲染器读取此数据决定渲染透明度。

## Player Fantasy

玩家只能看到周围 3 格，其他地方是黑暗。已探索区域保留半透明轮廓，给玩家方向感但不消除紧张感。

## Detailed Design

### Core Rules

```gdscript
enum TileVisibility { UNKNOWN, EXPLORED, VISIBLE }

var grid: Array = []  # grid[row][col]: TileVisibility，10×10

func initialize(rows: int, cols: int) -> void:
    grid = []
    for r in rows:
        var row: Array = []
        for c in cols:
            row.append(TileVisibility.UNKNOWN)
        grid.append(row)

func update_visibility(player_tile: Vector2i) -> void:
    # 先把所有 VISIBLE 降级为 EXPLORED
    for r in grid.size():
        for c in grid[r].size():
            if grid[r][c] == TileVisibility.VISIBLE:
                grid[r][c] = TileVisibility.EXPLORED
    # 以玩家格为中心，Chebyshev 距离 <= FOG_VISION_RADIUS 的格设为 VISIBLE
    var radius: int = Constants.FOG_VISION_RADIUS
    for dr in range(-radius, radius + 1):
        for dc in range(-radius, radius + 1):
            var r: int = player_tile.y + dr
            var c: int = player_tile.x + dc
            if r >= 0 and r < grid.size() and c >= 0 and c < grid[r].size():
                grid[r][c] = TileVisibility.VISIBLE
```

### States and Transitions

每次玩家移动后调用 `update_visibility()`；楼层开始时调用 `initialize()`。

### Interactions with Other Systems

| 系统 | 接口 |
|------|------|
| 游戏常量 | 读取 `FOG_VISION_RADIUS`, `FOG_EXPLORED_ALPHA` |
| 玩家实体 | 玩家移动时提供 `player_tile: Vector2i` |
| 楼层探索场景 | 调用 `initialize()` |
| 雾效渲染器 | 读取 `grid` 数组决定每格透明度 |

## Formulas

```
VISIBLE 范围：max(|dr|, |dc|) <= FOG_VISION_RADIUS   （Chebyshev 距离）
EXPLORED 渲染透明度：FOG_EXPLORED_ALPHA = 0.55
UNKNOWN 渲染透明度：1.0（完全黑）
```

## Edge Cases

| 场景 | 预期行为 |
|------|---------|
| 玩家在地图边缘 | 范围超出网格边界的格子跳过，不越界访问 |
| `FOG_VISION_RADIUS = 0` | 只有玩家所在格 VISIBLE，其他全黑 |

## Dependencies

| 系统 | 方向 | 性质 |
|------|------|------|
| 游戏常量 | 雾效 → 常量 | 硬依赖 |
| 玩家实体 | 玩家 → 雾效（提供位置） | 硬依赖 |
| 雾效渲染器 | 渲染器 → 雾效（读取 grid） | 硬依赖 |

## Tuning Knobs

| 参数 | 当前值 | 安全范围 | 效果 |
|------|--------|---------|------|
| `FOG_VISION_RADIUS` | 3 | 2–5 | 越小越压抑 |
| `FOG_EXPLORED_ALPHA` | 0.55 | 0.35–0.75 | 越高已探索区越暗 |

## Visual/Audio Requirements

N/A — 渲染属于雾效渲染器。

## UI Requirements

N/A。

## Acceptance Criteria

- [ ] 楼层初始化后所有格为 UNKNOWN
- [ ] `update_visibility()` 后，半径 3 内格为 VISIBLE，之前 VISIBLE 的格降为 EXPLORED
- [ ] 地图边缘不越界
- [ ] `FOG_VISION_RADIUS = 0` 时只有玩家格 VISIBLE

## Open Questions

无。
