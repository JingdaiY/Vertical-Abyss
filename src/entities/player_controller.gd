class_name PlayerController
extends CharacterBody2D

signal hp_changed(new_hp: int)
signal died()
signal item_picked_up(item_id: String)

var current_hp: int = Constants.PLAYER_MAX_HP
var _last_tile: Vector2i = Vector2i(-1, -1)
var _hazard_damage: Dictionary = {}  # Vector2i -> int, set by FloorScene


func _ready() -> void:
	var shape := CircleShape2D.new()
	shape.radius = Constants.PLAYER_COLLISION_RADIUS
	var col := CollisionShape2D.new()
	col.shape = shape
	add_child(col)

	# Visual: simple colored circle
	var vis := Node2D.new()
	vis.set_script(preload("res://src/entities/player_visual.gd"))
	add_child(vis)


func _physics_process(delta: float) -> void:
	var dir := Vector2(
		Input.get_axis("ui_left", "ui_right"),
		Input.get_axis("ui_up", "ui_down")
	).normalized()
	velocity = dir * Constants.PLAYER_SPEED
	move_and_slide()
	_check_hazard_tile()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_E:
			_try_pick_up()


func _check_hazard_tile() -> void:
	var tile := Vector2i(
		int(position.x / Constants.TILE_SIZE),
		int(position.y / Constants.TILE_SIZE)
	)
	if tile == _last_tile:
		return
	_last_tile = tile
	if _hazard_damage.has(tile):
		take_damage(_hazard_damage[tile])


func take_damage(amount: int) -> void:
	current_hp = max(0, current_hp - amount)
	hp_changed.emit(current_hp)
	if current_hp <= 0:
		died.emit()


func _try_pick_up() -> void:
	var items := get_tree().get_nodes_in_group("items")
	for node in items:
		if node is ItemPickup:
			var dist: float = position.distance_to(node.position)
			if dist <= Constants.PLAYER_INTERACTION_RADIUS:
				item_picked_up.emit(node.item_id)
				node.queue_free()
				return
