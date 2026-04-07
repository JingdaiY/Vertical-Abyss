# Godot Breaking Changes — 4.4 through 4.6

*Last verified: 2026-04-07*
*Sources: godotengine.org/releases/4.4, 4.5, 4.6 + official migration guides*

---

## Godot 4.4 (from 4.3)

### .NET / C#
- **Minimum .NET version raised to .NET 8** (was .NET 6)
  - Existing projects auto-upgrade on first open in 4.4
  - Not relevant for this project (GDScript only)

### 3D / Animation
- **`SkeletonIK3D` deprecated** → use `LookAtModifier3D` for procedural 3D
  - Not relevant for this project (2D top-down)

### CSG
- **CSG implementation replaced** with Manifold library
  - API surface unchanged for users; internal only
  - Not relevant for this project

### Rendering (macOS/iOS)
- **Metal backend replaces MoltenVK** on Apple Silicon
  - Transparent to GDScript code

### GDScript Additions (non-breaking)
- **Typed Dictionaries**: `var d: Dictionary[String, int] = {}`
- **`@export_tool_button`** annotation for inspector buttons in `@tool` scripts

---

## Godot 4.5 (from 4.4)

### Resource API
- **`Resource.duplicate(deep=true)` behavior changed** for nested structures
  - Old pattern: `resource.duplicate(true)` — unreliable for deep nesting
  - New pattern: use `resource.duplicate_deep()` for reliable deep copies
  - Also applies to Arrays: `array.duplicate_deep()` and Dicts: `dict.duplicate_deep()`

### Physics
- **3D physics interpolation moved** from RenderingServer to SceneTree
  - 2D physics interpolation unaffected — relevant to this project
  - No API change; behavior is more reliable

### GDScript Additions (non-breaking)
- **Variadic arguments**:
  ```gdscript
  func sum(first: float, ...numbers: Array) -> float:
  ```
- **Abstract classes and methods**:
  ```gdscript
  @abstract
  class_name Animal extends Node

  @abstract
  func cry() -> void:
  ```

### GUI
- `Control.focus_behavior_recursive` and `Control.mouse_behavior_recursive` added
  - New properties, no replacement needed for existing code

---

## Godot 4.6 (from 4.5)

### Scenes / Node IDs
- **New Unique Node ID system** — scenes saved in 4.5 or earlier should be
  re-saved in 4.6 to benefit from improved node tracking
  - Run: **Project → Tools → Upgrade Project Files** for existing projects
  - New projects unaffected

### Physics
- **Jolt Physics is now the default for new 3D projects**
  - Existing projects retain their physics engine setting
  - 2D projects (like this one) are unaffected

### Rendering / Shaders
- **GLSL shaders using `view_matrix` or `inv_view_matrix`** from built-in
  `SceneData` uniform now require transposed matrix operations
  - These changed from `mat4` to `mat3x4`
  - Only affects custom GLSL shaders — GDScript and VisualShader unaffected

- **Glow blending now occurs before tonemapping**
  - `Screen` is the new default glow blend mode (was additive)
  - May affect existing glow-heavy visual effects

### GUI
- **`TextEdit.background_color` deprecated** — use theme overrides instead
- **`pivot_offset_ratio`** added to Control nodes (new, not a replacement)

### GDExtension
- **GDExtension interface now defined in JSON** (previously C header)
  - C header still generated from JSON for backward compatibility
  - Only affects GDExtension authors, not GDScript users

### Editor
- **"Modern" editor theme is now the default** — revert in Editor Settings if needed
