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

    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    def set_name(self, name):
        self.name = name

    def get_damage(self):
        return random.randint(self.mindamage, self.maxdamage)

    def stats_text(self):
        return u'\U0001F466''{}\n' \
               u'\U0001F534'"Health: {}/{}\n" \
               u'\U0001F535'"Mana: {}/{}\n" \
               "{}Location: {}\n".format(self.name, self.health, self.max_health, self.mana, self.max_mana, self.location.emoji, self.location.string)

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
        self.bot.send_message(chat_id=self.chat_id, text=text, reply_markup=markup)
