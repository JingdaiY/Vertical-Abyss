class_name FogOfWarState extends Node

enum TileVisibility { UNKNOWN, EXPLORED, VISIBLE }

## 2D grid: grid[row][col] -> TileVisibility
var grid: Array = []


func initialize(rows: int, cols: int) -> void:
	grid = []
	for _r: int in rows:
		var row: Array = []
		for _c: int in cols:
			row.append(TileVisibility.UNKNOWN)
		grid.append(row)


## Call every time the player moves to a new tile.
func update_visibility(player_tile: Vector2i) -> void:
	# Demote all currently visible tiles to explored
	for r: int in grid.size():
		for c: int in grid[r].size():
			if grid[r][c] == TileVisibility.VISIBLE:
				grid[r][c] = TileVisibility.EXPLORED
	# Mark tiles within Chebyshev radius as visible
	var radius: int = Constants.FOG_VISION_RADIUS
	for dr: int in range(-radius, radius + 1):
		for dc: int in range(-radius, radius + 1):
			var r: int = player_tile.y + dr
			var c: int = player_tile.x + dc
			if r >= 0 and r < grid.size() and c >= 0 and c < grid[r].size():
				grid[r][c] = TileVisibility.VISIBLE


func get_visibility(tile: Vector2i) -> TileVisibility:
	if tile.y < 0 or tile.y >= grid.size():
		return TileVisibility.UNKNOWN
	if tile.x < 0 or tile.x >= grid[tile.y].size():
		return TileVisibility.UNKNOWN
	return grid[tile.y][tile.x]
