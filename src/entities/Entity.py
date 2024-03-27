from dataclasses import dataclass


@dataclass
class Entity:
    _id : int

    @property
    def id(self) -> int:
        return self._id