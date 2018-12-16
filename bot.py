from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
import logging
from configuration import TOKEN
from locations import *
from User import User

users = {}

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def register_user(bot, update):
    chat_id = update.message.chat_id
    users[chat_id] = User(bot, chat_id)
    bot.send_message(chat_id=chat_id, text="Enter your name")

def set_user_name(user, message):
    user.set_name(message)
    user.status = 'ready'
    user.send_message('You are ' + message + ' now', keyboard=actionsin[user.location])

def go_to_location(user, message):
    if message in paths[user.location]:
        user.location = message
        user.status = 'ready'
        user.send_message(user.stats_text() + '\n\n\n', keyboard=actionsin[user.location])

def choose_location(user, message):
    user.status = 'going'
    user.send_message('Where do you want to go?', keyboard=pathkeyboards[user.location])

def message(bot, update):
    if update.message.chat_id not in users:
        register_user(bot, update)
        return
    user = users[update.message.chat_id]
    message = update.message.text

    if user.status == 'set_name':
        set_user_name(user, message)
    elif user.status == 'going':
        go_to_location(user, message)
    elif message == 'Go somewhere':
        choose_location(user, message)
    else:
        user.send_message(user.stats_text(), keyboard=actionsin[user.location])

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Welcome to World of Magic!")
    if update.message.chat_id not in users:
        register_user(bot, update)
        return


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

message_handler = MessageHandler([Filters.text], message)

dispatcher.add_handler(message_handler)

updater.start_polling()
