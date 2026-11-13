"""Render the main menu and translate button clicks into game actions."""

import pygame


class MainMenu:
    """Draw the main menu and detect which option the user selects."""

    WHITE = (255, 255, 255)
    LIGHT = (170, 170, 170)
    DARK = (100, 100, 100)
    YELLOW = (255, 255, 0)
    BG = (60, 25, 60)

    def __init__(self, screen: pygame.Surface) -> None:
        """Create the menu buttons and load their fonts."""
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.font_title = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", 40
        )
        self.font_body = pygame.font.Font("assets/joystix monospace.otf", 30)
        self.font_body2 = pygame.font.Font("assets/Silkscreen-Bold.ttf", 20)
        button_width, button_height = 140, 50
        spacing = 80
        center_x = self.width // 2
        start_y = self.height // 2 - int(spacing * 1.5)

        self.start_button = pygame.Rect(0, 0, button_width, button_height)
        self.start_button.center = (center_x, start_y)
        self.exit_button = pygame.Rect(0, 0, button_width, button_height)
        self.exit_button.center = (center_x, start_y + spacing)
        self.highscores_button = pygame.Rect(0, 0, button_width, button_height)
        self.highscores_button.center = (center_x, start_y + spacing * 2)
        self.instructions = pygame.Rect(0, 0, button_width, button_height)
        self.instructions.center = (center_x, start_y + spacing * 3)

    def handle_event(
        self, event: pygame.event.Event, mouse: tuple[int, int]
    ) -> str | None:
        """Return the selected action when the user clicks a menu button."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(mouse):
                return "PLAY"
            if self.exit_button.collidepoint(mouse):
                return "EXIT"
            if self.highscores_button.collidepoint(mouse):
                return "HIGHSCORES"
            if self.instructions.collidepoint(mouse):
                return "INSTRUCTIONS"
        return None

    def draw(self, mouse: tuple[int, int]) -> None:
        """Draw the menu buttons and their labels."""
        self.screen.fill((0, 0, 0))
        buttons = (
            self.start_button,
            self.exit_button,
            self.highscores_button,
            self.instructions,
        )
        for button in buttons:
            color = self.LIGHT if button.collidepoint(mouse) else self.DARK
            pygame.draw.rect(self.screen, color, button)

        labels = (
            ("PLay", self.start_button),
            ("View Hightscores", self.highscores_button),
            ("Instructions", self.instructions),
            ("Exit", self.exit_button),
        )
        for label, button in labels:
            text = self.font_title.render(label, True, self.YELLOW)
            self.screen.blit(text, text.get_rect(center=button.center))
