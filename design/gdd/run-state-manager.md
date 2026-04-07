# 跑团状态管理器 (Run State Manager)

> **Status**: In Design
> **Author**: User + Claude
> **Last Updated**: 2026-04-07
> **Implements Pillar**: Pillar 2（电梯是家）+ All pillars（架构基础，硬重置惩罚的技术支撑）

## Overview

跑团状态管理器（`src/core/run_state_manager.gd`）是游戏中所有状态数据的分类层——它不存储逻辑，只定义"什么是跑团数据（死亡时清除）"和"什么是永久数据（跨跑团保留）"的边界。所有其他系统通过它读写状态，不直接持有全局状态变量。它是硬重置惩罚机制的技术基础：玩家死亡时，系统调用 `clear_run_data()` 清除当次跑团的所有临时状态；电梯解锁进度、死亡次数、历史最深楼层等永久数据不受影响，由持久化存储系统负责写入 localStorage。

## Player Fantasy

这是一个"你感受不到它存在，但你感受得到它的后果"的系统。当玩家死亡，背包归零，计时器消失，他们感受到的那种"一切都没了"的失落感——就是这个系统在正确工作。而当他们回到电梯，发现上次建好的房间还在，那盏灯还亮着——这也是这个系统在正确工作。

跑团状态管理器是 Pillar 2（电梯是家）的技术契约：电梯里的东西是真实的、持久的；深渊里的东西是借来的、脆弱的。每次进入楼层，玩家都知道这件事，这种知道本身就是游戏的一部分。

## Detailed Design

### Core Rules

1. **双结构原则**：所有游戏状态分为两类，分别持有在不同生命周期的结构体中：

   ```gdscript
   class_name RunStateManager extends Node

   # ── 跑团数据（Run Data）── 死亡时调用 clear_run_data() 全部归零 ──
   var run: RunData = RunData.new()

   # ── 永久数据（Persistent Data）── 跨跑团保留，持久化存储系统负责读写 ──
   var persistent: PersistentData = PersistentData.new()
   ```

2. **RunData 结构**（跑团内临时状态）：
   ```gdscript
   class_name RunData extends RefCounted

   var inventory: Dictionary[String, int] = {}  # {item_id: count}
   var current_floor: int = 0                   # 当前所在楼层（0 = 电梯）
   var current_hp: int = Constants.PLAYER_MAX_HP  # 当前血量；死亡时随 clear() 重置
   var timer_remaining: float = 0.0             # 楼层倒计时剩余秒数
   var floor_seed: int = 0                      # 当前楼层生成用的随机种子
   ```

3. **PersistentData 结构**（跨跑团永久状态）：
   ```gdscript
   class_name PersistentData extends RefCounted

   var unlocked_rooms: Array[String] = []  # 已解锁的电梯房间 ID 列表
   var total_deaths: int = 0               # 历史总死亡次数
   var deepest_floor_reached: int = 0      # 历史最深到达楼层
   ```

4. **clear_run_data() 行为**：死亡系统调用此方法。它将 `run` 替换为一个新的空 `RunData` 实例。永久数据不受影响。

5. **禁止系统直接持有状态**：背包系统、计时器系统等不得在各自脚本中声明独立的状态变量来重复存储 `RunData` 中已有的数据。它们只通过 `RunStateManager.run.*` 读写。

6. **访问方式**：`RunStateManager` 作为 Autoload（全局服务）注册。例外说明：它不包含任何游戏逻辑，纯粹是状态容器，符合"Autoload 只用于真正全局的服务"原则（见 technical-preferences.md Forbidden Patterns）。

### States and Transitions

```
[游戏启动]
    │
    ▼
IDLE（在电梯）
    │ 玩家下降进入楼层
    ▼
IN_FLOOR（探索楼层）── 计时器耗尽 or 死亡 ──► DEAD
    │                                            │
    │ 玩家成功撤离                             clear_run_data()
    ▼                                            │
IDLE（回到电梯）◄───────────────────────────────┘
```

| 状态 | `run.current_floor` | `run.inventory` | 描述 |
|------|---------------------|-----------------|------|
| IDLE | 0 | 保留（撤离带回的物品） | 玩家在电梯中枢 |
| IN_FLOOR | ≥ 1 | 当前携带中 | 玩家在某楼层探索 |
| DEAD | — | 清空 | 死亡后短暂状态，立即 clear_run_data()，回到 IDLE |

### Interactions with Other Systems

| 下游系统 | 读/写 | 具体接口 |
|---------|-------|---------|
| 背包系统 | 读写 | `run.inventory` — 拾取时写入，死亡时随 clear 归零 |
| 计时器系统 | 读写 | `run.timer_remaining` — 每帧更新；楼层开始时初始化 |
| 死亡系统 | 写 | 调用 `clear_run_data()`；写入 `persistent.total_deaths += 1` |
| 楼层生成器 | 读写 | `run.current_floor`（楼层编号）、`run.floor_seed`（生成种子） |
| 电梯房间系统 | 读写 | `persistent.unlocked_rooms` — 建造成功时追加 ID |
| 持久化存储 | 读写 | 游戏启动时从 localStorage 加载 `PersistentData`；每次更新永久数据后触发保存 |
| 难度追踪器/DDA | 读 | `persistent.deepest_floor_reached`（元进度等级输入） |

