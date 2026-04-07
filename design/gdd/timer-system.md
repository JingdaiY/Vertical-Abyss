# 计时器系统 (Timer System)

> **Status**: Designed
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: Pillar 1（压迫即乐趣）

## Overview

计时器系统管理 `RunStateManager.run.timer_remaining` 的倒计时。每帧递减；归零发射 `timer_expired` 信号。它是楼层内压迫感的技术核心。

## Player Fantasy

计时器不是惩罚——它是乐趣本身。玩家在 15 秒警戒线时的肾上腺素就是这个系统正常工作的证明。

## Detailed Design

### Core Rules

```gdscript
signal timer_expired()
signal timer_urgent()     # 只发射一次，当 timer_remaining 首次 <= TIMER_URGENCY_THRESHOLD

var _urgent_fired: bool = false

func start_floor_timer() -> void:
    RunStateManager.run.timer_remaining = Constants.TIMER_BASE_DURATION
    # [provisional] 未来由 DDA 系统提供实际值替换 TIMER_BASE_DURATION
    _urgent_fired = false

func stop() -> void:
    set_process(false)  # 撤离成功时调用

func _process(delta: float) -> void:
    var t: float = RunStateManager.run.timer_remaining
    if t <= 0.0:
        return
    RunStateManager.run.timer_remaining = maxf(0.0, t - delta)
    if not _urgent_fired and RunStateManager.run.timer_remaining <= Constants.TIMER_URGENCY_THRESHOLD:
        _urgent_fired = true
        timer_urgent.emit()
    if RunStateManager.run.timer_remaining <= 0.0:
        set_process(false)
        timer_expired.emit()
```

### States and Transitions

| 状态 | 描述 |
|------|------|
| STOPPED | 未在计时（电梯内、死亡后） |
| RUNNING | 每帧递减 |
| URGENT | timer_remaining ≤ 15s，已发射 timer_urgent |
| EXPIRED | timer_remaining = 0，已发射 timer_expired |

### Interactions with Other Systems

| 系统 | 接口 |
|------|------|
| RunStateManager | 读写 `run.timer_remaining` |
| 游戏常量 | 读取 `TIMER_BASE_DURATION`, `TIMER_URGENCY_THRESHOLD` |
| 楼层探索场景 | 调用 `start_floor_timer()` / `stop()` |
| 死亡系统 | 监听 `timer_expired` |
| 计时器 HUD | 读取 `run.timer_remaining` 显示 |

## Formulas

```
timer_remaining(t) = TIMER_BASE_DURATION - elapsed_seconds   （线性递减）
```

## Edge Cases

| 场景 | 预期行为 |
|------|---------|
| `timer_expired` 和 `player_died` 同时触发 | 死亡系统只处理一次（先到先处理） |
| 撤离成功时计时器归零之前 | `stop()` 停止计时，不发射 `timer_expired` |
| `start_floor_timer()` 重复调用 | 重置计时器和 `_urgent_fired` 标志 |

## Dependencies

| 系统 | 方向 | 性质 |
|------|------|------|
| RunStateManager | 计时器 → RSM | 硬依赖 |
| 游戏常量 | 计时器 → 常量 | 硬依赖 |
| 难度追踪器/DDA | DDA → 计时器 | 软依赖（provisional）— DDA 完成后提供初始时长 |

## Tuning Knobs

| 参数 | 当前值 | 安全范围 | 效果 |
|------|--------|---------|------|
| `TIMER_BASE_DURATION` | 60s | 30–120s | 调低更紧迫 |
| `TIMER_URGENCY_THRESHOLD` | 15s | 10–25s | 控制红色警戒持续时长 |

## Visual/Audio Requirements

- 计时器 HUD：`<= TIMER_URGENCY_THRESHOLD` 时变红色（由 HUD 实现，非此系统）

## UI Requirements

计时器 HUD 负责显示，此系统只提供数据。

## Acceptance Criteria

- [ ] `start_floor_timer()` 后 `run.timer_remaining` 等于 `TIMER_BASE_DURATION`
- [ ] 60 秒后 `timer_expired` 发射，误差 < 0.1s
- [ ] `timer_urgent` 只在首次穿过阈值时发射一次
- [ ] `stop()` 后不再发射任何信号
- [ ] `clear_run_data()` 后 `run.timer_remaining = 0.0`

## Open Questions

- `TIMER_BASE_DURATION` 初始值 60s 需在 Godot 原型实测后确认感受是否合适。
