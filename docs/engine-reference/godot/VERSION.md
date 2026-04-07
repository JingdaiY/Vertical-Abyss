# Godot — Version Reference

*Last verified: 2026-04-07*

| Field | Value |
|-------|-------|
| **Engine Version** | Godot 4.6.2 |
| **Project Pinned** | 2026-04-07 |
| **LLM Knowledge Cutoff** | August 2025 |
| **Estimated LLM Coverage** | Up to ~Godot 4.3 |
| **Risk Level** | HIGH — versions 4.4, 4.5, 4.6 are beyond LLM training data |

## Risk Summary

Godot 4.4, 4.5, and 4.6 introduced changes that the LLM was not trained on.
Before suggesting any API, agents must:

1. Check `deprecated-apis.md` — do not suggest deprecated methods
2. Check `breaking-changes.md` — do not suggest patterns removed in 4.4+
3. Use WebSearch to verify uncertain APIs against current docs at
   `docs.godotengine.org/en/stable/`

## Reference Files in This Directory

| File | Contents |
|------|----------|
| `breaking-changes.md` | Version-by-version breaking changes from 4.4 to 4.6 |
| `deprecated-apis.md` | "Don't use X → Use Y" replacement table |
| `current-best-practices.md` | New patterns and practices since Godot 4.3 |

## Official Documentation

- Docs: https://docs.godotengine.org/en/stable/
- Migration 4.3→4.4: https://docs.godotengine.org/en/4.4/tutorials/migrating/upgrading_to_godot_4.4.html
- Migration 4.4→4.5: https://docs.godotengine.org/en/4.5/tutorials/migrating/upgrading_to_godot_4.5.html
- Migration 4.5→4.6: https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.6.html
- Changelog: https://github.com/godotengine/godot/blob/master/CHANGELOG.md
