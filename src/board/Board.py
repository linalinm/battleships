from gamedataclasses.Coordinates import Coordinates
from board.EnemyMap import EnemyMap
from board.FriendlyMap import FriendlyMap


class Board:

    def __init__(self, size : Coordinates = Coordinates(10,10)) -> None:
        self._friendly = FriendlyMap(size)
        self._enemy = EnemyMap(size)

    @property
    def friendly(self):
        return self._friendly

    @property
    def enemy(self):
        return self._enemy

    