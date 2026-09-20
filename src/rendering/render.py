from mazegenerator.mazegenerator import MazeGenerator 
import pygame
from rendering.entry_page.entry import EntryFace
from Maze.Maze import Maze
from rendering.maze.maze_render import MazeRender

class Render:

    def __init__(self):
        pygame.init()
        self.maze = MazeGenerator()
        self.maze_binary = Maze.creat_cells(self.maze)
        screen = pygame.display.set_mode((1200, 700))
        self.entry_page = EntryFace(screen, 700, 1200)
        self.maze_draw = MazeRender(self.maze_binary, screen)

    # run pygame loop and call the entry page draw function to show the first page
    def entry(self):
        pygame.display.set_caption('Pacman')
        # Load and scale the background image ONCE before the loop starts
        bg_image = pygame.image.load("../assets/entry_page.jpeg").convert()
        # bg_image = pygame.transform.scale(bg_image, (1200, 700))

        run = True
        clock = pygame.time.Clock()
        while run:
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            # Draw the background image instead of clearing with solid black
            # self.entry_page.screen.blit(bg_image, (0, 0))
            
            # Draw remaining UI elements over the background
            # self.entry_page.draw()
            self.maze_draw.draw()
            pygame.display.flip()
            pygame.display.update()
            clock.tick(60)
            
        pygame.quit()

ren = Render()
ren.entry()

