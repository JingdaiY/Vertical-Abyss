# 死亡系统 (Death System)

> **Status**: Designed
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: Pillar 4（每次死亡都值得）

## Overview

监听 `player_died` 和 `timer_expired` 两个信号。触发后：更新永久统计 → `clear_run_data()` → 等待 `DEATH_SCREEN_DURATION` → 切换回电梯场景。

## Player Fantasy

死亡是游戏循环的一部分，不是惩罚终点。死亡画面短暂呈现本次跑团信息（到达楼层、携带物品），让玩家理解为什么死，然后给他们"再来一次"的机会。

## Detailed Design

### Core Rules

```gdscript
var _death_handled: bool = false

func _on_player_died() -> void:
    _handle_death()

func _on_timer_expired() -> void:
    _handle_death()

func _handle_death() -> void:
    if _death_handled:
        return
    _death_handled = true
    # 1. 更新永久数据
    RunStateManager.persistent.total_deaths += 1
    var floor: int = RunStateManager.run.current_floor
    if floor > RunStateManager.persistent.deepest_floor_reached:
        RunStateManager.persistent.deepest_floor_reached = floor
    # 2. 清除跑团数据（背包、HP、计时器归零）
    RunStateManager.clear_run_data()
    # 3. 等待死亡画面后切换场景
    await get_tree().create_timer(Constants.DEATH_SCREEN_DURATION).timeout
    get_tree().change_scene_to_file("res://scenes/elevator/ElevatorHub.tscn")
```

`_death_handled` 标志防止双重触发。

### States and Transitions

`ALIVE → DEAD（触发）→ 等待 3s → 切换到电梯`

### Interactions with Other Systems

| 系统 | 接口 |
|------|------|
| 玩家实体 | 监听 `player_died` 信号 |
| 计时器系统 | 监听 `timer_expired` 信号 |
| RunStateManager | 写入 `persistent.total_deaths`；调用 `clear_run_data()` |
| 死亡回顾 UI | 死亡画面期间展示本次跑团信息（Vertical Slice） |

## Formulas

无。

## Edge Cases

| 场景 | 预期行为 |
|------|---------|
| `player_died` 和 `timer_expired` 同时触发 | `_death_handled` 标志保证只处理一次 |
| 死亡画面期间玩家按任意键 | MVP 阶段忽略所有输入；等满 `DEATH_SCREEN_DURATION` |

## Dependencies

| 系统 | 方向 | 性质 |
|------|------|------|
| RunStateManager | 死亡系统 → RSM | 硬依赖 |
| 游戏常量 | 死亡系统 → 常量 | 硬依赖（`DEATH_SCREEN_DURATION`） |
| 玩家实体 | 死亡系统 → 玩家（监听信号） | 硬依赖 |
| 计时器系统 | 死亡系统 → 计时器（监听信号） | 硬依赖 |

## Tuning Knobs

| 参数 | 当前值 | 安全范围 | 效果 |
|------|--------|---------|------|
| `DEATH_SCREEN_DURATION` | 3s | 1–5s | 太短玩家看不清信息；太长打断节奏 |

## Visual/Audio Requirements

死亡画面：黑色渐入，显示"第 N 层 · 携带 M 件物品 · 存活 Xs"。

## UI Requirements

死亡回顾 UI 属于 Vertical Slice 系统，MVP 阶段只显示黑屏 + 简单文字。

## Acceptance Criteria

- [ ] 触发后 `persistent.total_deaths` 精确 +1
- [ ] `deepest_floor_reached` 在历史最深时更新
- [ ] `clear_run_data()` 在死亡画面显示前调用
- [ ] 双重触发不会导致 `clear_run_data()` 执行两次
- [ ] `DEATH_SCREEN_DURATION` 秒后切换到电梯场景

## Open Questions

无。
