from entities.Ship import Ship
from entities.ShipValidator import ShipValidator
from exceptions.ExceptionsEnum import *

class ShipRepository:

    def __init__(self) -> None:
        self._entity_list = {}
        self._val = ShipValidator()

    def add_ship(self, ship : Ship) -> None:
        """ Adds a ship to the repository. Can raise ValidationException and IdMismatch.
        
        param ship: a Ship object
        """
        self._val.validate(ship)
        if ship.id not in self._entity_list:
            self._entity_list[ship.id] = ship
            return
        raise IdMismatch("Id is already in use.")

    def get_ship(self, id : int) -> Ship:
        """ Gets a ship from the repository, by id. Can raise IdMismatch.
        
        param id: int, id of ship to return
        returns: a Ship object
        """
        if id not in self._entity_list:
            raise IdMismatch("Id does not exist.")
        return self._entity_list[id]

    def get_ships(self) -> list:
        """ Gets a list of all the ships in the repository.

        returns: list of Ship objects
        """
        li = []
        for id in self._entity_list:
            li.append(self._entity_list[id])
        return li

    def get_ids(self) -> list:
        """ Gets a list of all the ids in the repository.
        
        returns: list of integers
        """
        li = []
        for id in self._entity_list:
            li.append(id)
        return li

    def remove_ship(self, id : int) -> None:
        if id not in self._entity_list:
            raise IdMismatch("Id does not exist.")
        self._entity_list.pop(id)
