from base import Base
from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey

class Armor(Enum):
    LEATHER_JACKET = 'leather jacket', 20, 2, 1
    CHAIN_MAIL = 'chain mail', 200, 10, 2
    FULL_PLATE_ARMOR = 'full plate armor', 1000, 20, 3
    MITHRIL_ARMOR = 'mithril armor', 4000, 30, 4

    def __init__(self, string, base_cost, protection, id):
        self.string = string
        self.base_cost = base_cost
        self.protection = protection
        self.id = id

    @staticmethod
    def idToEnum(id):
        for a in Armor:
            if a.id == int(id):
                return a

    @staticmethod
    def toEnum(string):
        for a in Armor:
            if a.string.lower() == string.lower():
                return a

    @property
    def cstring(self):
        return self.string[0].capitalize()+self.string[1:]

    def __str__(self):
        return self.string[0].capitalize()+self.string[1:]

class ArmorEntry(Base):
    __tablename__ = 'user_armor'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    user_id = Column(Integer(), ForeignKey('users.chat_id'))
    quantity = Column(Integer())

    def __init__(self, name, user_id, quantity):
        self.name = name
        self.user_id = user_id
        self.quantity = quantity
