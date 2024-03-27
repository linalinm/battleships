


import asyncio
from board.MapRepository import MapRepository
from entities.Ship import Ship
from gamedataclasses.AttackResult import AttackResult
from gamedataclasses.Coordinates import Coordinates
from players.Player import Player
from exceptions.ExceptionsEnum import *

class ConsoleUI:


    def __init__(self, player : Player) -> None:
        self.player = player
        self.running = True 

        
    def print_map(self, map : MapRepository) -> None:
        map_dict = {
            "unknown": "~",
            "sea" : "~",
            "ship" : "$",
            "hit" : "X",
            "miss" : "."
        }
        out = "#|ABCDEFGHIJ\n-+----------\n"
        maptoprint = map.get_map()
        for y in range(map.get_size().y):
            out = out + str(y) + "|"
            for x in range(map.get_size().x):
                out = out + map_dict[maptoprint[(x,y)]]
            if y > 2:
                out = out + "    "
                if y == 3:
                    out = out + "Ships:"
                elif len(map.get_ships()) > y-4:
                    ship = map.get_ships()[y-4]
                    out = out + str(ship)
            out = out + "\n"
        print(out)
    

    def print_board(self) -> None:
        print("Enemy map:")
        self.print_map(self.player.board.enemy)
        print("Own map:")
        self.print_map(self.player.board.friendly)


    def resolve_location(self, location : str) -> Coordinates:
        if len(location) != 2:
            raise LocationException("Location must be expressed by letter and number!")
        x = location[0:1]
        y = location[1:2]
        location_dict = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9}
        if x not in location_dict:
            raise LocationException("Location letter out of bounds!")
        if not y.isdecimal():
            raise LocationException("Location number invalid!")
        y = int(y)
        if y < 0 or y > 9:
            raise LocationException("Location number out of bounds!")
        return Coordinates(location_dict[x],y)


    def resolve_rotation(self, rotation : str) -> bool:
        rotation_dict = {"h":False,"horizontal":False,"horisontal":False,"v":True,"vertical":True}
        if rotation.lower() not in rotation_dict:
            raise RotationException("Invalid rotation!")
        return rotation_dict[rotation.lower()]

    def place(self, ship_type : str) -> None:
        print(f"\nWhere should we place a {ship_type}?\nFormat: <location (letter and number)> <rotation (horisonal or vertical)>")
        inp = input("> ")
        inp = inp.split(" ")
        if len(inp) != 2:
            raise InputException("Invalid format!")
        self.player.place_ship(Ship(len(self.player.board.friendly.get_ship_ids()),ship_type),self.resolve_location(inp[0]),self.resolve_rotation(inp[1]))

    def attack(self) -> None:
        print("\nWhere should we attack?")
        inp = input("> ")
        if len(inp) != 2:
            raise InputException("Invalid format!")
        result = self.player.attack(self.resolve_location(inp))
        if result is None:
            print("Invalid attack position.")
            return
        if result.is_hit():
            print("We hit!")
            if result.resulted_in_sink():
                print(f"We managed to sink a {result.get_sunk_ship_type()}!\n")
        else:
            print("We missed!")
        print("")

    async def turn(self) -> None:
        while not self.player.placem and not self.player.turn and not self.player.lost() and not self.player.won():
            await asyncio.sleep(0.1)
        return

    async def main(self) -> None:
        self.running = True
        while not self.player.won() and not self.player.lost() and self.running:
            await self.turn()
            self.print_board()
            if self.player.placem:
                try:
                    self.place(self.player.ship_to_place)
                except (InputException,MapException) as e:
                    print(str(e))
            elif self.player.turn:
                try:
                    self.attack()
                except InputException as e:
                    print(str(e))
                    

        if self.player.won():
            print("You won!\n")
        else:
            print("You lost...\n")
        return