import sys
import pygame
from .player import Player, MovePlayer, Maze
from ..rendering.maze_render import MazeRender
from ..rendering.main_menu import MainMenu


class GameLoop:
    MOVE_DELAY = 200  # ms between player steps

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pacman")
        self.screen = pygame.display.set_mode((1200, 740))
        self.clock = pygame.time.Clock()

        self.menu = MainMenu(self.screen)
        self.screen_state = "MENU"          # "MENU" or "GAME"
        self.running = True

        # game data (filled by start_game)
        self.level = 0
        self.maze = None
        self.maze_render = None
        self.player = None
        self.moving = MovePlayer()
        self.direction = None
        self.last_move = 0

    # ---------- setup ----------
    def start_game(self, data):
        self.level = 0
        self.player = None
        self.load_level(data)
        self.screen_state = "GAME"

    def load_level(self, data):
        self.player_pos = (data.get_height(self.level) // 2,
                           data.get_width(self.level) // 2)
        self.maze, req_score = Maze.creat_cells(self.level, data, self.player_pos)
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

    # ---------- input ----------
    def key_to_move(self, event):
        if event.type != pygame.KEYDOWN:
            return None
        return {
            pygame.K_UP: "UP", pygame.K_w: "UP",
            pygame.K_DOWN: "DOWN", pygame.K_s: "DOWN",
            pygame.K_LEFT: "LEFT", pygame.K_a: "LEFT",
            pygame.K_RIGHT: "RIGHT", pygame.K_d: "RIGHT",
        }.get(event.key)

    # ---------- one method per screen ----------
    def menu_frame(self, events, data, mouse):
        for event in events:
            action = self.menu.handle_event(event, mouse)   # "PLAY" / "EXIT" / None
            if action == "PLAY":
                print("cc")
                self.start_game(data)
                return
            if action == "EXIT":
                print("cc")
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

        result = self.moving.check_level(self.player)
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
        elif result == "LOSE":
            #print("lose")
            #exit()
            self.player.dead = True
            self.screen_state = "MENU"

        # draw
        self.screen.fill((0, 0, 0))
        self.maze_render.draw()

    # ---------- main loop ----------
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