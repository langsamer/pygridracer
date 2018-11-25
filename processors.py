import esper
from utils import Rectangle
from components import *


class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        vel: Velocity
        pos: CurrentPosition
        newpos: NextPosition
        entities = self.world.get_components(Velocity, CurrentPosition, NextPosition)
        for ent, (vel, pos, newpos) in entities:
            newpos.x = pos.x + vel.dx
            newpos.y = pos.y + vel.dy


def last_legal_pos(pos: CurrentPosition, newpos: NextPosition) -> Point:
    return newpos


class TrackBoundary(Rectangle):
    def __init__(self, top_left, bottom_right):
        """
        Represent the track (for the time being: a rectangle)

        :param top_left:  top left corner of rectangle
        :param bottom_right: bottom left corner of rectangle
        """
        super().__init__(top_left[0], top_left[1], bottom_right[0], bottom_right[1])

    def _extrapolate(self, oldpos, newpos):
        m = (newpos.y - oldpos.y) / (newpos.x - oldpos.x)
        cross_y0 = oldpos.y + m * (self.x0 - oldpos.x)
        cross_y1 = oldpos.y + m * (self.x1 - oldpos.x)
        cross_x0 = oldpos.x + (self.y0 - oldpos.y) / m
        cross_x1 = oldpos.x + (self.y1 - oldpos.y) / m
        intersections = []
        if self.y0 <= cross_y0 <= self.y1:
            intersections.append((self.x0, cross_y0))
        if self.y0 <= cross_y1 <= self.y1:
            intersections.append((self.x1, cross_y1))
        if self.x0 <= cross_x0 <= self.x1:
            intersections.append((cross_x0, self.y0))
        if self.x0 <= cross_x1 <= self.x1:
            intersections.append((cross_x1, self.y1))

        return [point for point in intersections
                if point in self and point in Rectangle(oldpos.x, oldpos.y, newpos.x, newpos.y)]

    def crash_position(self, oldpos, newpos):
        """Find the point closest to the intersection of the line from oldpos to newpos
        with the edges for the track."""
        if oldpos in self and newpos not in self:
            crashpos = self._extrapolate(oldpos, newpos)[0]
            newpos.x = crashpos[0]
            newpos.y = crashpos[1]
        return newpos


class LoggingProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        pos: CurrentPosition
        newpos: NextPosition
        entities = self.world.get_components(CurrentPosition, NextPosition)
        for ent, (pos, newpos) in entities:
            print(f"{pos} -> {newpos}")