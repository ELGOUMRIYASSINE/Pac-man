# Explanation: From Game Engine to Pixels

This document explains how the game engine (`src/GameEngine/`) connects to the
rendering (`src/rendering/`). It covers:

- how a maze cell becomes a pixel position,
- how the player and the ghosts move between cells **smoothly** instead of jumping,
- how the player (200 ms per step) and the ghosts (400 ms per step) can run at
  different speeds without any conflict,
- why eating and collisions are decided on pixels, not on cells.

---

## 1. The big idea: two worlds

The game lives in **two worlds at the same time**:

| World | Where | Type of position | Example | Changes |
|---|---|---|---|---|
| **Logic** (the engine) | `Player`, `Ghost`, `Cell` | integers `(row, col)` | `(2, 3)` | instantly, one cell at a time |
| **Screen** (the rendering) | `Mover` in [move.py](src/rendering/move.py) | floats `(x, y)` in pixels | `(213.25, 160.0)` | a little bit every frame |

The engine only knows "the player **is** on cell (2, 3)". It never talks about
pixels. The renderer reads that cell, converts it to a pixel target, and
**slides** the sprite towards it over time.

```
   ENGINE (logic)                         RENDERING (pixels)
   ---------------                        ------------------
   player.position = (2, 3)  ──read──▶   _center(2, 3) = (213.25, 160.0)  ← target
   ghost.position  = (5, 1)  ──read──▶   _center(5, 1) = ( 94.25, 298.0)  ← target
                                                │
                                                ▼
                                       Mover slides the sprite from where
                                       it is now to the target, a little
                                       every frame
                                                │
                                                ▼
                                       screen.blit(image, center=pos)
```

The engine **jumps** from cell to cell. The screen **never** jumps: it follows.

---

## 2. One frame of the game loop

