import esper
from components import *
from processors import *


def run_game():
    world = esper.World()
    movement_processor = MovementProcessor()
    crash_processor = TrackBoundary()
    log_processor = LoggingProcessor()
    world.add_processor(movement_processor, priority=1)
    world.add_processor(crash_processor, priority=2)
    world.add_processor(log_processor, priority=3)

    player1 = world.create_entity(CurrentPosition(5, 0), Velocity(2, 0), NextPosition(1, 1))
    player2 = world.create_entity(CurrentPosition(6, 0), Velocity(0, 2), NextPosition(0, 0))

    world.process()

    p1 = world.component_for_entity(player1, CurrentPosition)
    print(p1)
    p1 = world.component_for_entity(player1, NextPosition)
    print(p1)

    world.process()

    p1 = world.component_for_entity(player1, CurrentPosition)
    print(p1)
    p1 = world.component_for_entity(player1, NextPosition)
    print(p1)


if __name__ == '__main__':
    run_game()
