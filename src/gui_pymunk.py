from math import degrees

import pyglet
import pymunk
from pymunk.pyglet_util import DrawOptions

options = DrawOptions()
space = pymunk.Space()
space.gravity = 0, -100

circle_position = (1100, 600)
circle_radius = 59
circle_friction = 5.0
path = "../res/levi_circle.png"
mass = 1

window = pyglet.window.Window(1280, 700, "Shapes with physics", resizable=False)


def update(dt):
    space.step(dt)
    circle_texture_sprite.position = circle_body.position
    circle_texture_sprite.rotation = degrees(-circle_body.angle)


@window.event
def on_mouse_press(x, y, button, modifiers):
    print x, y
    tuple_circle = get_circle(x, y)
    space.add(tuple_circle[0], tuple_circle[1])


@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)
    circle_texture_sprite.draw()
    for shape in space.shapes:
        if shape.body.position.y < -100:
            space.remove(shape, shape.body)
            print("bodies left: " + str(space.shapes.__len__() - 2))


def basic_shapes():
    print("hello:shapes")

    # BASIC CONFIGURATION OF SHAPES
    square_size = (50, 50)
    square_position = (200, 600)

    segment_vertices = ((0, 0), (0, 300))
    segment_position = (600, 600)
    segment_radius = 3

    triangle_vertices = ((0, 0), (0, 100), (100, 0))
    triangle_position = (650, 600)

    # SQUARE
    square_shape = pymunk.Poly.create_box(None, size=square_size)
    square_moment = pymunk.moment_for_poly(mass, vertices=square_shape.get_vertices())
    square_body = pymunk.Body(mass, square_moment)
    square_shape.body = square_body
    square_body.position = square_position

    # CIRCLE
    circle_shape = pymunk.Circle(None, radius=circle_radius)
    circle_moment = pymunk.moment_for_circle(mass, 0, circle_radius)
    circle_body = pymunk.Body(mass, circle_moment)
    circle_shape.body = circle_body
    circle_body.position = circle_position

    # SEGMENT
    segment_moment = pymunk.moment_for_segment(mass, segment_vertices[0], segment_vertices[1], 3)
    segment_body = pymunk.Body(mass, segment_moment)
    segment_shape = pymunk.Segment(segment_body, segment_vertices[0], segment_vertices[1], radius=segment_radius)
    segment_body.position = segment_position

    # TRIANGLE
    triangle_moment = pymunk.moment_for_poly(mass, triangle_vertices)
    triangle_body = pymunk.Body(mass, triangle_moment)
    triangle_shape = pymunk.Poly(triangle_body, vertices=triangle_vertices)
    triangle_body.position = triangle_position

    # ADDING ALL SHAPES TO A SPACE
    space.add(square_body, square_shape,
              circle_body, circle_shape,
              segment_body, segment_shape,
              triangle_body, triangle_shape)


def get_circle(x, y, radius=circle_radius, circle_mass=mass, friction=circle_friction, file_path=path):
    shape = pymunk.Circle(None, radius=radius)
    moment = pymunk.moment_for_circle(circle_mass, 0, radius)
    body = pymunk.Body(circle_mass, moment)
    shape.body = body
    body.position = (x, y)
    shape.friction = friction

    texture = pyglet.image.load(file_path)
    texture.anchor_x = texture.width / 2
    texture.anchor_y = texture.height / 2
    sprite = pyglet.sprite.Sprite(texture, x=x, y=y)

    return shape, body, sprite


circle_tuple = get_circle(circle_position[0], circle_position[1], circle_mass=mass*10)
space.add(circle_tuple[0], circle_tuple[1])
circle_body = circle_tuple[1]
circle_texture_sprite = circle_tuple[2]


def basic_physics():
    print("hello:physics")

    # BASIC CONFIGURATION OF SHAPES
    square_size = (120, 120)
    square_position = (900, 600)
    square_elasticity = 0.6

    triangle_vertices = ((0, 0), (20, 80), (80, 20))
    triangle_position = (650, 600)

    segment_vertices_1 = ((0, 0), (400, 50))
    segment_position_1 = (800, 400)
    segment_radius = 3

    segment_vertices_2 = ((0, 0), (500, -70))
    segment_position_2 = (300, 300)

    # SQUARE
    square_shape = pymunk.Poly.create_box(None, size=square_size)
    square_moment = pymunk.moment_for_poly(mass, vertices=square_shape.get_vertices())
    square_body = pymunk.Body(mass, square_moment)
    square_shape.body = square_body
    square_shape.elasticity = square_elasticity
    square_body.position = square_position
    space.add(square_shape, square_body)

    # TRIANGLE
    triangle_moment = pymunk.moment_for_poly(mass, triangle_vertices)
    triangle_body = pymunk.Body(mass, triangle_moment)
    triangle_shape = pymunk.Poly(triangle_body, vertices=triangle_vertices)
    triangle_body.position = triangle_position
    triangle_shape.elasticity = square_elasticity
    space.add(triangle_shape, triangle_body)

    # SEGMENT_1
    segment_shape = pymunk.Segment(space.static_body, segment_vertices_1[0], segment_vertices_1[1],
                                   radius=segment_radius)
    segment_shape.body.position = segment_position_1
    segment_shape.elasticity = square_elasticity
    segment_shape.friction = circle_friction
    space.add(segment_shape)

    # SEGMENT_2
    segment_shape_2 = pymunk.Segment(space.static_body, segment_vertices_2[0], segment_vertices_2[1],
                                     radius=segment_radius)
    segment_shape_2.body.position = segment_position_2
    segment_shape_2.elasticity = square_elasticity
    segment_shape_2.friction = circle_friction
    space.add(segment_shape_2)


def triangle_experiment():
    print("IT DOESNT WORK")

    triangle_vertices = ((0, 0), (50, 0), (50, 50))
    triangle_moment = pymunk.moment_for_poly(mass, triangle_vertices)
    triangle_body = pymunk.Body(mass, triangle_moment)
    triangle_shape = pymunk.Poly(triangle_body, vertices=triangle_vertices)
    triangle_body.position = 200, 400
    space.add(triangle_body, triangle_shape)

    segment_shape = pymunk.Segment(None, (0, 0), (500, 50), radius=3)
    segment_body = pymunk.Body(mass, 1800, pymunk.Body.STATIC)
    segment_body.position = 100, 300
    segment_shape.body = segment_body
    segment_shape.elasticity = 1.0
    segment_shape.friction = 1.0
    space.add(segment_shape)
