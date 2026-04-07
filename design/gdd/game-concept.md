# Game Concept: 垂直深渊 | Vertical Abyss

*Created: 2026-04-07*
*Status: Draft*

---

## Elevator Pitch

> 一款 Roguelite 生存游戏：你独自居住在一座崩塌建筑的电梯里，每次下降一层搜刮物资，在计时器归零前活着回来——用带回的东西扩建你的家，直到下一次死亡把你打回原点。
>
> *A roguelite survival game where you live in a broken elevator shaft, descend one floor at a time to scavenge under a merciless timer, and build your sanctuary with what you bring back — until death forces you to start over with nothing but the upgrades you've earned.*

---

## Core Identity

| Aspect | Detail |
| ---- | ---- |
| **Genre** | Roguelite / Survival Simulation / Base Management |
| **Platform** | Web (HTML5) — PC Browser, itch.io |
| **Target Audience** | Solo roguelite players who prefer tension over power fantasy |
| **Player Count** | Single-player |
| **Session Length** | 5–15 min per floor run; 30–60 min full session |
| **Monetization** | Free-to-play (itch.io) — no monetization planned for MVP |
| **Estimated Scope** | Small MVP (weeks) → Medium full vision (months) |
| **Comparable Titles** | Into the Dead: Our Darkest Days, Hades, Dead Cells |

---

## Core Fantasy

你是一个以电梯为家的幸存者。那里不安全，不舒适，但那是你的。每次按下"下一层"，你都是在用有限的时间换取让家变得更好一点的资源。你不是英雄，不会去征服这栋楼。你只是在尽力活着，一层一层地，直到某一层让你再也回不来。

*You are a survivor who has made a home in a broken elevator. It isn't safe. It isn't comfortable. But it's yours. Every descent is a trade: your time and safety for the resources to make it marginally better. You're not a hero conquering the building. You're just trying to stay alive, one floor at a time, until one floor doesn't let you come back.*

---

## Unique Hook

> 像 *Dead Cells* 一样有硬重置的 Roguelite 紧张感，**但电梯是你唯一能升级的永久家园**——你不是在征服地牢，你是用 60 秒的命换食物，然后把换来的东西变成下一次多活 10 秒的理由。
>
> *Like Dead Cells (hard run resets with meta-progression), AND ALSO your base — the elevator — is the only thing that persists and grows. You don't fight your way down. You survive your way down. Death takes everything you found; it can't take what you built.*

---

## Player Experience Analysis (MDA Framework)

### Target Aesthetics (What the player FEELS)

| Aesthetic | Priority | How We Deliver It |
| ---- | ---- | ---- |
| **Challenge** (obstacle course, mastery) | 1 — Core | 60s+ timer, hard death resets, DDA difficulty curve |
| **Sensation** (sensory pleasure) | 2 | Ticking red countdown, oppressive ambient sound, door-open moment |
| **Narrative** (drama, story arc) | 3 | Item descriptions, floor environment text, layered world mystery |
| **Discovery** (exploration, secrets) | 4 | Random floor layouts, locked deeper floors, room unlock reveals |
| **Fantasy** (make-believe) | 5 | Survivor identity — resourceful, desperate, alive |
| **Expression** (creativity) | N/A | No creative expression — scarcity is the point |
| **Fellowship** (social) | N/A | Deliberately solitary experience |
| **Submission** (relaxation) | N/A | Excluded by design — comfort destroys the core tension |

### Key Dynamics (Emergent player behaviors)

- Players will mentally calculate "is this item worth the time to grab it?"
- Players will develop risk heuristics: "floor type X is usually worth staying for"
- Players will feel genuine relief when they reach the exit — not just completion
- Players will remember specific deaths as stories ("I had 3 canned food and I went for one more item...")
- Players will prioritize which elevator room to build based on personal playstyle

### Core Mechanics

1. **DDA Timer System** — Base countdown scales with meta-progression level, random ±variance per floor keeps it unpredictable
2. **Procedural Floor Generation** — 10×10 grid with walls, items, obstacles, and fog of war
3. **Hard Run Reset** — Death clears all run resources; elevator room upgrades persist permanently
4. **Elevator Room Expansion** — Spend run resources to add functional rooms that provide passive run bonuses
5. **Resource Scarcity Model** — Items are rare enough that every pickup is a decision, never a guarantee

---

## Player Motivation Profile

### Primary Psychological Needs Served

| Need | How This Game Satisfies It | Strength |
| ---- | ---- | ---- |
| **Autonomy** (meaningful choice) | Which floor to risk; which items to grab; which room to build next; when to retreat | Core |
| **Competence** (mastery, skill growth) | Learning floor layouts faster, optimizing routes under pressure, reading DDA patterns | Core |
| **Relatedness** (connection) | Connection to the elevator as a "home" — not to other players | Supporting |

### Player Type Appeal (Bartle Taxonomy)

