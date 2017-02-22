"""A module of funtions dealing with angles in pygame.
    All functions (other than project) take lists or tuples
    of pygame coordinates as origin, destination
    and return the appropriate angle in radians."""


from math import pi, hypot, cos, sin, atan2


def get_distance(origin, destination):
    """Returns distance from origin to destination."""
    return hypot(destination[0] - origin[0],
                 destination[1] - origin[1])


def get_angle(origin, destination):
    """Returns angle in radians from origin to destination.
        This is the angle that you would get if the points were
        on a cartesian grid. Arguments of (0,0), (1, -1)
        return pi/4 (45 deg) rather than  7/4.
        """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return atan2(-y_dist, x_dist) % (2 * pi)


def get_xaxis_reflection(origin, destination):
    """Returns angle in radians reflected on x-axis. This is the
        reflection angle of a top or bottom collision."""
    x_dist = origin[0] - destination[0]
    y_dist = origin[1] - destination[1]
    return atan2(-y_dist, -x_dist) % (2 * pi)


def get_yaxis_reflection(origin, destination):
    """Returns angle in radians reflected on y-axis.
        This is the angle of reflection for a side collision."""
    x_dist = origin[0] - destination[0]
    y_dist = origin[1] - destination[1]
    return atan2(y_dist, x_dist) % (2 * pi)


def get_opposite_angle(origin, destination):
    """Returns angle in radians from destination to origin."""
    x_dist = origin[0] - destination[0]
    y_dist = origin[1] - destination[1]
    return atan2(-y_dist, x_dist) % (2 * pi)


def project(pos, angle, distance):
    """
    Returns tuple of pos projected distance at angle
    adjusted for pygame's y-axis.

    EXAMPLES

    Move a sprite using it's angle and speed
    new_pos = project(sprite.pos, sprite.angle, sprite.speed)

    Find the relative x and y components of an angle and speed
    x_and_y = project((0, 0), angle, speed)
    """
    return (pos[0] + (cos(angle) * distance),
            pos[1] - (sin(angle) * distance))

