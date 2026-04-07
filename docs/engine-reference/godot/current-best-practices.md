# Godot 4.6 Current Best Practices

*Last verified: 2026-04-07*
*New patterns introduced since Godot 4.3 (LLM training cutoff ~4.3)*

---

## GDScript: Always Use Static Typing

Godot 4.x GDScript has full static typing. Use it everywhere — it enables
faster runtime performance, better autocomplete, and earlier error detection.

```gdscript
# ❌ Untyped — avoid
var speed = 150
var items = []
func move(delta):
    position.x += speed * delta

# ✅ Fully typed
var speed: float = 150.0
var items: Array[ItemData] = []
func move(delta: float) -> void:
    position.x += speed * delta
```

---

## GDScript: Typed Dictionaries (New in 4.4)

```gdscript
# ✅ Use typed dictionaries where key/value types are known
var inventory: Dictionary[String, int] = {}
inventory["scrap_metal"] = 3

# For heterogeneous data, prefer typed Resources or custom classes
```

---

## GDScript: Abstract Classes (New in 4.5)

Use for shared interfaces between systems (e.g., all FloorGenerators):

```gdscript
# base_floor_generator.gd
@abstract
class_name BaseFloorGenerator extends Node

@abstract
func generate(width: int, height: int) -> Array[Array]:
    pass
```

---

## GDScript: Signals Best Practices

```gdscript
# ✅ Declare signals with typed parameters
signal item_collected(item: ItemData)
signal timer_expired()
signal floor_exited(items_carried: Array[ItemData])

# ✅ Connect using Callable (not string-based)
timer.timeout.connect(_on_timer_timeout)

# ✅ Emit with dot notation
item_collected.emit(item)

# ❌ Never use string-based connect (Godot 3 style)
# connect("item_collected", self, "_on_item_collected")
```

---

## Resource Deep Copy (Changed in 4.5)

```gdscript
# ✅ Use duplicate_deep() for nested resources
var floor_layout_copy: FloorLayout = floor_layout.duplicate_deep()

# ❌ Avoid duplicate(true) — unreliable for nested structures
```

---

## Scene Architecture for This Project

Each major system should be a scene:

```
scenes/
  elevator/
    ElevatorHub.tscn        # Root: ElevatorHub (Node2D)
    elevator_hub.gd         # Script on root node
  floor/
    FloorScene.tscn         # Root: FloorScene (Node2D)
    floor_scene.gd
  ui/
    HUD.tscn
    hud.gd
```

---

## Web Export Constraints (HTML5)

Godot 4.6 Web export limitations to keep in mind:

- **No threads by default** — avoid `Thread` class; use `call_deferred()` for
  heavy operations or coroutines with `await`
- **GDExtension limited** — most GDExtensions don't support Web export
- **File system is virtual** — `user://` maps to IndexedDB, not a real filesystem
- **Shader compilation** — Web has no shader cache; first run may stutter;
  keep shader count low
- **Draw calls** — Mobile-level budget (~300 draw calls); use CanvasItem batching

---

## Performance: 2D Specific

```gdscript
# ✅ Use Node2D.top_level = true for UI nodes that shouldn't inherit transform
# ✅ Use CanvasLayer for HUD elements (avoids camera transform)
# ✅ Use TileMapLayer (Godot 4.4+) instead of TileMap for floor rendering
# ✅ Prefer AnimatedSprite2D over AnimationPlayer for simple sprite animations
# ✅ Visibility notifiers (VisibleOnScreenNotifier2D) to pause off-screen nodes
```

---

## TileMap → TileMapLayer (Godot 4.4+)

Godot 4.4 introduced `TileMapLayer` as a replacement for multi-layer `TileMap`:

```gdscript
# ✅ New: use TileMapLayer node directly
# Each layer is its own node — more flexible, better performance

# ✅ Query tiles
var tile_data: TileData = tile_map_layer.get_cell_tile_data(Vector2i(x, y))

# ❌ Old TileMap multi-layer API (still works but prefer TileMapLayer for new code)
# tile_map.get_cell_tile_data(layer_index, Vector2i(x, y))
```
