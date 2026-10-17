from .player import Player, MovePlayer
import pygame
from ..rendering.entry_page.entry import EntryFace
from ..rendering.maze_render import MazeRender
from .move_ghosts import Ghost, MoveGhost
from ..Maze.Maze import Maze
from ..rendering.main_menu import MainMenu
from ..rendering.instructions import Instructions

from typing import Any
from collections import deque
import sys


class GameLoop:
    MOVE_DELAY = 200  # ms between player steps
    GHOST_MOVE_DELAY = 400

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
        self.direction = None
        self.last_move = 0
        self.last_ghost_moves = [0 for _ in self.ghosts]
        self.move = None
        self.maze = None

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
        # there is problem here, player take place inside 42 in some cases
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
                position=self.player_pos
            )
        else:  # next level: keep score/lives, reset position
            self.player.position = self.player_pos
            self.player.required_score = req_score + self.player.score
            self.player.positiony, self.player.positionx = self.player_pos
        self.direction = None

    def menu_frame(self, events, data, mouse):
        print("entering menu frame")
        for event in events:
            action = self.menu.handle_event(
                event, mouse
            )  # "PLAY" / "EXIT" / None
            if action == "PLAY":
                print("PLAY")
                self.start_game(data)
                return
            if action == "EXIT":
                print("EXITING GAME")
                self.running = False
                return
            if action == "HIGHSCORES":
                print("HIGHSCORES")
                # self.screen_state = "HIGHSCORES"
                return
            if action == "INSTRUCTIONS":
                print("INST")
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

    def check_collision(self):
            if self.player is None or getattr(self, 'maze_render', None) is None:
                return
                
            # Try to get visual positions. If not initialized yet, wait for next frame.
            player_mover = self.maze_render.player_mover
            if player_mover is None:
                return
                
            # Determine a collision threshold (e.g., within 50% of a cell's size)
            collision_threshold = min(self.maze_render.cell_width, self.maze_render.cell_height) * 0.5
            
            for ghost in self.ghosts:
                if ghost.eaten or ghost.position != self.player.position:
                    continue
                    
                ghost_mover = self.maze_render.ghosts.get(ghost.id)
                if ghost_mover is None:
                    continue

                # Calculate pixel distance between player and ghost
                distance = player_mover.pos.distance_to(ghost_mover.pos)

                # Trigger collision only if visually close enough
                if distance < collision_threshold:
                    if self.player.super_power and ghost.weak:
                        self.player.edible_score += 200
                        ghost.eaten = True
                        ghost.respawn_at = pygame.time.get_ticks() + 4000
                        self.maze[ghost.position[0]][ghost.position[1]].edible_ghost = False
                    elif not ghost.weak and not self.player.super_power:
                        self.player.dead = True
                        player_row, player_col = self.player.position
                        self.maze[player_row][player_col].has_player = False

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
        now = pygame.time.get_ticks()
        if self.direction and now - self.last_move >= self.MOVE_DELAY:
            self.moving.move_player(self.direction, player, data, self.maze)
            had_super_power = player.super_power
            if now >= player.super_until:
                player.super_power = False
                for ghost in self.ghosts:
                    ghost.weak = False
                    ghost.eaten = False
            elif had_super_power:
                for ghost in self.ghosts:
                    ghost.weak = True
            self.last_move = now
        self.check_collision()
        result = self.moving.check_level(player, data)
        # now = pygame.time.get_ticks()
        if result == "END":
            player.score += player.edible_score
            player.edible_score = 0
            # exit()# win
            self.screen_state = "MENU"
        elif result == "NEXT":
            self.level = player.level
            self.load_level(data)
            player.super_power = False
            player.super_until = 0
            # player.score += player.edible_score
            # player.edible_score = 0
        elif result == "RESPOWN":
            player.lives -= 1
            player.position = self.player_pos
            player.positiony, player.positionx = self.player_pos
            self.direction = None
            player.dead = False
            self.maze[self.player_pos[0]][self.player_pos[1]].has_player = True
            _, _, self.ghosts, _= Maze.creat_cells(
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
            # update (throttled so speed doesn't depend on FPS)
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

            MoveGhost().move_ghost_bfs(
                ghost.position,
                self.maze,
                maze_size,
                ghost,
                player.position
            )
            if len(ghost.neighboars) > 1 and not player.super_power:
                if ghost.id % 2 == 0:
                    self.maze[ghost.position[0]][
                        ghost.position[1]
                    ].has_ghost = False
                    ghost.position = ghost.neighboars[1]
                    self.maze[ghost.position[0]][
                        ghost.position[1]
                    ].has_ghost = True
                    self.maze[ghost.position[0]][
                                                        ghost.position[1]
                                                    ].ghost_id = ghost.id
                    self.last_ghost_moves[index] = now
                else:
                    moves = MoveGhost()._get_neighboars(ghost.position, self.maze, maze_size)
                    self.maze[ghost.position[0]][
                                                        ghost.position[1]
                                                    ].has_ghost = False
                    ghost.position = min(moves, key=lambda x:abs(x[0] - player.position[0]) + abs(x[1] - player.position[1]))
                    self.maze[ghost.position[0]][
                        ghost.position[1]
                    ].has_ghost = True
                    self.maze[ghost.position[0]][
                                                    ghost.position[1]
                                                ].ghost_id = ghost.id
                    self.last_ghost_moves[index] = now
            elif  len(ghost.neighboars) > 1 and player.super_power:
                moves = MoveGhost()._get_neighboars(ghost.position, self.maze, maze_size)
                self.maze[ghost.position[0]][
                                                    ghost.position[1]
                                                ].has_ghost = False
                ghost.position = max(moves, key=lambda x:abs(x[0] - player.position[0]) + abs(x[1] - player.position[1]))
                self.maze[ghost.position[0]][
                    ghost.position[1]
                ].has_ghost = True
                self.maze[ghost.position[0]][
                                                ghost.position[1]
                                            ].ghost_id = ghost.id
                self.last_ghost_moves[index] = now

            self.check_collision()
        self.sync_ghost_cells()
        # draw
        self.screen.fill((0, 0, 0))
        # if not move:
        self.maze_render.draw(self.move, self.player)

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
                # print("menu")
                self.menu_frame(events, data, mouse)
            elif self.screen_state == "GAME":
                # print("game")
                # exit()
                self.game_frame(events, data)            
                self.screen.fill((0, 0, 0))
                self.maze_render.draw(self.move, self.player)
            elif self.screen_state == "INSTRUCTIONS":
                print("instructions")
                # exit()
                self.instructions_frame(events, data)
            if self.maze and self.screen_state == "GAME":
                self.screen.fill((0, 0, 0))
                self.maze_render.draw(self.move, self.player)
                # print(self.player.score)
                # print(self.player.lives)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
