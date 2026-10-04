import pygame

class MazeRender:
    def __init__(self, maze, screen: pygame.Surface):
        self.maze = maze
        self.screen = screen
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.screen_width, self.screen_height = self.screen.get_size()
        self.wall_thinckness = 10
        self.radius = self.wall_thinckness / 2
        self.wall_color = (0, 0, 205)  
        self.padding = 10
        self.dot_color = (255, 184, 174)  # classic pale pink/white pac-dot color
        self.pacman = pygame.image.load("assets/pacman.jpg").convert()
        self.ghost = pygame.image.load("assets/ghost.png").convert()
    def draw_corner(self, point, scale):
        pygame.draw.circle(self.screen, (0, 0, 205), point, scale)
        pygame.draw.circle(self.screen, (0, 0, 205), point, scale)
    def draw(self):
        padding = self.wall_thinckness
        available_width = self.screen_width - padding
        available_height = self.screen_height - padding
        cell_width = available_width / self.cols
        cell_height = available_height / self.rows

        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.maze[row][col]

                x = int(col * cell_width) + self.radius
                y = int(row * cell_height) + self.radius
                right = int((col + 1) * cell_width) + self.radius
                bottom = int((row + 1) * cell_height) + self.radius

                if cell.North:
                    self._draw_rounded_line(self.wall_color, (x, y), (right, y), 10)
                if cell.Est:
                    self._draw_rounded_line(self.wall_color, (right, y), (right, bottom), self.wall_thinckness)
                if cell.South:
                    self._draw_rounded_line(self.wall_color, (x, bottom), (right, bottom), self.wall_thinckness)
                if cell.West:
                    self._draw_rounded_line(self.wall_color, (x, y), (x, bottom), self.wall_thinckness)
        self.draw_pacgum()

    def _draw_rounded_line(self, color, start, end, thickness):
        pygame.draw.line(self.screen, color, start, end, thickness)
        radius = thickness // 2
        self.draw_corner(start, radius)
        self.draw_corner(end, radius)

    def draw_pacgum(self):
        padding = 10
        available_width = self.screen_width - padding
        available_height = self.screen_height - padding

        cell_width = available_width / self.cols
        cell_height = available_height / self.rows
    
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.maze[row][col]

                center_x = int((col + 0.5) * cell_width) + 1
                center_y = int((row + 0.5) * cell_height) + 1

                if getattr(cell, "supgum", True):
                    dot_radius = max(2, int(min(cell_width, cell_height) * 0.12))
                    pygame.draw.circle(self.screen, self.dot_color, (center_x, center_y), dot_radius)
                elif getattr(cell, "gum", True):
                    dot_radius = max(2, int(min(cell_width, cell_height) * 0.05))
                    pygame.draw.circle(self.screen, self.dot_color, (center_x, center_y), dot_radius)

                if cell.has_player:
                    self.pacman = pygame.transform.scale(self.pacman, (30, 30))
                    self.screen.blit(self.pacman, (center_x, center_y))
                if cell.has_ghost:
                    self.ghost = pygame.transform.scale(self.ghost, (30, 30))
                    self.screen.blit(self.ghost, (center_x, center_y))