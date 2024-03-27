from exceptions.ExceptionsEnum import *
from gamedataclasses.Coordinates import Coordinates
from gamedataclasses.CoordinatesValidator import CoordinatesValidator

class MapRepository:

    def __init__(self, size : Coordinates, default_option : str) -> None:
        self._map = {}
        self._coordval = CoordinatesValidator()
        self._coordval.validate(size)
        self._size = size
        for x in range(size.x):
            for y in range(size.y):
                self._map[(x,y)] = default_option

    def check_within_bounds(self, coord : Coordinates) -> None:
        self._coordval.validate(coord)
        if coord.x+1 > self.get_size().x or coord.y+1 > self.get_size().y or coord.x < 0 or coord.y < 0:
            raise MapOutOfBoundsException("Map coordinates out of bounds.")
    
    def is_within_bounds(self, coord : Coordinates) -> bool:
        self._coordval.validate(coord)
        if coord.x+1 > self.get_size().x or coord.y+1 > self.get_size().y or coord.x < 0 or coord.y < 0:
            return False
        return True

    def get_size(self) -> Coordinates:
        return self._size

    def get_tile(self, coord : Coordinates) -> str:
        self.check_within_bounds(coord)
        return self._map[(coord.x,coord.y)]

    def get_map(self) -> list:
        return self._map

    def set_hit(self, coord : Coordinates) -> None:
        self.check_within_bounds(coord)
        self._map[(coord.x,coord.y)] = "hit"
    
    def set_miss(self, coord : Coordinates) -> None:
        self.check_within_bounds(coord)
        self._map[(coord.x,coord.y)] = "miss"