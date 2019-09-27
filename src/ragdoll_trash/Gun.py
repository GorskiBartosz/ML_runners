from globals import GUN_VELOCITY_LIMIT, GUN_ANGULAR_VELOCITY_LIMIT
import pygame
import pymunk


class Gun(pygame.sprite.Sprite):
    """ Describes a gun held by a Character.
        For now, this is just a line segment. """
    _gun_types = {"pistol": {"length": 5,
                             "thickness": 1,
                             "mass": 1,
                             "force": 5,  # force exerted upon firing
                             "handle": (5, 0)
                             # relative coordinates of the point at which the gun attaches to a Character's hand
                             }
                  }

    def __init__(self, gun_type="pistol"):
        # set gun attributes

        gun_attrs = self._gun_types[gun_type]
        l = self.length = gun_attrs["length"]
        t = self.thickness = gun_attrs["thickness"]
        m = self.mass = gun_attrs["mass"]
        mo = self.moment = pymunk.moment_for_box(m, (l, t))
        f = self.force = gun_attrs["force"]
        h = self.handle = gun_attrs["handle"]

        # pygame init

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([l, t])
        self.rect = self.image.get_rect()

        # pymunk init

        self.body = pymunk.Body(m, mo)
        self.body_shape = pymunk.Poly(self.body, [(0, 0), (0, -t), (l, -t), (l, 0)])
        self.body_shape.color = pygame.color.THECOLORS["black"]

        self.body.velocity_limit = GUN_VELOCITY_LIMIT
        self.body.angular_velocity_limit = GUN_ANGULAR_VELOCITY_LIMIT
