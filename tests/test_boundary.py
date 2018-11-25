from processors import TrackBoundary
from components import Point


def test_tb_contains_1():
    p = Point(1, 1)
    track = TrackBoundary((0, 0), (2, 2))
    assert p in track


def test_tb_contains_2():
    p = Point(2, 2)
    track = TrackBoundary((0, 0), (2, 2))
    assert p in track


def test_tb_contains_3():
    p = Point(3, 3)
    track = TrackBoundary((0, 0), (2, 2))
    assert p not in track


def test_tb_crash_1():
    p_old = Point(1, 1)
    p_new = Point(3, 4)
    track = TrackBoundary((0, 0), (2, 2))
    assert p_new not in track
    cp = track.crash_position(p_old, p_new)
    assert cp.y == 2


def test_tb_crash_2():
    p_old = Point(1, 1)
    p_new = Point(4, 3)
    track = TrackBoundary((0, 0), (2, 2))
    assert p_new not in track
    cp = track.crash_position(p_old, p_new)
    assert cp.x == 2
