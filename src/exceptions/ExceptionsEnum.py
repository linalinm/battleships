class GameException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ValidationException(GameException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "Validation Exception: " + super().__str__()

class ValidationTypeException(ValidationException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ValidationValueException(ValidationException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)



class MapException(GameException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "Map Exception: " + super().__str__()

class MapOutOfBoundsException(MapException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class IdMismatch(GameException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class PlayerMismatch(GameException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InputException(GameException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class LocationException(InputException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class RotationException(InputException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ConnectionException(GameException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)