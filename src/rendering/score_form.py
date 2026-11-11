import pygame
import sys

# start game
# View Highscores
# Instructions 

class SCOREFORM:
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
            "assets/PressStart2P-Regular.ttf", 20
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

    def draw(self, mouse):
        print("drawing menu")
        self.screen.fill((0, 0, 0))

        start_text = self.font_title.render("Enter your name to save your score", True, self.yellow)

        self.screen.blit(start_text, start_text.get_rect(center=self.start_button.center))        