- [x] **Achievers** — Meta-progression rooms to unlock, floors to survive, deeper levels to reach
- [x] **Explorers** — What happened to this building? What's on floor 20? What does the generator room unlock?
- [ ] **Socializers** — Not served (intentional)
- [ ] **Killers/Competitors** — Not served (no PvP)

### Flow State Design

- **Onboarding curve**: First floor is low-risk, generous timer, few items — teaches movement and scavenging. Second floor introduces fog. Third introduces tighter timer.
- **Difficulty scaling**: DDA system ensures challenge stays near the player's current ability regardless of meta-progression level
- **Feedback clarity**: Timer is always visible in red; items highlight on approach; exit zone glows when timer < 15s
- **Recovery from failure**: Death screen shows timeline of decisions (what you grabbed, where you were when time ran out). Elevator is immediately visible — the progress you kept.

---

## Core Loop

### Moment-to-Moment (30 seconds)
Move through the fog. Spot an item. Decide: grab it (costs 2–3 seconds) or continue toward exit. Check timer. Decide again.

### Short-Term (5–15 minutes)
One floor run: enter from elevator, navigate fog, scavenge 3–8 items, return to exit before timer hits zero. Success: bring items home. Failure: hard reset, but elevator rooms survive.

### Session-Level (30–60 minutes)
Multiple floor runs accumulate enough resources to build or upgrade one elevator room. Each room changes the calculus for future runs. Session ends when player dies, steps away, or completes a room upgrade.

### Long-Term Progression
Unlock all elevator rooms. Discover the full narrative of the building. Reach the deepest accessible floor. Understand what caused the collapse.

### Retention Hooks

- **Curiosity**: What's behind the locked deeper floors? What do the item descriptions add up to?
- **Investment**: The elevator grows — players are attached to what they've built
- **Mastery**: Getting faster, reading floors better, surviving tighter timers
- **The near-miss**: "I almost made it. I had four items. Next run I'll know that floor."

---

## Game Pillars

### Pillar 1: 压迫即乐趣 (Pressure IS the Game)
The timer is not an obstacle to overcome — it is the experience. Every system must amplify the feeling of being in a race against time. Features that reduce tension work against the game's identity.

*Design test*: Should we add a pause button? → No. Pausing breaks the pressure and removes the sensation aesthetic entirely.

### Pillar 2: 电梯是你唯一的家 (The Elevator Is Worth Fighting For)
The hub must feel intimate, earned, and emotionally valuable. Players should make slightly irrational decisions to protect it. The elevator growing stronger over time is the emotional spine of the game.

*Design test*: Should room upgrades be cosmetic or functional? → Always functional. The player must feel the elevator becoming a better survival tool.

### Pillar 3: 资源讲述世界 (Resources Tell the Story)
The building has a history. That history is told through what you find, not through cutscenes or menus. Every item description, floor name, and environment text is a fragment of what happened here.

*Design test*: Should we add a separate lore journal? → Only if lore entries are also usable resources. No standalone collectible system — items must be dual-purpose.

### Pillar 4: 每次死亡都值得 (Every Death Teaches)
Hard resets are brutal but always legible. The player must understand why they died and have a clear theory about what they'll do differently. Death is a design conversation, not a punishment.

*Design test*: Should we add a death recap screen? → Yes, brief. Show the last 30 seconds of decisions. No statistics wall — just the story of how this run ended.

### Anti-Pillars (What This Game Is NOT)

- **NOT a combat game**: Avoiding danger is more interesting than defeating it. No attack mechanics.
- **NOT a hero story**: The player is a desperate survivor, not a chosen one. No power fantasy arc.
- **NOT a relaxing experience**: Any feature that reduces tension is actively hostile to the core design.
- **NOT a content-volume game**: 10 tight floors beats 50 padded ones. Scarcity applies to content too.

---

## Inspiration and References

| Reference | What We Take From It | What We Do Differently | Why It Matters |
| ---- | ---- | ---- | ---- |
| Into the Dead: Our Darkest Days | Resource scarcity, evacuation pressure, oppressive atmosphere | Vertical structure instead of horizontal; base building adds long-term investment | Validates the emotional target — this is the feeling we're after |
| Hades | Hard resets with persistent meta-progression; death as narrative beat | No combat; elevator room building vs. weapon/upgrade selection | Proves hard resets can coexist with emotional investment in progress |
| Dead Cells | Per-run tension, satisfying run rhythm, DDA difficulty | No platforming; top-down; the home base is the star, not the combat | Validates the roguelite loop for repeat play |
| Don't Starve | Oppressive atmosphere, resource scarcity as core tension | No survival meters; Web-friendly session length; narrower scope | Art direction and mood reference |

**Non-game inspirations**:
- *I Am Legend* (novel) — the psychology of a lone survivor making a home in a hostile world
- Brutalist architecture — the elevator shaft as a vertical, oppressive living space
- *The Road* (McCarthy) — scarcity as an emotional state, not just a resource state

