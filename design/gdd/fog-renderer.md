# 雾效渲染器 (Fog Renderer)

> **Status**: Designed
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: Pillar 1（压迫即乐趣）

## Overview

用 CanvasLayer 覆盖楼层，每格根据 `TileVisibility` 状态设置透明度。UNKNOWN = 完全黑，EXPLORED = 半透明，VISIBLE = 透明。

## Detailed Design

### Core Rules

使用 `Node2D` + `_draw()` 逐格绘制矩形覆盖层：

```gdscript
func _draw() -> void:
    var grid: Array = FogOfWarState.grid
    for r in grid.size():
        for c in grid[r].size():
            var vis: FogOfWarState.TileVisibility = grid[r][c]
            var alpha: float
            match vis:
                FogOfWarState.TileVisibility.UNKNOWN:   alpha = 1.0
                FogOfWarState.TileVisibility.EXPLORED:  alpha = Constants.FOG_EXPLORED_ALPHA
                FogOfWarState.TileVisibility.VISIBLE:   alpha = 0.0
            if alpha > 0.0:
                var rect: Rect2 = Rect2(
                    c * Constants.TILE_SIZE,
                    r * Constants.TILE_SIZE,
                    Constants.TILE_SIZE,
                    Constants.TILE_SIZE
                )
                draw_rect(rect, Color(0, 0, 0, alpha))

func _process(_delta: float) -> void:
    queue_redraw()  # 每帧重绘
```

**性能注意**：每帧绘制 100 个矩形。Web 平台需测试是否在 draw call 预算内。若有性能问题，改为只在玩家移动时 `queue_redraw()`。

## Acceptance Criteria

- [ ] UNKNOWN 格完全不可见（alpha=1.0 黑色覆盖）
- [ ] EXPLORED 格半透明（alpha=0.55）
- [ ] VISIBLE 格无覆盖
- [ ] 60fps 下 Web 平台帧率不低于 55fps（需实测）

## Dependencies

→ FogOfWarState（读取 grid）、→ 游戏常量（FOG_EXPLORED_ALPHA, TILE_SIZE）
