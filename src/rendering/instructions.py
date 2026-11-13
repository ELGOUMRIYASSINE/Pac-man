"""Render the instructions screen and handle its back button."""

import os

import pygame


class Instructions:
    """Display game instructions in a window and respond to mouse input."""

    WHITE = (255, 255, 255)
    LIGHT = (170, 170, 170)
    DARK = (100, 100, 100)
    YELLOW = (255, 255, 0)
    BG = (60, 25, 60)

    def __init__(self, screen: pygame.Surface) -> None:
        """Prepare fonts, instructions text, and the back button."""
        pygame.init()
        pygame.font.init()

        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.font_title = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", 40
        )
        self.font_body = pygame.font.Font("assets/joystix monospace.otf", 30)
        self.font_body2 = pygame.font.Font("assets/Silkscreen-Bold.ttf", 20)
        if os.path.exists("assets/instructions.txt"):
            with open("assets/instructions.txt", encoding="utf-8") as file:
                self.lines = [line.strip() for line in file]
        else:
            self.lines = ["instructions.txt not found."]

        button_width, button_height = 140, 50
        self.back_button = pygame.Rect(
            self.width // 2 - button_width // 2,
            self.height - 100,
            button_width,
            button_height,
        )

    def handle_event(
        self, event: pygame.event.Event, mouse: tuple[int, int]
    ) -> str | None:
        """Return a screen action when the user clicks the back button."""
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and self.back_button.collidepoint(mouse)
        ):
            return "BACK"
        return None

    def draw(self, mouse: tuple[int, int]) -> None:
        """Draw the instructions and update the button hover appearance."""
        self.screen.fill((0, 0, 0))
        title_text = self.font_title.render("INSTRUCTIONS", True, self.YELLOW)
        self.screen.blit(
            title_text,
            title_text.get_rect(center=(self.width // 2, 80)),
        )

        start_y = 180
        line_spacing = 40
        for index, line in enumerate(self.lines):
            text_surface = self.font_body2.render(line, True, self.WHITE)
            center = (self.width // 2, start_y + index * line_spacing)
            text_rect = text_surface.get_rect(center=center)
            self.screen.blit(text_surface, text_rect)

        color = (
            self.LIGHT
            if self.back_button.collidepoint(mouse)
            else self.DARK
        )
        pygame.draw.rect(self.screen, color, self.back_button)
        back_text = self.font_body2.render("Back", True, self.YELLOW)
        self.screen.blit(
            back_text,
            back_text.get_rect(center=self.back_button.center),
        )
