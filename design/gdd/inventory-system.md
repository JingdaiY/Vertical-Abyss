# 背包系统 (Inventory System)

> **Status**: Designed
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: Pillar 1（压迫即乐趣）

## Overview

背包系统是 `RunStateManager.run.inventory` 的操作接口层。它不持有自己的状态——数据全部在 RSM 里。提供 add/remove/query 三类方法，供物品拾取系统和电梯房间系统调用。

## Player Fantasy

背包快满的时候，玩家面临"再拿一个还是现在就跑"的压迫感。这个系统让每次拾取决策都有重量。

## Detailed Design

### Core Rules

```gdscript
# 容量按总件数计算，非槽位数
func is_full() -> bool:
    var total: int = 0
    for count in RunStateManager.run.inventory.values():
        total += count
    return total >= Constants.INVENTORY_MAX_CAPACITY

func add_item(item_id: String, count: int = 1) -> bool:
    # 检查总容量上限
    if is_full():
        return false
    # 检查同类堆叠上限
    var item_data: ItemData = ItemDatabase.get_item(item_id)
    var current: int = RunStateManager.run.inventory.get(item_id, 0)
    var addable: int = mini(count, item_data.stack_limit - current)
    if addable <= 0:
        return false
    RunStateManager.run.inventory[item_id] = current + addable
    return true

func remove_item(item_id: String, count: int = 1) -> void:
    var current: int = RunStateManager.run.inventory.get(item_id, 0)
    var new_count: int = current - count
    if new_count <= 0:
        RunStateManager.run.inventory.erase(item_id)
    else:
        RunStateManager.run.inventory[item_id] = new_count

func get_count(item_id: String) -> int:
    return RunStateManager.run.inventory.get(item_id, 0)
```

### States and Transitions

N/A — 无状态机，纯操作层。

### Interactions with Other Systems

| 系统 | 接口 |
|------|------|
| RunStateManager | 读写 `run.inventory` |
| 游戏常量 | 读取 `INVENTORY_MAX_CAPACITY` |
| 物品数据库 | 读取 `stack_limit` |
| 物品拾取系统 | 调用 `add_item()` |
| 电梯房间系统 | 调用 `remove_item()` 消耗建造材料 |

## Formulas

```
可用容量 = INVENTORY_MAX_CAPACITY - Σ(inventory.values())
```

## Edge Cases

| 场景 | 预期行为 |
|------|---------|
| `count` 传入负数或 0 | 断言失败（开发模式崩溃） |
| `item_id` 不存在于物品数据库 | 日志警告，返回 false |
| `get_count` 查询不存在的 item_id | 返回 0，不报错 |
| 背包已满但物品未达堆叠上限 | 总容量优先，返回 false |

## Dependencies

| 系统 | 方向 | 性质 |
|------|------|------|
| RunStateManager | 背包 → RSM | 硬依赖 |
| 游戏常量 | 背包 → 常量 | 硬依赖 |
| 物品数据库 | 背包 → 物品数据库 | 硬依赖 |

## Tuning Knobs

| 参数 | 当前值 | 安全范围 | 效果 |
|------|--------|---------|------|
| `INVENTORY_MAX_CAPACITY` | 20 | 5–30 | 越低压迫感越强 |

## Visual/Audio Requirements

N/A — 纯逻辑层。

## UI Requirements

背包 HUD 读取 `inventory` 显示内容，不属于本系统。

## Acceptance Criteria

- [ ] 总件数达到 20 后 `add_item` 返回 false
- [ ] `remove_item` 降到 0 时 key 从 dictionary 中删除
- [ ] `add_item` 不超过物品 `stack_limit`
- [ ] `clear_run_data()` 后背包为空

## Open Questions

无。
