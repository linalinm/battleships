from board.ShipRepository import ShipRepository
from entities.Ship import Ship
from gamedataclasses.Coordinates import Coordinates
from gamedataclasses.CoordinatesValidator import CoordinatesValidator
from exceptions.ExceptionsEnum import *

class PositionalShipRepository(ShipRepository):

    def __init__(self, size : Coordinates) -> None:
        super().__init__()
        self._size = size.copy
        self._coordval = CoordinatesValidator()
        self._pos_list = {}


    def add_ship(self, ship: Ship, coord : Coordinates, vertical : bool) -> None:
        """
            Adds the given ship at the given coordinates and rotation.


            param ship: Ship class, the ship to be placed
            param coord: Coordinates class, location of ship
            param vertical: boolean, expressing rotation (True -> vertical, False -> horizontal)
        """
        self._coordval.validate(coord)
        if not isinstance(vertical, bool):
            raise ValidationTypeException("Rotation must be expressed as a boolean.")
        if not self.is_within_bounds(coord):
            raise MapOutOfBoundsException("Ship will end up out of bounds!")
        super().add_ship(ship)
        self._pos_list[ship.id] = (coord,vertical)

    def get_ship_coordinates(self, id : int) -> Coordinates:
        """
            Returns the coordinates at the beginning of a ship, through ID.

            param id: int, ship's ID

            returns: Coordinates, the beginning of the ship
        """
        if id in self._pos_list:
            return Coordinates(self._pos_list[id][0].x,self._pos_list[id][0].y)
        raise IdMismatch("Id does not exist.")


    def get_ship_at(self, coord : Coordinates) -> int or None:
        """ Returns the id of the ship at the given coordinates, or None if there is no ship.
        
            param coord: Coordinates class, location to check for

            returns: int or None
        """
        for id in self._entity_list:
            coords = self.get_ship_coordinates(id).copy
            for i in range(self.get_ship(id).size):
                if coord.x == coords.x and coord.y == coords.y:
                    return id
                if self.ship_is_vertical(id):
                    coords.y = coords.y + 1
                else:
                    coords.x = coords.x + 1

        return None

    def get_ship_end(self, id : int) -> Coordinates:
        """
            Returns the coordinates at the end of a ship, through ID. Used to check if ship will end up out of bounds.

            param id: int, ship's ID

            returns: Coordinates, the end of the ship
        """
        coords = self.get_ship_coordinates(id)
        for i in range(self.get_ship(id).size-1):
            if self.ship_is_vertical(id):
                coords.y = coords.y + 1
            else:
                coords.x = coords.x + 1
        return coords

    def is_within_bounds(self, coords : Coordinates) -> bool:
        if coords.x > self._size.x or coords.y > self._size.y:
            return False
        return True


    def ship_is_vertical(self, id : int) -> bool:
        if id in self._pos_list:
            return self._pos_list[id][1]
        raise IdMismatch("Id does not exist.")