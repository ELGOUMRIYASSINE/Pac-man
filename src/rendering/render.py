import pygame
# from .maze import Cell

class MazeRender:
    def __init__(self, maze, screen: pygame.Surface):
        self.maze = maze
        self.screen = screen
        self.rows = len(maze)
        self.cols = len(maze[0])
        
    def draw(self):
        screen_width, screen_height = self.screen.get_size()

        # 1. Subtract the 2-pixel line thickness from the total available space
        padding = 2
        available_width = screen_width - padding
        available_height = screen_height - padding

        # 2. Calculate cell dimensions based on the slightly smaller available space
        cell_width = available_width / self.cols
        cell_height = available_height / self.rows

        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.maze[row][col]
                
                # 3. Add 1 pixel to x and y to push the walls away from the absolute 0 edge
                x = int(col * cell_width) + 1
                y = int(row * cell_height) + 1
                right = int((col + 1) * cell_width) + 1
                bottom = int((row + 1) * cell_height) + 1
                
                if cell.North:
                    pygame.draw.line(self.screen, (255, 255, 255), (x, y), (right, y), 2)
                if cell.Est:
                    pygame.draw.line(self.screen, (255, 255, 255), (right, y), (right, bottom), 2)
                if cell.South:
                    pygame.draw.line(self.screen, (255, 255, 255), (x, bottom), (right, bottom), 2)
                if cell.West:
                    pygame.draw.line(self.screen, (255, 255, 255), (x, y), (x, bottom), 2)