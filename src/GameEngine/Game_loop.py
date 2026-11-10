from .player import Player, MovePlayer
import pygame
from ..rendering.entry_page.entry import EntryFace
from ..rendering.maze_render import MazeRender
from ..rendering.move import closest_distance
from .move_ghosts import Ghost, MoveGhost
from ..Maze.Maze import Maze
from ..rendering.main_menu import MainMenu
from ..rendering.instructions import Instructions

import sys


class GameLoop:
    MOVE_DELAY = 200  # ms between player steps
    GHOST_MOVE_DELAY = 400
    GHOST_RESPAWN_MS = 4000
    DEATH_PAUSE_MS = 800  # freeze after a death: the player sees what happened
    # Sprites are 0.8 cell wide, so they visibly overlap at 0.5 cell. It must
    # stay below 1.0: sprites separated by a wall are always 1 cell apart.
    COLLISION_RATIO = 0.5
    EAT_AT_PROGRESS = 0.5  # gums are eaten when the sprite is half way there
    GHOST_SAFE_CELLS = 2   # no respawn this close to the player

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pac man")
        self.screen = pygame.display.set_mode((1200, 740))
        self.entry_page = EntryFace(self.screen, 700, 1200)
        self.clock = pygame.time.Clock()
        self.ghosts = [Ghost(id=x) for x in range(4)]
        self.running = True
        self.screen_state = "MENU"
        self.menu = MainMenu(self.screen)
        self.instructions = Instructions(self.screen)
        self.moving = MovePlayer()
        self.ghost_ai = MoveGhost()
        self.direction = None        # the way the player is going
        self.next_direction = None   # last key, applied as soon as it is free
        self.last_move = 0
        self.last_ghost_moves = [0 for _ in self.ghosts]
        self.maze = None
        self.maze_render = None
        self.player = None
        self.freeze_until = 0        # > 0 during the pause after a death
        self.after_freeze = None     # "RESPOWN" or "LOSE"

    def key_to_move(self, event):
        if event.type != pygame.KEYDOWN:
            return None
        return {
            pygame.K_UP: "UP",
            pygame.K_w: "UP",
            pygame.K_DOWN: "DOWN",
            pygame.K_s: "DOWN",
            pygame.K_LEFT: "LEFT",
            pygame.K_a: "LEFT",
            pygame.K_RIGHT: "RIGHT",
            pygame.K_d: "RIGHT",
        }.get(event.key)

    def start_game(self, data):
        self.level = 0
        self.player = None
        self.load_level(data)
        self.screen_state = "GAME"

    def load_level(self, data):
        wanted_pos = (
            data.get_height(self.level) // 2,
            data.get_width(self.level) // 2,
        )
        self.maze, self.ghosts, self.player_pos = Maze.creat_cells(
            self.level, data, wanted_pos, self.ghosts
        )

        if self.player is None:  # new game
            self.player = Player(lives=data.get_lives())
        player = self.player
        player.position = self.player_pos
        player.positiony, player.positionx = self.player_pos
        player.super_power = False
        player.super_until = 0
        player.facing = None

        self.direction = None
        self.next_direction = None
        self.freeze_until = 0
        self.after_freeze = None
        self.reset_ghost_movement()
        self.maze_render = MazeRender(
            self.maze, self.screen, self.MOVE_DELAY, self.GHOST_MOVE_DELAY
        )
        self.maze_render.bind_entities(player, self.ghosts)

    def menu_frame(self, events, data, mouse):
        for event in events:
            action = self.menu.handle_event(
                event, mouse
            )  # "PLAY" / "EXIT" / None
            if action == "PLAY":
                self.start_game(data)
                return
            if action == "EXIT":
                self.running = False
                return
            if action == "HIGHSCORES":
                # self.screen_state = "HIGHSCORES"
                return
            if action == "INSTRUCTIONS":
                self.screen_state = "INSTRUCTIONS"
                return
        self.menu.draw(mouse)

    def instructions_frame(self, events, data):
        for event in events:
            action = self.instructions.handle_event(
                event, pygame.mouse.get_pos()
            )
            if action == "BACK":
                self.screen_state = "MENU"
                return
        self.instructions.draw(pygame.mouse.get_pos())

    def check_collision(self, now, data):
        """Player against ghosts, decided on what is really on the screen.

        The logical cells cannot decide this: they change the instant a step
        starts (death before the sprites touch) and two entities walking
        towards each other swap cells without ever sharing one (pass through).
        """
        render = self.maze_render
        player_mover = render.player_mover
        limit = (
            min(render.cell_width, render.cell_height) * self.COLLISION_RATIO
        )
        for ghost in self.ghosts:
            if ghost.eaten:
                continue
            ghost_mover = render.ghosts[ghost.id]
            distance = closest_distance(
                player_mover.previous, player_mover.pos,
                ghost_mover.previous, ghost_mover.pos,
            )
            if distance >= limit:
                continue
            if ghost.weak:
                self.player.score += data.get_ghostpoint()
                ghost.eaten = True
                ghost.respawn_at = now + self.GHOST_RESPAWN_MS
            else:
                self.player.dead = True
                return

    def sync_ghost_cells(self):
        for row in self.maze:
            for cell in row:
                cell.has_ghost = False
                cell.ghost_id = None
        for ghost in self.ghosts:
            if ghost.eaten:
                continue
            ghost_row, ghost_col = ghost.position
            self.maze[ghost_row][ghost_col].has_ghost = True
            self.maze[ghost_row][ghost_col].ghost_id = ghost.id

    def reset_ghost_movement(self):
        now = pygame.time.get_ticks()
        self.last_ghost_moves = [now for _ in self.ghosts]

    def respawn(self, now):
        """After a death: same maze and gums, everybody back to the start."""
        player = self.player
        self.maze[player.positiony][player.positionx].has_player = False
        player.position = self.player_pos
        player.positiony, player.positionx = self.player_pos
        self.maze[player.positiony][player.positionx].has_player = True
        player.dead = False
        player.super_power = False
        player.super_until = 0
        player.facing = None
        self.direction = None
        self.next_direction = None
        for ghost in self.ghosts:
            ghost.reset()
        self.reset_ghost_movement()
        self.sync_ghost_cells()
        self.maze_render.snap_all(now)

    def step_player(self, now, data):
        if now - self.last_move < self.MOVE_DELAY:
            return
        player = self.player
        if self.next_direction and self.moving.can_move(
            self.next_direction, player, data, self.maze
        ):
            self.direction = self.next_direction
            self.next_direction = None
        if self.direction and self.moving.move_player(
            self.direction, player, data, self.maze
        ):
            self.last_move = now

    def step_ghosts(self, now, data):
        player = self.player
        maze_size = (data.get_height(self.level), data.get_width(self.level))
        for index, ghost in enumerate(self.ghosts):
            if ghost.eaten:
                gap = (abs(ghost.home[0] - player.positiony)
                       + abs(ghost.home[1] - player.positionx))
                if now < ghost.respawn_at or gap <= self.GHOST_SAFE_CELLS:
                    continue
                ghost.reset()
                self.maze_render.snap_ghost(ghost, now)
                self.last_ghost_moves[index] = now
            if now - self.last_ghost_moves[index] < self.GHOST_MOVE_DELAY:
                continue
            cell = self.ghost_ai.next_cell(
                ghost, self.maze, maze_size, player.position
            )
            if cell is not None:
                ghost.previous = ghost.position
                ghost.position = cell
                self.last_ghost_moves[index] = now

    def eat_when_arrived(self, now, data):
        """Gums disappear when the sprite reaches them, not when it leaves."""
        progress = self.maze_render.player_mover.progress(now)
        if progress < self.EAT_AT_PROGRESS:
            return
        if self.moving.eat_cell(self.player, data, self.maze, now):
            for ghost in self.ghosts:
                if not ghost.eaten:
                    ghost.weak = True
                    ghost.previous = None  # allowed to turn back and run

    def end_expired_power(self, now):
        player = self.player
        if player.super_power and now >= player.super_until:
            player.super_power = False
            for ghost in self.ghosts:
                ghost.weak = False

    def game_frame(self, events, data):
        player = self.player
        if player is None:
            return
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.screen_state = "MENU"
                return
            move = self.key_to_move(event)
            if move:
                self.next_direction = move
        now = pygame.time.get_ticks()

        if self.freeze_until:
            if now < self.freeze_until:
                return
            self.freeze_until = 0
            if self.after_freeze == "LOSE":
                self.screen_state = "MENU"
            else:
                self.respawn(now)
            return

        # 1) logic: decide the next cells
        self.step_player(now, data)
        self.end_expired_power(now)
        self.step_ghosts(now, data)
        self.sync_ghost_cells()
        
        # 2) pixels: slide the sprites towards those cells
        self.maze_render.update_entities(now)
        # 3) what the player sees decides what happens
        self.eat_when_arrived(now, data)
        self.check_collision(now, data)

        result = self.moving.check_level(player, data, self.maze)
        if result == "END":
            self.screen_state = "MENU"
        elif result == "NEXT":
            self.level = player.level
            self.load_level(data)
        elif result in ("RESPOWN", "LOSE"):
            player.lives -= 1
            self.after_freeze = result
            self.freeze_until = now + self.DEATH_PAUSE_MS

    def entry(self, data):
        while self.running:
            mouse = pygame.mouse.get_pos()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            if not self.running:
                break

            if self.screen_state == "MENU":
                self.menu_frame(events, data, mouse)
            elif self.screen_state == "GAME":
                self.game_frame(events, data)
            elif self.screen_state == "INSTRUCTIONS":
                self.instructions_frame(events, data)
            if self.maze and self.screen_state == "GAME":
                self.maze_render.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
