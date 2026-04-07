class_name FloorScene
extends Node2D

# Wired up by FloorScene.tscn child nodes
@onready var _floor_map: FloorMap = $FloorMap
@onready var _fog_renderer: FogRenderer = $FogRenderer
@onready var _player: PlayerController = $Player
@onready var _timer_system: TimerSystem = $TimerSystem
@onready var _fog_state: FogOfWarState = $FogOfWarState
@onready var _evacuation: EvacuationDetection = $EvacuationDetection
@onready var _death_system: DeathSystem = $DeathSystem
@onready var _inventory: InventorySystem = $InventorySystem
@onready var _timer_hud: TimerHud = $TimerHud
@onready var _inventory_hud: InventoryHud = $InventoryHud

var _floor_type: FloorTypeData = null
var _item_pickup_system: ItemPickupSystem = ItemPickupSystem.new()
var _rng: RandomNumberGenerator = RandomNumberGenerator.new()


func _ready() -> void:
	_floor_type = load("res://data/floors/abandoned_industrial.tres") as FloorTypeData

	# Generate floor
	var gen := FloorGenerator.new()
	add_child(gen)
	_rng.seed = RunStateManager.run.floor_seed
	gen.generate(RunStateManager.run.floor_seed, _floor_type)

	# Draw map
	_floor_map.set_tiles(gen.tiles)

	# Spawn walls (physics)
	_spawn_walls(gen.tiles)

	# Spawn items
	_item_pickup_system = ItemPickupSystem.new()
	add_child(_item_pickup_system)
	for tile_pos in gen.item_spawns:
		var item_id: String = _item_pickup_system.pick_random_item_id(_rng, _floor_type)
		if item_id.is_empty():
			continue
		var pickup := ItemPickup.new()
		pickup.item_id = item_id
		pickup.position = Vector2(
			tile_pos.x * Constants.TILE_SIZE + Constants.TILE_SIZE * 0.5,
			tile_pos.y * Constants.TILE_SIZE + Constants.TILE_SIZE * 0.5
		)
		# Label is a child of pickup — freed together
		var lbl := Label.new()
		lbl.text = "•"
		lbl.position = Vector2(-6, -8)
		lbl.modulate = Color.YELLOW
		pickup.add_child(lbl)
		add_child(pickup)

	# Hazards
	_player._hazard_damage = gen.hazard_damage

	# Fog
	_fog_state.initialize(Constants.FLOOR_ROWS, Constants.FLOOR_COLS)
	_fog_renderer.setup(_fog_state)

	# Place player at center of corridor entrance
	_player.position = Vector2(
		(Constants.FLOOR_COLS / 2) * Constants.TILE_SIZE + Constants.TILE_SIZE * 0.5,
		1 * Constants.TILE_SIZE + Constants.TILE_SIZE * 0.5
	)
	_player.current_hp = RunStateManager.run.current_hp
	_player.hp_changed.connect(_on_hp_changed)
	_player.died.connect(_on_player_died)
	_player.item_picked_up.connect(_on_item_picked_up)

	# Evacuation
	_evacuation.setup(_player)
	_evacuation.evacuated.connect(_on_evacuated)

	# Death system
	_death_system.death_screen_done.connect(_on_death_screen_done)

	# Timer
	_timer_system.timer_expired.connect(_on_timer_expired)
	_timer_system.start_floor_timer()

	# HUDs
	_inventory_hud.update(RunStateManager.run.inventory)
	_timer_hud.update_time(Constants.TIMER_BASE_DURATION)
	_timer_hud.update_hp(_player.current_hp)


func _process(_delta: float) -> void:
	# Sync timer display
	_timer_hud.update_time(RunStateManager.run.timer_remaining)
	# Sync fog to player tile
	var player_tile := Vector2i(
		int(_player.position.x / Constants.TILE_SIZE),
		int(_player.position.y / Constants.TILE_SIZE)
	)
	_fog_state.update_visibility(player_tile)
	_fog_renderer.refresh()


func _spawn_walls(tiles: Array) -> void:
	var ts: int = Constants.TILE_SIZE
	for row in range(Constants.FLOOR_ROWS):
		for col in range(Constants.FLOOR_COLS):
			if tiles[row][col] == FloorGenerator.TileType.WALL:
				var body := StaticBody2D.new()
				var shape := CollisionShape2D.new()
				var rect := RectangleShape2D.new()
				rect.size = Vector2(ts, ts)
				shape.shape = rect
				shape.position = Vector2(
					col * ts + ts * 0.5,
					row * ts + ts * 0.5
				)
				body.add_child(shape)
				add_child(body)


func _on_hp_changed(new_hp: int) -> void:
	RunStateManager.run.current_hp = new_hp
	_timer_hud.update_hp(new_hp)


func _on_item_picked_up(item_id: String) -> void:
	var data: ItemData = ItemDatabase.get_item(item_id)
	if data == null:
		return
	var added: bool = _inventory.add_item(item_id)
	if added:
		RunStateManager.run.inventory = _inventory.get_all()
		_inventory_hud.update(RunStateManager.run.inventory)


func _on_evacuated() -> void:
	_timer_system.stop()
	_evacuation_success()


func _on_timer_expired() -> void:
	_evacuation.stop()
	_death_system.trigger_death()


func _on_player_died() -> void:
	_timer_system.stop()
	_evacuation.stop()
	_death_system.trigger_death()


func _evacuation_success() -> void:
	# Persist run state
	RunStateManager.run.current_floor += 1
	if RunStateManager.run.current_floor > RunStateManager.persistent.deepest_floor_reached:
		RunStateManager.persistent.deepest_floor_reached = RunStateManager.run.current_floor
	get_tree().change_scene_to_file("res://scenes/elevator/ElevatorHub.tscn")


func _on_death_screen_done() -> void:
	get_tree().change_scene_to_file("res://scenes/elevator/ElevatorHub.tscn")
