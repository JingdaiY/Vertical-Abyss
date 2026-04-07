class_name DeathSystem
extends Node

signal death_screen_done()

var _timer: float = 0.0
var _counting: bool = false


func trigger_death() -> void:
	RunStateManager.persistent.total_deaths += 1
	RunStateManager.clear_run_data()
	_timer = Constants.DEATH_SCREEN_DURATION
	_counting = true


func _process(delta: float) -> void:
	if not _counting:
		return
	_timer -= delta
	if _timer <= 0.0:
		_counting = false
		death_screen_done.emit()