---

## Target Player Profile

| Attribute | Detail |
| ---- | ---- |
| **Age range** | 18–35 |
| **Gaming experience** | Mid-core to Hardcore |
| **Time availability** | 15–60 minute sessions; Web means no install friction |
| **Platform preference** | Browser (itch.io), desktop secondary |
| **Current games they play** | Hades, Dead Cells, Slay the Spire, The Binding of Isaac |
| **What they're looking for** | Tension, meaningful decisions, a game that respects their time |
| **What would turn them away** | Grinding, padded content, tutorials that won't stop talking |

---

## Technical Considerations

| Consideration | Assessment |
| ---- | ---- |
| **Recommended Engine** | **Godot 4 (GDScript)** — best HTML5 export for free engines; GDScript ≈ Python (low transition cost from Pygame prototype); 2D is first-class |
| **Key Technical Challenges** | DDA system calibration; fog of war performance in Web; procedural floor quality (ensuring always-solvable layouts) |
| **Art Style** | 2D top-down; dark atmospheric; functional over decorative — oppression through negative space |
| **Art Pipeline Complexity** | Low-Medium — tile-based, limited palette, heavy use of darkness/shadow |
| **Audio Needs** | Moderate — ambient tension loops, timer escalation SFX, door open/close, item pickup. Music-minimal (silence amplifies tension) |
| **Networking** | None |
| **Content Volume** | MVP: 5 floor types, 5 item types, 1 elevator layout. Full: 15–20 floor types, 10+ item types, 8–10 elevator rooms |
| **Procedural Systems** | Floor layout generation (10×10 grid), loot distribution, DDA difficulty variance |

---

## Risks and Open Questions

### Design Risks
- DDA calibration may feel artificial if variance range is too narrow (predictable) or too wide (unfair)
- Hard reset may alienate casual Web players who expect lighter stakes
- Elevator room expansion may not provide enough agency if rooms feel passive

### Technical Risks
- HTML5 export performance — fog of war surface blending can be expensive in Godot Web
- Procedural floor generation must guarantee exit reachability (currently solved in Pygame prototype with L-corridor carve)
- Font rendering for CJK characters in Web export (already encountered and solved in Pygame prototype)

### Market Risks
- Roguelite Web space is crowded — hook must be immediately legible on itch.io thumbnail and one-line description
- Hard resets on Web may have higher abandonment rate than desktop equivalents

### Scope Risks
- "以上皆有" full vision (Roguelite + base building + narrative) is ambitious for a solo developer
- Narrative system may require significant writing and lore design work
- Room expansion system adds significant design and implementation complexity

### Open Questions
- What is the DDA formula? (Target: prototype in Godot vertical slice, measure feel)
- How many rooms make the elevator feel "complete" without becoming a management sim?
- What is the narrative payoff at maximum depth? (World mystery needs an answer)
- Should there be a "win condition" or is it infinite descent?

---

## MVP Definition

**Core hypothesis**: *Players find the scavenge-and-return loop engaging for repeated 5–10 minute sessions, even with a hard reset death penalty.*

**Required for MVP** (already built in Pygame prototype):
1. Elevator hub with player movement
2. Procedural 10×10 floor with fog of war
3. Timer (variable) with exit detection
4. 5 item types with inventory
5. Hard reset death (currently: soft penalty — to be upgraded to full reset)
6. 5 floor environment types with atmospheric text

**Explicitly NOT in MVP**:
- Elevator room expansion (deferred to Vertical Slice)
- DDA system (deferred — MVP uses fixed timer)
- Narrative depth / item lore text (deferred)
- Sound design (deferred)
- Godot port (Pygame prototype is sufficient for loop validation)

### Scope Tiers

| Tier | Content | Features | Notes |
| ---- | ---- | ---- | ---- |
| **MVP** | 5 floor types, 5 items | Core loop, fog of war, timer, basic inventory | ✅ Pygame prototype complete |
| **Vertical Slice** | 8 floor types, 8 items, 3 rooms | Godot port, DDA system, 3 elevator rooms, hard reset | Next milestone |
| **Alpha** | 15 floor types, 10 items, 8 rooms | Full difficulty curve, narrative text, ambient audio | Full roguelite loop |
| **Full Vision** | 20+ floor types, full narrative | All rooms, lore, win condition, Web-polished | itch.io release |

---

## Next Steps

- [ ] Run `/setup-engine godot 4` to configure Godot 4 as the production engine
- [ ] Run `/design-review design/gdd/game-concept.md` to validate completeness
- [ ] Run `/map-systems` to decompose into individual systems with dependencies and design order
- [ ] Port prototype core loop to Godot (Vertical Slice milestone)
- [ ] Prototype DDA system — test calibration feel
- [ ] Run `/sprint-plan new` to plan the first Godot sprint
