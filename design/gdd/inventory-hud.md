# 背包 HUD (Inventory HUD)

> **Status**: Designed
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: Pillar 1（压迫即乐趣）

## Overview

显示当前背包内容和容量使用情况。楼层内和电梯内均显示。

## Detailed Design

### Core Rules

```gdscript
@onready var item_list: VBoxContainer = $ItemList
@onready var capacity_label: Label = $CapacityLabel

func _process(_delta: float) -> void:
    # 清空并重建列表（MVP 简单实现）
    for child in item_list.get_children():
        child.queue_free()
    var total: int = 0
    for item_id in RunStateManager.run.inventory:
        var count: int = RunStateManager.run.inventory[item_id]
        total += count
        var item_data: ItemData = ItemDatabase.get_item(item_id)
        var label: Label = Label.new()
        label.text = "%s × %d" % [item_data.display_name, count]
        item_list.add_child(label)
    capacity_label.text = "%d / %d" % [total, Constants.INVENTORY_MAX_CAPACITY]
    if total >= Constants.INVENTORY_MAX_CAPACITY:
        capacity_label.add_theme_color_override("font_color", Color.RED)
```

位置：屏幕右侧或底部。

## Acceptance Criteria

- [ ] 拾取物品后 HUD 立即更新
- [ ] 容量满时容量数字变红
- [ ] 死亡后背包清空，HUD 显示空

## Dependencies

→ RunStateManager、→ 物品数据库、→ 游戏常量（INVENTORY_MAX_CAPACITY）
