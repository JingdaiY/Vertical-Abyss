class_name RunStateManager extends Node

## Autoload singleton. Single source of truth for all game state.
## Run data is wiped on death; persistent data survives forever.

var run: RunData = RunData.new()
var persistent: PersistentData = PersistentData.new()


func _ready() -> void:
	# Crash recovery: if a floor was active on startup, the previous session
	# was interrupted. Clear run data and return to elevator.
	if run.current_floor > 0:
		push_warning("RunStateManager: interrupted session detected — clearing run data")
		clear_run_data()


## Wipe all transient run data. Idempotent — safe to call multiple times.
func clear_run_data() -> void:
	run = RunData.new()
