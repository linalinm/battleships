import unittest
from entities.Entity import Entity
from entities.EntityValidator import EntityValidator
from entities.Ship import Ship
from entities.ShipValidator import ShipValidator
from gamedataclasses.Coordinates import Coordinates
from gamedataclasses.CoordinatesValidator import CoordinatesValidator
from exceptions.ExceptionsEnum import *

class ValidationTests(unittest.TestCase):
    def test_entity(self):
        validator = EntityValidator()
        with self.assertRaises(ValidationTypeException):
            validator.validate(0)
            validator.validate(Entity("a"))
        validator.validate(Entity(0))

    def test_ships(self):
        validator = ShipValidator()
        with self.assertRaises(ValidationTypeException):
            validator.validate(Ship(0,0))
            validator.validate(Ship(0,"a",0))
        with self.assertRaises(ValidationValueException):
            validator.validate(Ship(0,"a"))
        validator.validate(Ship(0,"carrier"))
        validator.validate(Ship(0,"battleship"))
        validator.validate(Ship(0,"cruiser"))
        validator.validate(Ship(0,"submarine"))
        validator.validate(Ship(0,"destroyer"))

    def test_coordinates(self):
        validator = CoordinatesValidator()
        with self.assertRaises(ValidationTypeException):
            validator.validate(0)
            validator.validate(Coordinates("a",0))
            validator.validate(Coordinates(0,"a"))
        validator.validate(Coordinates(0,0))

if __name__ == "__main__":
    unittest.main()