class_name FloorGenerator
extends Node

enum TileType { FLOOR = 0, WALL = 1, EXIT_ZONE = 2, HAZARD = 3 }

var tiles: Array = []                      # Array[Array[int]]
var item_spawns: Array[Vector2i] = []
var hazard_positions: Array[Vector2i] = []
var hazard_damage: Dictionary = {}         # Vector2i -> int


func generate(seed_value: int, floor_type: FloorTypeData) -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = seed_value

	_init_walls()
	_carve_rooms(rng)
	_carve_corridor()
	_place_exit()
	_place_hazards(rng, floor_type)
	_place_items(rng, floor_type)


func _init_walls() -> void:
	tiles = []
	for row in range(Constants.FLOOR_ROWS):
		var row_arr: Array[int] = []
		for col in range(Constants.FLOOR_COLS):
			row_arr.append(TileType.WALL)
		tiles.append(row_arr)


func _carve_rooms(rng: RandomNumberGenerator) -> void:
	# Carve the interior — each non-border cell has a chance to be floor
	for row in range(1, Constants.FLOOR_ROWS - 1):
		for col in range(1, Constants.FLOOR_COLS - 1):
			if rng.randf() > Constants.FLOOR_WALL_DENSITY:
				tiles[row][col] = TileType.FLOOR


func _carve_corridor() -> void:
	# L-corridor through column 5 to guarantee the exit is reachable
	var mid_col: int = Constants.FLOOR_COLS / 2
	for row in range(1, Constants.FLOOR_ROWS - 1):
		tiles[row][mid_col] = TileType.FLOOR
	# Horizontal segment: row 1, cols 1..mid_col
	for col in range(1, mid_col + 1):
		tiles[1][col] = TileType.FLOOR


func _place_exit() -> void:
	# Exit zone: right-most 2 columns, rows 1..FLOOR_ROWS-2
	for row in range(1, Constants.FLOOR_ROWS - 1):
		for col in range(Constants.FLOOR_COLS - Constants.EXIT_ZONE_WIDTH, Constants.FLOOR_COLS - 1):
			tiles[row][col] = TileType.EXIT_ZONE


func _place_hazards(rng: RandomNumberGenerator, floor_type: FloorTypeData) -> void:
	hazard_positions = []
	hazard_damage = {}
	if floor_type == null or floor_type.hazard_tiles.is_empty():
		return
	for row in range(1, Constants.FLOOR_ROWS - 1):
		for col in range(1, Constants.FLOOR_COLS - Constants.EXIT_ZONE_WIDTH - 1):
			if tiles[row][col] != TileType.FLOOR:
				continue
			for hazard in floor_type.hazard_tiles:
				if rng.randf() < hazard.spawn_density:
					tiles[row][col] = TileType.HAZARD
					var pos := Vector2i(col, row)
					hazard_positions.append(pos)
					hazard_damage[pos] = hazard.damage_per_step
					break  # one hazard type per tile


func _place_items(rng: RandomNumberGenerator, floor_type: FloorTypeData) -> void:
	item_spawns = []
	# Build candidate floor tiles
	var candidates: Array[Vector2i] = []
	for row in range(1, Constants.FLOOR_ROWS - 1):
		for col in range(1, Constants.FLOOR_COLS - Constants.EXIT_ZONE_WIDTH - 1):
			if tiles[row][col] == TileType.FLOOR:
				candidates.append(Vector2i(col, row))

	if candidates.is_empty():
		return

	var count: int = rng.randi_range(
		Constants.FLOOR_ITEM_COUNT_MIN,
		Constants.FLOOR_ITEM_COUNT_MAX
	)
	count = min(count, candidates.size())

	# Fisher-Yates partial shuffle to pick `count` unique positions
	for i in range(count):
		var j: int = rng.randi_range(i, candidates.size() - 1)
		var tmp: Vector2i = candidates[i]
		candidates[i] = candidates[j]
		candidates[j] = tmp
		item_spawns.append(candidates[i])
