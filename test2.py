import pygame
import random
from src.rendering.score_form import SCOREFORM

pygame.init()
screen = pygame.display.set_mode((1200, 740))
clock = pygame.time.Clock()
score = SCOREFORM(screen)

running = True
while running:
    # 1. Event Handling
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((0, 0, 0))
    # create the box surface
    box = pygame.Surface((30, 30))

    # draw on the box surface
    box.fill((255, 255, 255))



    # draw in the main surface
    screen.blit(box, (205, 205))    
    # display the page here
    # score.draw(mouse)

    pygame.display.flip()
    clock.tick(60) # Lock to 60 FPS

pygame.quit()