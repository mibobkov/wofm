import telegram
import random
from locations import Location

class User:
    location = Location.VILLAGE
    max_health = 100
    health = 100
    mana = 100
    max_mana = 100
    name = ""
    status= 'set_name'
    fighting = None
    mindamage = 2
    maxdamage = 4
    exp = 0
    gold = 0
    level = 1
    levelled_up = False

    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    def set_name(self, name):
        self.name = name

    def get_damage(self):
        return random.randint(self.mindamage, self.maxdamage)

    def give_exp(self, amount):
        self.exp += amount
        if self.should_level_up():
            self.level_up()

    def should_level_up(self):
        return self.exp > 10*(self.level-1)**1.2

    def level_up(self):
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
            levelled_up_text = '<b>You have levelled up! Congratulations</b>'
        self.levelled_up = False
        return u'\U0001F466''<b>{}</b>\n' \
               u'\U0001F534'"Health: {}/{}\n" \
               u'\U0001F535'"Mana: {}/{}\n" \
               "{}Location: {}".format(self.name, self.health, self.max_health, self.mana, self.max_mana, self.location.emoji, self.location.cstring) + \
                levelled_up_text + '\n\n\n'

    def die(self):
        self.status == 'ready'
        self.location = Location.VILLAGE
        self.health = self.max_health
        self.mana = self.max_mana

    def receive_damage(self, damage):
        self.health -= damage
        self.health = max(0, self.health)

    def send_message(self, text, keyboard=None):
        if keyboard != None:
            markup = telegram.ReplyKeyboardMarkup(keyboard)
        else:
            markup = telegram.ReplyKeyboardRemove()
        self.bot.send_message(chat_id=self.chat_id, text=text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)
