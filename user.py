import telegram
import random

from armor_entry import Armor
from locations import Location
import math
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, Enum as sqEnum
from base import Base
from enum import Enum
from weapon_entry import Weapon

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
    equipped_weapon = Column(Integer)
    equipped_armor = Column(Integer)

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
        self.equipped_weapon = None
        self.equipped_armor = None

    def set_name(self, name):
        self.name = name

    def get_damage(self):
        weapon_damage = 0
        if self.equipped_weapon:
            weapon_damage = Weapon.idToEnum(self.equipped_weapon).damage
        return random.randint(self.mindamage+weapon_damage, self.maxdamage+weapon_damage)

    def give_gold(self, amount):
        self.gold += amount

    def give_exp(self, amount):
        self.exp += amount
        if self.should_level_up():
            self.level_up()

    def should_level_up(self):
        return self.exp >= self.next_level_req()

    def next_level_req(self):
        return math.ceil(10*(1.3**self.level-1)/(0.2))

    def level_up(self):
        self.level += 1
        self.levelled_up = True
        self.max_health = int(100*(1.08**(self.level-1)))
        self.health = self.max_health
        self.max_mana += 10
        self.mana = self.max_mana
        self.mindamage = 2 + self.level + ((self.level-1)*(self.level))//10
        self.maxdamage = 4 + 2*self.level + 2*((self.level-1)*(self.level))//10

    def stats_text(self):
        levelled_up_text = ''
        if self.levelled_up:
            levelled_up_text = '<b>You have levelled up! Congratulations!</b>\n'
        self.levelled_up = False

        return u'\U0001F466''<b>{}</b>\n'.format(self.name) + \
               u'\U000026A1'"Level: {}\n".format(self.level) + \
               u'\U00002764'"Health: {}/{}\n".format(self.health, self.max_health) + \
               u'\U0001F535'"Mana: {}/{}\n".format(self.mana, self.max_mana) + \
               u'\U0001F4A1'"Exp: {}/{}\n".format(self.exp, int(self.next_level_req())) + \
               u'\U0001F4B0'"Gold: {}\n".format(self.gold) + \
               u'\U0001F5E1''{}'.format('Equipped weapon: {}\n'.format(Weapon.idToEnum(self.equipped_weapon).cstring) if self.equipped_weapon else '') + \
               u'\U0001F5E1''{}'.format('Equipped armor: {}\n'.format(Armor.idToEnum(self.equipped_armor).cstring) if self.equipped_armor else '') + \
               u"{}Location: {}\n".format(self.location.emoji, self.location.cstring) + \
                levelled_up_text + '\n' + \
                self.location_text()
    def battle_text(self):
        return u'\U0001F466''<b>{}</b>\n'.format(self.name) + \
               u'\U000026A1'"Level: {}\n".format(self.level) + \
               u'\U00002764'"Health: {}/{}\n".format(self.health, self.max_health) + \
               u'\U0001F535'"Mana: {}/{}\n".format(self.mana, self.max_mana) + '\n\n'

    def location_text(self):
        paths = self.location.paths
        nPath = None if not paths['N'] else Location.toEnum(paths['N'])
        sPath = None if not paths['S'] else Location.toEnum(paths['S'])
        wPath = None if not paths['W'] else Location.toEnum(paths['W'])
        ePath = None if not paths['E'] else Location.toEnum(paths['E'])

        nPathString = nPath.emoji + '/go_' + str(nPath.id) + ' ' + nPath.cstring if nPath else ''
        sPathString = sPath.emoji + '/go_' + str(sPath.id) + ' ' + sPath.cstring if sPath else ''
        ePathString = ePath.emoji + '/go_' + str(ePath.id) + ' ' + ePath.cstring if ePath else ''

        text  = '             {}\n'.format(nPathString)
        text += '    {}{}{}\n'.format('__' + wPath.emoji if wPath else '         ', u'\U0001F466', ePathString)
        text += '  {}          {}\n'.format('/' if wPath else ' ', sPathString)
        text += '/go_{}\n'.format(str(wPath.id) + ' ' +  wPath.cstring + '\n') if wPath else '\n'
        return text

    def die(self):
        self.status = UserStatus.READY
        self.location = Location.VILLAGE
        self.health = self.max_health
        self.mana = self.max_mana

    def receive_damage(self, damage):
        if self.equipped_armor:
            armor = Armor.idToEnum(self.equipped_armor)
            damage = max(0, int(damage*(1-armor.protection/100))-armor.protection)
        self.health = max(0, self.health-damage)
        return damage
