from .player import Player, MovePlayer
import pygame
from ..rendering.entry_page.entry import EntryFace
from ..rendering.maze_render import MazeRender
from .move_ghosts import Ghost, MoveGhost
from ..Maze.Maze import Maze

import sys


class GameLoop:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 740))
        self.entry_page = EntryFace(self.screen, 700, 1200)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
        player_pos = (
            data.get_height(level) // 2 - (data.get_height(level) % 2 == 0),
            data.get_width(level) // 2 - (data.get_width(level) % 2 == 0),
        )

        ghosts = [Ghost(id=x) for x in range(4)]
        maze, req_score, ghosts = Maze.creat_cells(level, data, player_pos,ghosts)
        player = Player(
            positiony=player_pos[0],
            positionx=player_pos[1],
            required_score=req_score,
            position=player_pos
        )
        moving = MovePlayer()
        check_move = None
        while run:
            pygame.time.delay(10)
            for event in pygame.event.get():
                move = self.handle_event(event)

                if move == "OUT":
                    break
            if move is not None:
                check_move = move
            if not run:
                break
            if check_move is not None:
                moving.move_player(check_move, player, data, maze)
            state = moving.check_level(player, data)
            if state == "END":
                break
                # GAME SHOULD END WITH WIN
            elif state == "NEXT":
                # should show the page of next level and stop the current level
                level = player.level
                player_pos = (
                            data.get_height(level) // 2 - (data.get_height(level) % 2 == 0),
                            data.get_width(level) // 2 - (data.get_width(level) % 2 == 0),
                        )
                player.positiony=player_pos[0]
                player.positionx=player_pos[1]
                player.position = player_pos
                maze, req_score, ghosts = Maze.creat_cells(level, data, player_pos, ghosts)
                player.required_score = req_score + player.score
            elif state == "RESPOWN":
                # should make the player appear in the center
                player.lives -= 1
                player.dead = False
                player.position = player_pos
                player.positiony = player_pos[0]
                player.positionx = player_pos[1]
                check_move = None
                _, _, ghosts = Maze.creat_cells(level, data, player_pos, ghosts)
            elif state == "LOSE":
                player.dead = True
                break
            elif state == "CON":
                pass
            MoveGhost().move_ghost_dfs(
                ghosts[0].position,
                maze,
                (data.get_height(level), data.get_width(level)), ghosts[0],
                player.position, None
            )
            if ghosts[0].neighboars and len(ghosts[0].neighboars)>0:
                maze[ghosts[0].position[0]][ghosts[0].position[1]].has_ghost = False
                ghosts[0].position = ghosts[0].neighboars[1]
                maze[ghosts[0].position[0]][ghosts[0].position[1]].has_ghost = True
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

            # Check if the player won/lost/ate a pill
                # GAME SHOULD END WITH LOSE
                # run = False

            # get all moves

            # game logic

            # drawing all

            # Draw the background image instead of clearing with solid black
            # self.screen.fill((255, 255, 255))
            self.screen.fill((0, 0, 0))
            maze_draw = MazeRender(maze, self.screen)
            maze_draw.draw()
            # self.entry_page.draw()
            pygame.display.flip()
            # pygame.display.update()
            clock.tick(3)

        pygame.quit()
