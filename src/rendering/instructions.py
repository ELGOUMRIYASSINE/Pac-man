import pygame
import os

class Instructions:
    
    WHITE = (255, 255, 255)
    LIGHT = (170, 170, 170)
    DARK = (100, 100, 100)
    YELLOW = (255, 255, 0)
    BG = (60, 25, 60)

    def __init__(self, screen):
        pygame.init()  # Initialize all imported pygame modules
        pygame.font.init()  # Initialize the font module
    
        self.screen = screen 
        self.width, self.height = self.screen.get_size()
        
        # Fonts
        self.font_title = pygame.font.Font("assets/PressStart2P-Regular.ttf", 40)
        self.font_body = pygame.font.Font("assets/joystix monospace.otf", 30)
        self.font_body2 = pygame.font.Font("assets/Silkscreen-Bold.ttf", 20)

        # Load file once during initialization, not 60 times a second in the draw loop
        self.lines = []
        if os.path.exists("assets/instructions.txt"):
            with open("assets/instructions.txt", "r") as file:
                self.lines = [line.strip() for line in file.readlines()]
        else:
            self.lines = ["instructions.txt not found."]

        # Set up a Back button to return to the main menu
        button_width, button_height = 140, 50
        self.back_button = pygame.Rect(
            self.width // 2 - button_width // 2,
            self.height - 100,  # Positioned near the bottom
            button_width,
            button_height
        )

    def handle_event(self, event, mouse):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(mouse):
                return "BACK"
        return None

    def draw(self, mouse):
        # print("ccccc")
        self.screen.fill((0, 0, 0))
        
        # Draw Title
        title_text = self.font_title.render("INSTRUCTIONS", True, self.YELLOW)
        self.screen.blit(title_text, title_text.get_rect(center=(self.width // 2, 80)))

        # Draw text lines with vertical spacing
        start_y = 180
        line_spacing = 40
        for index, line in enumerate(self.lines):
            # Pass the variable 'line', not the string "line"
            text_surface = self.font_body2.render(line, True, self.WHITE)
            # Center horizontally, offset vertically based on index
            text_rect = text_surface.get_rect(center=(self.width // 2, start_y + (index * line_spacing)))
            self.screen.blit(text_surface, text_rect)

        # Draw Back Button (hover effect)
        pygame.draw.rect(
            self.screen, 
            self.LIGHT if self.back_button.collidepoint(mouse) else self.DARK, 
            self.back_button
        )
        
        # Draw Back Button Text
        back_text = self.font_body2.render("Back", True, self.YELLOW)
        self.screen.blit(back_text, back_text.get_rect(center=self.back_button.center))
        
# if __name__ == "__main__":
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#     pygame.display.set_caption("Instructions")
#     clock = pygame.time.Clock()

#     instructions = Instructions(screen)

#     running = True
#     while running:
#         mouse = pygame.mouse.get_pos()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#             result = instructions.handle_event(event, mouse)
#             if result == "BACK":
#                 print("Back button clicked")  # switch to your main menu here
#                 running = False

#         instructions.draw(mouse)
#         pygame.display.flip()   # <-- makes the drawing visible
#         clock.tick(60)          # limit to 60 FPS

#     pygame.quit()