import pygame
import sys

# start game
# View Highscores
# Instructions 

class MainMenu:
    WHITE = (255,255,255)
    LIGHT = (170,170,170)
    DARK = (100,100,100)
    yellow = (255, 255, 0)
    white = (255, 255, 255)
    BG = (60,25,60)
    def __init__(self, screen):
        # w, h = pygame.display.get_surface().get_size()
        self.screen = screen 
        self.width, self.height = self.screen.get_size()
        self.font_title = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", 40
        )
        self.font_body = pygame.font.Font(
            "assets/joystix monospace.otf", 30
        )
        self.font_body2 = pygame.font.Font(
            "assets/Silkscreen-Bold.ttf", 20
        )
        self.yellow = (255, 255, 0)
        self.white = (255, 255, 255)
        button_width, button_height = 140, 50
        spacing = 80  # vertical gap between buttons
        center_x = self.width // 2

        # Vertical center of the whole menu block
        start_y = self.height // 2 - (spacing * 1.5)

        self.start_button = pygame.Rect(0, 0, button_width, button_height)
        self.start_button.center = (center_x, start_y)

        self.exit_button = pygame.Rect(0, 0, button_width, button_height)
        self.exit_button.center = (center_x, start_y + spacing)

        self.highscores_button = pygame.Rect(0, 0, button_width, button_height)
        self.highscores_button.center = (center_x, start_y + spacing * 2)

        self.instructions = pygame.Rect(0, 0, button_width, button_height)
        self.instructions.center = (center_x, start_y + spacing * 3)
    def handle_event(self, event, mouse):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(mouse):
                return "PLAY"
            if self.exit_button.collidepoint(mouse):
                return "EXIT"
        return None
    def draw(self, mouse):
        self.screen.fill((0, 0, 0))


        pygame.draw.rect(self.screen, self.LIGHT if self.start_button.collidepoint(mouse) else self.DARK, self.start_button)
        pygame.draw.rect(self.screen, self.LIGHT if self.exit_button.collidepoint(mouse) else self.DARK, self.exit_button)
        pygame.draw.rect(self.screen, self.LIGHT if self.highscores_button.collidepoint(mouse) else self.DARK, self.highscores_button)
        pygame.draw.rect(self.screen, self.LIGHT if self.instructions.collidepoint(mouse) else self.DARK, self.instructions)

        start_text = self.font_title.render("PLay", True, self.yellow)
        score_text = self.font_title.render("View Hightscores", True, self.yellow)
        instru_text = self.font_title.render("Instructions", True, self.yellow)
        exit_text = self.font_title.render("Exit", True, self.yellow)

        self.screen.blit(start_text, start_text.get_rect(center=self.start_button.center))        
        self.screen.blit(score_text, score_text.get_rect(center=self.highscores_button.center))
        self.screen.blit(instru_text, instru_text.get_rect(center=self.instructions.center))
        self.screen.blit(exit_text, exit_text.get_rect(center=self.exit_button.center))
