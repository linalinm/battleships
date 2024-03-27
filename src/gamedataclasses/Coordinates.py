
from dataclasses import dataclass


@dataclass
class Coordinates:
    x : int
    y : int

    @property
    def copy(self):
        return Coordinates(self.x,self.y)