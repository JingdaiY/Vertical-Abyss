# Sprint 1 — Foundation & Logic Layer

**开始**: 2026-04-07
**结束**: 任务全部完成时
**里程碑**: MVP 可玩原型

## Sprint Goal

实现游戏的全部数据结构和纯逻辑系统——不含任何场景和视觉输出。Sprint 结束时，所有核心数据可以被读写，背包/计时器/雾效逻辑可以被单元测试验证。

---

## Tasks

### Must Have（关键路径，按实现顺序）

| ID | 任务 | 对应 GDD | 输出文件 | 验收标准 |
|----|------|---------|---------|---------|
| S1-01 | 实现 `constants.gd` | game-constants.md | `src/core/constants.gd` | 所有 18 个常量可从任意脚本访问，含 `PLAYER_MAX_HP` |
| S1-02 | 实现 `RunData` + `PersistentData` | run-state-manager.md | `src/core/run_data.gd`, `src/core/persistent_data.gd` | 字段与 GDD 一致；`RunData` 含 `current_hp` |
| S1-03 | 实现 `RunStateManager` Autoload | run-state-manager.md | `src/core/run_state_manager.gd` | `clear_run_data()` 幂等；不影响 persistent |
| S1-04 | 实现 `ItemData` Resource 类 | item-database.md | `src/data/item_data.gd` | 5 个字段 `@export`，可在 Godot Inspector 填写 |
| S1-05 | 创建 5 件物品的 `.tres` 文件 | item-database.md | `res://data/items/*.tres` | 废铁/罐头/旧电池/急救包/燃料桶，权重总和=100 |
| S1-06 | 实现 `FloorTypeData` + `HazardTileData` | floor-content-data.md | `src/data/floor_type_data.gd`, `src/data/hazard_tile_data.gd` | Resource 类，字段可 Inspector 编辑 |
| S1-07 | 创建废弃工业区 `.tres` 文件 | floor-content-data.md | `res://data/floors/abandoned_industrial.tres` | 含 1 种危险地块（broken_floor, damage=1, density=0.08） |
| S1-08 | 实现 `InventorySystem` | inventory-system.md | `src/systems/inventory_system.gd` | `add/remove/get_count/is_full` 通过单元测试 |
| S1-09 | 实现 `TimerSystem` | timer-system.md | `src/systems/timer_system.gd` | `start/stop/_process`，`timer_expired` 只发射一次 |
| S1-10 | 实现 `FogOfWarState` | fog-of-war-state.md | `src/systems/fog_of_war_state.gd` | `initialize` + `update_visibility`，Chebyshev 距离正确 |

### Should Have

| ID | 任务 | 输出文件 | 验收标准 |
|----|------|---------|---------|
| S1-11 | GUT 单元测试：InventorySystem | `tests/unit/test_inventory.gd` | 容量上限、堆叠上限、清空逻辑 |
| S1-12 | GUT 单元测试：TimerSystem | `tests/unit/test_timer.gd` | 归零信号、重复触发防护 |
| S1-13 | GUT 单元测试：RunStateManager | `tests/unit/test_run_state.gd` | clear_run_data 不影响 persistent |

### Nice to Have

| ID | 任务 | 备注 |
|----|------|------|
| S1-14 | `ItemDatabase` 工具类（加载所有 .tres 的静态方法） | 方便其他系统通过 item_id 查询 ItemData |
| S1-15 | 补 `prototypes/vertical-abyss-mvp/README.md` | Gate Check 建议项 |

---

## 文件结构目标（Sprint 1 结束时）

```
src/
├── core/
│   ├── constants.gd
│   ├── run_data.gd
│   ├── persistent_data.gd
│   └── run_state_manager.gd
├── data/
│   ├── item_data.gd
│   └── floor_type_data.gd
│   └── hazard_tile_data.gd
├── systems/
│   ├── inventory_system.gd
│   ├── timer_system.gd
│   └── fog_of_war_state.gd
res://data/
├── items/
│   ├── scrap_metal.tres
│   ├── canned_food.tres
│   ├── old_battery.tres
│   ├── first_aid_kit.tres
│   └── fuel_barrel.tres
└── floors/
    └── abandoned_industrial.tres
tests/
└── unit/
    ├── test_inventory.gd
    ├── test_timer.gd
    └── test_run_state.gd
```

---

## Risks

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| Godot `.tres` 文件格式学习曲线 | 中 | 低 | Resource 类 + Inspector 编辑是 Godot 标准模式；参考 docs/engine-reference |
| GUT 测试框架配置 | 低 | 低 | GUT 已在 technical-preferences.md 指定；按官方文档安装 |
| `RunStateManager` 作为 Autoload 的全局访问模式 | 低 | 高 | GDD 已明确架构；`constants.gd` 同样是全局访问，模式一致 |

---

## Definition of Done

- [ ] S1-01 到 S1-10 全部完成
- [ ] 无魔法数字（src/ 下无裸露的 60、150、48 等关键数值）
- [ ] 所有 GDScript 使用静态类型（`var x: int`，不用 `var x`）
- [ ] Should Have 测试（S1-11 到 S1-13）通过

---

## Sprint 2 预览

**目标**：可见层——玩家实体 + 楼层生成器 + 楼层场景可运行（无 HUD，无雾效渲染）

主要任务：`PlayerController.tscn`、`FloorGenerator`、`FloorScene` 组装、`EvacuationDetection`、`DeathSystem`
