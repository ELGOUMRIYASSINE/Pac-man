import pygame


class EntryFace:
    def __init__(self):
        # get some names just for test 
        self.highscores = [
            ("Sannaka", 1110),
            ("foliole", 20),
            ("Marmelade", 20),
            ("goldfish", 20),
        ]

    def draw(self, screen, width, height):
        font_title = pygame.font.Font("../assets/fonts/HennyPenny-Regular.ttf", 50)
        font_body = pygame.font.Font("../assets/fonts/Kranky-Regular.ttf", 40)
        font_body2 = pygame.font.Font("../assets/fonts/Kranky-Regular.ttf", 35)

        yellow = (255, 255, 0)
        white = (255, 255, 255)

        title = font_title.render("Pac-Man", True, yellow)
        title_rect = title.get_rect(center=(width // 2, height // 8))
        screen.blit(title, title_rect)

        subtitle = font_body.render("Push SPACE to play", True, white)
        subtitle_rect = subtitle.get_rect(center=(width // 2, height // 4))
        screen.blit(subtitle, subtitle_rect)

        header = font_body.render("highscores:", True, yellow)
        header_rect = header.get_rect(center=(width // 2, height // 3))
        screen.blit(header, header_rect)

    
        line_spacing = font_body.get_linesize()
        start_y = header_rect.bottom + 40
        for i, (name, score) in enumerate(self.highscores):
            line_text = f"{i + 1}. {name} - {score} pts"
            line_surf = font_body2.render(line_text, True, white)
            line_rect = line_surf.get_rect(center=(width // 2, start_y + i * line_spacing))
            screen.blit(line_surf, line_rect)