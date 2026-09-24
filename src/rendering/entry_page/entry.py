import pygame


class EntryFace:
    def __init__(self, screen, height, width):
        # get some names just for test
        pygame.font.init()
        self.screen = screen
        self.height = height
        self.width = width
        try:
            self.font_title = pygame.font.Font(
                "assets/PressStart2P-Regular.ttf", 50
            )
            self.font_body = pygame.font.Font(
                "assets/joystix monospace.otf", 30
            )
            self.font_body2 = pygame.font.Font(
                "assets/Silkscreen-Bold.ttf", 20
            )
        except Exception as e:
            raise Exception(f"Error loading fonts: {e}")
        self.yellow = (255, 255, 0)
        self.white = (255, 255, 255)
        self.highscores = [
            ("Sannaka", 1110),
            ("foliole", 20),
            ("Marmelade", 20),
            ("goldfish", 20),
        ]

    def draw_scores(self, header_rect):
        line_spacing = self.font_body.get_linesize()
        start_y = header_rect.bottom + 40
        for i, (name, score) in enumerate(self.highscores):
            line_text = f"{i + 1} {name}  {score} pts"
            line_surf = self.font_body2.render(line_text, True, self.white)
            line_rect = line_surf.get_rect(
                center=(self.width // 2, start_y + i * line_spacing)
            )
            self.screen.blit(line_surf, line_rect)

    def draw(self):
        title = self.font_title.render("Pac-Man", True, self.yellow)
        title_rect = title.get_rect(center=(self.width // 2, self.height // 5))
        self.screen.blit(title, title_rect)

        # --- blinking "Push SPACE to play" ---
        blink_interval = (
            500  # milliseconds — half a second on, half a second off
        )
        show_subtitle = (pygame.time.get_ticks() // blink_interval) % 2 == 0

        if show_subtitle:
            subtitle = self.font_body.render(
                "Push SPACE to play", True, self.yellow
            )
            subtitle_rect = subtitle.get_rect(
                center=(self.width // 2, self.height // 1.10)
            )
            self.screen.blit(subtitle, subtitle_rect)

        # --- end blinking ---
        header = self.font_body.render("highscores:", True, self.yellow)
        header_rect = header.get_rect(
            center=(self.width // 2, self.height // 2.88)
        )
        self.screen.blit(header, header_rect)
        self.draw_scores(header_rect)
