from Maze.maze_integration import MazeIntegration
import pygame
from rendering.entry_page.entry import EntryFace


class Render:

    def __init__(self):
        self.maze = MazeIntegration().get_maze(0, 20, 20)
        screen = pygame.display.set_mode((1200, 700))
        self.entry_page = EntryFace(screen, 700, 1200)

    # run pygame loop and call the entry page draw function to show the first page
    def entry(self):
        pygame.init()
        pygame.display.set_caption('Pacman')
        # Load and scale the background image ONCE before the loop starts
        bg_image = pygame.image.load("../assets/entry_page.jpeg").convert()
        bg_image = pygame.transform.scale(bg_image, (1200, 700))

        run = True
        while run:
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            # Draw the background image instead of clearing with solid black
            self.entry_page.screen.blit(bg_image, (0, 0))
            
            # Draw remaining UI elements over the background
            self.entry_page.draw()
            
            pygame.display.update()
            
        pygame.quit()

ren = Render()
ren.entry()

