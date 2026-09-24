import pygame


class MazeRender:
    def __init__(self, maze, screen):
        self.maze_binary = maze
        self.cell_size = 40
        self.screen = screen

    def draw(self):
        TOP, RIGHT, BOTTOM, LEFT = 1, 2, 4, 8
        for row in range(len(self.maze_binary)):
            for col in range(len(self.maze_binary[0])):
                val = self.maze_binary[row][col]
                x = col * self.cell_size
                y = row * self.cell_size
                if val & TOP:
                    pygame.draw.line(
                        self.screen,
                        (255, 255, 255),
                        (x, y),
                        (x + self.cell_size, y),
                        2,
                    )
                if val & BOTTOM:
                    pygame.draw.line(
                        self.screen,
                        (255, 255, 255),
                        (x, y + self.cell_size),
                        (x + self.cell_size, y + self.cell_size),
                        2,
                    )
                if val & LEFT:
                    pygame.draw.line(
                        self.screen,
                        (255, 255, 255),
                        (x, y),
                        (x, y + self.cell_size),
                        2,
                    )
                if val & RIGHT:
                    pygame.draw.line(
                        self.screen,
                        (255, 255, 255),
                        (x + self.cell_size, y),
                        (x + self.cell_size, y + self.cell_size),
                        2,
                    )
