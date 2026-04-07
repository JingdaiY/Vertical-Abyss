class_name TimerHud
extends CanvasLayer

var _time_label: Label = null
var _hp_label: Label = null


func _ready() -> void:
	_time_label = Label.new()
	_time_label.position = Vector2(8, 8)
	add_child(_time_label)

	_hp_label = Label.new()
	_hp_label.position = Vector2(8, 32)
	_hp_label.modulate = Color(1.0, 0.4, 0.4)
	add_child(_hp_label)


func update_time(seconds: float) -> void:
	var secs: int = int(ceil(seconds))
	_time_label.text = "⏱ %d" % secs
	_time_label.modulate = Color.RED if seconds <= Constants.TIMER_URGENCY_THRESHOLD else Color.WHITE


func update_hp(hp: int) -> void:
	_hp_label.text = "HP %d / %d" % [hp, Constants.PLAYER_MAX_HP]
