class_name ItemPickup
extends Node2D

var item_id: String = ""


func _ready() -> void:
	add_to_group("items")
