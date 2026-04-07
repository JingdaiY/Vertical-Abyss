class_name EvacuationDetection
extends Node

signal evacuated()

var _player: PlayerController = null
var _active: bool = false


func setup(player: PlayerController) -> void:
	_player = player
	_active = true


func stop() -> void:
	_active = false


func _process(_delta: float) -> void:
	if not _active or _player == null:
		return
	var tile := Vector2i(
		int(_player.position.x / Constants.TILE_SIZE),
		int(_player.position.y / Constants.TILE_SIZE)
	)
	var exit_start_col: int = Constants.FLOOR_COLS - Constants.EXIT_ZONE_WIDTH
	if tile.x >= exit_start_col and tile.x < Constants.FLOOR_COLS - 1 \
			and tile.y >= 1 and tile.y < Constants.FLOOR_ROWS - 1:
		_active = false
		evacuated.emit()
