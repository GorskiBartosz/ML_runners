from Character import Character
from globals import SCREEN_SIZE, FPS, STEP_TIME, CROSSHAIRS_SIZE, WALL_WIDTH, \
    COLLISION_GROUP, flipy
from pymunk import pygame_util
import pygame
import pymunk

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
draw_options = pymunk.pygame_util.DrawOptions(screen)

pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(pygame.color.THECOLORS["white"])

me = Character()

space = pymunk.Space()
space.gravity = (0.0, -900.0)

# add walls

walls = [pymunk.Segment(space.static_body, (0, 0 + WALL_WIDTH), (SCREEN_SIZE, 0 + WALL_WIDTH), WALL_WIDTH),  # bottom
         pymunk.Segment(space.static_body, (0, 0), (0, SCREEN_SIZE), WALL_WIDTH),  # left
         pymunk.Segment(space.static_body, (0, SCREEN_SIZE), (SCREEN_SIZE, SCREEN_SIZE), WALL_WIDTH),  # top
         pymunk.Segment(space.static_body, (SCREEN_SIZE - WALL_WIDTH, 0), (SCREEN_SIZE - WALL_WIDTH, SCREEN_SIZE),
                        WALL_WIDTH)  # right
         ]

for w in walls:
    w.color = pygame.color.THECOLORS["black"]
    w.friction = 1.0
    w.group = COLLISION_GROUP["wall"]

space.add(walls)
space.add(me.bodies, me.body_shapes, me.joints)
space.add(me.gun.body, me.gun.body_shape, me.gun_constraints)

# add crosshairs at the location of the mouse
pointer_body = pymunk.Body()
pointer_shape1 = pymunk.Segment(pointer_body, (0, CROSSHAIRS_SIZE), (0, -CROSSHAIRS_SIZE), 1)  # vertical segment
pointer_shape2 = pymunk.Segment(pointer_body, (-CROSSHAIRS_SIZE, 0), (CROSSHAIRS_SIZE, 0), 1)  # horizontal segment

# add a spring that will angle the gun toward the mouse
spring = pymunk.constraint.DampedRotarySpring(me.gun.body, pointer_body, 0, 125000., 6000.)

space.add(pointer_shape1, pointer_shape2, spring)

while True:
    # handle event queue
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            # update location of pointer
            pointer_body.position = pygame_util.get_mouse_pos(screen)
            # update angle of pointer
            pointer_body.angle = (pointer_body.position - me.gun.body.position).angle

        elif event.type == pygame.MOUSEBUTTONDOWN:
            me.shoot_gun()

    # the gun is constrained to the right hand, which is a rogue body
    me.update_hand_position()

    screen.fill((0, 0, 0))

    space.debug_draw(draw_options)

    space.step(STEP_TIME)

    pygame.display.flip()
    clock.tick(FPS)