## Formulas

跑团状态管理器不定义公式——它是状态容器，不是计算单元。以下引用关系记录哪些系统依赖其数据作为公式输入：

| 公式 | 所在 GDD | 引用的状态字段 |
|------|---------|-------------|
| DDA 元进度等级计算 | 难度追踪器/DDA GDD | `persistent.deepest_floor_reached` |
| 楼层生成确定性随机 | 楼层生成器 GDD | `run.floor_seed` |
| 死亡惩罚清零 | 死亡系统 GDD | `run.*`（全部跑团字段） |

## Edge Cases

| 场景 | 预期行为 | 理由 |
|------|---------|------|
| 游戏崩溃发生在 `clear_run_data()` 之前（死亡时） | 下次启动时检测到 `run.current_floor > 0` 但玩家在电梯——强制执行 `clear_run_data()` 并跳回电梯 | 防止玩家卡在"幽灵楼层"状态 |
| localStorage 数据损坏或缺失 | 从空 `PersistentData` 重新开始（所有永久进度归零），日志打印警告 | 不能因存储损坏导致游戏无法启动 |
| `persistent.unlocked_rooms` 包含不存在的房间 ID | 启动时过滤无效 ID，日志打印警告；不崩溃 | 容忍内容配置变更导致的 ID 失效 |
| `clear_run_data()` 被调用多次（如死亡系统 bug 导致双重触发） | 幂等操作——多次 clear 结果相同，不报错 | 防御性设计 |
| `run.inventory` 中出现未知 `item_id`（物品被从数据库删除） | 背包系统跳过该条目，日志警告；不崩溃 | 内容迭代期间常见 |

## Dependencies

| 系统 | 方向 | 依赖性质 |
|------|------|---------|
| （无上游依赖） | — | Foundation 根节点 |
| 背包系统 | 背包系统 → 此系统 | 硬依赖 — 读写 `run.inventory` |
| 计时器系统 | 计时器系统 → 此系统 | 硬依赖 — 读写 `run.timer_remaining` |
| 死亡系统 | 死亡系统 → 此系统 | 硬依赖 — 调用 `clear_run_data()`；写入 `persistent.total_deaths` |
| 楼层生成器 | 楼层生成器 → 此系统 | 硬依赖 — 读写 `run.current_floor`, `run.floor_seed` |
| 电梯房间系统 | 电梯房间系统 → 此系统 | 硬依赖 — 读写 `persistent.unlocked_rooms` |
| 持久化存储 | 持久化存储 → 此系统 | 硬依赖 — 启动时加载/运行时保存 `PersistentData` |
| 难度追踪器/DDA | DDA → 此系统 | 软依赖 — 读取 `persistent.deepest_floor_reached` 作为元进度输入 |

## Tuning Knobs

跑团状态管理器没有可调节的数值参数——它是结构定义，不是行为实现。影响"多少数据在死亡时丢失"的决策已在 Core Rules 中固化为架构边界。

若未来需要增加新的永久数据字段（如"已解锁的剧情节点"），只需向 `PersistentData` 添加字段并更新持久化存储的序列化逻辑——无需修改任何其他系统。

## Visual/Audio Requirements

N/A — 跑团状态管理器是纯数据层，无视觉或音频输出。

## UI Requirements

N/A — 玩家不直接与此系统交互。状态变化通过背包 HUD、计时器 HUD 等 UI 系统间接呈现。

## Acceptance Criteria

- [ ] `RunStateManager` 以 Autoload 注册后，任意场景的 GDScript 均可通过 `RunStateManager.run.inventory` 访问跑团背包数据，无需实例化任何节点
- [ ] 调用 `clear_run_data()` 后：`run.inventory` 为空字典，`run.current_floor == 0`，`run.timer_remaining == 0.0`
- [ ] 调用 `clear_run_data()` 不影响 `persistent.*` 中的任何字段
- [ ] 多次连续调用 `clear_run_data()` 结果幂等（不报错，不出现意外状态）
- [ ] 游戏启动时若检测到 `run.current_floor > 0`（崩溃恢复场景），自动调用 `clear_run_data()` 并跳回电梯场景
- [ ] `persistent.total_deaths` 在每次 `clear_run_data()` 触发后准确递增 1
- [ ] localStorage 数据损坏时游戏正常启动，`PersistentData` 重置为初始值，日志打印警告

## Open Questions

| 问题 | 负责人 | 目标解决时间 | 解决方案 |
|------|-------|------------|---------|
| 成功撤离后返回电梯，`run.inventory` 中的物品如何转移到电梯房间建造流程？背包系统是否保留 `run.inventory` 直到玩家主动消耗？ | 开发者 | 电梯房间系统 GDD 设计时 | 届时明确"撤离背包"与"建造消耗"的触发时机 |
| `run.floor_seed` 是否应该支持"重播某楼层"功能（相同 seed 生成相同地图）？ | 开发者 | 楼层生成器 GDD 设计时 | 若需要，seed 需设计为可序列化存储的确定性值 |