Everything happens in `GameLoop.game_frame()` in
[Game_loop.py:244-290](src/GameEngine/Game_loop.py#L244-L290), then
`MazeRender.draw()` is called, and `clock.tick(60)` keeps the loop at
**60 frames per second** (about one frame every 16.7 ms).

The order of every frame:

```
1) LOGIC   step_player()      -> maybe move the player one cell   (every 200 ms)
           end_expired_power()
           step_ghosts()      -> maybe move each ghost one cell   (every 400 ms)
           sync_ghost_cells() -> write ghosts into the maze cells

2) PIXELS  maze_render.update_entities(now)
                              -> every sprite slides towards its cell

3) RESULTS eat_when_arrived() -> eat the gum when the sprite is half way
           check_collision()  -> touch a ghost? decided with pixels

4) DRAW    maze_render.draw() -> walls, gums, player, ghosts, score
           pygame.display.flip()
```

The logic runs first and decides **where** everyone should be. The pixels
then catch up. The results (eating, dying) are decided on **what the player
really sees on the screen**.

---

## 3. How a cell becomes pixels

### 3.1 The size of one cell

In [maze_render.py:133-140](src/rendering/maze_render.py#L133-L140):

```python
available_width  = screen_width  - padding                # 1200 - 10      = 1190
available_height = screen_height - padding - hud_height   # 740 - 10 - 40  = 690

cell_width  = available_width  / cols
cell_height = available_height / rows
```

The 40 px `hud_height` is the band at the top for the score and the lives,
so the maze never goes under the text.

**Example** with a maze of 20 columns × 15 rows:

```
cell_width  = 1190 / 20 = 59.5 px
cell_height =  690 / 15 = 46.0 px
```

The cells are not square. This is why the code keeps them as floats and
never rounds too early.

### 3.2 The center of a cell (where sprites go)

In [maze_render.py:142-145](src/rendering/maze_render.py#L142-L145):

```python
def _center(self, row, col):
    top = self.radius + self.hud_height          # 5 + 40 = 45
    return ((col + 0.5) * self.cell_width  + self.radius,
            (row + 0.5) * self.cell_height + top)
```

- `col + 0.5` means "half a cell after the left edge", so the **middle** of the cell.
- `radius` (5 px = half the wall thickness) moves everything a bit so the
  first wall is not cut by the screen edge.
- `hud_height` pushes the whole maze down under the score.

**Example**: the cell `(row=2, col=3)` with the sizes above:

```
x = (3 + 0.5) * 59.5 + 5       = 213.25
y = (2 + 0.5) * 46.0 + 5 + 40  = 160.0
```

### 3.3 The corners of a cell (where walls go)

Walls are drawn on the **grid lines**, not on the centers, with
`_grid_point(col, row)` in [maze_render.py:42-46](src/rendering/maze_render.py#L42-L46).
It is the same formula without the `+ 0.5`. So a wall is always exactly half
a cell away from a sprite center: sprites never overlap walls.

The walls never change during a level, so they are drawn **once** into a
cached surface (`_wall_layer`) and just copied every frame. That keeps the
game fast enough to really run at 60 FPS, which matters for smoothness.

### 3.4 The size of a sprite

In [maze_render.py:149](src/rendering/maze_render.py#L149):

```python
size = int(min(cell_width, cell_height) * 0.8)    # int(46 * 0.8) = 36 px
```

A sprite is 80 % of the smallest side of a cell, so it fits in the corridor.
Images are loaded and scaled **once**, and the player is pre-rotated for the
4 directions, because loading or rotating images every frame is slow.

---

## 4. The `Mover`: how a sprite slides

Every entity on the screen has its own `Mover`
([move.py:5-39](src/rendering/move.py#L5-L39)): one for the player, one per ghost.

A `Mover` remembers:

| Field | Meaning |
|---|---|
| `start` | pixel position when the current step began |
| `target` | pixel center of the cell the engine chose |
| `t0` | the time (ms) when the current step began |
| `duration` | how long one step lasts: **200** for the player, **400** for a ghost |
| `pos` | the pixel position right now (what is drawn) |
| `previous` | `pos` on the last frame (used for collisions) |

### 4.1 Progress: from 0.0 to 1.0

```python
def progress(self, now):
    return max(0.0, min(1.0, (now - self.t0) / self.duration))
```

- `0.0` = the sprite just left its old cell
- `0.5` = it is exactly between the two cells
- `1.0` = it has arrived (and it stays at 1.0, it never goes past the target)

### 4.2 Linear interpolation (lerp)

```python
def update(self, now):
    self.previous = self.pos
    self.pos = self.start.lerp(self.target, self.progress(now))
```

`lerp` means: `pos = start + (target - start) * progress`.

**Example**: the player goes from cell `(2, 3)` to cell `(2, 4)` (one step right).

```
start  = (213.25, 160.0)
target = (272.75, 160.0)        # 59.5 px to the right
duration = 200 ms
```

At 60 FPS there are about 12 frames during those 200 ms:

```
time after t0   progress   x position
    0 ms          0.00      213.25
   17 ms          0.08      218.3
   33 ms          0.17      223.1
   50 ms          0.25      228.1
  100 ms          0.50      243.0    <- half way: the gum is eaten here
  150 ms          0.75      257.9
  200 ms          1.00      272.75   <- arrived
```

Each frame the sprite moves about 5 px, which is too small for the eye to see
as a jump, so the movement looks smooth.

### 4.3 Getting a new target

```python
def set_target(self, new_target, now):
    new_target = Vector2(new_target)
    if new_target == self.target:
        return                      # same cell: keep sliding, do nothing
    self.start = Vector2(self.pos)  # start from where the sprite IS NOW
    self.target = new_target
    self.t0 = now
```

`update_entities()` calls `set_target()` **every frame** for everyone, but it
only restarts the slide when the engine has really moved the entity to a new
cell. Two important details:

1. **`start = pos`, not the old cell**: the new slide always begins at the
   exact pixel where the sprite is drawn now. Even if a step started before the
   previous one was finished, the sprite would never teleport.
2. **`t0 = now`**: the clock of this step starts the moment the engine
   decides the move.

### 4.4 `snap`: the only allowed jump

After a death, or when an eaten ghost respawns, sliding would make the sprite
travel **through walls** to its spawn. So `snap()` teleports it directly:
`start = target = pos = spawn`. This is the only time a sprite jumps, and it
is on purpose.

---

## 5. Why 200 ms and 400 ms work together without conflict

This is the most important part.

### 5.1 Every entity has its own timer

In the engine:

```python
MOVE_DELAY = 200          # player
GHOST_MOVE_DELAY = 400    # ghosts

self.last_move           # one timer for the player
self.last_ghost_moves    # one timer PER ghost: [t, t, t, t]
```

`step_player()` only moves the player if 200 ms have passed since **its own**
last move. `step_ghosts()` checks each ghost against **its own** timer. They
never wait for each other and they never share a counter.

### 5.2 Every sprite has its own duration

The renderer gets the same numbers:

```python
MazeRender(self.maze, self.screen, self.MOVE_DELAY, self.GHOST_MOVE_DELAY)
...
self.player_mover = Mover(..., self.player_step_ms)     # 200
self.ghosts = {id: Mover(..., self.ghost_step_ms)}      # 400 each
```

**The slide duration is equal to the step delay.** This is the key rule:

```
player:  |---- slide 200 ms ----|---- slide 200 ms ----|---- slide 200 ms ----|
         step                   step                   step                   step
ghost:   |------------- slide 400 ms --------------|------------- slide 400 ms ...
         step                                      step
```

- The player sprite **arrives** at its cell exactly when the engine is
  allowed to make the next step, so the next slide starts right away.
  There is no pause and no jump: one continuous movement, cell after cell.
- A ghost takes twice as long to cross one cell, so it simply moves at
  **half the speed** of the player, also continuously.

What would happen with other values:

| Slide duration vs step delay | Result |
|---|---|
| duration **<** delay | the sprite arrives early and **waits** → stop-and-go movement |
| duration **=** delay | perfect continuous movement ✅ (what the game does) |
| duration **>** delay | the next target comes before arrival → the sprite falls behind the logic |

### 5.3 One clock for everybody

All the timers read the same clock: `pygame.time.get_ticks()` (milliseconds
since the game started). `now` is read **once** per frame and passed to every
function. So in one frame:

- the player can be at progress 0.75 of its step,
- ghost 0 at progress 0.30 of its step,
- ghost 2 at progress 0.90 of its step,

and there is no conflict, because each position is just a formula of the time:

```
pos = lerp(start, target, (now - t0) / duration)
```

Nobody "pushes" anybody, nobody waits for a turn. Each sprite computes its own
position from the shared clock. That is why the 200 and the 400 can never
fight each other.

### 5.4 The FPS does not change the speed

If the computer is slow and a frame takes 33 ms instead of 16 ms, the sprite
does not move slower: progress is based on **real time** (`now - t0`), not on
the number of frames. A slow frame only means a slightly bigger step on that
frame. The player still crosses one cell in 200 ms and a ghost in 400 ms.

---

## 6. Deciding results on pixels, not on cells

Because the engine changes the cell **instantly** but the sprite needs 200 ms
to arrive, using the cells for eating or dying would look wrong.

### 6.1 Eating gums at half way

`move_player()` only changes the position. It does **not** eat. Eating is done
in `eat_when_arrived()` ([Game_loop.py:226-236](src/GameEngine/Game_loop.py#L226-L236)):

```python
progress = self.maze_render.player_mover.progress(now)
if progress < self.EAT_AT_PROGRESS:      # 0.5
    return
self.moving.eat_cell(...)
```

The gum disappears when Pac-Man's mouth reaches it on the screen (half way),
not 200 ms too early when the step only started.

### 6.2 Collisions with ghosts

Checking `player.position == ghost.position` has two problems:

1. **Too early death**: the cell changes the instant a step starts, so you
   would die before the sprites touch.
2. **Passing through**: if the player goes from A to B while a ghost goes
   from B to A, they swap cells and are **never** on the same cell. They would
   cross each other with no collision.

So `check_collision()` ([Game_loop.py:125-153](src/GameEngine/Game_loop.py#L125-L153))
measures the **pixel distance** between the sprites:

```python
limit = min(cell_width, cell_height) * COLLISION_RATIO   # 46 * 0.5 = 23 px
distance = closest_distance(player_mover.previous, player_mover.pos,
                            ghost_mover.previous,  ghost_mover.pos)
if distance < limit: ...   # touched
```

`closest_distance()` ([move.py:42-53](src/rendering/move.py#L42-L53)) does not
only compare the end positions of the frame. It looks at the **whole movement
during the frame** (from `previous` to `pos` for both sprites) and finds the
moment they were the closest. Even if a slow frame makes both sprites move a
lot, they cannot jump over each other.

Why `COLLISION_RATIO = 0.5`: sprites are 0.8 cell wide, so at 0.5 cell they
visibly overlap. It must stay below 1.0, because two sprites separated by a
wall are always 1 full cell apart, and they must not "kill" through the wall.

---

## 7. Other small things that help smoothness

- **Rounding only at the end**: positions stay floats in the `Mover`. They
  are rounded with `round(pos.x), round(pos.y)` only when drawing
  ([maze_render.py:229-241](src/rendering/maze_render.py#L229-L241)). Rounding
  earlier would add small errors every frame.
- **Drawing by the center**: `image.get_rect(center=...)` puts the middle of
  the sprite on the position, so the sprite is centered in the corridor
  whatever its size.
- **Animation is independent**: the mouth of Pac-Man opens and closes every
  150 ms (`anim_delay`) with its own timer. It is not linked to the movement,
  so it never makes the movement stutter.
- **Rotation follows `facing`**: `player.facing` is the last real move, so
  the sprite turns at the same moment as the new slide starts.
- **Input buffer**: the last key pressed is kept in `next_direction` and used
  as soon as the turn is possible (no wall). You can press the key a bit early
  before a corner and the turn still happens.
- **Start already arrived**: a new `Mover` sets `t0 = now - duration`, so its
  progress is already 1.0. A sprite never slides at the start of a level.

---

## 8. Summary

```
ENGINE  decides the cell          (integers, instant, on its own timer)
   │        player: every 200 ms        ghosts: every 400 ms each
   ▼
_center(row, col)                 (cell -> pixel center of the cell)
   │
   ▼
Mover.set_target()                (new slide only if the cell changed,
   │                               starting from the current pixel)
   ▼
Mover.update(now)                 pos = lerp(start, target, (now - t0) / duration)
   │                               duration = step delay -> continuous movement
   ▼
eat at progress 0.5, collide on pixel distance
   │
   ▼
blit at round(pos)                (drawn 60 times per second)
```

- The engine works with **cells** and moves in **jumps**.
- The renderer works with **pixels** and moves **a little every frame**.
- Each entity has **its own timer** and **its own Mover**, all reading
  **one shared clock**, so different speeds never conflict.
- The slide duration is **equal** to the step delay, so a sprite arrives at
  its cell exactly when the next step begins: no pause, no jump.
