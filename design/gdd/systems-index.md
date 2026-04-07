# Systems Index: 垂直深渊 | Vertical Abyss

> **Status**: Draft
> **Created**: 2026-04-07
> **Last Updated**: 2026-04-07
> **Source Concept**: design/gdd/game-concept.md

---

## Overview

垂直深渊是一款以"压迫感"为核心的 Roguelite 生存游戏。其系统规模适中，围绕三条核心动词轴展开：**押注进入（COMMIT）→ 压力下搜刮（SEARCH）→ 活着回来（SURVIVE）**。游戏需要一个能严格区分"跑团数据"与"永久数据"的架构——这是硬重置惩罚机制的技术基础，也是电梯中枢成为"真实家园"的情感基础。所有系统都服从四个设计支柱：压迫即乐趣、电梯是家、资源讲故事、每次死亡都值得。

---

## Systems Enumeration

| # | 系统名称 | 类别 | 优先级 | 状态 | 设计文档 | 依赖系统 |
|---|---------|------|--------|------|---------|---------|
| 1 | 游戏常量 | Foundation | MVP | Designed | design/gdd/game-constants.md | — |
| 2 | 物品数据库 | Economy | MVP | Designed | design/gdd/item-database.md | — |
| 3 | 楼层内容数据 | Economy | MVP | Designed | design/gdd/floor-content-data.md | — |
| 4 | 跑团状态管理器 | Persistence | MVP | Designed | design/gdd/run-state-manager.md | — |
| 5 | 玩家实体 | Core | MVP | Designed | design/gdd/player-entity.md | 游戏常量 |
| 6 | 背包系统 | Gameplay | MVP | Designed | design/gdd/inventory-system.md | 物品数据库, 游戏常量, 跑团状态管理器 |
| 7 | 计时器系统 | Gameplay | MVP | Designed | design/gdd/timer-system.md | 游戏常量, 难度追踪器(provisional) |
| 8 | 楼层生成器 | Gameplay | MVP | Designed | design/gdd/floor-generator.md | 楼层内容数据, 游戏常量 |
| 9 | 雾效状态 | Gameplay | MVP | Designed | design/gdd/fog-of-war-state.md | 游戏常量 |
| 10 | 物品拾取系统 | Gameplay | MVP | Designed | design/gdd/item-pickup-system.md | 玩家实体, 背包系统, 物品数据库 |
| 11 | 撤离检测 | Gameplay | MVP | Designed | design/gdd/evacuation-detection.md | 玩家实体, 计时器系统 |
| 12 | 死亡系统 | Gameplay | MVP | Designed | design/gdd/death-system.md | 背包系统, 计时器系统, 跑团状态管理器 |
| 13 | 楼层探索场景 | Core | MVP | Designed | design/gdd/floor-scene.md | 玩家实体, 计时器系统, 楼层生成器, 雾效状态, 物品拾取系统, 撤离检测, 死亡系统 |
| 14 | 电梯中枢场景 | Core | MVP | Designed | design/gdd/elevator-hub-scene.md | 玩家实体, 背包系统, 电梯房间系统(provisional), 持久化存储(provisional) |
| 15 | 计时器HUD | UI | MVP | Designed | design/gdd/timer-hud.md | 计时器系统 |
| 16 | 背包HUD | UI | MVP | Designed | design/gdd/inventory-hud.md | 背包系统 |
| 17 | 雾效渲染器 | UI | MVP | Designed | design/gdd/fog-renderer.md | 雾效状态 |
| 18 | 难度追踪器/DDA | Gameplay | Vertical Slice | Not Started | — | 游戏常量, 跑团状态管理器 |
| 19 | 电梯房间系统 | Gameplay | Vertical Slice | Not Started | — | 物品数据库, 游戏常量, 跑团状态管理器 |
| 20 | 持久化存储 | Persistence | Vertical Slice | Not Started | — | 跑团状态管理器, 电梯房间系统 |
| 21 | 电梯中枢UI | UI | Vertical Slice | Not Started | — | 背包系统, 电梯房间系统 |
| 22 | 死亡回顾UI | UI | Vertical Slice | Not Started | — | 死亡系统 |
| 23 | 叙事文本显示 | Narrative | Vertical Slice | Not Started | — | 物品数据库, 楼层内容数据 |
| 24 | 摄像机系统 | Core | Alpha | Not Started | — | 玩家实体 |
| 25 | 音频系统 | Audio | Alpha | Not Started | — | 计时器系统, 死亡系统 |
| 26 | 场景过渡 | Core | Alpha | Not Started | — | 楼层探索场景, 电梯中枢场景 |

