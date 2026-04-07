class_name ElevatorHub
extends Node2D

var _status_label: Label = null
var _descend_button: Button = null


func _ready() -> void:
	var bg := ColorRect.new()
	bg.color = Color(0.08, 0.08, 0.10)
	bg.size = Vector2(
		Constants.FLOOR_COLS * Constants.TILE_SIZE,
		Constants.FLOOR_ROWS * Constants.TILE_SIZE
	)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bg)

	_status_label = Label.new()
	_status_label.position = Vector2(20, 30)
	_status_label.size = Vector2(300, 140)
	add_child(_status_label)

	_descend_button = Button.new()
	_descend_button.text = "进入下一层"
	_descend_button.position = Vector2(20, 180)
	_descend_button.size = Vector2(160, 40)
	_descend_button.pressed.connect(_on_descend_pressed)
	add_child(_descend_button)

	_refresh_ui()


func _refresh_ui() -> void:
	var run := RunStateManager.run
	var persistent := RunStateManager.persistent
	_status_label.text = (
		"当前楼层: %d\n生命值: %d / %d\n死亡次数: %d\n最深记录: %d层"
		% [
			run.current_floor,
			run.current_hp,
			Constants.PLAYER_MAX_HP,
			persistent.total_deaths,
			persistent.deepest_floor_reached
		]
	)


func _on_descend_pressed() -> void:
	print("descend pressed")
	RunStateManager.run.floor_seed = randi()
	RunStateManager.run.timer_remaining = Constants.TIMER_BASE_DURATION
	get_tree().change_scene_to_file("res://scenes/floor/FloorScene.tscn")
