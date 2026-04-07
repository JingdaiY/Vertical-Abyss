# 楼层内容数据 (Floor Content Data)

> **Status**: Designed
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: Pillar 1（压迫即乐趣）+ Pillar 3（资源讲故事）

## Overview

楼层内容数据（`res://data/floors/`）定义楼层的环境类型和危险地块类型。MVP 只有一种环境类型。它是楼层生成器的原材料——生成器读取这里的数据决定哪些地块可以是危险的、物品以何种权重出现。纯静态数据，无运行时逻辑。

## Player Fantasy

同一栋废弃建筑，每次下去都可能踩到不同的危险。玩家学会"走中间、绕开深色地块"——这种对楼层环境的警觉感就是这个系统在工作。MVP 阶段只有一种环境，但危险地块分布每次随机，让玩家永远无法完全放松。

## Detailed Design

### Core Rules

1. **FloorTypeData 资源结构**（每种环境类型一个 `.tres` 文件）：
   ```gdscript
   class_name FloorTypeData extends Resource

   @export var type_id: String           # 例如 "abandoned_industrial"
   @export var display_name: String      # 例如 "废弃工业区"
   @export var hazard_tiles: Array[HazardTileData] = []  # 该环境包含的危险地块类型
   @export var item_weight_overrides: Dictionary[String, float] = {}
   # 空字典 = 使用 ItemData.spawn_weight 全局默认值
   # 非空则覆盖特定物品权重，例如 {"fuel_barrel": 15.0}（工业区燃料更多）
   ```

2. **HazardTileData 资源结构**（内嵌在 FloorTypeData 中）：
   ```gdscript
   class_name HazardTileData extends Resource

   @export var tile_id: String        # 例如 "broken_floor"
   @export var display_name: String   # 例如 "破损地板"
   @export var damage_per_step: int   # 每次踩上扣除的 HP（整数）
   @export var spawn_density: float   # 占非出口、非必要通道格子的比例（0.0–0.20）
   ```

3. **MVP 楼层类型（1种）**：

   **废弃工业区（abandoned_industrial）**
   | 字段 | 值 |
   |------|---|
   | `type_id` | `"abandoned_industrial"` |
   | `display_name` | `"废弃工业区"` |
   | `item_weight_overrides` | `{}`（使用全局权重） |

   **危险地块（1种）**：
   | tile_id | display_name | damage_per_step | spawn_density |
   |---------|-------------|-----------------|---------------|
   | `broken_floor` | 破损地板 | 1 | 0.08（约 8% 的可行走格） |

### States and Transitions

N/A — 静态数据层，无状态机。

### Interactions with Other Systems

| 下游系统 | 读取数据 | 接口 |
|---------|---------|------|
| 楼层生成器 | `hazard_tiles`, `item_weight_overrides` | 生成地图时放置危险地块、决定物品权重 |
| 玩家实体 | `damage_per_step`（经楼层生成器传递） | 踩到危险地块时触发扣血 |
| 叙事文本显示 | `display_name` | 进入楼层时显示环境名称 |

## Formulas

```
期望危险地块数 = FLOOR_COLS × FLOOR_ROWS × (1 - FLOOR_WALL_DENSITY) × spawn_density
             = 10 × 10 × (1 - 0.30) × 0.08
             ≈ 5.6 块/层
```

*危险地块不放置于出口通道格子。实际数量略低于理论值。*

## Edge Cases

| 场景 | 预期行为 | 理由 |
|------|---------|------|
| `spawn_density` 导致危险地块与出口通道冲突 | 楼层生成器优先保证出口通道安全；超出部分降级为普通地板 | 楼层必须可通过 |
| `damage_per_step` ≥ 玩家最大 HP | 允许（一踩即死）；Tuning Knobs 注明安全上限 | 保留为极端难度配置 |
| `item_weight_overrides` 包含不存在的 `item_id` | 忽略该条目，日志打印警告 | 容忍内容迭代期间的 ID 失效 |
| MVP 之外增加第二种楼层类型 | 只需新建一个 `FloorTypeData .tres` 文件；楼层生成器无需修改 | 开放/封闭原则 |

## Dependencies

| 系统 | 方向 | 依赖性质 |
|------|------|---------|
| （无上游依赖） | — | Foundation 根节点 |
| 楼层生成器 | 楼层生成器 → 此系统 | 硬依赖 — 读取 `hazard_tiles`, `item_weight_overrides` |
| 玩家实体 | 玩家实体 → 此系统（间接） | 软依赖 — `damage_per_step` 经楼层生成器传递后触发玩家扣血 |
| 叙事文本显示 | 叙事文本显示 → 此系统 | 软依赖 — 读取 `display_name` 显示环境名称 |

## Tuning Knobs

| 参数 | 当前值 | 安全范围 | 调高效果 | 调低效果 |
|------|--------|---------|---------|---------|
| `broken_floor.damage_per_step` | 1 | 1–3 | 危险地块更致命，玩家需要绕路（增加时间成本） | 踩了无所谓，玩家忽略危险 |
| `broken_floor.spawn_density` | 0.08 | 0.03–0.15 | 楼层更难导航，绕路更多 | 危险稀少，玩家感受不到威胁 |

## Visual/Audio Requirements

N/A — 楼层内容数据是纯数据层。危险地块的视觉表现（颜色、图标）属于楼层生成器的渲染职责。

## UI Requirements

N/A — 无直接 UI 需求。环境名称通过叙事文本显示系统呈现。

## Acceptance Criteria

- [ ] 楼层生成器能正确加载 `FloorTypeData`，危险地块实际生成比例在期望值 ±3% 以内（1000 次模拟）
- [ ] 出口通道格子不出现 `broken_floor` 危险地块
- [ ] `item_weight_overrides` 为空时，物品出现概率与全局 `spawn_weight` 一致
- [ ] 新增环境类型只需创建一个 `.tres` 文件，楼层生成器无需修改

## Open Questions

| 问题 | 负责人 | 目标解决时间 |
|------|-------|------------|
| Vertical Slice 阶段是否增加第二种楼层类型（如"潮湿管道区"）？ | 开发者 | Vertical Slice 设计时 |
