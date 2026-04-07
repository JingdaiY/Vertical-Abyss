class_name TimerSystem extends Node

signal timer_expired()
signal timer_urgent()  ## Emitted once when remaining time first drops to urgency threshold.

var _running: bool = false
var _urgent_fired: bool = false


## Call at the start of each floor. Resets the countdown.
func start_floor_timer() -> void:
	RunStateManager.run.timer_remaining = Constants.TIMER_BASE_DURATION
	# [provisional] DDA system will provide the actual duration in Vertical Slice.
	_urgent_fired = false
	_running = true


## Call on successful evacuation to stop the timer without firing signals.
func stop() -> void:
	_running = false


func _process(delta: float) -> void:
	if not _running:
		return
	var t: float = RunStateManager.run.timer_remaining
	if t <= 0.0:
		return
	RunStateManager.run.timer_remaining = maxf(0.0, t - delta)
	if not _urgent_fired and RunStateManager.run.timer_remaining <= Constants.TIMER_URGENCY_THRESHOLD:
		_urgent_fired = true
		timer_urgent.emit()
	if RunStateManager.run.timer_remaining <= 0.0:
		_running = false
		timer_expired.emit()
