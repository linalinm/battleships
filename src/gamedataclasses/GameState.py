


class GameState:

    def __init__(self) -> None:
        self.__state = "placement"

    def is_placement(self) -> bool:
        return self.__state == "placement"

    def set_to_battle(self) -> None:
        self.__state = "battle"

    def is_battle(self) -> bool:
        return self.__state == "battle"

    def set_to_end(self) -> None:
        self.__state = "end"

    def is_finished(self) -> bool:
        return self.__state == "end"