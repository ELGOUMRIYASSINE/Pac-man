# Road Structure: How This Pac-Man Project Works

This guide explains the whole project from launch to game over, so you can explain and defend it.

**Read it in this order:** sections 1 to 4 give you the cycle, section 5 the ideas behind it, section 7 what is missing, and section 8 practice questions.

---

## 1. The project in 30 seconds

This is a Pac-Man game written in Python with **pygame**. Every level has a generated maze, and its size comes from a config file.

The player eats every gum to finish a level, while 4 ghosts chase them. A super gum makes the ghosts edible for 7 seconds.

The whole program follows one chain:

```
config.json  ->  validated data  ->  window + menu  ->  PLAY  ->  build a maze
                                                                      |
                     +------------------------------------------------+
                     v
          game loop, 60 times per second:
          read input -> update the game -> draw the screen
                     |
                     +-- all gums eaten -> next level (or back to the menu after the last one)
                     +-- touched a ghost -> lose a life, restart the level positions
                     +-- no lives left   -> back to the menu
```

---

## 2. Project map: the role of every file

```
Pac-man/
├── pac-man.py                  Entry point: starts everything
├── config.json                 Game settings: levels, lives, points
├── scores.json                 Saved high scores
├── pyproject.toml / uv.lock    Dependencies and their exact versions
├── Makefile                    Shortcuts: install, run, debug, clean, lint
├── test.py                     Small pygame experiment, not part of the game
├── assets/                     Images, fonts, instructions text
└── src/
    ├── metadata.py             Simple getters over the config data
    ├── Parsing/
    │   ├── parse_args.py       Checks the command line, reads config.json
    │   ├── parse_config_file.py Removes comments and validates the config
    │   └── parse_highscore.py  Reads scores.json, asks for the player's name
    ├── Maze/
    │   ├── get_maze_bylevel.py Asks the library for a maze for one level
    │   └── Maze.py             Turns that maze into Cell objects, places everything
    ├── GameEngine/             THE RULES OF THE GAME
    │   ├── Game_loop.py        The main loop and screen states (the conductor)
    │   ├── player.py           Player data, movement, eating, level result
    │   ├── gosts.py            Ghost data
    │   └── move_ghosts.py      Ghost AI (BFS, greedy, fleeing)
    ├── rendering/              EVERYTHING YOU SEE
    │   ├── main_menu.py        Menu buttons
    │   ├── instructions.py     Instructions screen
    │   ├── maze_render.py      Draws walls, gums, sprites, score and lives
    │   ├── move.py             Smooth sliding and collision math
    │   ├── score_board.py      EMPTY
    │   └── entry_page/entry.py Title page: created but never drawn
    ├── Highscore_system/
    │   └── get_highscore.py    Saves the top 10: written but never called
    └── Cheat_mode/             EMPTY
```

The main design idea is **separation of responsibilities**:

| Layer | Question it answers | Folder |
|---|---|---|
| Parsing | Is the input data valid? | `Parsing/` |
| Maze | What does the level look like? | `Maze/` |
| Engine | What happens in the game? | `GameEngine/` |
| Rendering | What does it look like on screen? | `rendering/` |

---

## 3. The tools used and why

| Tool | Role here | Why it is useful |
|---|---|---|
| **pygame** | Window, keyboard and mouse, drawing, clock | Standard Python 2D game library |
| **mazegenerator** | Creates the maze for each level | External package, provided as a `.whl` file |
| **pydantic** | Final check of the config data (types and limits) | Rules are declared once, in a class |
| **uv** | Installs dependencies and runs the project in `.venv` | `uv.lock` gives everyone the same versions |
| **Makefile** | Short commands such as `make run` | Nobody needs to remember the long commands |
| **cleanpy** | Removes Python cache files (`make clean`) | Keeps the folder clean |
| **flake8 / mypy** | Style and type checks (`make lint`) | Not listed as dependencies and not in `.venv`, so they must be installed separately |

From the Python standard library:

- **`argparse`** reads the command line.
- **`json`** reads the config and scores.
- **`pathlib`** handles file paths.
- **`dataclasses`** defines `Cell`, `Player` and `Ghost`.
- **`enum`** defines the wall directions.
- **`collections.deque`** is the queue used by BFS.

---

## 4. The full cycle, step by step

### Step 1: Launch

```bash
.venv/bin/python pac-man.py config.json
```

Run it from the project root, because `config.json` and `assets/...` are found relative to the current folder.

