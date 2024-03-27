from board.MapRepository import MapRepository
from board.ShipRepository import ShipRepository
from entities.Ship import Ship
from exceptions.ExceptionsEnum import *
from gamedataclasses.Coordinates import Coordinates
from gamedataclasses.CoordinatesValidator import CoordinatesValidator

class EnemyMap(MapRepository):

    def __init__(self, size: Coordinates) -> None:
        super().__init__(size,"unknown")
        self._ships = ShipRepository()
        
    def add_ship(self, ship : Ship) -> None:
        self._ships.add_ship(ship)
    
    def get_ships(self) -> list:
        return self._ships.get_ships()

    def get_ship_ids(self) -> list:
        return self._ships.get_ids()

    def sink_ship(self, id : int) -> None:
        self._ships.get_ship(id).sunk = True

    def remove_ship(self, id : int) -> None:
        """
            Rare ish bug where a ship gets added by mistake? Added this to help fix that
        """
        self._ships.remove_ship(id)
    