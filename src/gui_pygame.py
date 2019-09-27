import pygame
from pygame.locals import *


def sim_gui():
    print("hello:simulation")
    pygame.init()

    win_width = 500
    win_height = 500
    win = pygame.display.set_mode((win_width, win_height))

    pygame.display.set_caption("Simulation")

    x = 5
    y = 5
    rect_width = 50
    rect_height = 50
    velocity = 5

    opened = True

    while opened:

        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                opened = False
            if pygame.mouse.get_pressed()[0]:
                x = pygame.mouse.get_pos()[0] - rect_width / 2
                y = pygame.mouse.get_pos()[1] - rect_height / 2

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and x > velocity:
            x -= velocity
        if keys[pygame.K_RIGHT] and x < win_width - rect_width - velocity:
            x += velocity
        if keys[pygame.K_UP] and y > velocity:
            y -= velocity
        if keys[pygame.K_DOWN] and y < win_height - rect_height - velocity:
            y += velocity

        win.fill((0, 0, 0))
        pygame.draw.rect(win, (255, 0, 0), (x, y, rect_width, rect_height))
        pygame.display.update()
