"""Draw maze walls, collectibles, the player, and ghosts."""

import pygame
from .move import Mover
from ..GameEngine.gosts import Ghost
from ..GameEngine.player import Move, Player
from ..Maze.Maze import Cell


class MazeRender:
    """Render a maze and interpolate the movement of its entities."""

    def __init__(
        self,
        maze: list[list[Cell]],
        screen: pygame.Surface,
        player_step_ms: int = 200,
        ghost_step_ms: int = 400,
    ) -> None:
        """Prepare maze geometry, sprites, and entity animation state."""
        self.maze = maze
        self.screen = screen
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.screen_width, self.screen_height = self.screen.get_size()
        self.wall_thinckness = 10
        self.radius = self.wall_thinckness / 2
        self.wall_color = (0, 0, 205)
        self.padding = 10
        self.hud_height = 40  # band above the maze, so the HUD hides nothing
        self.dot_color = (255, 184, 174)  # classic pale pink pac-dot color
        self.player_images = ["1.png", "2.png"]
        self.anim_delay = 150
        self.state_counter = 0
        self.last_anim_time = pygame.time.get_ticks()
        self.cell_width, self.cell_height = self.cell_sizes()
        self.player_step_ms = player_step_ms
        self.ghost_step_ms = ghost_step_ms
        # the game data this renderer draws (see bind_entities)
        self.player: Player | None = None
        self.ghost_list: list[Ghost] = []
        # the sprites on screen: one Mover per entity
        self.player_mover: Mover | None = None
        self.ghosts: dict[int, Mover] = {}
        # --- maze design (only used by the wall drawing below) ---
        self.wall_inner_color = (4, 4, 40)
        self.wall_glow_color = (0, 40, 255, 60)
        self._wall_layer: pygame.Surface | None = None
        self._wall_key: tuple[object, ...] | None = None
        self.player_frames: dict[Move | None, list[pygame.Surface]] = {}
        self.score_font = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", 20
        )
        self._build_sprites()

    def _grid_point(self, col: int, row: int) -> tuple[float, float]:
        """Return the pixel position of a grid intersection."""
        top = self.radius + self.hud_height
        return (
            int(col * self.cell_width) + self.radius,
            int(row * self.cell_height) + top,
        )

    def _wall_segments(
        self,
    ) -> set[tuple[tuple[int, int], tuple[int, int]]]:
        """Return each wall segment once, including shared cell boundaries."""
        segments = set()
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.maze[row][col]
                if cell.North:
                    segments.add(((col, row), (col + 1, row)))
                if cell.Est:
                    segments.add(((col + 1, row), (col + 1, row + 1)))
                if cell.South:
                    segments.add(((col, row + 1), (col + 1, row + 1)))
                if cell.West:
                    segments.add(((col, row), (col, row + 1)))
        return segments

    def _wall_signature(self) -> tuple[object, ...]:
        """Return a cache key for the current screen and maze geometry."""
        walls = tuple(
            (c.North, c.Est, c.South, c.West)
            for line in self.maze
            for c in line
        )
        return (
            self.screen.get_size(),
            self.cell_width,
            self.cell_height,
            self.wall_thinckness,
            self.wall_color,
            walls,
        )

    def _build_wall_layer(self) -> None:
        """Render the maze walls into a cached transparent surface."""
        width, height = self.screen.get_size()
        t = self.wall_thinckness
        inner_t = max(1, t - 6)  # leaves a ~3px colored outline

        lines = [
            (self._grid_point(*a), self._grid_point(*b))
            for a, b in self._wall_segments()
        ]
        joints = {p for line in lines for p in line}

        # 1) glow: fat translucent lines, blurred by scaling down then up
        glow = pygame.Surface((width, height), pygame.SRCALPHA)
        for start, end in lines:
            pygame.draw.line(glow, self.wall_glow_color, start, end, t * 3)
        for p in joints:
            pygame.draw.circle(glow, self.wall_glow_color, p, int(t * 1.5))
        small_size = (max(1, width // 4), max(1, height // 4))
        small = pygame.transform.smoothscale(glow, small_size)
        glow = pygame.transform.smoothscale(small, (width, height))

        layer = pygame.Surface((width, height), pygame.SRCALPHA)
        layer.blit(glow, (0, 0))

        # 2) outer wall body, round caps have the same radius as the line
        for start, end in lines:
            pygame.draw.line(layer, self.wall_color, start, end, t)
        for p in joints:
            pygame.draw.circle(layer, self.wall_color, p, t // 2)

        # 3) dark inner core -> hollow tube; drawn after ALL outer lines so
        #    junctions and corners merge cleanly
        for start, end in lines:
            pygame.draw.line(layer, self.wall_inner_color, start, end, inner_t)
        for p in joints:
            pygame.draw.circle(
                layer, self.wall_inner_color, p, max(1, inner_t // 2)
            )

        self._wall_layer = layer
        self._wall_key = self._wall_signature()

    def draw_score(self) -> None:
        """Draw the player's score and remaining lives."""
        assert self.player is not None
        score = f"Score: {self.player.score}"
        lives = f"Lives: {self.player.lives}"
        score_text = self.score_font.render(score, True, (255, 255, 0))
        lives_text = self.score_font.render(lives, True, (255, 255, 0))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(
            lives_text, (self.screen_width - lives_text.get_width() - 10, 10)
        )

    def draw(self) -> None:
        """Draw the cached walls, maze contents, and score display."""
        self.screen.fill((0, 0, 0))

        if self._wall_key != self._wall_signature():
            self._build_wall_layer()
        assert self._wall_layer is not None
        self.screen.blit(self._wall_layer, (0, 0))

        self.draw_content()
        self.draw_score()

    def cell_sizes(self) -> tuple[float, float]:
        """Return the width and height of a maze cell in pixels."""
        padding = 10
        available_width = self.screen_width - padding
        available_height = self.screen_height - padding - self.hud_height

        cell_width = available_width / self.cols
        cell_height = available_height / self.rows
        return cell_width, cell_height

    def _center(self, row: int, col: int) -> tuple[float, float]:
        """Return the pixel center of the cell at ``row`` and ``col``."""
        top = self.radius + self.hud_height
        return (
            (col + 0.5) * self.cell_width + self.radius,
            (row + 0.5) * self.cell_height + top,
        )

    def _build_sprites(self) -> None:
        """Load and prepare sprite images once for use during rendering."""
        size = int(min(self.cell_width, self.cell_height) * 0.8)
        frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/{img}").convert_alpha(),
                (size, size),
            )
            for img in self.player_images
        ]
        angles: dict[Move | None, int] = {
            None: 0,
            "UP": 270,
            "DOWN": 90,
            "LEFT": 0,
            "RIGHT": 180,
        }
        self.player_frames = {
            move: [pygame.transform.rotate(frame, angle) for frame in frames]
            for move, angle in angles.items()
        }
        self.ghost = pygame.transform.scale(
            pygame.image.load("assets/ghost.webp").convert_alpha(),
            (size, size),
        )
        # blue version: the player must see which ghosts can be eaten
        self.weak_ghost = self.ghost.copy()
        for x in range(size):
            for y in range(size):
                r, g, b, a = self.weak_ghost.get_at((x, y))
                self.weak_ghost.set_at((x, y), (b, g, r, a))  # swap red/blue

    def bind_entities(self, player: Player, ghosts: list[Ghost]) -> None:
        """Bind player and ghost state and place their sprites on the grid."""
        self.player = player
        self.ghost_list = ghosts
        self.player_mover = Mover(
            self._center(*player.position), self.player_step_ms
        )
        self.ghosts = {
            ghost.id: Mover(self._center(*ghost.position), self.ghost_step_ms)
            for ghost in ghosts
        }

    def snap_ghost(self, ghost: Ghost, now: int) -> None:
        """Place one ghost instantly at its logical position."""
        self.ghosts[ghost.id].snap(self._center(*ghost.position), now)

    def snap_all(self, now: int) -> None:
        """Place the player and ghosts at their logical positions."""
        assert self.player is not None
        assert self.player_mover is not None
        self.player_mover.snap(self._center(*self.player.position), now)
        for ghost in self.ghost_list:
            self.snap_ghost(ghost, now)

    def update_entities(self, now: int) -> None:
        """Move every sprite towards its logical cell. Call once per frame.

        Reads ghost.position directly: a cell has room for one ghost_id only,
        so two ghosts on the same cell would lose one of them.
        """
        assert self.player is not None
        assert self.player_mover is not None
        self.player_mover.set_target(self._center(*self.player.position), now)
        self.player_mover.update(now)
        for ghost in self.ghost_list:
            if ghost.eaten:
                continue
            mover = self.ghosts[ghost.id]
            mover.set_target(self._center(*ghost.position), now)
            mover.update(now)

    def draw_content(self) -> None:
        """Draw collectibles and animate the player and ghost sprites."""
        assert self.player is not None
        assert self.player_mover is not None
        now = pygame.time.get_ticks()

        if now - self.last_anim_time >= self.anim_delay:
            frame_count = len(self.player_images)
            self.state_counter = (self.state_counter + 1) % frame_count
            self.last_anim_time = now

        size = min(self.cell_width, self.cell_height)
        big_dot = max(2, int(size * 0.12))
        small_dot = max(2, int(size * 0.05))
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.maze[row][col]
                if cell.supgum:
                    pygame.draw.circle(
                        self.screen, self.dot_color,
                        self._center(row, col), big_dot,
                    )
                elif cell.gum:
                    pygame.draw.circle(
                        self.screen, self.dot_color,
                        self._center(row, col), small_dot,
                    )

        image = self.player_frames[self.player.facing][self.state_counter]
        pos = self.player_mover.pos
        self.screen.blit(
            image, image.get_rect(center=(round(pos.x), round(pos.y)))
        )

        for ghost in self.ghost_list:
            if ghost.eaten:
                continue
            image = self.weak_ghost if ghost.weak else self.ghost
            pos = self.ghosts[ghost.id].pos
            self.screen.blit(
                image, image.get_rect(center=(round(pos.x), round(pos.y)))
            )
