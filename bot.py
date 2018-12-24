from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
import logging
from configuration import TOKEN
from locations import *
from User import User
from Monster import Monster
import random

users = {}

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG)

def register_user(bot, update):
    chat_id = update.message.chat_id
    users[chat_id] = User(bot, chat_id)
    bot.send_message(chat_id=chat_id, text="Enter your name")

def set_user_name(user, message):
    user.set_name(message)
    user.status = 'ready'
    user.send_message(user.stats_text() + 'You are ' + message + ' now\n', keyboard=actionsin[user.location])

def go_to_location(user, message):
    if message in user.location.prettypaths:
        user.location = Location.toEnum(message)
        user.status = 'ready'
        user.send_message(user.stats_text() + user.location.text, keyboard=actionsin[user.location])

def choose_location(user, message):
    user.status = 'going'
    user.send_message('Where do you want to go?', keyboard=pathkeyboards[user.location])

rat_params = ('Rat', 'This rat is agressive because it is ugly\n', 10, 1, 2, 2, 2)
fightactions = [['Attack']]

def fight_monsters(user, message):
    monster = Monster(*rat_params)
    user.fighting = monster
    user.status = 'fighting'
    user.send_message('You are fighting a {}\n'
                      '{}/{} hp\n'
                      '{}'.format(monster.name, monster.health, monster.maxhealth, monster.text), keyboard=fightactions)

def attack(user, message):
    if user.fighting != None:
        damage_dealt = user.get_damage()
        damage_received = user.fighting.get_damage()
        user.receive_damage(damage_received)
        user.fighting.receive_damage(damage_dealt)
        text = 'You attacked and were attacked (3rd Law of Newton)!\n' + \
                          'You dealt {} damage and received {} damage\n'.format(damage_dealt, damage_received)
        if user.health == 0:
            user.die()
            user.send_message('You died, but were revived in the village by the hobo community.\n')
        if user.fighting.health == 0:
            text += 'You killed the monster!'
            gold = user.fighting.get_gold()
            user.gold += gold
            exp = user.fighting.get_exp()
            user.give_exp(exp)
            text += 'You have gained <b>{}</b> exp and <b>{}</b> gold!'.format(exp, gold)
            text = user.stats_text() + text
            user.fighting = None
            keyboard = actionsin[user.location]
        else:
            keyboard = fightactions
        user.send_message(text, keyboard=keyboard)
    else:
        user.send_message('You are not fighting anyone\n', keyboard=actionsin[user.location])

def show_leaderboard(user, message):
    userlist = []
    for u in users:
        userlist.append(users[u])
    sortedList = sorted(userlist, lambda x: x.exp, reverse=True)
    text = 'Leaderboard: \n'
    count = 1
    for el in sortedList:
        if el.chat_id == user.chat_id:
            text += '{}. <b>{}</b>: {} lvl, {} exp\n'.format(count, el.name, el.level, el.exp)
        else:
            text += '{}. {}: {} lvl, {} exp\n'.format(count, el.name, el.level, el.exp)
        count += 1
    user.send_message(text, keyboard=actionsin[user.location])

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
    elif message == 'Fight monsters' and user.location == Location.FOREST:
        fight_monsters(user, message)
    elif message == 'Attack' and user.status == 'fighting':
        attack(user, message)
    elif message == 'Leaderboard':
        show_leaderboard(user, message)
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
