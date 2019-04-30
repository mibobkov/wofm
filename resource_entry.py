from enum import Enum
from base import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum as sqEnum, ForeignKey

class Resource(Enum):
    MEAT = 'meat'
    PELT = 'pelt'
    WOLF_FANG = 'wolf fang'
    GOBLIN_EAR = 'goblin ear'
    CLUB = 'club'
    AEGON_TARGARYEN = 'Aegon Targaryen'
    AMARANTHINE = 'Amaranthine'

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string.capitalize()

class ResourceEntry(Base):
    __tablename__ = 'user_resources'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.chat_id'))
    resource = Column(sqEnum(Resource))
    quantity = Column(Integer)
    def __init__(self, user_id, resource, quantity):
        self.user_id = user_id
        self.resource = resource
        self.quantity = quantity
