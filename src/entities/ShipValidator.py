from entities.EntityValidator import EntityValidator
from entities.Ship import Ship
from exceptions.ExceptionsEnum import *

class ShipValidator(EntityValidator):
    
    def __init__(self) -> None:
        self._entity_type = Ship
        self._entity_type_name = "Ship"
        self._valid_types = ["carrier","battleship","cruiser","submarine","destroyer"]

    def validate(self, ship : Ship) -> None:
        super().validate(ship)
        if not isinstance(ship.ship_type,str):
            raise ValidationTypeException("Ship type must be a string.")
        elif ship.ship_type not in self._valid_types:
            raise ValidationValueException("Invalid ship type.")
        if not isinstance(ship.sunk,bool):
            raise ValidationTypeException("Ship sunk property must be boolean.")
    