from board.EnemyMap import EnemyMap
from board.FriendlyMap import FriendlyMap
from gamedataclasses.Coordinates import Coordinates
from random import randint

class RandomStrategy:

    def __init__(self) -> None:
        pass

    def get_next_move(self, enemy_map : EnemyMap, memory : list) -> Coordinates:
        memory.clear()
        return Coordinates(randint(0,9),randint(0,9))

    def get_next_placement(self, friendly_map : FriendlyMap, ship_size : int) -> tuple:
        return [Coordinates(randint(0,9),randint(0,9)),[True,False][randint(0,1)]]