
from board.EnemyMap import EnemyMap
from gamedataclasses.AttackResult import AttackResult
from gamedataclasses.Coordinates import Coordinates
from strategies.RandomStrategy import RandomStrategy
from random import randint
from copy import deepcopy

class HitStrategy(RandomStrategy):


    def __init__(self) -> None:
        self._sinkings = []

    def get_direction(self, initial : Coordinates, last : Coordinates):
        if last.x > initial.x:
            return "right"
        elif last.y > initial.y:
            return "down"
        elif last.x < initial.x:
            return "left"
        elif last.y < initial.y:
            return "up"
        return "same"

    def add_in_direction(self, coords : Coordinates, direction : str) -> Coordinates:
        if direction == "right":
            return Coordinates(coords.x+1,coords.y)
        elif direction == "down":
            return Coordinates(coords.x,coords.y+1)
        elif direction == "left":
            return Coordinates(coords.x-1,coords.y)
        elif direction == "up":
            return Coordinates(coords.x,coords.y-1)

    def next_direction(self, direction : str) -> str:
        next_dir = {"start":"right","right":"left","left":"down","down":"up","up":None,"same":None}
        return next_dir[direction]

    def handle_start(self, enemy_map : EnemyMap, initial_coordinates : str, memory : list) -> Coordinates:
        direction = "start"
        while direction is not None:
            direction = self.next_direction(direction)
            if enemy_map.is_within_bounds(self.add_in_direction(initial_coordinates,direction)):
                if enemy_map.get_tile(self.add_in_direction(initial_coordinates,direction)) == "unknown":
                    return self.add_in_direction(initial_coordinates, direction)
        
        memory.clear()
        return Coordinates(randint(0,9),randint(0,9))


    def get_next_move(self, enemy_map: EnemyMap, memory : list) -> Coordinates:
        if len(memory) == 0:
            return Coordinates(randint(0,9),randint(0,9))
        if not memory[0].is_hit():
            memory.clear()
            return Coordinates(randint(0,9),randint(0,9))
        initial_location = memory[0].coords.copy
        last_location = memory[-1].coords.copy
        if initial_location == last_location:
            return self.handle_start(enemy_map, initial_location, memory)
        direction = self.get_direction(initial_location,last_location)
        if not memory[-1].is_hit():
            direction = self.next_direction(direction)
            last_location = initial_location
        while direction is not None:
            if enemy_map.is_within_bounds(self.add_in_direction(last_location,direction)):
                if enemy_map.get_tile(self.add_in_direction(last_location,direction)) == "unknown":
                    return self.add_in_direction(last_location,direction)
            direction = self.next_direction(direction)
            last_location = initial_location
        memory.clear()
        return Coordinates(randint(0,9),randint(0,9))

        

        
        