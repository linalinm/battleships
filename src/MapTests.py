

from board.EnemyMap import EnemyMap
from board.FriendlyMap import FriendlyMap
import unittest
from entities.Ship import Ship

from gamedataclasses.Coordinates import Coordinates
from exceptions.ExceptionsEnum import *

class Test(unittest.TestCase):


    def test_friendly_map(self):
        map = FriendlyMap(Coordinates(5,5))

        self.assertEqual(map.get_tile(Coordinates(0,1)),"sea")
        with self.assertRaises(MapOutOfBoundsException):
            map.add_ship(Ship(0,"carrier"),Coordinates(4,4),False)
        map.add_ship(Ship(0,"submarine"),Coordinates(0,0),False)
        map.add_ship(Ship(1,"destroyer"),Coordinates(0,1),True)

        self.assertEqual(map.get_tile(Coordinates(0,0)),"ship")
        self.assertEqual(map.get_tile(Coordinates(0,2)),"ship")

    def test_enemy_map(self):
        map = EnemyMap(Coordinates(5,5))

        self.assertEqual(map.get_tile(Coordinates(0,1)),"unknown")
        map.add_ship(Ship(0,"carrier"))

        self.assertIn(0,map.get_ship_ids())
        self.assertIn(Ship(0,"carrier"),map.get_ships())

        map.set_hit(Coordinates(0,1))
        self.assertEqual(map.get_tile(Coordinates(0,1)),"hit")
        map.set_miss(Coordinates(1,1))
        self.assertEqual(map.get_tile(Coordinates(1,1)),"miss")
        map.set_miss(Coordinates(0,1))
        self.assertEqual(map.get_tile(Coordinates(0,1)),"miss")





if __name__ == "__main__":
    unittest.main()