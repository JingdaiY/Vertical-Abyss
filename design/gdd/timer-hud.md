# 计时器 HUD (Timer HUD)

> **Status**: Designed
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: Pillar 1（压迫即乐趣）

## Overview

楼层内显示倒计时秒数的 UI 元素。`<= TIMER_URGENCY_THRESHOLD` 时变红色。

## Detailed Design

### Core Rules

```gdscript
@onready var label: Label = $Label

func _process(_delta: float) -> void:
    var t: float = RunStateManager.run.timer_remaining
    label.text = "%.0f" % ceilf(t)
    if t <= Constants.TIMER_URGENCY_THRESHOLD:
        label.add_theme_color_override("font_color", Color.RED)
    else:
        label.remove_theme_color_override("font_color")
```

放置于 HUD CanvasLayer，位置：屏幕顶部中央。

## Acceptance Criteria

- [ ] 显示数字与 `run.timer_remaining` 误差 < 1 帧
- [ ] ≤ 15s 时变红色
- [ ] 0s 时显示"0"

## Dependencies

→ RunStateManager（读取 `run.timer_remaining`）、→ 游戏常量（TIMER_URGENCY_THRESHOLD）