[pac-man.py:12-20](pac-man.py#L12-L20) does only three things: load the config, wrap it in `MetaData`, and start `GameLoop`.

> `make run ARG=config.json` is the intended command, but it **fails right now**. See [section 7](#7-honest-status-what-works-and-what-does-not).

### Step 2: Read and validate the config

```
Args.get_args         checks the argument is exactly "config.json", returns the file text
      |
_clean_content        removes full lines starting with # or //, and blank lines
      |
json.loads            text -> Python dictionary
      |
load_json checks      wrong or missing value -> print a warning, use the default
      |
pydantic              final validation of types and limits
      |
MetaData              get_width(level), get_lives(), get_pacgum_points(), ...
```

Code: [parse_args.py:15](src/Parsing/parse_args.py#L15), [parse_config_file.py:54](src/Parsing/parse_config_file.py#L54), [metadata.py](src/metadata.py).

Defaults are 10 levels of 10x10, 6 lives, and 13 / 37 / 42 points for gum / super gum / ghost.

Tested behaviour:

| Input | Result |
|---|---|
| Broken JSON, or a comment at the end of a line | Warning, then **all** defaults |
| Missing key | Warning, default for that key |
| Number below 1, like `pacgum_points: -13` | Warning, default (13) |
| Level width or height missing, 0, or above 900 | Warning, 10 |
| `player_lives: 21` | **Crash**: pydantic `ValidationError` |
| Text instead of a number | **Crash**: `TypeError` |
| Top level is a list, like `[1,2]` | **Crash**: `TypeError` |
| `levels: []` | Accepted by the parser, but PLAY would then fail because level 0 does not exist (from reading the code, not run) |

> The current `config.json` contains `"pacgum_points": -13`, so every launch prints a warning and gums are worth 13. An examiner may ask about this.

### Step 3: Create the window and objects

[GameLoop.\_\_init\_\_](src/GameEngine/Game_loop.py#L25) starts pygame, opens a **1200x740** window, and creates the menu, the instructions screen, the clock and 4 ghosts. The starting state is `"MENU"`.

### Step 4: The main loop runs

[GameLoop.entry](src/GameEngine/Game_loop.py#L292) is the heart of the program. It repeats until the window closes:

```
while running:
    1. read mouse position and events
    2. window closed? -> stop
    3. run the current screen:  MENU | GAME | INSTRUCTIONS
    4. if in GAME, draw the maze
    5. pygame.display.flip()    show the finished picture
    6. clock.tick(60)           wait, so we run at most 60 frames per second
```

Step 3 is a **state machine**. `screen_state` says which screen is active:

```
   MENU --- PLAY click ---------------------------> GAME
   MENU <-- ESC / no lives / last level cleared --- GAME
   GAME --- all gums eaten, more levels remain ---> GAME (next level)

   MENU --- Instructions click --> INSTRUCTIONS
   MENU <-- Back click ----------- INSTRUCTIONS

   Exit click or closing the window: the program stops
```

### Step 5: The player clicks PLAY: build the level

[start_game](src/GameEngine/Game_loop.py#L62) resets to level 0, then [load_level](src/GameEngine/Game_loop.py#L68) calls [Maze.creat_cells](src/Maze/Maze.py#L57):

1. **Generate:** [LevelMaze](src/Maze/get_maze_bylevel.py#L15) creates a `MazeGenerator`. Level 0 uses `seed=42`, so it is always the same. Other levels are random.
2. **Place the player:** the middle of the maze, or the closest cell that is not sealed.
3. **Convert:** each number from the library becomes a `Cell` with 4 wall booleans.
4. **Fill the cells:**
   - The player's cell stays empty.
   - The 4 corners get **super gums**.
   - Every other open cell gets a **gum**.
5. **Place the ghosts:** one in each corner, and a ghost's corner is its `home`.

Then a new `MazeRender` is created. It computes the cell size and loads the sprites.

**What the library does inside `MazeGenerator`:**

1. Creates an empty grid with outer walls.
2. Inserts a sealed "42" pattern if the maze is big enough (at least 14 wide and 10 high).
3. Carves corridors with **depth-first search**.
4. With `perfect=False`, **braids** the maze: it opens extra walls so corridors form loops and dead ends disappear.
5. Computes a shortest path with BFS. The game never uses that path.

### Step 6: One frame of gameplay

This is the most important function to know: [game_frame](src/GameEngine/Game_loop.py#L244).

```
INPUT    arrow keys / WASD -> stored in next_direction; ESC -> menu

FREEZE   just died? wait 800 ms and skip everything below

LOGIC    (decide which cell everyone goes to)
  1. step_player        every 200 ms: try the wanted direction, then move
  2. end_expired_power  7 seconds over? ghosts become dangerous again
  3. step_ghosts        every 400 ms: ask the AI for the next cell
  4. sync_ghost_cells   update the has_ghost flags in the cells

PIXELS   (slide the sprites)
  5. update_entities    move each sprite a little towards its cell

RESULTS  (based on what the player actually sees)
  6. eat_when_arrived   sprite half way there? eat the gum
  7. check_collision    sprites touching? eat the ghost or die
  8. check_level        decide the result (next section)
```

After this, `entry` calls [MazeRender.draw](src/rendering/maze_render.py#L123), which draws black background, walls, gums, player, ghosts, then score and lives, in that order. Later drawings appear on top.

### Step 7: Decide the result

[check_level](src/GameEngine/player.py#L76) returns one of these:

| Result | Condition | What happens |
|---     |---        |---           |
| `"CON"` | Gums remain | Keep playing |
| `"RESPOWN"` | Dead, with more than 1 life | Lose a life, freeze 800 ms, everyone returns to their start. **Eaten gums stay eaten.** |
| `"LOSE"` | Dead on the last life | Freeze 800 ms, back to the menu |
| `"NEXT"` | No gums left, more levels exist | Next level with a new maze. **Score is kept, lives are reset.** |
| `"END"` | No gums left on the last level | Back to the menu |

The cycle then starts again from Step 4 or Step 5.

---

## 5. The key ideas to explain

### 5.1 Walls stored as bits

The library stores each cell as a number from 0 to 15, where each bit is one wall. A bit set to 1 means **the wall exists**.

```
N = 1   E = 2   S = 4   W = 8
```

| Value | Binary | Meaning |
|---|---|---|
| 9 | `1001` | Walls north and west (a top-left corner) |
| 0 | `0000` | No walls |
| 15 | `1111` | Sealed: part of the "42" pattern |

Test one wall with AND: `bool(walls & Directions.N)`, in [Maze.py:82](src/Maze/Maze.py#L82). This is compact and fast, and each cell needs only one number.

### 5.2 Row and column order

The maze is `maze[row][col]`, so positions are **(row, col)**, which means (y, x). The library's `size` is the opposite: `(width, height)`.

To move up, the row decreases, because row 0 is at the top of the screen. The [`MOVES`](src/GameEngine/player.py#L7) table holds this.

### 5.3 Two separate worlds: logic and pixels

This is the main design decision of the game engine.

- **Logic** is cells: `player.position = (7, 7)`. It changes instantly, in one step.
- **Pixels** are the sprite's position on screen. It slides there over time.

A [`Mover`](src/rendering/move.py#L5) connects the two by using **linear interpolation (lerp)**:

```
progress = (now - start_time) / duration      from 0.0 to 1.0
position = start + (target - start) * progress
```

The player's slide takes 200 ms and a ghost's takes 400 ms, so **the player is twice as fast**.

The movement uses real clock time and not frame counts, so the speed stays the same even if the frame rate drops.

### 5.4 Why collisions use pixels and not cells

Comparing cells has two bugs, both explained at [Game_loop.py:126](src/GameEngine/Game_loop.py#L126):

1. **Early death:** the cell changes when a step begins, so you would die before the sprites touch.
2. **Passing through:** a player and a ghost walking towards each other can swap cells without ever sharing one.

So [closest_distance](src/rendering/move.py#L42) checks the whole movement in a frame, not just the end positions. It uses relative motion:

```
gap     = a_start - b_start
closing = (a_move) - (b_move)
distance at time t = |gap + closing * t|      with t between 0 and 1

the smallest distance is at  t = -(gap . closing) / |closing|^2
```

If that distance is below **half a cell**, they collide. The limit must stay below 1 cell, because sprites separated by a wall are always at least 1 cell apart.

### 5.5 Ghost AI

All of this is in [next_cell](src/GameEngine/move_ghosts.py#L63):

| Ghost | Behaviour | Method |
|---|---|---|
| ID 0 and 2 | Chase by the true shortest path | **BFS** |
| ID 1 and 3 | Go to the neighbour closest to the player | **Greedy** with Manhattan distance |
| Any weak ghost | Run away | Neighbour **furthest** from the player |

**BFS** ([move_ghost_bfs](src/GameEngine/move_ghosts.py#L30)) explores the maze in rings from the ghost, using a queue. In a maze where every step costs the same, the first time it reaches the player is by a shortest path. It records each cell's parent, walks back from the player to rebuild the path, and the ghost takes only the first step. It recalculates at each step because the player keeps moving. Its cost is proportional to the number of cells.

**Greedy** ignores walls when measuring distance, so it can be blocked. That gives these ghosts a different, less perfect personality. **Manhattan distance** is `|row1 - row2| + |col1 - col2|`.

**No turning back:** greedy and weak ghosts cannot return to `ghost.previous` unless it is the only move. Otherwise they would shake between two cells forever. When a super gum is eaten, `previous` is cleared so ghosts may turn around and flee.

### 5.6 Super gum and ghost life cycle

```
NORMAL -- player eats super gum --> WEAK (blue, 7 seconds)
  ^                                   |
  |                                   +-- 7 seconds end --> NORMAL
  |                                   |
  |                              player touches it: +ghost points
  |                                   v
  +----- reset at home <------------ EATEN (invisible, cannot collide)
       at least 4 s later, and only if the
       player is more than 2 cells from home
```

A respawned ghost is **dangerous** even if the power is still active, because `reset()` clears `weak`.

### 5.7 Input buffering

A key press does not move the player directly. It is stored in `next_direction`, and [step_player](src/GameEngine/Game_loop.py#L190) applies it as soon as that way is free.

So you can press a direction just **before** reaching a corner and the turn still happens. Meanwhile, the player keeps going in the current `direction`.

### 5.8 Drawing tricks

- **Cached walls:** walls have a glow and three layers, which is too slow to redo 60 times a second. [_build_wall_layer](src/rendering/maze_render.py#L73) draws them once onto a surface, and each frame just copies it.
- **No doubled walls:** [_wall_segments](src/rendering/maze_render.py#L48) uses a `set`, so a wall shared by two cells is drawn once.
- **Glow:** thick translucent lines are scaled down then back up, which blurs them.
- **Prepared sprites:** [_build_sprites](src/rendering/maze_render.py#L147) loads images once. Pac-Man is rotated for each direction, and the blue ghost is made by swapping red and blue in every pixel.
- **Scaling:** cell width is `(1200 - 10) / columns` and height is `(740 - 10 - 40) / rows`, where 40 is the HUD band. The maze always fills the window. On level 0, a cell is about 79x46 pixels, so cells are not square.

---

## 6. Reference tables

### Main data objects

| Class | Important fields |
|---|---|
| [`Cell`](src/Maze/Maze.py#L11) | `North`, `Est`, `South`, `West` (walls), `gum`, `supgum` |
| [`Player`](src/GameEngine/player.py#L16) | `position`, `lives`, `score`, `level`, `dead`, `super_power`, `super_until`, `facing` |
| [`Ghost`](src/GameEngine/gosts.py#L6) | `id`, `position`, `home`, `previous`, `weak`, `eaten`, `respawn_at` |

`Cell` also has `has_player`, `has_ghost` and `ghost_id`. They are updated but no game decision reads them. `edible_ghost` is never used, and `palyer_init_pos` is set but never read.

### Game constants

| Value | Meaning | Where |
|---|---|---|
| 60 | Maximum frames per second | `Game_loop.py` |
| 200 ms | Time per player step | `MOVE_DELAY` |
| 400 ms | Time per ghost step | `GHOST_MOVE_DELAY` |
| 7000 ms | Super power duration | `SUPER_POWER_MS` |
| 4000 ms | Minimum time before an eaten ghost returns | `GHOST_RESPAWN_MS` |
| 800 ms | Freeze after a death | `DEATH_PAUSE_MS` |
| 0.5 cell | Collision distance | `COLLISION_RATIO` |
| 0.5 | Step progress at which a gum is eaten | `EAT_AT_PROGRESS` |
| 2 cells | Ghost won't respawn this close to the player | `GHOST_SAFE_CELLS` |

### Current `config.json`

10 levels: 15x15, 6x6, 15x15, 20x20, then 7x7 six times. 20 lives per level. Points after validation: gum 13, super gum 37, ghost 65.

The "42" only appears on the 15x15 and 20x20 levels, because the others are too small. Sizes do not always grow, even though the comment in the config says levels get harder as the maze gets bigger.

---

## 7. Honest status: what works and what does not

**Prepare for this section first.** An examiner can find these quickly, and it is better if you mention them yourself.

### What I checked

I ran the real code without a visible window, using SDL's dummy video driver and a fake clock. So nothing below was checked by eye, including how the screens look.

- The game starts and the menu loop runs.
- Menu to game, ESC, death, respawn, losing, next level and last level all behave as described.
- A simple bot played a full game from PLAY to the menu using the real ghosts. It lost all its lives on level 0, but it is a basic bot, so this says nothing about difficulty.
- Across 200 generated mazes per random level, **every gum was reachable**.

### Task list from the README

| Task | Owner | Status |
|---|---|---|
| Parsing | Falamlih | Works, with the crash cases in Step 2 |
| Game engine | Falamlih | Works |
| Maze integration | Falamlih | Works |
| Levels | Falamlih | Works |
| High score system | Falamlih | **Code exists but is not connected** |
| Cheat mode | Falamlih | **Not done**: empty folder |
| Main menu | Yelgoumr | Works, but the High Scores button does nothing |
| In-game HUD | Yelgoumr | Shows score and lives |
| Pause menu | Yelgoumr | **Not done**: ESC goes to the menu, and PLAY starts a new game |
| Game over screen | Yelgoumr | **Not done**: returns straight to the menu |
| Victory screen | Yelgoumr | **Not done**: returns straight to the menu |
| Deployment | Yelgoumr | **Broken**: see the first problem below |

The project subject is not in this repository, so I could not compare the project against its official requirements. Check them yourself.

### Problems to fix first

1. **`uv` commands fail, including `make run`.** [pyproject.toml:15](pyproject.toml#L15) looks for the wheel in `mazegenerator-00001/`, but that folder does not exist. The wheel is in the project root.
   - `uv sync`, `uv run` and `make run` all stop with `failed to open file`.
   - `.gitignore` also excludes the wheel, so a fresh clone does not have it at all.
   - `.venv/bin/python pac-man.py config.json` works today only because `.venv` is already installed.
2. **Scores are never saved.** `top_10_scores` is never called, so a finished game's score is lost.
3. **The instructions screen shows placeholder "Lorem Ipsum" text**, from [instructions.txt](assets/instructions.txt).
4. **Config crashes.** The `try/except` in [pac-man.py:9](pac-man.py#L9) is commented out, so the crashes in Step 2 show a raw traceback.

### Smaller bugs

| Problem | Where | Effect |
|---|---|---|
| `make run` uses `ARG`, `make debug` uses `ARGS` | [Makefile:11](Makefile#L11), [Makefile:14](Makefile#L14) | Easy to pass the argument wrongly |
| `make run` needs an argument | [parse_args.py:20](src/Parsing/parse_args.py#L20) | Plain `make run` stops with an argparse error, even once uv is fixed |
| `\|\| true` on every Makefile command | [Makefile](Makefile) | Hides failures: `make` reports success even when the command fails |
| Name retry result is ignored | [parse_highscore.py:20](src/Parsing/parse_highscore.py#L20) | Tested: enter the taken name "alice", then "bob", and alice's old score is overwritten while "bob" is thrown away |
| Top 10 with tied scores | [get_highscore.py:31-35](src/Highscore_system/get_highscore.py#L31-L35) | Tested: with 11 scores of 10, a new score of 5 enters the table and removes a 10 |
| `print("drawing menu")` | [main_menu.py:60](src/rendering/main_menu.py#L60) | Prints up to 60 lines per second in the terminal |
| Menu text is too large | [main_menu.py:30](src/rendering/main_menu.py#L30) | 40 px labels on 140 px buttons, so the text overflows |
| Typos on screen | [main_menu.py:69-70](src/rendering/main_menu.py#L69-L70) | "PLay", "View Hightscores" |
| Options documented but not implemented | [config.json:3](config.json#L3), [config.json:12](config.json#L12) | `hiscore_file` and `level_max_time` do nothing: levels have no time limit |

### Unused code and files

- `EntryFace` is created but never drawn, and it holds fake scores.
- `pac-man.py` imports `HighScore`, `Player` and `Maze` without using them.
- `src/rendering/score_board.py` and `src/Cheat_mode/` are empty.
- `assets/ghost.png`, the `pacman10-hp-sprite` image and the `assets/fonts/` copies are not used by the code.
- `test.py` is a separate experiment.

---

## 8. Likely defence questions

**What happens when I run the program?**
The config is read, cleaned and validated, then wrapped in `MetaData`. `GameLoop` opens the window and enters the main loop in the `MENU` state. Clicking PLAY builds level 0 and switches to `GAME`.

**What is a game loop?**
A loop that repeats input, update and draw, many times per second. Here it runs at up to 60 FPS, limited by `clock.tick(60)`.

**What does `flip()` do?**
pygame draws onto a hidden picture. `flip()` shows it all at once, so the player never sees a half-drawn frame.

**How do you keep the speed the same on slow computers?**
Movement is based on clock time from `get_ticks()`, not on frames. A slow computer shows fewer frames, but the sprites travel at the same speed.

**Why BFS for the ghosts and not DFS?**
All steps cost the same, so BFS guarantees a shortest path. DFS finds a path, but it may be a very long one.

**Why are there two kinds of chasing ghosts?**
If all ghosts used BFS, they would follow the same paths and bunch together. The greedy ones are less perfect, so ghosts behave differently and the player has more chances to escape.

**What is a perfect maze? Why `perfect=False`?**
A perfect maze has exactly one path between any two cells, so it has no loops. Pac-Man needs loops to escape from ghosts, so the generator opens extra walls.

**Are there really no dead ends?**
Almost. On the 15x15 and 20x20 levels I found exactly 2 dead-end cells in every maze tested, in the same two positions each time, such as (6,9) and (8,9) on 15x15. They are pockets inside the sealed "2" of the "42" pattern, and braiding is not allowed to open sealed cells. The 6x6 and 7x7 levels had none.

**Can a level be impossible to finish?**
No gum was unreachable in my tests. Sealed "42" cells never receive a gum, because `Maze.py` checks `walls != SEALED`.

**How do you know the level is finished?**
After every frame, `check_level` looks for any cell still holding a gum or super gum. If none are left, the level is complete.

**Why is the gum eaten at 50% of the step?**
So it disappears when the sprite visibly reaches it, not when the step starts.

**Why not compare cells for collisions?**
Because of early deaths and of entities swapping cells without ever sharing one. See section 5.4.

**Why cache the walls?**
They never change during a level and they are expensive to draw, so they are drawn once and copied each frame. A signature check rebuilds them only if something changes.

**Why bits for the walls?**
One small number stores 4 yes-or-no values, and `&` tests each one easily. It is also the format the library gives us.

**Why pydantic if you already check the values by hand?**
The manual checks repair bad values with a warning. Pydantic is the final guard on types and limits. For example, `player_lives` above 20 is only caught by pydantic. It currently crashes because nothing catches the error.

**Why is the logic separate from rendering?**
Rules can change without touching the drawing, and the reverse. It is also why the game could be tested without a window.

**How would you add the pause menu?**
Add a `"PAUSE"` state to the state machine. ESC would switch to it without resetting anything, and the resume button would switch back to `GAME`. All timers use `get_ticks()`, so they keep running during a pause. Resume would need to shift `last_move`, the ghost timers, `super_until`, `respawn_at` and the movers' start times by the paused time.

**How would you connect the high scores?**
When the result is `"LOSE"` or `"END"`, go to a screen that asks for the name, then call `top_10_scores(score)`. `get_name` currently uses `input()` in the terminal, so it would need to become a pygame text field, and its retry bug must be fixed.

---

## 9. How to study the code

Read in this order. Each step builds on the one before it.

1. [pac-man.py](pac-man.py): the start, only a few lines
2. [config.json](config.json), then [parse_config_file.py](src/Parsing/parse_config_file.py)
3. [Maze.py](src/Maze/Maze.py): how the level is built
4. [player.py](src/GameEngine/player.py) and [gosts.py](src/GameEngine/gosts.py): the data and the rules
5. [Game_loop.py](src/GameEngine/Game_loop.py): read `entry`, then `game_frame`, then the functions it calls
6. [move_ghosts.py](src/GameEngine/move_ghosts.py): the AI
7. [move.py](src/rendering/move.py): sliding and collision math
8. [maze_render.py](src/rendering/maze_render.py): the drawing

**Good practice:** change one constant at a time and watch the result. Try `GHOST_MOVE_DELAY = 200`, `SUPER_POWER_MS = 2000`, or a single 10x10 level in the config. Being able to predict what a change does is the best proof that you understand the project.
