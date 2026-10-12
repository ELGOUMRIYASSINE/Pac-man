import pygame
from .move import Mover
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
        self.upload_player = None
        self.anim_delay = 150
        self.state_counter = 0
        # self.player_image = self.upload_player[self.state_counter]
        self.last_anim_time = pygame.time.get_ticks()
        self.last_move = None
        self.ghost = None
        self.cell_width = 0
        self.cell_height = 0
        self.player_mover = None
    def draw_corner(self, point, scale):
        pygame.draw.circle(self.screen, (0, 0, 205), point, scale)
        pygame.draw.circle(self.screen, (0, 0, 205), point, scale)
    def draw(self, move=None):
        self.cell_width, self.cell_height = self.cell_sizes()
        self.screen.fill((0, 0, 0))

        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.maze[row][col]

                x = int(col * self.cell_width) + self.radius
                y = int(row * self.cell_height) + self.radius
                right = int((col + 1) * self.cell_width) + self.radius
                bottom = int((row + 1) * self.cell_height) + self.radius

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
    def cell_sizes(self):
        padding = 10
        available_width = self.screen_width - padding
        available_height = self.screen_height - padding

        cell_width = available_width / self.cols
        cell_height = available_height / self.rows
        return cell_width, cell_height
    def _center(self, row, col):
        return ((col + 0.5) * self.cell_width + self.radius,
                (row + 0.5) * self.cell_height + self.radius)
    def _build_sprites(self):
        player_size = int(min(self.cell_width, self.cell_height) * 0.8)
        self.upload_player = [
            pygame.transform.scale(pygame.image.load(f"assets/{img}").convert_alpha(), (player_size, player_size)) for img in self.player_images
        ]
        self.ghost = pygame.transform.scale(pygame.image.load("assets/ghost.png").convert_alpha(), (player_size, player_size))
        self.p_rotations = {
            "UP": pygame.transform.rotate(self.upload_player[self.state_counter], 270),
            "DOWN": pygame.transform.rotate(self.upload_player[self.state_counter], 90),
            "LEFT": pygame.transform.rotate(self.upload_player[self.state_counter], 360),
            "RIGHT": pygame.transform.rotate(self.upload_player[self.state_counter], 180),
        }
        self.player_image = self.p_rotations.get(self.last_move, self.upload_player[self.state_counter])
    def draw_content(self, move):
        now = pygame.time.get_ticks()

        if now - self.last_anim_time >= self.anim_delay:
            self.state_counter = (self.state_counter + 1) % len(self.player_images)
            self.last_anim_time = now
    
        self.cell_width, self.cell_height = self.cell_sizes()
    
        
        player_target = None
        ghost_targets = []
        self._build_sprites()
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.maze[row][col]

                center_x, center_y = self._center(row, col)

                if getattr(cell, "supgum", True):
                    dot_radius = max(2, int(min(self.cell_width, self.cell_height) * 0.12))
                    pygame.draw.circle(self.screen, self.dot_color, (center_x, center_y), dot_radius)
                elif getattr(cell, "gum", True):
                    dot_radius = max(2, int(min(self.cell_width, self.cell_height) * 0.05))
                    pygame.draw.circle(self.screen, self.dot_color, (center_x, center_y), dot_radius)
                
                if cell.has_player:
                    player_target = (center_x, center_y)
                if cell.has_ghost:
                    ghost_targets.append((center_x, center_y))
        # self.last_move = self.move_player(move, self.last_move)
        # self.screen.blit(self.player_image, player_target)
        self.last_move = self.move_player(move, self.last_move)

        if player_target is not None:
            if self.player_mover is None:
                self.player_mover = Mover(player_target, 200)
            self.player_mover.set_target(player_target, now)
            pos = self.player_mover.update(now)
            rect = self.player_image.get_rect(center=(round(pos.x), round(pos.y)))
            self.screen.blit(self.player_image, rect)
            for ghost_target in ghost_targets:
                self.screen.blit(self.ghost, ghost_target)
            # self.screen.blit(self.ghost, ghost_targets[0])