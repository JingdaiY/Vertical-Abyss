class_name FloorMap
extends Node2D

# Color palette
const COLOR_FLOOR  := Color(0.18, 0.18, 0.20)
const COLOR_WALL   := Color(0.10, 0.10, 0.12)
const COLOR_EXIT   := Color(0.20, 0.55, 0.30)
const COLOR_HAZARD := Color(0.55, 0.20, 0.20)

var _tiles: Array = []  # Array[Array[int]] — FloorGenerator.TileType


func set_tiles(tiles: Array) -> void:
	_tiles = tiles
	queue_redraw()


func _draw() -> void:
	if _tiles.is_empty():
		return
	var ts: int = Constants.TILE_SIZE
	for row in range(Constants.FLOOR_ROWS):
		for col in range(Constants.FLOOR_COLS):
			var tile_type: int = _tiles[row][col]
			var color: Color
			match tile_type:
				1:  # WALL
					color = COLOR_WALL
				2:  # EXIT_ZONE
					color = COLOR_EXIT
				3:  # HAZARD
					color = COLOR_HAZARD
				_:  # FLOOR
					color = COLOR_FLOOR
			draw_rect(Rect2(col * ts, row * ts, ts, ts), color)
