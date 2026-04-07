# 电梯中枢场景 (Elevator Hub Scene)

> **Status**: Designed
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: Pillar 2（电梯是家）

## Overview

电梯中枢场景（`ElevatorHub.tscn`）是玩家的安全港。玩家在此看到带回的物品，并可以按"下降"按钮开始新的楼层探索。MVP 阶段建造功能为占位（Vertical Slice 实现）。

## Player Fantasy

回到电梯，看到背包里的收获，短暂的安全感。然后是"再下去一层"的冲动。

## Detailed Design

### Core Rules

**节点树**：
```
ElevatorHub (Node2D)
├── ElevatorTileMap       # 2×2 大格（ELEVATOR_TILE_SIZE = 96px）
├── PlayerController      # 玩家在电梯内移动
├── DescendButton         # 按钮节点，触发下降
└── HUD (CanvasLayer)
    └── InventoryHUD      # 显示当前背包内容
```

**生命周期**：
```gdscript
func _ready() -> void:
    RunStateManager.run.current_floor = 0
    DescendButton.pressed.connect(_on_descend_pressed)

func _on_descend_pressed() -> void:
    RunStateManager.run.current_floor = 1
    RunStateManager.run.floor_seed = randi()  # 新楼层种子
    get_tree().change_scene_to_file("res://scenes/floor/FloorScene.tscn")
```

MVP 阶段电梯内没有建造界面——背包里的物品只是展示，等待 Vertical Slice 的电梯房间系统接入。

### States and Transitions

`[场景加载] → IDLE（等待玩家按下降）→ [切换到楼层场景]`

### Interactions with Other Systems

| 系统 | 接口 |
|------|------|
| RunStateManager | 写入 `run.current_floor = 0`；下降时写入 `run.floor_seed` |
| 背包系统 | 读取 `run.inventory` 显示内容 |

## Formulas

无。

## Edge Cases

| 场景 | 预期行为 |
|------|---------|
| 背包为空时进入电梯 | 正常显示空背包，允许直接下降 |

## Dependencies

| 系统 | 方向 | 性质 |
|------|------|------|
| RunStateManager | 电梯 → RSM | 硬依赖 |
| 背包系统 | 电梯 → 背包 | 软依赖（显示） |

## Tuning Knobs

`ELEVATOR_TILE_SIZE = 96px`（在常量中调整）。

## Visual/Audio Requirements

电梯内感觉温暖、安全，与楼层的压迫感对比。具体视觉留给 art-director。

## UI Requirements

背包 HUD 在电梯内同样显示。下降按钮简单可见即可。

## Acceptance Criteria

- [ ] 进入场景时 `run.current_floor = 0`
- [ ] 按下降后切换到楼层场景，`run.current_floor = 1`，`floor_seed` 已设置

## Open Questions

- 电梯内是否需要玩家可以自由移动？MVP 阶段可以简化为静态画面 + 下降按钮。
