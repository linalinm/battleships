from board.MapRepository import MapRepository
from board.PositionalShipRepository import PositionalShipRepository
from entities.Ship import Ship
from exceptions.ExceptionsEnum import *
from gamedataclasses.AttackResult import AttackResult
from gamedataclasses.Coordinates import Coordinates
from gamedataclasses.CoordinatesValidator import CoordinatesValidator

class FriendlyMap(MapRepository):

    def __init__(self, size: Coordinates) -> None:
        super().__init__(size,"sea")
        self._ships = PositionalShipRepository(size)

    def add_ship(self, ship : Ship, coord : Coordinates, vertical : bool) -> bool:
        """ Adds the given ship at the given coordinates and rotation.
            Returns False if there would be a collision with another ship after the operation.
            Returns True if the operation was successful.
        """
        coord1 = coord.copy
        for i in range(ship.size):
            if self.get_tile(coord1) == "ship":
                return False
            if vertical:
                coord1.y = coord1.y+1
            else:
                coord1.x = coord1.x+1
        self._ships.add_ship(ship,coord,vertical)
        coord1 = coord.copy
        for i in range(ship.size):
            self._set_tile_to_ship(coord1)
            if vertical:
                coord1.y = coord1.y+1
            else:
                coord1.x = coord1.x+1
        return True

    def get_ships(self) -> list:
        return self._ships.get_ships()

    def get_ship_ids(self) -> list:
        return self._ships.get_ids()

    def get_ship_coords(self, id : int) -> Coordinates:
        return self._ships.get_ship_coordinates(id)

    def ship_is_vertical(self, id : int) -> bool:
        return self._ships.ship_is_vertical(id)

    def ship_is_sunk(self, id : int) -> bool:
        if id is None:
            return False
        if self._ships.get_ship(id).sunk:
            return True
        coords = self.get_ship_coords(id).copy
        for i in range(self._ships.get_ship(id).size):
            if self.get_tile(coords) != "hit":
                return False
            if self.ship_is_vertical(id):
                coords.y = coords.y + 1
            else:
                coords.x = coords.x + 1
        return True

    def process_attack(self, coord : Coordinates) -> AttackResult:
        tile_hit = self.get_tile(coord)
        sunk_ship_id = None
        sunk_ship_type = None
        if tile_hit == "ship":
            self.set_hit(coord)
            target_ship = self._ships.get_ship_at(coord)
            if self.ship_is_sunk(target_ship):
                sunk_ship_id = target_ship
                sunk_ship_type = self._ships.get_ship(sunk_ship_id).ship_type
                self._ships.get_ship(sunk_ship_id).sunk = True
        else:
            self.set_miss(coord)
        return AttackResult(coord, tile_hit, sunk_ship_id, sunk_ship_type)

    def _set_tile_to_ship(self, coord : Coordinates) -> None:
        self.check_within_bounds(coord)
        self._map[(coord.x,coord.y)] = "ship"
