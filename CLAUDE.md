# 垂直深渊 | Vertical Abyss — Project Configuration

## Project Overview

A roguelite survival game where you descend floor by floor into a collapsing
vertical structure, scavenge resources under a merciless timer, and build your
elevator sanctuary with what you bring back. Web-first (HTML5), solo developer.

- **Concept**: `design/gdd/game-concept.md`
- **Systems Index**: `design/gdd/systems-index.md` *(run /map-systems to generate)*
- **Technical Preferences**: `.claude/docs/technical-preferences.md`

---

## Technology Stack

- **Engine**: Godot 4.6.2
- **Language**: GDScript (primary) — C++ via GDExtension only if performance-critical
- **Build System**: Godot Export Templates (HTML5 target)
- **Asset Pipeline**: Godot Import System
- **Prototype Engine**: Python / Pygame (prototype only — do not reference from src/)

---

## Engine Version Reference

@docs/engine-reference/godot/VERSION.md

---

## Architecture

- **Source**: `src/` — production GDScript only; no prototype code
- **Prototypes**: `prototypes/` — isolated; never imported by src/
- **Design Docs**: `design/gdd/` — GDD per system, systems-index.md as root
- **Engine Ref**: `docs/engine-reference/godot/` — breaking changes, deprecated APIs

---

## Coding Standards

Full standards: `.claude/docs/coding-standards.md`

Key rules for this project:
- **Always use static typing** in GDScript — `var x: int`, not `var x`
- **Signals use snake_case past tense** — `health_changed`, not `on_health_change`
- **No autoloads for gameplay logic** — pass dependencies explicitly
- **Scene-first architecture** — each system is a scene with a root node script
- **No magic numbers** — all tuning values go in `src/core/constants.gd`

---

## Agent Guidelines

- All agents must read `docs/engine-reference/godot/VERSION.md` before suggesting APIs
- Check `docs/engine-reference/godot/deprecated-apis.md` before suggesting any method
- Check `docs/engine-reference/godot/breaking-changes.md` before suggesting patterns from Godot 4.3 or earlier
- Game concept and pillars are in `design/gdd/game-concept.md` — read before making design suggestions
- Technical preferences are in `.claude/docs/technical-preferences.md`

---

## Platform Target

- **Primary**: Web (HTML5) via Godot HTML5 export
- **Secondary**: PC (Windows/macOS) desktop builds
- **Web constraints**: No threads by default; keep draw calls low; no heavy GDExtension

---

## Game Pillars (Quick Reference)

1. **压迫即乐趣** — Pressure IS the game. Never reduce tension.
2. **电梯是家** — The elevator hub is the emotional core. Make it feel earned.
3. **资源讲故事** — Items tell the world's story. No separate lore menus.
4. **死亡有意义** — Every death is legible. Players must understand why they died.

*Full pillar definitions with design tests: `design/gdd/game-concept.md`*
