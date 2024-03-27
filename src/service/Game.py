import asyncio
from board.Board import Board
from board.ShipRepository import ShipRepository
from entities.Ship import Ship
from players.Player import Player
from gamedataclasses.Coordinates import Coordinates
from gamedataclasses.AttackResult import AttackResult
from exceptions.ExceptionsEnum import *
from gamedataclasses.GameState import GameState

class Game:

    def __init__(self, player1 : Player, player2 : Player, board_size : Coordinates = Coordinates(10,10)) -> None:
        self.state = GameState()
        self._player1 = player1
        self._player2 = player2
        self._players = [player1,player2]
        self._boards = {self._player1 : Board(board_size), self._player2 : Board(board_size)}
        self._player1.set_game(self)
        self._player2.set_game(self)
        self._winner = None
        self._turn = player1
        if player2.is_client():
            self._turn = player2

    def get_opposite_player(self, player : Player) -> Player:
        """
            Returns the given player's enemy.
        """
        if player == self._player1:
            return self._player2
        else:
            return self._player1

    def get_board(self, player : Player) -> Board:
        """
            Returns the given player's board.
        """
        if player in self._players:
            return self._boards[player]
        raise PlayerMismatch("Player is not part of game.")

    def add_ship(self, player : Player, ship : Ship, coord : Coordinates, vertical : bool) -> None:
        """
            Adds the given ship at the given coordinates and rotation.

            param player: Player class, given through self._game.add_ship(self, ... )
            param ship: Ship class, the ship to be placed
            param coord: Coordinates class, location of ship
            param vertical: boolean, expressing rotation (True -> vertical, False -> horizontal)
        """
        if not self.state.is_placement():
            return
        if ship.id in self.get_opposite_player(player).board.enemy.get_ship_ids():
            self.get_opposite_player(player).remove_enemy_ship(ship.id)
        player.board.friendly.add_ship(ship,coord,vertical)
        self.get_opposite_player(player).add_enemy_ship(ship, coord, vertical)

    def get_unsunk_ship_count(self, player : Player) -> int:
        """
            Returns the amount of unsunk ships for player, used in determining the victor.

            param player: Player class, player to check for

            returns: int, amount of unsunk ships
        """
        count = 0
        for id in player.board.friendly.get_ship_ids():
            if not player.board.friendly.ship_is_sunk(id):
                count = count + 1
        return count

    def get_ship_count(self, player : Player) -> int:
        """
            Returns the amount of ships for player, used in determining how many ships we need to place.

            param player: Player class, player to check for

            returns: int, amount of ships
        """
        return len(player.board.friendly.get_ship_ids())

    
    
    @property
    def winner(self) -> Player or None:
        return self._winner

    def declare_winner(self, player : Player) -> None:
        self.state.set_to_end()
        self._winner = player


    def process_hit(self, source_player : Player, coord : Coordinates) -> AttackResult or None:
        """
            Processes the hit given by the source player

            param source_player: Player class, given with self._game.process_hit(self, ... )
            param coord: Coordinates class, location to attack at

            returns: AttackResult class, given by the target player
        """
        if source_player != self._turn or source_player.board.enemy.get_tile(coord) != "unknown" or not self.state.is_battle():
            return None

        target_player = self.get_opposite_player(source_player)
        result = target_player.process_attack(coord)
        if not result.is_hit():
            self._turn = self.get_opposite_player(self._turn)
        if result.resulted_in_sink():
            if self.get_unsunk_ship_count(target_player) == 0:
                self.declare_winner(source_player)
        return result

    def advance(self) -> None:
        """
            Advances the game, made to be called from the async main loop.
        """
        if self.state.is_placement():
            ships_to_place = ["carrier","battleship","cruiser","submarine","destroyer"]
            if self.get_ship_count(self._player1) == 5 and self.get_ship_count(self._player2) == 5:
                self.state.set_to_battle()
                return
            if self.get_ship_count(self._player1) < self.get_ship_count(self._player2):
                player_to_place = self._player1
            else:
                player_to_place = self._player2
            if self._player2.is_client():
                player_to_place = self.get_opposite_player(player_to_place)
            player_to_place.place(ships_to_place[self.get_ship_count(player_to_place)])
        elif self.state.is_battle():
            self._turn.move()


    async def main(self) -> None:
        """
            Async main loop. Made to work in parallel with internet conenctions.
        """
        while not self.state.is_finished():
            await asyncio.sleep(0.1)
            self.advance()

