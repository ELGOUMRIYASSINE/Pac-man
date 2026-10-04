from .player import Player, MovePlayer
import pygame
from ..rendering.entry_page.entry import EntryFace
from ..rendering.maze_render import MazeRender
from .move_ghosts import Ghost, MoveGhost
from ..Maze.Maze import Maze
from ..rendering.main_menu import MainMenu

import sys


class GameLoop:
    MOVE_DELAY = 200  # ms between player steps

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pacman")
        self.screen = pygame.display.set_mode((1200, 740))
        self.entry_page = EntryFace(self.screen, 700, 1200)
        self.clock = pygame.time.Clock()
        self.ghosts  =[Ghost(id=x) for x in range(4)]
        self.running = True
        self.screen_state = "MENU"
        self.menu = MainMenu(self.screen)
        self.moving = MovePlayer()
        self.direction = None
        self.last_move = 0

    def key_to_move(self, event):
        if event.type != pygame.KEYDOWN:
            return None
        return {
            pygame.K_UP: "UP", pygame.K_w: "UP",
            pygame.K_DOWN: "DOWN", pygame.K_s: "DOWN",
            pygame.K_LEFT: "LEFT", pygame.K_a: "LEFT",
            pygame.K_RIGHT: "RIGHT", pygame.K_d: "RIGHT",
        }.get(event.key)
    def start_game(self, data):
        self.level = 0
        self.player = None
        self.load_level(data)
        self.screen_state = "GAME"

    def load_level(self, data):
        self.player_pos = (data.get_height(self.level) // 2,
                           data.get_width(self.level) // 2)
        self.maze, req_score, self.ghosts = Maze.creat_cells(self.level, data, self.player_pos, self.ghosts)
        self.maze_render = MazeRender(self.maze, self.screen)

        if self.player is None:   # new game
            self.player = Player(positiony=self.player_pos[0],
                                 positionx=self.player_pos[1],
                                 required_score=req_score,
                                 position=self.player_pos)
        else:                     # next level: keep score/lives, reset position
            self.player.position = self.player_pos
            self.player.positiony, self.player.positionx = self.player_pos
        self.direction = None
        self.ghosts = [Ghost(id=x) for x in range(4)]
    def menu_frame(self, events, data, mouse):
        for event in events:
            action = self.menu.handle_event(event, mouse)   # "PLAY" / "EXIT" / None
            if action == "PLAY":
                # print("cc")
                self.start_game(data)
                return
            if action == "EXIT":
                # print("cc")
                self.running = False
                return
        self.menu.draw(mouse)
    def game_frame(self, events, data):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.screen_state = "MENU"
                return
            move = self.key_to_move(event)
            if move:
                self.direction = move

        # update (throttled so speed doesn't depend on FPS)
        now = pygame.time.get_ticks()
        if self.direction and now - self.last_move >= self.MOVE_DELAY:
            self.moving.move_player(self.direction, self.player, data, self.maze)
            self.last_move = now

        result = self.moving.check_level(self.player, data)
        if result == "END":      
            #print("END")
            #exit()# win
            self.screen_state = "MENU"
        elif result == "NEXT":
            self.level = self.player.level
            self.load_level(data)
        elif result == "RESPOWN":
            self.player.lives -= 1
            self.player.position = self.player_pos
            self.player.positiony, self.player.positionx = self.player_pos
            self.direction = None
            self.player.dead = False
            _, _, self.ghosts = Maze.creat_cells(self.level, data, self.player_pos, self.ghosts)
        elif result == "LOSE":
            #print("lose")
            #exit()
            self.player.dead = True
            self.screen_state = "MENU"
        MoveGhost().move_ghost_dfs(
        self.ghosts[0].position,
        self.maze,
        (data.get_height(self.level), data.get_width(self.level)), self.ghosts[0],
        self.player.position, None
    )
        if self.ghosts[0].neighboars and len(self.ghosts[0].neighboars)>=0:
            self.maze[self.ghosts[0].position[0]][self.ghosts[0].position[1]].has_ghost = False
            self.ghosts[0].position = self.ghosts[0].neighboars[1]
            self.maze[self.ghosts[0].position[0]][self.ghosts[0].position[1]].has_ghost = True
        # if ghosts[1].neighboars and len(ghosts[1].neighboars)>0:
        #     maze[ghosts[1].position[0]][ghosts[1].position[1]].has_ghost = False
        #     ghosts[1].position = ghosts[1].neighboars[1]
        #     maze[ghosts[1].position[0]][ghosts[1].position[1]].has_ghost = True
        # if ghosts[2].neighboars and len(ghosts[2].neighboars)>0:
        #     maze[ghosts[2].position[0]][ghosts[2].position[1]].has_ghost = False
        #     ghosts[2].position = ghosts[2].neighboars[1]
        #     maze[ghosts[2].position[0]][ghosts[2].position[1]].has_ghost = True
        # if ghosts[3].neighboars and len(ghosts[3].neighboars)>0:
        #     maze[ghosts[3].position[0]][ghosts[3].position[1]].has_ghost = False
        #     ghosts[3].position = ghosts[3].neighboars[1]
        #     maze[ghosts[3].position[0]][ghosts[3].position[1]].has_ghost = True
            # draw
        self.screen.fill((0, 0, 0))
        self.maze_render.draw()
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