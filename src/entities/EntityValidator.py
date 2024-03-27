from entities.Entity import Entity
from exceptions.ExceptionsEnum import *

class EntityValidator:

    def __init__(self) -> None:
        self._entity_type = Entity
        self._entity_type_name = "Entity"

    def validate(self, entity : Entity) -> None:
        if not isinstance(entity,self._entity_type):
            raise ValidationTypeException("Entity must be of type " + self._entity_type_name)
        if not isinstance(entity.id,int):
            raise ValidationTypeException("Entity id must be integer")

            