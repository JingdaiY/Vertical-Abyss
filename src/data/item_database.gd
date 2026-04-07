class_name ItemDatabase

## Static helper for loading ItemData resources by item_id.
## Usage: ItemDatabase.get_item("scrap_metal")

const _BASE_PATH: String = "res://data/items/"


static func get_item(item_id: String) -> ItemData:
	var path: String = _BASE_PATH + item_id + ".tres"
	if not ResourceLoader.exists(path):
		push_warning("ItemDatabase: item_id '%s' not found at %s" % [item_id, path])
		return null
	return load(path) as ItemData


## Returns all item IDs by scanning the items directory.
## Use sparingly — performs disk access.
static func get_all_ids() -> Array[String]:
	var ids: Array[String] = []
	var dir: DirAccess = DirAccess.open(_BASE_PATH)
	if dir == null:
		push_error("ItemDatabase: cannot open %s" % _BASE_PATH)
		return ids
	dir.list_dir_begin()
	var file_name: String = dir.get_next()
	while file_name != "":
		if file_name.ends_with(".tres"):
			ids.append(file_name.get_basename())
		file_name = dir.get_next()
	dir.list_dir_end()
	return ids
