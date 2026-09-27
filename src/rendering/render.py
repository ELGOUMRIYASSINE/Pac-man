import pygame
# from .maze import Cell

class MazeRender:
    def __init__(self, maze, screen: pygame.Surface):
        self.maze = maze
        self.screen = screen
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.GLOW_COLOR = (0, 0, 140)   # darker blue halo
        self.CORE_COLOR = (33, 33, 255) # bright blue core
        # print(f"rows: {len(maze)}")
        # print(f"columns: {len(maze[0])}")
        # exit()
    def draw_corner(self, point):
        pygame.draw.circle(self.screen, self.GLOW_COLOR, point, 3)
        pygame.draw.circle(self.screen, self.CORE_COLOR, point, 1.5)
    def draw_wall_segment(self, start, end):
        pygame.draw.line(self.screen, self.GLOW_COLOR, start, end, 6)
        pygame.draw.line(self.screen, self.CORE_COLOR, start, end, 3)
    def draw(self):
        screen_width, screen_height = self.screen.get_size()

        wall_thickness = 10
        radius = wall_thickness // 2
        color = (0, 0, 205)

        padding = wall_thickness
        available_width = screen_width - padding
        available_height = screen_height - padding

        cell_width = available_width / self.cols
        cell_height = available_height / self.rows

        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.maze[row][col]

                x = int(col * cell_width) + radius
                y = int(row * cell_height) + radius
                right = int((col + 1) * cell_width) + radius
                bottom = int((row + 1) * cell_height) + radius

                if cell.North:
                    self._draw_rounded_line(color, (x, y), (right, y), wall_thickness)
                if cell.Est:
                    self._draw_rounded_line(color, (right, y), (right, bottom), wall_thickness)
                if cell.South:
                    self._draw_rounded_line(color, (x, bottom), (right, bottom), wall_thickness)
                if cell.West:
                    self._draw_rounded_line(color, (x, y), (x, bottom), wall_thickness)
        self.draw_pacgum()

    def _draw_rounded_line(self, color, start, end, thickness):
        pygame.draw.line(self.screen, color, start, end, thickness)
        radius = thickness // 2
        pygame.draw.circle(self.screen, color, start, radius)
        pygame.draw.circle(self.screen, color, end, radius)

    def draw_pacgum(self):
        screen_width, screen_height = self.screen.get_size()

        padding = 2
        available_width = screen_width - padding
        available_height = screen_height - padding

        cell_width = available_width / self.cols
        cell_height = available_height / self.rows
    
        dot_radius = max(2, int(min(cell_width, cell_height) * 0.05))  # scales with cell size
        dot_color = (255, 184, 174)  # classic pale pink/white pac-dot color

        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.maze[row][col]

                # skip cells that shouldn't have a dot (already eaten, start position, etc.)
                if not getattr(cell, "supgum", True) and not getattr(cell, "gum", True):
                    continue

                center_x = int((col + 0.5) * cell_width) + 1
                center_y = int((row + 0.5) * cell_height) + 1

                if getattr(cell, "supgum", True):
                    dot_radius = max(2, int(min(cell_width, cell_height) * 0.08))
                else:
                    dot_radius = max(2, int(min(cell_width, cell_height) * 0.05))
                pygame.draw.circle(self.screen, dot_color, (center_x, center_y), dot_radius)