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
        return random.randint(int(self.gold*0.5), int(self.gold*1.5))

    def get_exp(self):
        return random.randint(int(self.exp*0.5), int(self.exp*1.5))

    def receive_damage(self, damage):
        self.health = max(0, self.health-damage)

    def get_damage(self):
        return random.randint(self.mindamage, self.maxdamage)

    def get_loot(self):
        loot_rate = loot_rates[self.name]
        loot = {}
        for l in loot_rate:
            r = random.random()
            if r < loot_rate[l]:
                loot[l] = 1
        return loot



from resource_entry import Resource
loot_rates = {'Rat': {Resource.MEAT: 1},
           'Goblin' : {Resource.GOBLIN_EAR: 0.7, Resource.AMARANTHINE: 0.2, Resource.AEGON_TARGARYEN: 0.1},
           'Spider' : {Resource.AMARANTHINE: 0.4, Resource.AEGON_TARGARYEN: 0.2},
           'Wolf' : {Resource.PELT: 1, Resource.AMARANTHINE: 0.4, Resource.AEGON_TARGARYEN: 0.2 },
           'Devil' : {},
           'Orc' : {Resource.MEAT: 0.4, Resource.AEGON_TARGARYEN: 0.4}
           }
rat_params = ('Rat', 'You see a rat. This rat is agressive because it is ugly\n', 10, 1, 2, 2, 2)
goblin_params = ('Goblin', 'You see Goblin. Goblin. Goblin, Gobliiiiiin. Nasty creature with eyes of emerald green. \n', 30, 4, 8, 8, 10)
spider_params = ('Spider', 'You see a spider. Its called Spider-spider, because it is half spider, half spider. \n', 15, 1, 4, 2, 4)
wolf_params = ('Wolf', 'You see a wolf. A wolf says: Awooo!. You say nothing.\n', 20, 7, 7, 4, 8)
devil_params = ('Devil', 'You see the devil. You probably do not want to mess with him.\n', 20000, 7000, 15000, 4000, 8000)
orc_params = ('Orc', 'You see a big orc, looks scary. He starts speaking french to you so you think may be its better to attack him.\n', 100, 20, 40, 20, 30)
