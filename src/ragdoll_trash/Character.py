from Gun import Gun
from globals import *
import pygame
import pymunk


class Character(pygame.sprite.Sprite):
    """ Describes a moving character ingame made up of pymunk bodies/shapes. """

    def __init__(self, body_type="ragdoll", w=10, h=10, m=1, mo=1, pos=(SCREEN_SIZE / 2, SCREEN_SIZE / 2)):

        # pygame init

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, h])
        self.rect = self.image.get_rect()

        # pymunk init

        # construct the character's body here
        # need PinJoint and RotaryLimitJoint between the gun and the character to keep them stuck together
        if body_type == "square":
            # for testing

            self.right_hand = pymunk.Body(m, mo)
            self.right_hand.position = pos

            # poly vertices are ordered counterclockwise
            # pymunk coordinates: positive (x,y) is quadrant 4, i.e. bottom right
            self.right_hand_shape = pymunk.Poly(self.right_hand, [(0, 0), (0, -h), (w, -h),
                                                                  (w, 0)])  # vertices are ordered counterclockwise

            self.bodies = [self.right_hand]
            self.body_shapes = [self.right_hand_shape]

        elif body_type == "ragdoll":

            # create the body pieces

            head = pymunk.Body(HEAD_MASS, HEAD_MOMENT)
            torso = pymunk.Body(TORSO_MASS, TORSO_MOMENT)
            upper_arm_l = pymunk.Body(UPPER_ARM_MASS, UPPER_ARM_MOMENT)
            upper_arm_r = pymunk.Body(UPPER_ARM_MASS, UPPER_ARM_MOMENT)
            lower_arm_l = pymunk.Body(LOWER_ARM_MASS, LOWER_ARM_MOMENT)
            lower_arm_r = pymunk.Body(LOWER_ARM_MASS, LOWER_ARM_MOMENT)
            upper_leg_l = pymunk.Body(UPPER_LEG_MASS, UPPER_LEG_MOMENT)
            upper_leg_r = pymunk.Body(UPPER_LEG_MASS, UPPER_LEG_MOMENT)
            lower_leg_l = pymunk.Body(LOWER_LEG_MASS, LOWER_LEG_MOMENT)
            lower_leg_r = pymunk.Body(LOWER_LEG_MASS, LOWER_LEG_MOMENT)

            self.bodies = [head,
                           torso,
                           upper_arm_l,
                           upper_arm_r,
                           lower_arm_l,
                           lower_arm_r,
                           upper_leg_l,
                           upper_leg_r,
                           lower_leg_l,
                           lower_leg_r
                           ]

            # give the body pieces shapes

            head_shape = pymunk.Circle(head, HEAD_RADIUS)
            torso_shape = pymunk.Poly(torso,
                                      [(0, 0), (0, TORSO_LENGTH), (BODY_THICKNESS, TORSO_LENGTH), (BODY_THICKNESS, 0)])
            upper_arm_l_shape = pymunk.Poly(upper_arm_l,
                                            [(0, 0), (0, UPPER_ARM_LENGTH), (BODY_THICKNESS, UPPER_ARM_LENGTH),
                                             (BODY_THICKNESS, 0)])
            upper_arm_r_shape = pymunk.Poly(upper_arm_r,
                                            [(0, 0), (0, UPPER_ARM_LENGTH), (BODY_THICKNESS, UPPER_ARM_LENGTH),
                                             (BODY_THICKNESS, 0)])
            lower_arm_l_shape = pymunk.Poly(lower_arm_l,
                                            [(0, 0), (0, LOWER_ARM_LENGTH), (BODY_THICKNESS, LOWER_ARM_LENGTH),
                                             (BODY_THICKNESS, 0)])
            lower_arm_r_shape = pymunk.Poly(lower_arm_r,
                                            [(0, 0), (0, LOWER_ARM_LENGTH), (BODY_THICKNESS, LOWER_ARM_LENGTH),
                                             (BODY_THICKNESS, 0)])
            upper_leg_l_shape = pymunk.Poly(upper_leg_l,
                                            [(0, 0), (0, UPPER_LEG_LENGTH), (BODY_THICKNESS, UPPER_LEG_LENGTH),
                                             (BODY_THICKNESS, 0)])
            upper_leg_r_shape = pymunk.Poly(upper_leg_r,
                                            [(0, 0), (0, UPPER_LEG_LENGTH), (BODY_THICKNESS, UPPER_LEG_LENGTH),
                                             (BODY_THICKNESS, 0)])
            lower_leg_l_shape = pymunk.Poly(lower_leg_l,
                                            [(0, 0), (0, LOWER_LEG_LENGTH), (BODY_THICKNESS, LOWER_LEG_LENGTH),
                                             (BODY_THICKNESS, 0)])
            lower_leg_r_shape = pymunk.Poly(lower_leg_r,
                                            [(0, 0), (0, LOWER_LEG_LENGTH), (BODY_THICKNESS, LOWER_LEG_LENGTH),
                                             (BODY_THICKNESS, 0)])

            self.body_shapes = [head_shape,
                                torso_shape,
                                upper_arm_l_shape,
                                upper_arm_r_shape,
                                lower_arm_l_shape,
                                lower_arm_r_shape,
                                upper_leg_l_shape,
                                upper_leg_r_shape,
                                lower_leg_l_shape,
                                lower_leg_r_shape
                                ]

            for s in self.body_shapes:
                s.color = pygame.color.THECOLORS["black"]
                s.group = COLLISION_GROUP["character"]

            # set positions of bodies

            offset = 0

            torso.position = pos
            head.position = (torso.position.x, torso.position.y + TORSO_LENGTH / 2 + HEAD_RADIUS + offset)
            upper_arm_l.position = (torso.position.x - offset, torso.position.y + TORSO_LENGTH / 2)
            upper_arm_r.position = (torso.position.x + offset, torso.position.y + TORSO_LENGTH / 2)
            lower_arm_l.position = (upper_arm_l.position.x - offset, upper_arm_l.position.y - UPPER_ARM_LENGTH / 2)
            lower_arm_r.position = (upper_arm_r.position.x + offset, upper_arm_r.position.y - UPPER_ARM_LENGTH / 2)
            upper_leg_l.position = (torso.position.x - offset, torso.position.y - TORSO_LENGTH / 2)
            upper_leg_r.position = (torso.position.x + offset, torso.position.y - TORSO_LENGTH / 2)
            lower_leg_l.position = (upper_leg_l.position.x - offset, upper_leg_l.position.y - UPPER_LEG_LENGTH / 2)
            lower_leg_r.position = (upper_leg_r.position.x + offset, upper_leg_r.position.y - UPPER_LEG_LENGTH / 2)

            # link pieces of the body together
            # attach bodies at midpoints of edges
            self.joints = [pymunk.PivotJoint(head, torso, (0, -HEAD_RADIUS), (BODY_THICKNESS / 2, 0)),
                           pymunk.PivotJoint(torso, upper_arm_l, (0, 0), (BODY_THICKNESS / 2, 0)),
                           pymunk.PivotJoint(torso, upper_arm_r, (BODY_THICKNESS, 0), (BODY_THICKNESS / 2, 0)),
                           pymunk.PivotJoint(upper_arm_l, lower_arm_l, (BODY_THICKNESS / 2, UPPER_ARM_LENGTH),
                                             (BODY_THICKNESS / 2, 0)),
                           pymunk.PivotJoint(upper_arm_r, lower_arm_r, (BODY_THICKNESS / 2, UPPER_ARM_LENGTH),
                                             (BODY_THICKNESS / 2, 0)),
                           pymunk.PivotJoint(torso, upper_leg_l, (0, TORSO_LENGTH), (BODY_THICKNESS / 2, 0)),
                           pymunk.PivotJoint(torso, upper_leg_r, (BODY_THICKNESS, TORSO_LENGTH),
                                             (BODY_THICKNESS / 2, 0)),
                           pymunk.PivotJoint(upper_leg_l, lower_leg_l, (BODY_THICKNESS / 2, UPPER_LEG_LENGTH),
                                             (BODY_THICKNESS / 2, 0)),
                           pymunk.PivotJoint(upper_leg_r, lower_leg_r, (BODY_THICKNESS / 2, UPPER_LEG_LENGTH),
                                             (BODY_THICKNESS / 2, 0))
                           ]

            # set joint rotation constraints

            neck_rot = pymunk.RotaryLimitJoint(head, torso, NECK_ROTATION_MIN, NECK_ROTATION_MAX)
            shoulder_rot_l = pymunk.RotaryLimitJoint(torso, upper_arm_l, SHOULDER_L_ROTATION_MIN,
                                                     SHOULDER_L_ROTATION_MAX)
            shoulder_rot_r = pymunk.RotaryLimitJoint(torso, upper_arm_r, SHOULDER_R_ROTATION_MIN,
                                                     SHOULDER_R_ROTATION_MAX)
            elbow_rot_l = pymunk.RotaryLimitJoint(upper_arm_l, lower_arm_l, ELBOW_L_ROTATION_MIN, ELBOW_L_ROTATION_MAX)
            elbow_rot_r = pymunk.RotaryLimitJoint(upper_arm_r, lower_arm_r, ELBOW_R_ROTATION_MIN, ELBOW_R_ROTATION_MAX)
            hip_rot_l = pymunk.RotaryLimitJoint(torso, upper_leg_l, HIP_L_ROTATION_MIN, HIP_L_ROTATION_MAX)
            hip_rot_r = pymunk.RotaryLimitJoint(torso, upper_leg_r, HIP_R_ROTATION_MIN, HIP_R_ROTATION_MAX)
            knee_rot_l = pymunk.RotaryLimitJoint(upper_leg_l, lower_leg_l, KNEE_L_ROTATION_MIN, KNEE_L_ROTATION_MAX)
            knee_rot_r = pymunk.RotaryLimitJoint(upper_leg_r, lower_leg_r, KNEE_R_ROTATION_MIN, KNEE_R_ROTATION_MAX)

            self.joints.extend([neck_rot,
                                shoulder_rot_l,
                                shoulder_rot_r,
                                elbow_rot_l,
                                elbow_rot_r,
                                hip_rot_l,
                                hip_rot_r,
                                knee_rot_l,
                                knee_rot_r
                                ])

            # finally done creating the body! phew!
            # now we just have to create the location at which the ragdoll holds its gun

            self.right_hand = pymunk.Body()
            self.right_hand.position = (
                lower_arm_l.position.x + BODY_THICKNESS / 2, lower_arm_l.position.y + LOWER_ARM_LENGTH)
            self.joints.append(pymunk.PivotJoint(lower_arm_r, self.right_hand, self.right_hand.position))

            # now we're done at last!

        # locate the gun at the character's right hand
        self.gun = Gun("pistol")
        self.gun.body.position = self.right_hand.position
        self.gun_constraints = [pymunk.PivotJoint(self.right_hand, self.gun.body, (0, 0), self.gun.handle),
                                # stick 'em together
                                pymunk.RotaryLimitJoint(self.right_hand, self.gun.body, 0, 0)  # don't pivot at all
                                ]

        for b in self.bodies:
            b.velocity_limit = CHARACTER_VELOCITY_LIMIT
            b.angular_velocity_limit = CHARACTER_ANGULAR_VELOCITY_LIMIT

        for b in self.body_shapes:
            b.color = pygame.color.THECOLORS["black"]
            b.friction = BODY_FRICTION

    def update(self):
        self.gun.update()

    def update_hand_position(self):
        # body #4 is the left lower arm, don't care about fixing this right now
        self.right_hand.position = (
            self.bodies[4].position.x + BODY_THICKNESS / 2, self.bodies[4].position.y + LOWER_ARM_LENGTH)

    def shoot_gun(self):
        f = pymunk.vec2d.Vec2d(self.gun.force, 0)
        f.angle = self.gun.body.angle
        print f
        # self.bodies[4].apply_impulse(f, (BODY_THICKNESS / 2, LOWER_ARM_LENGTH))
        self.bodies[4].apply_impulse_at_local_point(f, (BODY_THICKNESS / 2, LOWER_ARM_LENGTH))
