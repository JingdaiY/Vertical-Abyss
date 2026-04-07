# 物品拾取系统 (Item Pickup System)

> **Status**: Designed
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: Pillar 1（压迫即乐趣）

## Overview

玩家按 E 键时，检查交互半径内是否有物品节点；有则调用 `InventorySystem.add_item()`，成功后从场景移除该物品节点并显示短暂提示。

## Player Fantasy

按下 E 的瞬间紧张感：背包快满了，这件物品值得拿吗？

## Detailed Design

### Core Rules

1. 物品节点（`ItemPickup.tscn`）放置在楼层场景中，持有 `item_id: String`
2. 玩家实体发射 `item_in_range(item_node)` / `item_out_of_range(item_node)` 信号
3. 物品拾取系统维护 `nearby_items: Array[Node2D]` 列表
4. 玩家按 E 键时：取 `nearby_items` 中最近的物品，调用 `InventorySystem.add_item(item_id)`
5. 成功：从场景 `queue_free()` 物品节点；失败（背包满）：HUD 显示"背包已满"提示

### States and Transitions

N/A。

### Interactions with Other Systems

| 系统 | 接口 |
|------|------|
| 玩家实体 | 监听 `item_in_range` / `item_out_of_range` |
| 背包系统 | 调用 `add_item()` |
| 物品数据库 | 读取 `display_name`（用于拾取提示文本） |
| 叙事文本显示 | 拾取成功时显示 `lore_text` |

## Formulas

无。

## Edge Cases

| 场景 | 预期行为 |
|------|---------|
| 同时有多个物品在范围内 | 拾取距离最近的一件 |
| 背包满 | 返回 false，物品留在场景中，HUD 提示 |
| 物品节点已被 queue_free（竞态） | 检查节点是否有效再操作 |

## Dependencies

| 系统 | 方向 | 性质 |
|------|------|------|
| 玩家实体 | 物品拾取 → 玩家 | 硬依赖（信号） |
| 背包系统 | 物品拾取 → 背包 | 硬依赖 |
| 物品数据库 | 物品拾取 → 数据库 | 硬依赖 |

## Tuning Knobs

`PLAYER_INTERACTION_RADIUS = 56px`（在游戏常量中调整）。

## Visual/Audio Requirements

拾取成功：短暂弹出物品名称文字（0.8s 淡出）。

## UI Requirements

"背包已满"提示属于背包 HUD 的职责。

## Acceptance Criteria

- [ ] 按 E 后物品从场景消失，`inventory` 中该物品数量 +1
- [ ] 背包满时物品不消失
- [ ] 交互半径外按 E 无响应

## Open Questions

无。
