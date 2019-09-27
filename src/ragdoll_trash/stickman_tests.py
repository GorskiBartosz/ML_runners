import sys

from math import degrees
import pygame
import pymunk
import random
import pymunk.pygame_util
from pygame.locals import *
from math import sqrt


def add_ball(space):
    """Add a ball to the given space at a random position"""
    mass = 1
    radius = 14
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    x = random.randint(120, 380)
    body.position = x, 550
    shape = pymunk.Circle(body, radius, (0, 0))
    space.add(body, shape)
    return shape


def add_L(space):
    """Add a inverted L shape with two joints"""
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (300, 300)

    rotation_limit_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_limit_body.position = (200, 300)

    body = pymunk.Body(10, 10000)
    body.position = (300, 300)
    l1 = pymunk.Segment(body, (-150, 0), (255.0, 0.0), 5.0)
    l2 = pymunk.Segment(body, (-150.0, 0), (-150.0, 50.0), 5.0)

    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
    joint_limit = 25
    rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-100, 0), (0, 0), 0, joint_limit)

    space.add(l1, l2, body, rotation_center_joint, rotation_limit_joint)
    return l1, l2


def add_pendulum(space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (300, 300)

    mom = pymunk.moment_for_segment(10, (0, -150), (0, 150), 5)
    body = pymunk.Body(10, mom)
    body.position = (300, 300)
    segment = pymunk.Segment(body, (0, -150), (0, 150), 5)

    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))

    space.add(segment, body, rotation_center_joint)
    return body


def add_polygon(space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (300, 300)

    mom = pymunk.moment_for_poly(10, [(0, 0), (150, 0), (150, 5), (5, 5), (5, 150), (0, 150)])
    body = pymunk.Body(10, mom)
    body.position = (300, 300)
    polygon = pymunk.Poly(body, vertices=[(0, 0), (150, 0), (150, 5), (5, 5), (5, 150), (0, 150)])

    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))

    space.add(polygon, body, rotation_center_joint)
    return body


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    pygame.display.set_caption("Stick-man: tests")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 0.0)

    pendulum = add_pendulum(space)
    # pendulum = add_polygon(space)

    impulse = 100
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)

            # pendulum control
            if event.type == KEYDOWN and event.key == K_KP1:
                pendulum.apply_impulse_at_local_point((-impulse, 0), (0, -150))
            if event.type == KEYDOWN and event.key == K_KP3:
                pendulum.apply_impulse_at_local_point((impulse, 0), (0, -150))
            if event.type == KEYDOWN and event.key == K_KP7:
                pendulum.apply_impulse_at_local_point((-impulse, 0), (0, 150))
            if event.type == KEYDOWN and event.key == K_KP9:
                pendulum.apply_impulse_at_local_point((impulse, 0), (0, 150))

        screen.fill((0, 0, 0))
        space.debug_draw(draw_options)
        space.step(1 / 100.0)
        pygame.display.flip()
        clock.tick(50)


if __name__ == '__main__':
    main()
