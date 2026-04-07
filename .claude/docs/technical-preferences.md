# Technical Preferences

<!-- Populated by /setup-engine. Updated as the user makes decisions throughout development. -->
<!-- All agents reference this file for project-specific standards and conventions. -->

## Engine & Language

- **Engine**: Godot 4.6.2
- **Language**: GDScript (primary) — C++ via GDExtension only for performance-critical paths
- **Rendering**: Godot Rendering Server (2D, Compatibility renderer for Web)
- **Physics**: Godot 2D Physics (default) — Jolt is 3D only, not relevant

## Naming Conventions

- **Classes**: PascalCase — `PlayerController`, `FloorGenerator`, `ElevatorHub`
- **Variables/Functions**: snake_case — `move_speed`, `pickup_item()`, `floor_number`
- **Signals**: snake_case past tense — `item_collected`, `timer_expired`, `floor_exited`
- **Files**: snake_case matching class — `player_controller.gd`, `floor_generator.gd`
- **Scenes**: PascalCase matching root node — `PlayerController.tscn`, `FloorScene.tscn`
- **Constants**: UPPER_SNAKE_CASE — `MAX_INVENTORY_SIZE`, `BASE_TIMER_SECONDS`

## Performance Budgets

- **Target Framerate**: 60 FPS
- **Frame Budget**: 16.6ms
- **Draw Calls**: ≤ 300 (Web/mobile constraint — use CanvasItem batching)
- **Memory Ceiling**: 256 MB (Web export constraint)

## Testing

- **Framework**: GUT (Godot Unit Testing) — https://github.com/bitwes/Gut
- **Minimum Coverage**: Balance formulas, floor generation determinism, timer logic
- **Required Tests**: DDA difficulty formula, floor exit reachability, inventory death penalty

## Forbidden Patterns

- **Untyped GDScript variables** — always declare types (`var x: int`, not `var x`)
- **String-based signal connections** — use `signal.connect(callable)`, never `connect("name", self, "method")`
- **Global state via Autoload for gameplay logic** — pass dependencies explicitly; Autoloads only for truly global services (settings, audio bus)
- **`Resource.duplicate(true)`** — use `duplicate_deep()` instead (Godot 4.5+ fix)
- **Direct scene imports from `prototypes/`** — prototype code must never be referenced from `src/`
- **Magic numbers in gameplay code** — all tuning values belong in `src/core/constants.gd`

## Allowed Libraries / Addons

- **GUT** (Godot Unit Testing) — for unit and integration tests
- *No other addons approved yet — add via /architecture-decision*

## Architecture Decisions Log

<!-- Quick reference linking to full ADRs in docs/architecture/ -->
- [No ADRs yet — use /architecture-decision to create one]
