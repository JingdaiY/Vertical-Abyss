extends Node2D

func _draw() -> void:
	draw_circle(Vector2.ZERO, Constants.PLAYER_COLLISION_RADIUS, Color(0.2, 0.6, 1.0))
