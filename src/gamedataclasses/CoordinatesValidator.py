from gamedataclasses.Coordinates import Coordinates
from exceptions.ExceptionsEnum import *

class CoordinatesValidator:

    def validate(self, coord : Coordinates):
        if not isinstance(coord,Coordinates):
            raise ValidationTypeException("Coordinates must be of dataclass Coordinate type.")
        if not isinstance(coord.x,int) or not isinstance(coord.y,int):
            raise ValidationTypeException("Coordinate values must be integers.")