from dataclasses import dataclass
from entities.Entity import Entity

@dataclass
class Ship(Entity):
    _ship_type : str
    sunk : bool = False

    @property
    def ship_type(self) -> str:
        return self._ship_type

    @property
    def size(self) -> int:
        sizes = {
            "carrier": 5,
            "battleship": 4,
            "cruiser": 3,
            "submarine": 3,
            "destroyer": 2
        }
        return sizes[self.ship_type]

    def __str__(self) -> str:
        sunkstr = ""
        if self.sunk:
            sunkstr = " - sunk" 
        return self.ship_type + " " + sunkstr