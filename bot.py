import telegram
from telegram.ext import Updater
from configuration import TOKEN
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
import logging

users = {}
SET_NAME = 'set_name'

# Village - spawn point
# Forest - kill random things
# Arena - pvp

locationtexts = {}
locationtexts['village'] = "You are in the village\n"
locationtexts['forest'] = "You are in the forest\n"
locationtexts['arena'] = "You are in the arena\n"

actionsin = {}
actionsin['village'] = [['Stand in the middle of the village and do nothing\n'], ['Go somewhere']]
actionsin['arena'] = [['Look around\n'], ['Go somewhere'] ]
actionsin['forest'] = [['Bam bam, I am in the forest.\n'], ['Go somewhere']]

paths = {}
paths['village'] = ['arena', 'forest']
paths['forest'] = ['village']
paths['arena'] = ['village']

pathkeyboards = {}
for path in paths:
    pathkeyboards[path] = []
    for place in paths[path]:
        pathkeyboards[path].append([place])

class User:
    location = 'village'
    mana = 100
    max_mana = 100
    name= ""
    status= SET_NAME

    def __User__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    def set_name(self, name):
        self.name = name

    def stats_text(self):
        return "{}\n" \
               "You are in {}\n".format(self.name, self.location)
    def send_message(self, text, keyboard=None):
        if keyboard != None:
            markup = telegram.ReplyKeyboardMarkup(keyboard)
        else:
            markup = telegram.ReplyKeyboardRemove()
        self.bot.send_message(chat_id=self.chat_id, text=text, reply_markup=markup)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def register_user(bot, update):
    chat_id = update.message.chat_id
    users[chat_id] = User(bot, chat_id)
    bot.send_message(chat_id=chat_id, text="Enter your name")

def message(bot, update):
    if update.message.chat_id not in users:
        register_user(bot, update)
        return
    user = users[update.message.chat_id]
    text = update.message.text
    if user.status == SET_NAME:
        user.set_name(text)
        user.status = 'ready'
        user.send_message('You are ' + text + ' now', keyboard=actionsin[user.location])
        return
    elif user.status == 'going':
        if text in paths[user.location]:
            user.location = text
            user.status = 'ready'
            user.send_message(user.stats_text() + '\n\n\n', keyboard=actionsin[user.location])
    else:
        if text == 'Go somewhere':
            user.status = 'going'
            user.send_message('Where do you want to go?', keyboard=pathkeyboards[user.location])
            return
        else:
            user.send_message(user.stats_text(), keyboard=actionsin[user.location])
        return



def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Welcome to world of magic!")
    if update.message.chat_id not in users:
        register_user(bot, update)
        return


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

message_handler = MessageHandler([Filters.text], message)

dispatcher.add_handler(message_handler)

updater.start_polling()
