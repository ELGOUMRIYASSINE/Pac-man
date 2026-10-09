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
        # self.pacman = pygame.image.load("assets/pacman.jpg").convert()
        self.player_images = ["1.png","2.png"]
        self.upload_player = [pygame.transform.scale(pygame.image.load(f"assets/{img}").convert_alpha(), (30, 30)) for img in self.player_images]
        self.anim_delay = 150
        self.state_counter = 0
        self.player_image = self.upload_player[self.state_counter]
        self.last_anim_time = pygame.time.get_ticks()
        self.last_move = None
        self.ghost = pygame.image.load("assets/ghost.png").convert()
    def draw_corner(self, point, scale):
        pygame.draw.circle(self.screen, (0, 0, 205), point, scale)
        pygame.draw.circle(self.screen, (0, 0, 205), point, scale)
    def draw(self, move=None):
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
        self.draw_content(move)

    def _draw_rounded_line(self, color, start, end, thickness):
        pygame.draw.line(self.screen, color, start, end, thickness)
        radius = thickness // 2
        self.draw_corner(start, radius)
        self.draw_corner(end, radius)

    def move_player(self, move, last_move):
        if not move:
            move = self.last_move
            if move == "UP":
                self.player_image = pygame.transform.rotate(self.upload_player[self.state_counter], 270)
            if move == "DOWN":
                self.player_image = pygame.transform.rotate(self.upload_player[self.state_counter], 90) # good
            if move == "LEFT":
                self.player_image = pygame.transform.rotate(self.upload_player[self.state_counter], 360)
            if move == "RIGHT":
                self.player_image = pygame.transform.rotate(self.upload_player[self.state_counter], 180)
        return move

    def draw_content(self, move):
        now = pygame.time.get_ticks()

        if now - self.last_anim_time >= self.anim_delay:
            self.state_counter = (self.state_counter + 1) % len(self.player_images)
            self.last_anim_time = now
    
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
                
                self.last_move = self.move_player(move, self.last_move)
                if cell.has_player:
                    self.screen.blit(self.player_image, (center_x - 10, center_y))
                if cell.has_ghost:
                    self.ghost = pygame.transform.scale(self.ghost, (30, 30))
                    self.screen.blit(self.ghost, (center_x, center_y))