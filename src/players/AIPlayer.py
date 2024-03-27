



from entities.Ship import Ship
from exceptions.ExceptionsEnum import MapException
from players.Player import Player
from strategies.RandomStrategy import RandomStrategy


class AIPlayer(Player):
    
    def __init__(self,strategy : RandomStrategy) -> None:
        super().__init__()
        self.strategy = strategy
        self._memory = []

    def move(self) -> None:
        result = self.attack(self.strategy.get_next_move(self.board.enemy,self._memory))
        if result is not None:
            self._memory.append(result)

    def place(self, ship_type: str) -> None:
        id = 0
        while id in self.board.friendly.get_ship_ids():
            id = id + 1
        try:
            plc = self.strategy.get_next_placement(self.board.friendly,Ship(0,ship_type).size)
            self.place_ship(Ship(id,ship_type),*plc)
            if self._ui is not None:
                self._ui.place_abs(Ship(id,ship_type), *plc)
        except MapException:
            pass