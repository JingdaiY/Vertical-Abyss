# 玩家实体 (Player Entity)

> **Status**: Designed
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: Pillar 1（压迫即乐趣）

## Overview

玩家实体（`src/entities/player.gd` + `PlayerController.tscn`）是玩家在楼层内的物理存在。MVP 只有三个属性：HP（当前/最大）、移动速度（读自 Constants）、背包容量（读自 Constants）。它负责在场景中移动、与危险地块交互（踩踏触发扣血）、触发物品拾取半径检测。HP 存储在 `RunStateManager.run.current_hp`，死亡时随跑团数据清除。

## Player Fantasy

玩家永远感觉自己"差一步"——时间不够、背包要满、HP 还在掉。移动速度决定了楼层的"心跳节奏"；HP 给了玩家一条除计时器之外的死亡线，让每块破损地板都是一个需要判断的决策点：绕路费时间，直走费血量。两条死亡线同时收紧，这就是 Pillar 1 的物理实现。

## Detailed Design

### Core Rules

1. **玩家实体读取的常量（来自 `src/core/constants.gd`）**：
   - `PLAYER_SPEED = 150.0 px/s` — 移动速度
   - `PLAYER_COLLISION_RADIUS = 14.0 px` — 碰撞体半径
   - `PLAYER_INTERACTION_RADIUS = 56.0 px` — 物品拾取交互范围
   - `PLAYER_MAX_HP = 5` — 最大血量（整数）
   - `INVENTORY_MAX_CAPACITY = 20` — 背包上限（由背包系统读取）

2. **HP 存储位置**：`RunStateManager.run.current_hp: int`，初始值为 `Constants.PLAYER_MAX_HP`。死亡后随 `clear_run_data()` 重置。

3. **危险地块扣血流程**：
   - 玩家移动进入某格
   - 若该格被楼层生成器标记为危险地块，读取其 `damage_per_step`
   - 执行 `RunStateManager.run.current_hp -= damage_per_step`
   - 每次**进入**该格扣一次血；驻留不持续扣血
   - 若 `current_hp <= 0`，发射信号 `player_died()`

4. **移动方式**：4方向（上下左右）。简化碰撞逻辑，避免对角移动导致的地块检测复杂性。

5. **信号定义**：
   ```gdscript
   signal player_died()
   signal item_in_range(item_node: Node2D)   # 物品进入交互半径
   signal item_out_of_range(item_node: Node2D)
   ```

### States and Transitions

| 状态 | 描述 | 进入条件 | 退出条件 |
|------|------|---------|---------|
| ALIVE | 正常探索 | 楼层开始 / 新跑团 | `current_hp <= 0` 或 `timer_expired` |
| DEAD | 死亡等待 | `current_hp <= 0` 或计时器归零 | 死亡系统处理完成后回到电梯（新跑团 → ALIVE） |

死亡只触发一次：`player_died` 信号发射后玩家实体冻结输入，等待死亡系统接管。

### Interactions with Other Systems

| 系统 | 接口 | 方向 |
|------|------|------|
| 游戏常量 | 读取 `PLAYER_SPEED`, `PLAYER_MAX_HP`, `PLAYER_COLLISION_RADIUS`, `PLAYER_INTERACTION_RADIUS` | 玩家 → 常量 |
| 跑团状态管理器 | 读写 `run.current_hp` | 玩家 → RSM |
| 楼层生成器 | 读取当前格的 `damage_per_step` | 玩家 → 楼层（间接） |
| 物品拾取系统 | 发射 `item_in_range` / `item_out_of_range` | 玩家 → 物品拾取 |
| 撤离检测 | 玩家进入出口区域触发撤离 | 玩家 → 撤离检测 |
| 死亡系统 | 监听 `player_died` 信号 | 死亡系统 → 玩家 |

## Formulas

HP 是整数加减运算，无公式。

```
current_hp_new = current_hp - damage_per_step   （踩危险地块）
死亡条件: current_hp_new <= 0
重置: current_hp = PLAYER_MAX_HP                （新跑团开始）
```

## Edge Cases

| 场景 | 预期行为 | 理由 |
|------|---------|------|
| 玩家在危险地块上按住方向键不动 | 进入时扣一次血，之后不扣 | 惩罚"误踩"而非"站在上面" |
| `current_hp <= 0` 和 `timer_expired` 同时发生 | 死亡系统只触发一次；先到信号优先，第二路信号忽略 | 防止死亡逻辑执行两次 |
| 急救包能否回血 | MVP 阶段不回血；急救包仅作建造材料 | 简化 MVP；回血机制留 Vertical Slice |
| `PLAYER_MAX_HP = 1` | 一踩即死；合法边缘配置，不崩溃 | 保留为高难模式可选 |

## Dependencies

| 系统 | 方向 | 依赖性质 |
|------|------|---------|
| 游戏常量 | 玩家实体 → 此系统 | 硬依赖 — `PLAYER_SPEED`, `PLAYER_MAX_HP` 等 |
| 跑团状态管理器 | 玩家实体 → 此系统 | 硬依赖 — 读写 `run.current_hp` |
| 楼层内容数据 | 玩家实体 → 此系统（间接） | 软依赖 — 通过楼层生成器获取危险地块 `damage_per_step` |
| 物品拾取系统 | 物品拾取系统 → 玩家实体 | 依赖方向：物品拾取系统监听玩家信号 |
| 死亡系统 | 死亡系统 → 玩家实体 | 依赖方向：死亡系统监听 `player_died` 信号 |
| 撤离检测 | 撤离检测 → 玩家实体 | 依赖方向：撤离检测监听玩家位置 |

## Tuning Knobs

| 参数 | 当前值 | 安全范围 | 调高效果 | 调低效果 |
|------|--------|---------|---------|---------|
| `PLAYER_MAX_HP` | 5 | 3–10 | 玩家更耐打，危险地块威胁降低 | 玩家更脆弱，绕路决策更紧张 |
| `PLAYER_SPEED` | 150 px/s | 100–220 px/s | 楼层感觉更小，节奏加快 | 楼层感觉更大，返回出口成本更高 |

## Visual/Audio Requirements

- 玩家角色：简单方形或圆形精灵，MVP 可用纯色占位
- 受伤反馈：踩到危险地块时短暂闪烁红色（0.2s）
- 死亡：玩家精灵淡出，触发 `player_died` 信号

## UI Requirements

- HP 显示：楼层内 HUD 显示当前/最大 HP（如"HP: 3/5"）
- 参考：计时器 HUD 同层显示，保持视觉一致性

## Acceptance Criteria

- [ ] 玩家进入危险地块格子一次，`RunStateManager.run.current_hp` 精确减少 `damage_per_step`
- [ ] 驻留在危险地块格子不持续扣血（每次进入只触发一次）
- [ ] `current_hp <= 0` 时发射 `player_died` 信号，且只发射一次
- [ ] 计时器归零与 `current_hp <= 0` 同时发生时，死亡系统只执行一次
- [ ] `clear_run_data()` 后 `RunStateManager.run.current_hp` 恢复为 `Constants.PLAYER_MAX_HP`
- [ ] 移动速度严格等于 `Constants.PLAYER_SPEED`，无本地硬编码

## Open Questions

| 问题 | 负责人 | 目标解决时间 |
|------|-------|------------|
| 移动方向：4方向是否足够？是否需要8方向支持斜向移动？ | 开发者 | Godot 原型实测时确认 |
