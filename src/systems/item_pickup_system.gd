class_name ItemPickupSystem
extends Node

# Chooses a random item_id from the database using spawn weights,
# respecting floor_type overrides.
func pick_random_item_id(rng: RandomNumberGenerator, floor_type: FloorTypeData) -> String:
	var ids: Array[String] = ItemDatabase.get_all_ids()
	if ids.is_empty():
		return ""

	# Build weight list
	var weights: Array[float] = []
	var total: float = 0.0
	for id in ids:
		var data: ItemData = ItemDatabase.get_item(id)
		var w: float = data.spawn_weight if data != null else 1.0
		if floor_type != null and floor_type.item_weight_overrides.has(id):
			w = float(floor_type.item_weight_overrides[id])
		weights.append(w)
		total += w

	if total <= 0.0:
		return ids[rng.randi() % ids.size()]

	var roll: float = rng.randf() * total
	var cumulative: float = 0.0
	for i in range(ids.size()):
		cumulative += weights[i]
		if roll <= cumulative:
			return ids[i]

	return ids[-1]
