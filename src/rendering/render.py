from Maze.maze_integration import MazeIntegration
import pygame
from rendering.entry_page.entry import EntryFace


class Render:

    def __init__(self):
        self.maze = MazeIntegration().get_maze(0, 20, 20)
        self.entry_page = EntryFace()

    # run pygame loop and call the entry page draw function to show the first page
    def entry(self):
        pygame.init()
        screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption('Pacman')

        # Load and scale the background image ONCE before the loop starts
        bg_image = pygame.image.load("../assets/f9c31768-0380-4802-9bbb-abb5470726ea.jpeg").convert()
        bg_image = pygame.transform.scale(bg_image, (1200, 700))

        run = True
        while run:
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            # Draw the background image instead of clearing with solid black
            screen.blit(bg_image, (0, 0))
            
            # Draw remaining UI elements over the background
            self.entry_page.draw(screen, 1200, 700)
            
            pygame.display.update()
            
        pygame.quit()

ren = Render()
ren.entry()

