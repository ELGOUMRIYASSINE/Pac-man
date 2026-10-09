from .player import Player, MovePlayer
import pygame
from ..rendering.entry_page.entry import EntryFace
from ..rendering.maze_render import MazeRender
from .move_ghosts import Ghost, MoveGhost
from ..Maze.Maze import Maze
from ..rendering.main_menu import MainMenu
from typing import Any
from collections import deque

import sys


class GameLoop:
    MOVE_DELAY = 200  # ms between player steps
    GHOST_MOVE_DELAY = 900

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
        self.moving = MovePlayer()
        self.direction = None
        self.last_move = 0
        self.last_ghost_moves = [0 for _ in self.ghosts]
        self.move = None

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
        self.player_pos = (
            data.get_height(self.level) // 2,
            data.get_width(self.level) // 2,
        )
        self.maze, req_score, self.ghosts, self.player_pos = Maze.creat_cells(
            self.level, data, self.player_pos, self.ghosts
        )
        for ghost in self.ghosts:
            ghost.weak = self.player is not None and self.player.super_power
        self.reset_ghost_movement()
        self.maze_render = MazeRender(self.maze, self.screen)

        if self.player is None:  # new game
            self.player = Player(
                positiony=self.player_pos[0],
                positionx=self.player_pos[1],
                required_score=req_score,
                position=self.player_pos,
            )
        else:  # next level: keep score/lives, reset position
            self.player.position = self.player_pos
            self.player.positiony, self.player.positionx = self.player_pos
        self.direction = None

    def menu_frame(self, events, data, mouse):
        for event in events:
            action = self.menu.handle_event(
                event, mouse
            )  # "PLAY" / "EXIT" / None
            if action == "PLAY":
                # print("cc")
                self.start_game(data)
                return
            if action == "EXIT":
                # print("cc")
                self.running = False
                return
        self.menu.draw(mouse)

    def check_collision(self):
        if self.player is None:
            return
        for ghost in self.ghosts:
            if ghost.eaten or ghost.position != self.player.position:
                continue
            if self.player.super_power and ghost.weak:
                self.player.edible_score += 100
                ghost.eaten = True
                ghost.respawn_at = pygame.time.get_ticks() + 3000
            else:
                self.player.dead = True
                player_row, player_col = self.player.position
                self.maze[player_row][player_col].has_player = False
            return

    def check_edible(self, player):
        player_row, player_col = player.position
        if player.super_power:
            if (
                self.maze[player_row][player_col].has_player
                and self.maze[player_row][player_col].edible_ghost
            ):
                self.maze[player_row][player_col].edible_ghost = False

    def sync_ghost_cells(self):
        for row in self.maze:
            for cell in row:
                cell.has_ghost = False
        for ghost in self.ghosts:
            if ghost.eaten:
                continue
            ghost_row, ghost_col = ghost.position
            self.maze[ghost_row][ghost_col].has_ghost = True

    def get_flee_target(self, ghost, player_position, maze_size):
        movement = MoveGhost()
        distances = {player_position: 0}
        queue = deque([player_position])
        while queue:
            position = queue.popleft()
            for neighbor in movement._get_neighboars(
                position, self.maze, maze_size
            ):
                if neighbor not in distances:
                    distances[neighbor] = distances[position] + 1
                    queue.append(neighbor)

        options = movement._get_neighboars(
            ghost.position, self.maze, maze_size
        )
        return max(
            options,
            key=lambda position: distances.get(position, -1),
            default=ghost.position,
        )

    def reset_ghost_movement(self):
        now = pygame.time.get_ticks()
        self.last_ghost_moves = [now for _ in self.ghosts]
        for ghost in self.ghosts:
            ghost.neighboars = []

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
            self.move = self.key_to_move(event)
            if self.move:
                self.direction = self.move

        # update (throttled so speed doesn't depend on FPS)
        now = pygame.time.get_ticks()
        if self.direction and now - self.last_move >= self.MOVE_DELAY:
            had_super_power = player.super_power
            self.moving.move_player(self.direction, player, data, self.maze)
            if player.super_power and not had_super_power:
                for ghost in self.ghosts:
                    ghost.weak = True
            self.last_move = now

        self.check_collision()
        result = self.moving.check_level(player, data)
        if result == "END":
            # print("END")
            player.score += player.edible_score
            player.edible_score = 0
            # exit()# win
            self.screen_state = "MENU"
        elif result == "NEXT":
            self.level = player.level
            self.load_level(data)
            player.score += player.edible_score
            player.edible_score = 0
        elif result == "RESPOWN":
            player.lives -= 1
            player.position = self.player_pos
            player.positiony, player.positionx = self.player_pos
            self.direction = None
            player.dead = False
            self.maze[self.player_pos[0]][self.player_pos[1]].has_player = True
            _, _, self.ghosts, _ = Maze.creat_cells(
                self.level, data, self.player_pos, self.ghosts
            )
            self.reset_ghost_movement()
            self.sync_ghost_cells()
        elif result == "LOSE":
            # print("lose")
            # exit()
            player.dead = True
            player.score += player.edible_score
            player.edible_score = 0
            self.screen_state = "MENU"
        now = pygame.time.get_ticks()
        maze_size = (data.get_height(self.level), data.get_width(self.level))
        for index, ghost in enumerate(self.ghosts):
            if ghost.eaten:
                if now < ghost.respawn_at:
                    continue
                ghost.position = ghost.home
                ghost.eaten = False
                self.last_ghost_moves[index] = now
            if now - self.last_ghost_moves[index] < self.GHOST_MOVE_DELAY:
                continue

            target = player.position
            if ghost.weak:
                target = self.get_flee_target(
                    ghost, player.position, maze_size
                )

            MoveGhost().move_ghost_bfs(
                ghost.position,
                self.maze,
                maze_size,
                ghost,
                target,
            )
            if len(ghost.neighboars) > 1:
                self.maze[ghost.position[0]][
                    ghost.position[1]
                ].has_ghost = False
                ghost.position = ghost.neighboars[1]
                self.maze[ghost.position[0]][
                    ghost.position[1]
                ].has_ghost = True
                self.last_ghost_moves[index] = now
            self.check_collision()
        self.sync_ghost_cells()
        # draw
        self.screen.fill((0, 0, 0))
        # if not move:
        self.maze_render.draw(self.move)

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
                # exit()
                print("menu")
                self.menu_frame(events, data, mouse)
            elif self.screen_state == "GAME":
                print("game")
                # exit()
                self.game_frame(events, data)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
