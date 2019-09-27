import sys

import pygame
import pymunk
import pymunk.pygame_util
from pygame.locals import *
from math import sqrt


def add_floor(space, floor_friction):
    floor_endpoints = ((0, 0), (5000, 0))
    floor_thickness = 5
    floor_position = (0, 10)

    floor_shape = pymunk.shapes.Segment(space.static_body, floor_endpoints[0], floor_endpoints[1], floor_thickness)
    floor_shape.body.position = floor_position
    floor_shape.friction = floor_friction
    space.add(floor_shape)


def get_body_part(end_points, thickness, mass, position, friction):
    moment = pymunk.moment_for_segment(mass, end_points[0], end_points[1], thickness)
    body = pymunk.Body(mass, moment)
    shape = pymunk.Segment(body, end_points[0], end_points[1], thickness)
    shape.body.position = position
    shape.friction = friction
    return body, shape


def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    pygame.display.set_caption("Stick-man: tests")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, -100.0)

    # CONSTANSES
    leg_thickness = 3
    leg_mass = 1
    ache_thickness = 6
    ache_mass = 1
    friction = 0.6
    add_floor(space, friction)

    # segment_body = add_segment(space)
    # segment_body = add_polygon(space)

    sinus = 0.8
    cosinus = sqrt(1 - sinus * sinus)
    leg_length = 40
    ache_length = 23
    CENTRE = 60

    legs_end_points = (
        ((0, 0), (cosinus * leg_length, -sinus * leg_length)),  # right
        ((0, 0), (-cosinus * leg_length, -sinus * leg_length)),  # left
        ((0, 0), (0, ache_length))  # ache
    )

    legs_positions = (
        (CENTRE + ache_thickness - 1, CENTRE - ache_thickness + 1),
        (CENTRE - ache_thickness + 1, CENTRE - ache_thickness + 1),
        (CENTRE, CENTRE + leg_thickness)
    )

    leg_right = get_body_part(legs_end_points[0], leg_thickness, leg_mass, legs_positions[0], friction)
    leg_left = get_body_part(legs_end_points[1], leg_thickness, leg_mass, legs_positions[1], friction)
    ache = get_body_part(legs_end_points[2], ache_thickness, ache_mass, legs_positions[2], friction)

    rotation_joint_2 = pymunk.PinJoint(leg_right[0], ache[0], (0, 0), (0, 0))
    rotation_joint_3 = pymunk.PinJoint(leg_left[0], ache[0], (0, 0), (0, 0))

    space.add(leg_right[0], leg_right[1],
              leg_left[0], leg_left[1],
              ache[0], ache[1],
              rotation_joint_2, rotation_joint_3)

    force = 100
    while True:
        pressed = pygame.key.get_pressed()
        # ache control
        if pressed[pygame.K_KP1]:
            ache[0].apply_force_at_local_point((-force, 0), legs_end_points[2][0])
        if pressed[pygame.K_KP3]:
            ache[0].apply_force_at_local_point((force, 0), legs_end_points[2][0])
        if pressed[pygame.K_KP7]:
            ache[0].apply_force_at_local_point((-force, 0), legs_end_points[2][1])
        if pressed[pygame.K_KP9]:
            ache[0].apply_force_at_local_point((force, 0), legs_end_points[2][1])

        # left_leg control
        if pressed[pygame.K_z]:
            leg_left[0].apply_force_at_local_point((-sinus * force, cosinus * force), legs_end_points[1][1])
        if pressed[pygame.K_x]:
            leg_left[0].apply_force_at_local_point((sinus * force, -cosinus * force), legs_end_points[1][1])

        # right_leg control
        if pressed[pygame.K_n]:
            leg_right[0].apply_force_at_local_point((-sinus * force, -cosinus * force), legs_end_points[0][1])
        if pressed[pygame.K_m]:
            leg_right[0].apply_force_at_local_point((sinus * force, cosinus * force), legs_end_points[0][1])

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)

            """
            # ache control
            if event.type == KEYDOWN and event.key == K_KP1:
                ache[0].apply_impulse_at_local_point((-force, 0), legs_end_points[2][0])
            if event.type == KEYDOWN and event.key == K_KP3:
                ache[0].apply_impulse_at_local_point((force, 0), legs_end_points[2][0])
            if event.type == KEYDOWN and event.key == K_KP7:
                ache[0].apply_impulse_at_local_point((-force, 0), legs_end_points[2][1])
            if event.type == KEYDOWN and event.key == K_KP9:
                ache[0].apply_impulse_at_local_point((force, 0), legs_end_points[2][1])

            # left_leg control
            if event.type == KEYDOWN and event.key == K_z:
                leg_left[0].apply_impulse_at_local_point((-sinus * force, cosinus * force), legs_end_points[1][1])
            if event.type == KEYDOWN and event.key == K_x:
                leg_left[0].apply_impulse_at_local_point((sinus * force, -cosinus * force), legs_end_points[1][1])

            # right_leg control
            if event.type == KEYDOWN and event.key == K_n:
                leg_right[0].apply_impulse_at_local_point((-sinus * force, -cosinus * force), legs_end_points[0][1])
            if event.type == KEYDOWN and event.key == K_m:
                leg_right[0].apply_impulse_at_local_point((sinus * force, cosinus * force), legs_end_points[0][1])
            """

        screen.fill((0, 0, 0))
        space.debug_draw(draw_options)
        space.step(1 / 100.0)
        pygame.display.flip()
        clock.tick(50)


if __name__ == '__main__':
    main()
