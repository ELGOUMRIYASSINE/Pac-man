from .player import Player, MovePlayer, Maze
import pygame
from ..rendering.entry_page.entry import EntryFace
from ..rendering.render import MazeRender
from pathlib import Path

class GameLoop:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 700))
        self.entry_page = EntryFace(self.screen, 700, 1200)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return "OUT"
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                return "UP"

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                return "DOWN"

            elif event.key in (pygame.K_LEFT, pygame.K_a):
                return "LEFT"

            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                return "RIGHT"

    def entry(self, data):

        run = True
        level = 0
        player = Player()
        pygame.display.set_caption("Pacman")
        # Load and scale the background image ONCE before the loop starts
        bg_image = pygame.image.load("assets/entry_page.bmp").convert()
        # bg_image = pygame.transform.scale(bg_image, (1200, 700))

        run = True
        clock = pygame.time.Clock()
        while run:
            pygame.time.delay(10)
            for event in pygame.event.get():
                move = self.handle_event(event)
                if move == "OUT":
                    return
                # initialisation ========================================================================
                player_pos = (data.get_height(level) // 2, data.get_width(level) // 2)
                maze, req_score = Maze.creat_cells(level, data, player_pos)
                print(maze)
                player = Player(positiony=player_pos[0], positionx=player_pos[1], required_score=req_score, position=player_pos)
                moving = MovePlayer()
                # moving========================================================================
                moving.move_player(move, player, data, maze)
                # if player.super_power:

                state = moving.check_level(player)
                if state == "END":
                    break
                    # GAME SHOULD END WITH WIN
                elif state == "NEXT":
                    level = player.level
                elif state == "RESPOWN":
                    player.lives -= 1
                    player.position = player_pos
                    player.positiony = player_pos[0]
                    player.positionx = player_pos[1]
                elif state == "LOSE":
                    player.dead = True
                    # GAME SHOULD END WITH LOSE
                    break

            # get all moves

            # game logic

            # drawing all

            # Draw the background image instead of clearing with solid black
            self.screen.fill((0, 0, 0))
            maze_draw = MazeRender(maze, self.screen)
            maze_draw.draw()
            pygame.display.flip()
            # pygame.display.update()
            clock.tick(60)

        pygame.quit()
