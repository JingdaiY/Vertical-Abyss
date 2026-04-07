class_name InventoryHud
extends CanvasLayer

var _label: Label = null


func _ready() -> void:
	_label = Label.new()
	_label.position = Vector2(8, 32)
	add_child(_label)


func update(inventory: Dictionary) -> void:
	if inventory.is_empty():
		_label.text = "背包: 空"
		return
	var lines: Array[String] = []
	for id in inventory:
		var data: ItemData = ItemDatabase.get_item(id)
		var name: String = data.display_name if data != null else id
		lines.append("%s x%d" % [name, inventory[id]])
	_label.text = "背包:\n" + "\n".join(lines)
