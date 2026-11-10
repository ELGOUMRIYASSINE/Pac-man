import pygame
import inspect
pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Moving rectangle")

x = 200
y = 200

width = 20
height = 20

vel = 5
run = True

# print(dir(pygame.key))

old_x, old_y = x, y
places = [(x, y)]
draw = True
while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > 0:
        x -= vel
    if keys[pygame.K_RIGHT] and x < 500-width:
        x += vel
    if keys[pygame.K_DOWN] and y < 500-height:
        y += vel
    if keys[pygame.K_UP] and y > 0:
        y -= vel
    if keys[pygame.K_a]:
        draw = False
    if not keys[pygame.K_a]:
        draw = True
    if not keys[pygame.K_F1]:
        cercle = True

    win.fill((0, 0, 0))
    # pygame.draw.rect(win, (255, 255, 255), (old_x + 5, old_y, width // 2, height + 10))
    for index in places:
        pygame.draw.rect(win, (255, 255, 255), (index[0], index[1], width, height))
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    if draw:
        places.append((x, y))
    # pygame.draw.rect(win, (255, 255, 255), (x, y, width, height))
    pygame.display.update()

pygame.quit()


