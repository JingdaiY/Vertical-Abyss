class_name RunData extends RefCounted

## Transient per-run state. Wiped on death via RunStateManager.clear_run_data().

var inventory: Dictionary[String, int] = {}  # {item_id -> count}
var current_floor: int = 0                   # 0 = elevator hub
var current_hp: int = Constants.PLAYER_MAX_HP
var timer_remaining: float = 0.0
var floor_seed: int = 0
