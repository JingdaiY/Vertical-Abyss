# 撤离检测 (Evacuation Detection)

> **Status**: Designed
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: Pillar 1（压迫即乐趣）

## Overview

玩家进入出口区域（地图上边缘 `EXIT_ZONE_WIDTH` 格宽的区域）并停留 0.5 秒后，发射 `evacuation_success()` 信号。楼层探索场景处理场景切换。

## Player Fantasy

"跑回去了！"的解脱感。0.5 秒等待防止玩家误触出口区域时意外撤离。

## Detailed Design

### Core Rules

```gdscript
signal evacuation_success()

const DWELL_TIME: float = 0.5  # 秒，停留时间阈值
var _dwell_timer: float = 0.0
var _in_exit_zone: bool = false

func _process(delta: float) -> void:
    if not _in_exit_zone:
        _dwell_timer = 0.0
        return
    _dwell_timer += delta
    if _dwell_timer >= DWELL_TIME:
        set_process(false)
        evacuation_success.emit()

# 由楼层生成器/场景在玩家位置更新时调用
func update_player_tile(tile: Vector2i) -> void:
    _in_exit_zone = tile.y == 0  # 出口在顶边（row 0）
```

出口固定在地图顶边（row 0），宽度为整行（`EXIT_ZONE_WIDTH` 列）。

### States and Transitions

IN_FLOOR → （玩家进入出口区域并停留 0.5s）→ 发射 `evacuation_success`

### Interactions with Other Systems

| 系统 | 接口 |
|------|------|
| 玩家实体 | 读取玩家当前 tile 坐标 |
| 计时器系统 | 撤离成功后调用 `timer.stop()` |
| 楼层探索场景 | 监听 `evacuation_success`，执行场景切换 |
| RunStateManager | 撤离成功后 `run.current_floor = 0` |

## Formulas

无。

## Edge Cases

| 场景 | 预期行为 |
|------|---------|
| 玩家进入出口区域后退出（等待未满） | 重置 `_dwell_timer`，不触发撤离 |
| 计时器归零时玩家恰好在出口区域 | 死亡系统优先（`timer_expired` 已发射），撤离不再触发 |

## Dependencies

| 系统 | 方向 | 性质 |
|------|------|------|
| 玩家实体 | 撤离检测 → 玩家 | 硬依赖（位置） |
| 计时器系统 | 撤离检测 → 计时器 | 硬依赖（成功后停止） |

## Tuning Knobs

`DWELL_TIME = 0.5s`（硬编码在此系统，可提取为常量）。

## Visual/Audio Requirements

进入出口区域时地板高亮提示（绿色边框），停留期间显示进度条。

## UI Requirements

N/A — 进度条属于楼层 HUD。

## Acceptance Criteria

- [ ] 玩家在出口区域停留 0.5s 后 `evacuation_success` 发射
- [ ] 停留不足 0.5s 离开则不触发
- [ ] 信号只发射一次

## Open Questions

无。
