from gamedataclasses.Coordinates import Coordinates
from gamedataclasses.CoordinatesValidator import CoordinatesValidator

class AttackResult:

    def __init__(self, coord : Coordinates, tile_hit : str, sunk_ship_id : int = None, sunk_ship_type : str = None) -> None:
        self._coordval = CoordinatesValidator()
        self._coordval.validate(coord)
        self.coords = coord
        self.tile = tile_hit
        self.sunk = sunk_ship_id
        self.sunk_type = sunk_ship_type

    def is_hit(self) -> bool:
        if self.tile == "ship":
            return True
        return False

    def resulted_in_sink(self) -> bool:
        return self.sunk is not None

    def get_sunk_ship(self) -> int or None:
        return self.sunk

    def get_sunk_ship_type(self) -> str or None:
        return self.sunk_type


