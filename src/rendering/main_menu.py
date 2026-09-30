import pygame
import sys

# start game
# View Highscores
# Instructions 

class MainMenu:
    WHITE = (255,255,255)
    LIGHT = (170,170,170)
    DARK = (100,100,100)
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
        self.start_button = pygame.Rect(300, 300, 140, 50)
        self.exit_button = pygame.Rect(300, 380, 140, 50)
    def handle_event(self, event, mouse):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(mouse):
                return "PLAY"
            if self.exit_button.collidepoint(mouse):
                return "EXIT"
        return None
    def draw(self, mouse):
        self.screen.fill(self.BG)

        # mouse = pygame.mouse.get_pos()

        pygame.draw.rect(self.screen, self.LIGHT if self.start_button.collidepoint(mouse) else self.DARK, self.start_button)
        pygame.draw.rect(self.screen, self.LIGHT if self.exit_button.collidepoint(mouse) else self.DARK, self.exit_button)

        start_text = self.font_title.render("PLay", True, self.WHITE)
        exit_text = self.font_title.render("Exit", True, self.WHITE)

        self.screen.blit(start_text, start_text.get_rect(center=self.start_button.center))        
        self.screen.blit(exit_text, exit_text.get_rect(center=self.exit_button.center))


        # pygame.display.update()
