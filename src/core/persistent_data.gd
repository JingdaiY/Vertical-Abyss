class_name PersistentData extends RefCounted

## Permanent cross-run state. Survives death. Saved to localStorage by PersistenceStorage.

var unlocked_rooms: Array[String] = []  # elevator room IDs built so far
var total_deaths: int = 0
var deepest_floor_reached: int = 0