---

## Categories

| 类别 | 说明 | 本游戏中的系统 |
|------|------|--------------|
| **Foundation** | 所有系统共同依赖的纯数据/纯配置层 | 游戏常量 |
| **Core** | 场景架构和玩家基础行为 | 玩家实体, 楼层探索场景, 电梯中枢场景, 摄像机系统, 场景过渡 |
| **Gameplay** | 核心乐趣来源——每个都直接影响"搜刮-撤离"循环 | 背包, 计时器, 楼层生成器, 雾效状态, 物品拾取, 撤离检测, 死亡系统, DDA |
| **Economy** | 资源定义与稀缺性数据 | 物品数据库, 楼层内容数据, 电梯房间系统 |
| **Persistence** | 跨跑团/跨会话的状态管理 | 跑团状态管理器, 持久化存储 |
| **UI** | 玩家信息界面（不包含游戏逻辑） | 计时器HUD, 背包HUD, 雾效渲染器, 电梯中枢UI, 死亡回顾UI |
| **Narrative** | 世界叙事的呈现层 | 叙事文本显示 |
| **Audio** | 声音与音效管理 | 音频系统 |

---

## Priority Tiers

| 层级 | 定义 | 目标里程碑 |
|------|------|-----------|
| **MVP** | 核心循环（搜刮-撤离-死亡）能运行。无此系统无法验证"是否有趣" | Godot 可玩原型 |
| **Vertical Slice** | DDA + 电梯扩建 + 死亡回顾——完整的一次会话体验 | 垂直切片演示 |
| **Alpha** | 摄像机、音频、场景过渡——功能完整，内容粗糙 | Alpha 里程碑 |
| **Full Vision** | 内容完整 + 打磨——20+ 楼层类型，完整叙事弧 | itch.io 发布 |

---

## Dependency Map

### Foundation 层（无依赖）

1. **游戏常量** — 所有可调数值的唯一来源；其他系统从这里读取，不自定义魔法数字
2. **物品数据库** — 物品定义独立于任何游戏逻辑；系统只引用ID，不重复定义
3. **楼层内容数据** — 环境类型、战利品权重表；楼层生成器的原材料
4. **跑团状态管理器** — 定义"跑团数据"与"永久数据"的边界；所有持久化逻辑的架构基础

### Core 层（依赖 Foundation）

1. **玩家实体** → 游戏常量（移动速度、交互半径）
2. **背包系统** → 物品数据库 + 游戏常量 + 跑团状态管理器
3. **难度追踪器/DDA** → 游戏常量 + 跑团状态管理器（读取元进度等级）
4. **计时器系统** → 游戏常量 + 难度追踪器[provisional]（基准时长来源）
5. **楼层生成器** → 楼层内容数据 + 游戏常量（格子尺寸、出口保证算法）
6. **雾效状态** → 游戏常量（视野半径）

### Feature 层（依赖 Core）

1. **物品拾取系统** → 玩家实体 + 背包系统 + 物品数据库
2. **撤离检测** → 玩家实体 + 计时器系统
3. **死亡系统** → 背包系统 + 计时器系统 + 跑团状态管理器
4. **电梯房间系统** → 物品数据库 + 游戏常量 + 跑团状态管理器
5. **持久化存储** → 跑团状态管理器 + 电梯房间系统（Web localStorage 封装）
6. **楼层探索场景** → 玩家实体 + 计时器系统 + 楼层生成器 + 雾效状态 + 物品拾取系统 + 撤离检测 + 死亡系统
7. **电梯中枢场景** → 玩家实体 + 背包系统 + 电梯房间系统 + 持久化存储

### Presentation 层（依赖 Feature/Core）

1. **计时器HUD** → 计时器系统
2. **背包HUD** → 背包系统
3. **雾效渲染器** → 雾效状态
4. **电梯中枢UI** → 背包系统 + 电梯房间系统
5. **死亡回顾UI** → 死亡系统
6. **叙事文本显示** → 物品数据库 + 楼层内容数据

### Polish 层（依赖 Feature）

1. **摄像机系统** → 玩家实体
2. **音频系统** → 计时器系统 + 死亡系统
3. **场景过渡** → 楼层探索场景 + 电梯中枢场景

---

## Recommended Design Order

