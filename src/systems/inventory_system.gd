class_name InventorySystem extends Node

## Manages add/remove/query operations on RunStateManager.run.inventory.
## Does not hold its own state — all data lives in RunStateManager.


func is_full() -> bool:
	return get_total_count() >= Constants.INVENTORY_MAX_CAPACITY


func get_total_count() -> int:
	var total: int = 0
	for count: int in RunStateManager.run.inventory.values():
		total += count
	return total


## Returns true if the item was added. Returns false if backpack is full
## or the item's stack_limit is already reached.
func add_item(item_id: String, count: int = 1) -> bool:
	assert(count > 0, "InventorySystem.add_item: count must be > 0")
	if is_full():
		return false
	var item_data: ItemData = _load_item(item_id)
	if item_data == null:
		return false
	var current: int = RunStateManager.run.inventory.get(item_id, 0)
	var addable: int = mini(count, item_data.stack_limit - current)
	if addable <= 0:
		return false
	RunStateManager.run.inventory[item_id] = current + addable
	return true


func remove_item(item_id: String, count: int = 1) -> void:
	assert(count > 0, "InventorySystem.remove_item: count must be > 0")
	var current: int = RunStateManager.run.inventory.get(item_id, 0)
	var new_count: int = current - count
	if new_count <= 0:
		RunStateManager.run.inventory.erase(item_id)
	else:
		RunStateManager.run.inventory[item_id] = new_count


func get_count(item_id: String) -> int:
	return RunStateManager.run.inventory.get(item_id, 0)


func _load_item(item_id: String) -> ItemData:
	var path: String = "res://data/items/%s.tres" % item_id
	if not ResourceLoader.exists(path):
		push_warning("InventorySystem: unknown item_id '%s'" % item_id)
		return null
	return load(path) as ItemData
