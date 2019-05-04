import random
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from base import Base
from enum import Enum

class MonsterType(Enum):
    RAT =    'rat',    'You see a rat. This rat is agressive because it is ugly\n', \
                           10,    1,     2,    2,    2
    #                      HP|mn_dmg|mx_dmg|gold| exp
    GOBLIN = 'goblin', 'You see Goblin. Goblin. Goblin, Gobliiiiiin. Nasty creature with eyes of emerald green. \n', \
                           30,    4,     8,    8,   10
    #                      HP|mn_dmg|mx_dmg|gold| exp
    SPIDER = 'spider', 'You see a spider. Its called Spider-spider, because it is half spider, half spider. \n', \
                           15,    1,     4,    2,    4
    #                      HP|mn_dmg|mx_dmg|gold| exp
    ORC =    'orc',    'You see a big orc, looks scary. He starts speaking french to you so you think may be its better to attack him.\n', \
                          100,   20,    40,   20,   30
    #                      HP|mn_dmg|mx_dmg|gold| exp
    WOLF =   'wolf',   'You see a wolf. A wolf says: Awooo!. You say nothing.\n', \
                           20,    7,     7,    4,    8
    #                      HP|mn_dmg|mx_dmg|gold| exp
    DEVIL =  'devil',  'You see the devil. You probably do not want to mess with him.\n', \
                        20000, 7000, 15000, 4000, 8000
    #                      HP|mn_dmg|mx_dmg|gold| exp
    BEAR =   'bear',   'You see a bear. You are clearly in his territory and he looks angry.\n', \
                          200,    10,   40,   12,  45
    #                      HP|mn_dmg|mx_dmg|gold| exp
    TROLL =   'troll',   'You see a troll. Big and fat, at least this one doesn\'t regenerate.\n', \
                         4000,    30,   40,  400, 180
    #                      HP|mn_dmg|mx_dmg|gold| exp
    SKELETON = 'skeleton', 'You see a skeleton. He is young and fresh, but dangerous nonetheless.\n', \
                          100,    30,   60,   10,  30
    #                      HP|mn_dmg|mx_dmg|gold| exp
    ZOMBIE = 'zombie', 'You see a zombie. Dead and rotting, yet very durable\n', \
                          500,    20,   30,   30, 100
    #                      HP|mn_dmg|mx_dmg|gold| exp
    LICH = 'lich', 'You see a lich. This abomination is crazy powerful\n', \
                         8000,   200,   800,2000,1000
    #                      HP|mn_dmg|mx_dmg|gold| exp
    def __init__(self, mname, text, health, min_damage, max_damage, gold, exp):
        self.mname = mname
        self.text = text
        self.max_health = health
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.gold = gold
        self.exp = exp

    @staticmethod
    def toEnum(string):
        for m in MonsterType:
            if m.mname.lower() == string.lower():
                return m

    @property
    def cstring(self):
        return self.mname.capitalize()

    def __str__(self):
        return self.string.capitalize()


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

    def __init__(self, user_id, MonsterType):
        self.user_id = user_id
        self.gold = MonsterType.gold
        self.exp = MonsterType.exp
        self.maxhealth = MonsterType.max_health
        self.mindamage = MonsterType.min_damage
        self.maxdamage = MonsterType.max_damage
        self.text = MonsterType.text
        self.name = MonsterType.mname
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
        loot_rate = loot_rates[MonsterType.toEnum(self.name)]
        loot = {}
        for l in loot_rate:
            r = random.random()
            if r < loot_rate[l]:
                loot[l] = 1
        return loot



from resource_entry import Resource
loot_rates = {MonsterType.RAT: {Resource.MEAT: 1},
           MonsterType.GOBLIN: {Resource.GOBLIN_EAR: 0.7, Resource.AMARANTHINE: 0.2, Resource.AEGON_TARGARYEN: 0.1},
           MonsterType.SPIDER: {Resource.AMARANTHINE: 0.4, Resource.AEGON_TARGARYEN: 0.2},
           MonsterType.WOLF : {Resource.PELT: 1, Resource.AMARANTHINE: 0.4, Resource.AEGON_TARGARYEN: 0.2 },
           MonsterType.DEVIL : {},
           MonsterType.ORC : {Resource.MEAT: 0.4, Resource.AEGON_TARGARYEN: 0.4},
           MonsterType.BEAR: {Resource.MEAT: 1, Resource.BEAR_HIDE: 1, Resource.AEGON_TARGARYEN: 0.3},
           MonsterType.TROLL: {Resource.TROLL_SKIN: 0.7},
           MonsterType.SKELETON: {Resource.BONE: 1},
           MonsterType.ZOMBIE: {},
           MonsterType.LICH: {Resource.RUBY: 1, Resource.SAPHIRE: 0.3, Resource.MANA_CRYSTAL: 1},
           }
