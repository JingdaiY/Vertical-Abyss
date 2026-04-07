# 垂直深渊 | Vertical Abyss

> 电梯门打开。60秒。带着你找到的东西回来——或者永远留在那里。
>
> *The door opens. 60 seconds. Bring back what you find — or don't come back at all.*

A roguelite survival game. Descend floor by floor into a collapsing structure, scavenge resources under a merciless timer, and build your elevator sanctuary with what you bring back.

**Engine**: Godot 4.6.2 (Web/HTML5) · **Stage**: Production — Sprint 1

---

## Gameplay

- Start in the **elevator hub** — your only safe space
- Descend to a randomly generated floor
- **60 seconds** to scavenge items and reach the exit
- Make it back → keep your loot, build up the elevator
- Die (timer or hazard tiles) → lose everything in your backpack

### Controls

| Key | Action |
|-----|--------|
| `WASD` / Arrow Keys | Move |
| `E` | Pick up item |

---

## Project Structure

```
Vertical-Abyss/
├── project.godot                  # Godot 4.6.2 project file
├── src/
│   ├── core/
│   │   ├── constants.gd           # Single source of truth for all tuning values
│   │   ├── run_data.gd            # Transient per-run state (wiped on death)
│   │   ├── persistent_data.gd     # Permanent cross-run state (elevator progress)
│   │   └── run_state_manager.gd   # Autoload — owns all game state
│   ├── data/
│   │   ├── item_data.gd           # ItemData Resource class
│   │   ├── item_database.gd       # Static helper: load items by ID
│   │   ├── floor_type_data.gd     # FloorTypeData Resource class
│   │   └── hazard_tile_data.gd    # HazardTileData Resource class
│   └── systems/
│       ├── inventory_system.gd    # Backpack add/remove/query
│       ├── timer_system.gd        # Floor countdown timer
│       └── fog_of_war_state.gd    # Tile visibility grid
├── data/
│   ├── items/                     # ItemData .tres files (5 MVP items)
│   │   ├── scrap_metal.tres
│   │   ├── canned_food.tres
│   │   ├── old_battery.tres
│   │   ├── first_aid_kit.tres
│   │   └── fuel_barrel.tres
│   └── floors/                    # FloorTypeData .tres files
│       └── abandoned_industrial.tres
├── scenes/                        # Godot scenes (Sprint 2+)
├── tests/                         # GUT unit tests
├── prototypes/
│   └── vertical-abyss-mvp/        # Python/Pygame concept prototype (throwaway)
├── design/gdd/                    # Game Design Documents (17 systems)
└── production/                    # Sprint plans, milestones, stage tracking
```

---

## Running the Godot Project

1. Download [Godot 4.6.2](https://godotengine.org/download/)
2. Open Godot → **Import** → select `project.godot` in this directory
3. Godot will import assets and assign resource UIDs automatically

> Scenes are not yet created (Sprint 2). The data layer and logic systems are complete and unit-testable.

---

## Running the Pygame Prototype

The prototype in `prototypes/vertical-abyss-mvp/` validates the core loop concept. It is **not** the production game.

```bash
# Create environment
conda create -n vertical-abyss python=3.11 -y
conda run -n vertical-abyss pip install pygame

# Run
conda run -n vertical-abyss python prototypes/vertical-abyss-mvp/main.py
```

---

## Tech Stack

| | |
|---|---|
| Production Engine | Godot 4.6.2 |
| Production Language | GDScript (static typing) |
| Target Platform | Web (HTML5), PC |
| Prototype Engine | Python 3.11 + Pygame 2.6 |
| Unit Testing | GUT (Godot Unit Testing) |

---

## Development Status

**Stage: Production · Sprint 1 complete**

### Sprint 1 — Foundation & Logic Layer ✅
- [x] `constants.gd` — all tuning values in one place
- [x] `RunStateManager` autoload — run data / persistent data split
- [x] `ItemData` resource + 5 MVP items (废铁, 罐头, 旧电池, 急救包, 燃料桶)
- [x] `FloorTypeData` + 废弃工业区 configuration
- [x] `InventorySystem` — add / remove / capacity checks
- [x] `TimerSystem` — countdown with urgency signal
- [x] `FogOfWarState` — Chebyshev visibility grid

### Sprint 2 — Visual Layer (next)
- [ ] `PlayerController` — movement, HP, hazard tile damage
- [ ] `FloorGenerator` — procedural 10×10 map with guaranteed exit
- [ ] `FloorScene` — playable floor (no HUD yet)
- [ ] `ElevatorHubScene` — descent trigger

### Sprint 3 — Full MVP Loop
- [ ] All 3 HUDs (timer, inventory, fog renderer)
- [ ] Death system + death screen
- [ ] End-to-end playable loop

---

## Game Design

All 17 MVP systems are fully designed. See `design/gdd/systems-index.md` for the complete system map.

**Four Design Pillars:**
1. **压迫即乐趣** — Pressure IS the game. Never reduce tension.
2. **电梯是家** — The elevator hub is the emotional core. Make it feel earned.
3. **资源讲故事** — Items tell the world's story. No separate lore menus.
4. **死亡有意义** — Every death is legible. Players must understand why they died.
