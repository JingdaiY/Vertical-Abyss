class_name FogRenderer
extends Node2D

var _fog_state: FogOfWarState = null


func setup(fog_state: FogOfWarState) -> void:
	_fog_state = fog_state


func refresh() -> void:
	queue_redraw()


func _draw() -> void:
	if _fog_state == null:
		return
	var ts: int = Constants.TILE_SIZE
	for row in range(Constants.FLOOR_ROWS):
		for col in range(Constants.FLOOR_COLS):
			var vis: FogOfWarState.TileVisibility = _fog_state.get_visibility(Vector2i(col, row))
			match vis:
				FogOfWarState.TileVisibility.UNKNOWN:
					draw_rect(Rect2(col * ts, row * ts, ts, ts), Color(0, 0, 0, 1.0))
				FogOfWarState.TileVisibility.EXPLORED:
					draw_rect(Rect2(col * ts, row * ts, ts, ts), Color(0, 0, 0, Constants.FOG_EXPLORED_ALPHA))
				FogOfWarState.TileVisibility.VISIBLE:
					pass  # fully visible — draw nothing
