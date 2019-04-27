import random
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from base import Base

class Monster(Base):
    __tablename__ = 'monsters'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.chat_id'))
    gold = Column(Integer)
    exp = Column(Integer)
    health = Column(Integer)
    maxhealth = Column(Integer)
    mindamage = Column(Integer)
    maxdamage = Column(Integer)
    text = Column(String(100))
    name = Column(String(50))

    def __init__(self, user_id, name, text, health, mindamage, maxdamage, gold, exp):
        self.user_id = user_id
        self.gold = gold
        self.exp = exp
        self.maxhealth = health
        self.mindamage = mindamage
        self.maxdamage = maxdamage
        self.text = text
        self.name = name
        self.health = self.maxhealth

    def get_gold(self):
        return random.randint(self.gold*0.5, self.gold*1.5)

    def get_exp(self):
        return random.randint(self.exp*0.5, self.exp*1.5)

    def receive_damage(self, damage):
        self.health = max(0, self.health-damage)

    def get_damage(self):
        return random.randint(self.mindamage, self.maxdamage)

rat_params = ('Rat', 'This rat is agressive because it is ugly\n', 10, 1, 2, 2, 2)
