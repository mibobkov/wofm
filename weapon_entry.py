from base import Base
from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey

class Weapon(Enum):
    DAGGER = 'dagger', 10, 2, 1
    SCIMITAR = 'scimitar', 40, 5, 2
    SWORD = 'sword', 100, 10, 3
    SWORD_OF_DAWN = 'Sword of Dawn, Third of his Name, King of Vandals and Mother of Dogo', 500, 25, 4

    def __init__(self, string, base_cost, damage, id):
        self.string = string
        self.base_cost = base_cost
        self.damage = damage
        self.id = id

    @staticmethod
    def idToEnum(id):
        for w in Weapon:
            if w.id == int(id):
                return w

    @staticmethod
    def toEnum(string):
        for w in Weapon:
            if w.string.lower() == string.lower():
                return w

    @property
    def cstring(self):
        return self.string[0].capitalize()+self.string[1:]

    def __str__(self):
        return self.string[0].capitalize()+self.string[1:]

class WeaponEntry(Base):
    __tablename__ = 'user_weapons'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    user_id = Column(Integer(), ForeignKey('users.chat_id'))
    quantity = Column(Integer())

    def __init__(self, name, user_id, quantity):
        self.name = name
        self.user_id = user_id
        self.quantity = quantity
