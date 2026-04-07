# 楼层探索场景 (Floor Exploration Scene)

> **Status**: Designed
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: All pillars

## Overview

楼层探索场景（`FloorScene.tscn`）是核心游戏循环的主场景。它组装所有楼层子系统，处理生命周期（初始化→游戏中→结束），监听信号做场景切换。

## Player Fantasy

N/A — 场景是容器，乐趣来自子系统。

## Detailed Design

### Core Rules

**节点树结构**：
```
FloorScene (Node2D)
├── TileMapLayer          # 地图渲染
├── FogRenderer           # CanvasLayer，雾效覆盖层
├── PlayerController      # 玩家实体
├── ItemPickupSystem      # 物品拾取逻辑
├── EvacuationDetection   # 撤离检测
├── DeathSystem           # 死亡处理
├── TimerSystem           # 计时器
├── FogOfWarState         # 雾效数据
└── HUD (CanvasLayer)
    ├── TimerHUD
    └── InventoryHUD
```

**生命周期**：
```gdscript
func _ready() -> void:
    var seed: int = RunStateManager.run.floor_seed
    FloorGenerator.generate(seed)          # 生成地图
    FogOfWarState.initialize(10, 10)       # 初始化雾效
    TimerSystem.start_floor_timer()        # 启动计时器
    # 连接信号
    DeathSystem.connect_signals(PlayerController, TimerSystem)
    EvacuationDetection.evacuation_success.connect(_on_evacuation_success)

func _on_evacuation_success() -> void:
    TimerSystem.stop()
    RunStateManager.run.current_floor = 0
    get_tree().change_scene_to_file("res://scenes/elevator/ElevatorHub.tscn")
```

### States and Transitions

`[场景加载] → PLAYING → [撤离成功 / 死亡] → [场景切换]`

### Interactions with Other Systems

组装层，所有交互通过子节点信号处理。

## Formulas

无。

## Edge Cases

| 场景 | 预期行为 |
|------|---------|
| 撤离和死亡信号同时到达 | DeathSystem 的 `_death_handled` 标志防止双重处理 |

## Dependencies

依赖所有楼层子系统（见节点树）。

## Tuning Knobs

无（各子系统各自有旋钮）。

## Visual/Audio Requirements

N/A — 由子节点负责。

## UI Requirements

HUD CanvasLayer 包含计时器和背包显示。

## Acceptance Criteria

- [ ] 场景加载后计时器自动启动
- [ ] 撤离成功后切换到电梯场景
- [ ] 死亡后切换到电梯场景
- [ ] 两种结束方式不会同时触发场景切换

## Open Questions

无。
