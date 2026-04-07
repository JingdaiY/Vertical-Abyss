# Godot Deprecated APIs — Do Not Use

*Last verified: 2026-04-07*
*Covers deprecations introduced in Godot 4.4 through 4.6*

---

## Quick Reference Table

| ❌ Deprecated | ✅ Use Instead | Since | Notes |
|--------------|---------------|-------|-------|
| `SkeletonIK3D` | `LookAtModifier3D` | 4.4 | 3D only — not relevant for 2D |
| `Resource.duplicate(true)` | `resource.duplicate_deep()` | 4.5 | For reliable deep copies |
| `Array.duplicate(true)` | `array.duplicate_deep()` | 4.5 | For reliable deep copies |
| `Dictionary.duplicate(true)` | `dict.duplicate_deep()` | 4.5 | For reliable deep copies |
| `TextEdit.background_color` | Theme overrides | 4.6 | Use `add_theme_color_override()` |
| `ScriptLanguage.has_named_classes` | `ScriptLanguageExtension` version | 4.6 | Internal/extension use only |

---

## Deprecations Relevant to This Project (2D Roguelite)

### Resource Duplication
When duplicating floor layouts, item definitions, or any nested resource:

```gdscript
# ❌ Old — unreliable for nested resources
var copy = my_resource.duplicate(true)

# ✅ New — reliable deep copy (Godot 4.5+)
var copy = my_resource.duplicate_deep()
```

### TextEdit Styling (for inventory/UI text fields)
```gdscript
# ❌ Deprecated in 4.6
text_edit.background_color = Color(0.1, 0.1, 0.1)

# ✅ Use theme overrides
text_edit.add_theme_color_override("background_color", Color(0.1, 0.1, 0.1))
```

---

## APIs Removed or Significantly Changed (Pre-4.4, for Reference)

These were removed before 4.4 but may appear in older tutorials:

| ❌ Old (Godot 3.x / early 4.x) | ✅ Current |
|-------------------------------|-----------|
| `OS.get_ticks_msec()` loop | Use `delta` in `_process()` |
| `yield()` | `await` |
| `connect("signal", self, "method")` | `signal.connect(callable)` |
| `emit_signal("name")` | `signal_name.emit()` |
| `setget` | `@export` + property with getter/setter |
| `.gd` class registration via `class_name` without file match | File name must match `class_name` |
