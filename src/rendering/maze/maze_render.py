import pygame


class MazeRender:
    def __init__(self, maze_binary, screen):
        self.maze_binary = maze_binary
        self.cell_size = 40
        self.row = len(maze_binary)
        self.col = len(maze_binary[0])
        self.screen = screen

    def draw(self):
        for row_index, row in enumerate(self.maze_binary):
            for col_index, cell in enumerate(row):
                x = col_index * self.cell_size
                y = row_index * self.cell_size

                if cell.West:
                    pygame.draw.line(self.screen, (255, 255, 255), (x, y), (x, y + self.cell_size), 2)

                if cell.North:
                    pygame.draw.line(self.screen, (255, 255, 255), (x, y), (x + self.cell_size, y), 2)

                if cell.Est:
                    pygame.draw.line(self.screen, (255, 255, 255), (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), 2)

                if cell.South:
                    pygame.draw.line(self.screen, (255, 255, 255), (x, y + self.cell_size), (x + self.cell_size, y + self.cell_size), 2)