| 顺序 | 系统 | 优先级 | 层级 | 主要 Agent | 预计工作量 |
|------|------|--------|------|-----------|-----------|
| 1 | 游戏常量 | MVP | Foundation | game-designer | S |
| 2 | 物品数据库 | MVP | Economy | economy-designer | M |
| 3 | 楼层内容数据 | MVP | Economy | writer + game-designer | M |
| 4 | 跑团状态管理器 | MVP | Persistence | game-designer | S |
| 5 | 玩家实体 | MVP | Core | gameplay-programmer | S |
| 6 | 背包系统 | MVP | Gameplay | game-designer | S |
| 7 | 计时器系统 | MVP | Gameplay | game-designer | S |
| 8 | 楼层生成器 | MVP | Gameplay | game-designer + systems-designer | L |
| 9 | 雾效状态 | MVP | Gameplay | game-designer | S |
| 10 | 物品拾取系统 | MVP | Gameplay | game-designer | S |
| 11 | 撤离检测 | MVP | Gameplay | game-designer | S |
| 12 | 死亡系统 | MVP | Gameplay | game-designer | M |
| 13 | 楼层探索场景 | MVP | Core | game-designer | M |
| 14 | 电梯中枢场景 | MVP | Core | game-designer | M |
| 15 | 计时器HUD | MVP | UI | ux-designer | S |
| 16 | 背包HUD | MVP | UI | ux-designer | S |
| 17 | 雾效渲染器 | MVP | UI | game-designer | S |
| 18 | 难度追踪器/DDA | Vertical Slice | Gameplay | systems-designer | L |
| 19 | 电梯房间系统 | Vertical Slice | Gameplay | economy-designer | L |
| 20 | 持久化存储 | Vertical Slice | Persistence | game-designer | M |
| 21 | 电梯中枢UI | Vertical Slice | UI | ux-designer | M |
| 22 | 死亡回顾UI | Vertical Slice | UI | ux-designer | M |
| 23 | 叙事文本显示 | Vertical Slice | Narrative | writer | M |
| 24 | 摄像机系统 | Alpha | Core | gameplay-programmer | S |
| 25 | 音频系统 | Alpha | Audio | audio-director | M |
| 26 | 场景过渡 | Alpha | Core | technical-artist | M |

*工作量：S = 1次会话，M = 2-3次会话，L = 4+次会话（每次会话产出一份完整的GDD节）*

---

## Circular Dependencies

✅ **无循环依赖**——依赖图为有向无环图（DAG）。

**注**：计时器系统 → 难度追踪器/DDA 存在跨里程碑依赖（计时器是 MVP，DDA 是 Vertical Slice）。解决方案：计时器 GDD 中定义 `base_duration: float` 接口，标记为 provisional。DDA 完成设计后补全该接口的实现细节。

---

## High-Risk Systems

| 系统 | 风险类型 | 风险描述 | 缓解措施 |
|------|---------|---------|---------|
| **楼层生成器** | 技术风险 | 程序生成必须保证出口可达性；生成质量直接影响游戏体验 | Pygame 原型已用 L形走廊算法解决，Godot 版需重新验证；先实现，早测试 |
| **难度追踪器/DDA** | 设计风险 | DDA 公式尚无验证；波动范围过窄（可预测）或过宽（不公平）都会破坏游戏感 | 设计后立即原型测试；用 `/prototype dda-system` 验证数值感觉 |
| **跑团状态管理器** | 架构风险 | "什么数据跨跑团保留"是核心架构决策；定义模糊会导致8+个系统的返工 | 最先设计，最先实现；这是整个游戏的数据架构基础 |
| **持久化存储** | 技术风险 | Web localStorage 有配额限制（~5MB）和 origin 隔离；需要在 Godot Web 导出中验证 | 设计时确定最小化存储模式；原型阶段验证 Godot Web localStorage API |
| **雾效渲染器** | 技术风险 | 每帧绘制半透明覆盖层在 Web 上可能造成性能瓶颈 | 已在概念文档中标注为已知风险；参考 Godot Web 2D 性能限制提前规划批次渲染 |

---

## Progress Tracker

| 指标 | 数量 |
|------|------|
| 已识别系统总数 | 26 |
| 已开始设计文档 | 0 |
| 已通过审查 | 0 |
| 已批准 | 0 |
| MVP 系统已设计 | 17 / 17 |
| Vertical Slice 系统已设计 | 0 / 6 |
| Alpha 系统已设计 | 0 / 3 |

---

## Next Steps

- [ ] `/design-system 游戏常量` — 从第一个系统开始，逐节完成 GDD
- [ ] `/design-system 跑团状态管理器` — 架构风险最高，优先完成
- [ ] `/prototype dda-system` — DDA 公式需要原型验证，不要等到 Vertical Slice 再测
- [ ] `/gate-check pre-production` — MVP 系统全部设计完成后执行
