# 🏰 DUNGEON ENGINE

Hey, welcome! 👋 This is a little game I built — a **top-down dungeon shooter that you design with AI**. Describe a dungeon to any chatbot, paste what it gives you, and play it instantly in your browser. No installs, no sign-ups, no nonsense.

## ▶️ [**Click here to play it now →**](https://sumankayal247.github.io/Dungeon-engine/)

Runs right in your browser. A sample dungeon is already loaded, so you can jump straight in.

---

## What is this?

I wanted a game where the *levels* come from your imagination. So DUNGEON ENGINE doesn't have any AI baked into it — instead it comes with a ready-made prompt you can hand to **any** AI (ChatGPT, Claude, Gemini, whatever you like). You describe a dungeon in plain English, the AI writes the level data, you paste it in, and the engine builds and runs it.

It's all **pure code in a single file** — HTML5 Canvas and vanilla JavaScript, zero dependencies, no backend. The whole thing is just `index.html`, which means it loads fast and works offline too.

A few things I'm happy with:
- 🧱 Big `4000 × 4000` worlds with a camera that follows you
- 👾 Hand-made pixel sprites for the player and every monster, drawn entirely in code
- 🧠 Enemies that stay dormant until they actually spot you
- 🩹 A safe room you can retreat to and heal
- 🌀 A glowing exit portal — guarded, so you'll need to gear up first
- 🔊 Synthesized sound effects + screen-shake juice (all generated in code, no audio files)
- 📱 Works on mobile with on-screen touch sticks

---

## 🕹️ How to play

| Input | Action |
|-------|--------|
| **W A S D** | Move (hold two keys for diagonals) |
| **Arrow keys** | Aim **and** shoot in that direction (hold two to aim diagonally) |
| **Space** | Fire in your last aim direction |
| **Tab** | Switch between picked-up weapons |
| **Esc** / **P** | Pause (opens the menu) |
| **R** | Restart the dungeon |

📱 **On phones/tablets:** drag the on-screen sticks — **left to move, right to aim & shoot**.

**Your goal:** fight your way to the glowing **portal** and step through it to escape. It's heavily guarded, so explore the map and grab weapons and powerups before you make your run.

A few tips:
- The **green SAFE zone** where you start slowly heals you — duck back there when you're low.
- Enemies won't notice you until you're in their line of sight, so you can sneak around and pick your fights.
- If a weapon runs out of ammo, you'll automatically switch back to your trusty infinite pistol.

---

## 🤖 Make your own dungeons

There are two ways — pick whichever you like:

**A) The visual editor** (no JSON, no AI needed)

1. Click **✎ EDIT LEVEL**.
2. Pick a tool and click the map: draw **walls** (click-drag), place the **start**, the **exit**, **enemies**, **weapons** and **powerups**, or **move/erase** anything.
3. Right-drag to pan, scroll to zoom, "Snap to grid" keeps things tidy.
4. Hit **▶ TEST PLAY** to play it, or **⤓ EXPORT** to save the JSON.

**B) Describe it to an AI**

1. Hit **⧉ COPY AI PROMPT** in the side panel.
2. Paste it into any AI chat and tell it your theme — something like *"a flooded prison with sniper towers and a crumbling courtyard."*
3. Copy the JSON it gives back, paste it into the box, and hit **▶ BUILD & PLAY**.

**C) Roll the dice**

- **🎲 Remix** keeps a layout but shuffles the enemies, loot and weapons for instant replayability.
- **🏗️ Generate** builds a brand-new dungeon from scratch — a connected room-maze with a safe start, a guarded boss room, and loot spread throughout. It validates reachability and retries until the level is solvable, with a little "the Dungeon Master is building your level…" loader while it works.

Either way, the engine checks everything, fixes anything out of range, and even warns you if the exit accidentally got walled off.

## 🔗 Share your dungeon

Hit **⧉ SHARE LINK** and the whole level is packed into the URL (`…/#lvl=…`) and copied to your clipboard. Send that link to a friend and it opens straight into *your* dungeon — nothing to upload, no accounts. They can pause and remix it in the editor too.

---

## 📦 For the curious — the level format

A level is just one JSON object. The world is `4000 × 4000`, and every position is `[x, y]`.

```jsonc
{
  "name": "The Deep Vault",
  "world": 4000,
  "player": { "start": [260, 260], "hp": 100, "speed": 240, "radius": 14 },
  "goal":   { "pos": [3650, 3650], "radius": 46 },

  // Walls are line SEGMENTS — each is a pair of points.
  // List connected segments to draw any shape. (An inverted-L:)
  "walls": [
    [[300, 200], [400, 200]],
    [[300, 200], [300, 300]]
  ],

  "weapons": {
    "starting": "pistol",
    "pickups": [ { "type": "shotgun", "pos": [1750, 420] } ]
  },

  "powerups": [
    { "type": "health", "pos": [270, 470], "value": 40 }
  ],

  "enemies": [
    { "type": "brute", "pos": [3650, 3850], "hp": 420, "speed": 48, "damage": 36 },
    { "type": "mage",  "pos": [2000, 3400], "behavior": "patrol",
      "path": [[2000, 3400], [1500, 3400], [1500, 3800]] }
  ]
}
```

**The pieces you can use:**

| Category | Options |
|----------|---------|
| **Weapons** | `pistol` · `smg` · `shotgun` · `sniper` |
| **Powerups** | `health` · `shield` · `speed` · `damage` · `ammo` |
| **Enemies** | `grunt` · `runner` · `brute` · `sentry` · `turret` · `mage` · `bomber` (explodes on contact) · `splitter` (bursts into 5 babies) · `dasher` (lunges at you) · `boss` (spray-fires; put near the exit) |
| **Behaviors** | `chase` · `patrol` (needs a `path`) · `static` |

**Weapons at a glance:**

| Weapon | Damage | Fire rate | Ammo | Notes |
|--------|-------:|-----------|-----:|-------|
| Pistol | 18 | medium | ∞ | Your starter |
| SMG | 10 | very fast | 140 | Slight spread |
| Shotgun | 9 ×8 | slow | 28 | Wide pellet spread |
| Sniper | 75 | slow | 10 | Fast bullet, **pierces** enemies |

**Powerups:**

| Powerup | Effect |
|---------|--------|
| Health | Restores HP |
| Shield | Adds a damage-absorbing shield |
| Speed | Move faster for a few seconds |
| Damage | Double damage for a few seconds |
| Ammo | Refills your current weapon |

The per-enemy fields like `hp`, `speed`, `damage`, `sight`, and `path` are all optional — leave them out and each enemy uses sensible defaults.

---

## ⚙️ Handy extras

The side panel has a few quality-of-life toggles: minimap, background grid, pickup popups, an FPS counter, and an invincible "test mode" for when you just want to wander a level you're designing.

---

## 🛠️ Under the hood

Plain HTML5 Canvas and vanilla JavaScript — no libraries, no build step. The pixel sprites are defined as little character grids and drawn into the canvas at load. Everything you paste is parsed safely (`JSON.parse` only, never `eval`), so it's fine to try levels from anywhere.

---

Thanks for stopping by — I hope you have fun with it! Feel free to fork it, tinker with it, and build your own dungeons. 🗡️

## 📄 License

Released under the [MIT License](LICENSE) — do whatever you like with it.
