from board.Board import Board
from entities.Ship import Ship
from gamedataclasses.AttackResult import AttackResult
from gamedataclasses.Coordinates import Coordinates
#from service.Game import Game

class Player:

    def __init__(self) -> None:
        self._game = None
        self.turn = False
        self.placem = False
        self.ship_to_place = ""
        self._ui = None

    def set_ui(self, ui):
        self._ui = ui

    def move(self) -> None:
        self.turn = True

    def place(self, ship_type : str) -> None:
        self.placem = True
        self.ship_to_place = ship_type

    def add_enemy_ship(self, ship : Ship, coord, vertical):
        self.board.enemy.add_ship(ship)

    def remove_enemy_ship(self, id : int):
        self.board.enemy.remove_ship(id)

    def process_attack(self, coord : Coordinates):
        return self.board.friendly.process_attack(coord)

    def is_client(self) -> bool:
        return False

    @property
    def board(self) -> Board:
        return self._game.get_board(self)

    def set_game(self, game) -> None:
        self._game = game

    def place_ship(self, ship : Ship, coord : Coordinates, vertical : bool) -> None:
        self._game.add_ship(self, ship, coord, vertical)
        self.placem = False

    def attack(self, coord : Coordinates) -> AttackResult:
        result = self._game.process_hit(self, coord)

        if result is None:
            return None
        self.turn = False
            
        if result.is_hit():
            self.board.enemy.set_hit(coord)
            if result.resulted_in_sink():
                self.board.enemy.sink_ship(result.get_sunk_ship())
        else:
            self.board.enemy.set_miss(coord)
        return result 

    def won(self) -> bool:
        return self._game.winner == self

    def lost(self) -> bool:
        return self._game.winner is not None and not self._game.winner == self