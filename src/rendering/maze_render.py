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
        # --- maze design (only used by the wall drawing below) ---
        self.wall_inner_color = (4, 4, 40)        # dark core of the hollow walls
        self.wall_glow_color = (0, 40, 255, 60)   # soft halo around the walls
        self._wall_layer = None
        self._wall_key = None
        self.ghosts = {}

    def _grid_point(self, col, row):
        """Pixel position of a grid intersection."""
        return (int(col * self.cell_width) + self.radius,
                int(row * self.cell_height) + self.radius)

    def _wall_segments(self):
        """Every wall once (a shared wall between two cells is not doubled)."""
        segments = set()
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.maze[row][col]
                if cell.North:
                    segments.add(((col, row), (col + 1, row)))
                if cell.Est:
                    segments.add(((col + 1, row), (col + 1, row + 1)))
                if cell.South:
                    segments.add(((col, row + 1), (col + 1, row + 1)))
                if cell.West:
                    segments.add(((col, row), (col, row + 1)))
        return segments

    def _wall_signature(self):
        """Changes whenever the size or any wall changes -> cache rebuild."""
        walls = tuple(
            (c.North, c.Est, c.South, c.West)
            for line in self.maze for c in line
        )
        return (self.screen.get_size(), self.cell_width, self.cell_height,
                self.wall_thinckness, self.wall_color, walls)

    def _build_wall_layer(self):
        width, height = self.screen.get_size()
        t = self.wall_thinckness
        inner_t = max(1, t - 6)                     # leaves a ~3px colored outline

        lines = [(self._grid_point(*a), self._grid_point(*b))
                 for a, b in self._wall_segments()]
        joints = {p for line in lines for p in line}

        # 1) glow: fat translucent lines, blurred by scaling down then up
        glow = pygame.Surface((width, height), pygame.SRCALPHA)
        for start, end in lines:
            pygame.draw.line(glow, self.wall_glow_color, start, end, t * 3)
        for p in joints:
            pygame.draw.circle(glow, self.wall_glow_color, p, int(t * 1.5))
        small = pygame.transform.smoothscale(glow, (max(1, width // 4), max(1, height // 4)))
        glow = pygame.transform.smoothscale(small, (width, height))

        layer = pygame.Surface((width, height), pygame.SRCALPHA)
        layer.blit(glow, (0, 0))

        # 2) outer wall body, round caps have the same radius as the line
        for start, end in lines:
            pygame.draw.line(layer, self.wall_color, start, end, t)
        for p in joints:
            pygame.draw.circle(layer, self.wall_color, p, t // 2)

        # 3) dark inner core -> hollow tube; drawn after ALL outer lines so
        #    junctions and corners merge cleanly
        for start, end in lines:
            pygame.draw.line(layer, self.wall_inner_color, start, end, inner_t)
        for p in joints:
            pygame.draw.circle(layer, self.wall_inner_color, p, max(1, inner_t // 2))

        self._wall_layer = layer
        self._wall_key = self._wall_signature()

    def draw(self, move=None):
        self.cell_width, self.cell_height = self.cell_sizes()
        self.screen.fill((0, 0, 0))

        if self._wall_key != self._wall_signature():
            self._build_wall_layer()
        self.screen.blit(self._wall_layer, (0, 0))

        self.draw_content(move)


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
        self.ghost = pygame.transform.scale(pygame.image.load("assets/ghost.webp").convert_alpha(), (player_size, player_size))
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
                    if 
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
                g_rect = self.ghost.get_rect(center=(ghost_target[0], ghost_target[1]))
                self.screen.blit(self.ghost, g_rect)
            # self.screen.blit(self.ghost, ghost_targets[0])