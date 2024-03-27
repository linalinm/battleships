
import unittest
from entities.Ship import Ship
from gamedataclasses.Coordinates import Coordinates

from service.Game import Game
from players.Player import Player


class GameTests(unittest.TestCase):
    
    def tests(self):
        player1 = Player()
        player2 = Player()
        game = Game(player1, player2)
        game.advance()
        self.assertTrue(player2.placem)
        player2.place_ship(Ship(1,"carrier"),Coordinates(2,2),False)
        game.advance()
        self.assertTrue(player1.placem)
        self.assertFalse(player2.placem)
        player1.place_ship(Ship(1,"carrier"),Coordinates(2,2),False)
        game.advance()
        player2.place_ship(Ship(2,"battleship"),Coordinates(2,3),False)
        game.advance()
        player1.place_ship(Ship(2,"battleship"),Coordinates(2,3),False)
        game.advance()
        player2.place_ship(Ship(3,"cruiser"),Coordinates(2,4),False)
        game.advance()
        player1.place_ship(Ship(3,"cruiser"),Coordinates(2,4),False)
        game.advance()
        player2.place_ship(Ship(4,"submarine"),Coordinates(2,5),False)
        game.advance()
        player1.place_ship(Ship(4,"submarine"),Coordinates(2,5),False)
        game.advance()
        player2.place_ship(Ship(5,"destroyer"),Coordinates(2,6),False)
        game.advance()
        player1.place_ship(Ship(5,"destroyer"),Coordinates(2,6),False)
        game.advance()
        game.advance()

        self.assertTrue(player1.turn)
        result = player1.attack(Coordinates(9,9))
        self.assertFalse(result.is_hit())
        game.advance()
        self.assertTrue(player2.turn)
        result = player2.attack(Coordinates(1,1))
        game.advance()
        self.assertFalse(result.is_hit())
        result = player1.attack(Coordinates(1,1))
        game.advance()
        self.assertFalse(result.is_hit())
        result = player2.attack(Coordinates(2,2))
        game.advance()
        self.assertTrue(result.is_hit())
        self.assertIsNone(result.get_sunk_ship())
        result = player2.attack(Coordinates(3,2))
        game.advance()
        self.assertTrue(result.is_hit())
        self.assertIsNone(result.get_sunk_ship())
        result = player2.attack(Coordinates(4,7))
        game.advance()
        self.assertFalse(result.is_hit())

        result = player1.attack(Coordinates(1,1))
        game.advance()
        self.assertIsNone(result)
        result = player1.attack(Coordinates(2,1))
        game.advance()
        self.assertFalse(result.is_hit())
        result = player1.attack(Coordinates(3,1))
        game.advance()
        self.assertIsNone(result)

        
        result = player2.attack(Coordinates(4,2))
        game.advance()
        self.assertTrue(result.is_hit())
        result = player2.attack(Coordinates(5,2))
        game.advance()
        self.assertTrue(result.is_hit())
        result = player2.attack(Coordinates(6,2))
        game.advance()
        self.assertTrue(result.is_hit())
        self.assertTrue(result.resulted_in_sink())
        self.assertEqual(result.get_sunk_ship(),1)
        result = player2.attack(Coordinates(7,2))
        game.advance()
        self.assertFalse(result.is_hit())

        result = player1.attack(Coordinates(3,1))
        game.advance()
        self.assertFalse(result.is_hit())
        
        result = player2.attack(Coordinates(2,3))
        game.advance()
        self.assertTrue(result.is_hit())
        result = player2.attack(Coordinates(3,3))
        game.advance()
        self.assertTrue(result.is_hit())
        result = player2.attack(Coordinates(4,3))
        game.advance()
        self.assertTrue(result.is_hit())
        result = player2.attack(Coordinates(5,3))
        game.advance()
        self.assertTrue(result.is_hit())
        self.assertTrue(result.resulted_in_sink())
        self.assertEqual(result.get_sunk_ship(),2)


        result = player2.attack(Coordinates(2,4))
        game.advance()
        self.assertTrue(result.is_hit())
        result = player2.attack(Coordinates(3,4))
        game.advance()
        self.assertTrue(result.is_hit())
        result = player2.attack(Coordinates(4,4))
        game.advance()
        self.assertTrue(result.is_hit())
        self.assertTrue(result.resulted_in_sink())
        self.assertEqual(result.get_sunk_ship(),3)

        result = player2.attack(Coordinates(2,5))
        game.advance()
        self.assertTrue(result.is_hit())
        result = player2.attack(Coordinates(3,5))
        game.advance()
        self.assertTrue(result.is_hit())
        result = player2.attack(Coordinates(4,5))
        game.advance()
        self.assertTrue(result.is_hit())
        self.assertTrue(result.resulted_in_sink())
        self.assertEqual(result.get_sunk_ship(),4)

        result = player2.attack(Coordinates(2,6))
        game.advance()
        self.assertTrue(result.is_hit())
        result = player2.attack(Coordinates(3,6))
        game.advance()
        self.assertTrue(result.is_hit())
        self.assertTrue(result.resulted_in_sink())
        self.assertEqual(result.get_sunk_ship(),5)

        self.assertEqual(game.winner,player2)








if __name__ == "__main__":
    unittest.main()