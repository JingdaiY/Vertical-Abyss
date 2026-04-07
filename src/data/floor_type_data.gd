class_name FloorTypeData extends Resource

@export var type_id: String = ""
@export var display_name: String = ""
@export var hazard_tiles: Array[HazardTileData] = []
## Override per-item spawn weights for this floor type.
## Empty = use ItemData.spawn_weight global defaults.
@export var item_weight_overrides: Dictionary = {}  # {item_id: String -> weight: float}
