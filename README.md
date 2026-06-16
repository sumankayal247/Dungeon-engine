# 🏰 DUNGEON ENGINE

A **browser-based, data-driven dungeon shooter** that turns a single JSON description into a fully playable top-down game — walls, weapons, powerups, enemies, a safe room, and a guarded exit portal.

The twist: **the engine has no AI inside it.** Instead it ships a fixed prompt you can hand to *any* AI (ChatGPT, Claude, Gemini, …). The AI returns level data in the engine's format, you paste it in, and the engine builds and runs the game. You design dungeons by describing them in plain English.

- ⚙️ **Pure code, zero dependencies** — one self-contained `index.html` (HTML + Canvas + vanilla JS). No build step, no frameworks, no backend, no assets.
- 🎮 **Plays instantly** — open the file (or the live page) and a sample dungeon is already running.
- 🧱 **Coordinate-based levels** in a `4000 × 4000` world with a camera that follows the player.
- 👾 **Hand-made pixel sprites** for the player and every monster, drawn procedurally in code.

---

## ▶️ Play it live

If you deploy this repo to **GitHub Pages** (instructions below), it will be playable at:

```
https://<your-username>.github.io/<repo-name>/
```

Or just download `index.html` and open it in any modern browser — it runs entirely offline.

---

## 🕹️ How to play

| Input | Action |
|-------|--------|
| **W A S D** | Move (hold two keys for diagonals) |
| **Arrow keys** | Aim **and** shoot in that direction (hold two to aim diagonally) |
| **Space** | Fire in your last aim direction |
| **Esc** / **P** | Pause (opens the side panel — it's your pause menu) |
| **R** | Restart the current dungeon |

**Goal:** Fight your way to the glowing **portal** and step through it to escape.
The portal is heavily guarded, so **explore the map and collect weapons & powerups** before you make your run.

**Tips**
- The **green SAFE zone** at your start regenerates HP — retreat there when you're low.
- Enemies are **dormant until they spot you** (they need line-of-sight within their vision range), so you can sneak and pick fights on your terms.
- When a weapon runs out of ammo you automatically fall back to the infinite pistol.

---

## 🤖 Designing your own dungeons (with any AI)

1. Click **⧉ COPY AI PROMPT** in the side panel (or open [`AI_PROMPT.txt`](AI_PROMPT.txt)).
2. Paste it into any AI chat and replace the last line with your theme, e.g.
   *"a flooded prison with sniper towers and a flooded central courtyard."*
3. The AI returns a single JSON object.
4. Paste it into the text box and hit **▶ BUILD & PLAY**.

The engine validates and sanitizes everything: unknown values are skipped with a warning, numbers are clamped to safe ranges, and a flood-fill check warns you if the exit is accidentally walled off.

---

## 📦 Level format

A level is one JSON object. The world is a `4000 × 4000` grid; every position is `[x, y]`.

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

### Allowed values (use these exact strings)

| Category | Values |
|----------|--------|
| **Weapons** | `pistol` · `smg` · `shotgun` · `sniper` |
| **Powerups** | `health` · `shield` · `speed` · `damage` · `ammo` |
| **Enemies** | `grunt` · `runner` · `brute` · `sentry` · `turret` · `mage` |
| **Behaviors** | `chase` · `patrol` (needs a `path`) · `static` |

### Weapons

| Weapon | Damage | Fire rate | Ammo | Notes |
|--------|-------:|-----------|-----:|-------|
| Pistol | 18 | medium | ∞ | Starting weapon |
| SMG | 10 | very fast | 140 | Slight spread |
| Shotgun | 9 ×8 | slow | 28 | Wide pellet spread |
| Sniper | 75 | slow | 10 | Fast bullet, **pierces** enemies |

### Powerups

| Powerup | Effect |
|---------|--------|
| Health | Restores HP (`value`, default 30) |
| Shield | Adds damage-absorbing shield (default 50, caps at 150) |
| Speed | ~1.7× move speed for a few seconds |
| Damage | Double damage for a few seconds |
| Ammo | Refills the current weapon |

Per-enemy fields `hp`, `speed`, `damage`, `ranged`, `sight`, and `path` are **optional overrides** — omit them to use each enemy type's defaults.

---

## ⚙️ Side-panel settings (QoL)

- **Pause / Restart** buttons
- Toggle **minimap**, **background grid**, **pickup popups**, **FPS counter**
- **Invincible (test mode)** — for trying out levels without dying

---

## 🚀 Deploy to GitHub Pages

Because it's a single static file, hosting is trivial:

1. Push this folder to a GitHub repository.
2. Go to **Settings → Pages**.
3. Under **Build and deployment → Source**, choose **Deploy from a branch**.
4. Select branch **`main`** and folder **`/ (root)`**, then **Save**.
5. Wait ~1 minute — your game is live at `https://<your-username>.github.io/<repo-name>/`.

> `index.html` is at the repo root, so GitHub Pages serves it as the homepage automatically.

---

## 📁 Project structure

```
dungeon-engine/
├── index.html      # the entire engine + renderer + sample level (open this)
├── AI_PROMPT.txt   # the prompt to give any AI to generate levels
├── README.md
└── LICENSE         # MIT
```

---

## 🔒 Notes on safety

Level data is parsed with `JSON.parse` only (**never `eval`**), every field is type-checked and clamped, and all text is rendered with `textContent` (no HTML injection). The game makes no network requests and stores nothing — it's safe to run untrusted level JSON.

---

## 🛠️ Tech

Plain HTML5 Canvas + vanilla JavaScript. No libraries, no build tooling. Pixel sprites are defined as character grids and baked into offscreen canvases at load.

Made for fun — fork it, tweak the catalogs, and design your own dungeons. 🗡️

---

## 📄 License

Released under the [MIT License](LICENSE) — free to use, modify, and distribute.
