import telegram
import random
from locations import Location
import math
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, Enum as sqEnum
from base import Base
from enum import Enum

class UserStatus(Enum):
    READY = 'ready'
    FIGHTING = 'fighting'
    DUELLING = 'duelilng'
    SET_NAME = 'set_name'
    STARTING_DUEL = 'starting_duel'
    GOING = 'going'
    DUELLING_ATTACKED = 'duelling_attacked'

class User(Base):
    __tablename__ = 'users'
    chat_id = Column(Integer, primary_key=True)
    location = Column(sqEnum(Location))
    max_health = Column(Integer)
    health = Column(Integer)
    mana = Column(Integer)
    max_mana = Column(Integer)
    name = Column(String(50))
    status= Column(sqEnum(UserStatus))
    fighting = None
    opponent = Column(Integer)
    mindamage = Column(Integer)
    maxdamage = Column(Integer)
    exp = Column(Integer)
    gold = Column(Integer)
    level = Column(Integer)
    levelled_up = Column(Boolean)

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.location = Location.VILLAGE
        self.max_health = 100
        self.health = 100
        self.mana = 100
        self.max_mana = 100
        self.name = ""
        self.status = UserStatus.SET_NAME
        self.fighting = None
        self.mindamage = 2
        self.maxdamage = 4
        self.exp = 0
        self.gold = 0
        self.level = 1
        self.levelled_up = False

    def set_name(self, name):
        self.name = name

    def get_damage(self):
        return random.randint(self.mindamage, self.maxdamage)

    def give_gold(self, amount):
        self.gold += amount

    def give_exp(self, amount):
        self.exp += amount
        if self.should_level_up():
            self.level_up()

    def should_level_up(self):
        return self.exp >= self.next_level_req()

    def next_level_req(self):
        return math.ceil(10*(1.2**self.level-1)/(0.2))

    def level_up(self):
        self.level += 1
        self.levelled_up = True
        self.max_health += 10
        self.health = self.max_health
        self.max_mana += 10
        self.mana = self.max_mana
        self.mindamage += 1
        self.maxdamage += 2

    def stats_text(self):
        levelled_up_text = ''
        if self.levelled_up:
            levelled_up_text = '<b>You have levelled up! Congratulations!</b>\n'
        self.levelled_up = False
        return u'\U0001F466''<b>{}</b>\n'.format(self.name) + \
               u'\U000026A1'"Level: {}\n".format(self.level) + \
               u'\U0001F534'"Health: {}/{}\n".format(self.health, self.max_health) + \
               u'\U0001F535'"Mana: {}/{}\n".format(self.mana, self.max_mana) + \
               u'\U0001F4A1'"Exp: {}/{}\n".format(self.exp, int(self.next_level_req())) + \
               u"{}Location: {}\n".format(self.location.emoji, self.location.cstring) + \
                levelled_up_text + '\n\n'
    def battle_text(self):
        return u'\U0001F466''<b>{}</b>\n'.format(self.name) + \
               u'\U000026A1'"Level: {}\n".format(self.level) + \
               u'\U0001F534'"Health: {}/{}\n".format(self.health, self.max_health) + \
               u'\U0001F535'"Mana: {}/{}\n".format(self.mana, self.max_mana) + '\n\n'

    def die(self):
        self.status == UserStatus.READY
        self.location = Location.VILLAGE
        self.health = self.max_health
        self.mana = self.max_mana

    def receive_damage(self, damage):
        self.health = max(0, self.health-damage)