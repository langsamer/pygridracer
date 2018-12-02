# -*- coding: utf-8 -*-
"""
Python implementation of an algorithm described in:
http://www.geomalgorithms.com/a05-_intersect-1.html#intersect2D_2Segments()
I only deal with 2d objects, though

Created on Mon Nov 26 14:28:54 2018

@author: Malte Plath
"""

EPSILON = 1e-8  # close enough to zero


class Vector2:
    def __init__(self, x, y=None):
        if y is None:
            assert isinstance(x, Vector2)
            x, y = x.x, x.y
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Two Vectors are equal if they are equal in all their coordinates"""
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        """Add two Vectors by adding the x and y coordinates separately"""
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Subtract one point from another by subtracting coordinate-wise"""
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """Multiply a Vector2 with a number"""
        return Vector2(other * self.x, other * self.y)

    def __rmul__(self, other):
        """Multiply a number with a Vector2"""
        return Vector2(other * self.x, other * self.y)

    def __matmul__(self, other):
        """Matrix multiplication of two vector (of same dimension) is the dot product"""
        return self.x * other.x + self.y * other.y

    def perp(self):
        """Perpendicular vector"""
        return Vector2(-self.y, self.x)

    def cross(self, other):
        """Return the z coordinate of the cross product of two 2D lines embedded into
        3D space in the plane z=0"""
        return self.x * other.y - self.y * other.x  # == self.perp() @ other

    def __repr__(self):
        return "Vector2({0.x}, {0.y})".format(self)

    def __getitem__(self, index):
        """allow getting the coordinates by index"""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Vector2 has only two components")


class Line:
    """A line segment defined by starting point and end point"""
    def __init__(self, v0: Vector2, v1: Vector2):
        self.v0 = v0
        self.v1 = v1

    def direction(self) -> Vector2:
        """Return the directional vector of the line"""
        return self.v1 - self.v0

    def __matmul__(self, other) -> float:
        """Scalar product of the directions of two lines"""
        return self.direction() @ other.direction()

    def cross(self, other) -> float:
        """Return the z coordinate of the cross product of two 2D lines embedded into
        3D space in the plane z=0"""
        return self.direction().cross(other.direction())

    def __contains__(self, point: Vector2):
        """Determine if a point is inside a segment, if we already know that
        the point is on the infinite line defined by the segment.
        """
        if self.v0.x != self.v1.x:  # line is not vertical
            if self.v0.x <= point.x <= self.v1.x:
                return True
            if self.v1.x <= point.x <= self.v0.x:
                return True
        else:  # line is vertical, so test the y coordinate
            if self.v0.y <= point.y <= self.v1.y:
                return True
            if self.v1.y <= point.y <= self.v0.y:
                return True


class Rectangle:
    def __init__(self, top_left: Vector2, bottom_right: Vector2):
        self.x0 = top_left.x
        self.y0 = top_left.y
        self.x1 = bottom_right.x
        self.y1 = bottom_right.y

    @classmethod
    def from_line(cls, line: Line):
        return Rectangle(line.v0, line.v1)


def intersect_2d_segments(seg1: Line, seg2: Line):
    u = seg1.direction()
    v = seg2.direction()
    w = Vector2(seg1.v0 - seg2.v0)  # direction from base of seg2 to base of seg1
    d = u.cross(v)
    
    if abs(d) < EPSILON:  # seg1 and seg2 are parallel
        # if they were colinear, the connection vector would be parallel to the
        # direction of both segments
        if abs(u.cross(w)) > EPSILON or abs(v.cross(w)) > EPSILON:
            return None

        # they are colinear or degenerate: check if they are degenerate Vectors
        du, dv = u @ u, v @ v  # square of length
        if du == 0 and dv == 0:  # both segments are just points
            if seg1.v0 != seg2.v0:  # they are distinct points
                return None
            else:  # they are the same point
                return seg1.v0
        elif du == 0:  # seg1 is a single point
            # we know seg1 and seg2 are colinear, so we only need to check
            # if seg1 is inside the boundaries defined by seg2
            if in_segment(seg1.v0, seg2):
                return seg1.v0
            else:
                return None
        elif dv == 0:  # seg2 is a single point
            # we know seg1 and seg2 are colinear, so we only need to check
            # if seg2 is inside the boundaries defined by seg1
            if in_segment(seg2.v0, seg1):
                return seg2.v0
            else:
                return None

        # they are colinear segments: return overlap (if it exists)
        # we calculate the points on seg2 that delimit the overlap
        w2 = Vector2(seg1.v1 - seg2.v0)
        if v.x != 0:  # avoid division by zero
            t0 = w.x / v.x
            t1 = w2.x / v.x
        else:  # seg2 is vertical: use y coordinate
            t0 = w.y / v.y
            t1 = w2.y / v.y
        if t0 > t1:  # swap
            t0, t1 = t1, t0
        if t0 > 1 or t1 < 0:  # no overlap
            return None
        t0 = max(0, t0)
        t1 = min(1, t1)
        if t0 == t1:  # intersection is a point
            intersection_point = seg2.v0 + t0 * v
            return intersection_point
        # they overlap in a proper subsegment
        intersection_start = seg2.v0 + t0 * v
        intersection_end = seg2.v0 + t1 * v
        return Line(intersection_start, intersection_end)
    else:  # the segments are skew and may intersect in a point
        si = v.cross(w) / d  # project v onto u
        if si < 0 or si > 1:  # no intersection with seg1
            return None
        # get the intersection parameter for seg2
        ti = u.cross(v) / d  # project u onto v
        if ti < 0 or ti > 1:  # no intersection with seg2
            return None
        
        intersection_point = seg1.v0 + si * u
        return intersection_point


def in_segment(point, line):
    """Determine if a point is inside a segment, if we already know that
    the point is on the infinite line defined by the segment.
    """
    if line.v0.x != line.v1.x:  # line is not vertical
        if line.v0.x <= point.x <= line.v1.x:
            return True
        if line.v1.x <= point.x <= line.v0.x:
            return True
    else:  # line is vertical, so test the y coordinate
        if line.v0.y <= point.y <= line.v1.y:
            return True
        if line.v1.y <= point.y <= line.v0.y:
            return True

