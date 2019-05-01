from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext.commandhandler import CommandHandler
import logging
from configuration import TOKEN, db_param
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from bot_message_sender import BotMessageSender
from message_processor import MessageProcessor
from entity_manager import EntityManager

# Setting up mysqlalchemy
engine = create_engine(db_param, echo=True)
engine.connect()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

entity_manager = EntityManager(session)

# Setting up bot polling
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG)

ms = BotMessageSender(updater.bot)
mp = MessageProcessor(entity_manager, ms)

def start(bot, update):
    mp.start(update.message.chat_id, update.message.text)

def message(bot, update):
    mp.message(update.message.chat_id, update.message.text)

def broadcast(bot, update):
    mp.broadcast(update.message.chat_id, update.message.text)

def go(bot, update):
    mp.go(update.message.chat_id, update.message.text)

def buy(bot, update):
    mp.buy(update.message.chat_id, update.message.text)

def equip(bot, update):
    mp.equip(update.message.chat_id, update.message.text)

start_handler = CommandHandler('start', start)
message_handler = MessageHandler([Filters.text], message)
broadcast_handler = CommandHandler('broadcast', broadcast)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(broadcast_handler)

for i in range(0, 100):
    h = CommandHandler('go_' + str(i), go)
    dispatcher.add_handler(h)

for i in range(0, 100):
    h = CommandHandler('buy_w' + str(i), buy)
    dispatcher.add_handler(h)

for i in range(0, 100):
    h = CommandHandler('buy_a' + str(i), buy)
    dispatcher.add_handler(h)

for i in range(0, 100):
    h = CommandHandler('equip_w' + str(i), equip)
    dispatcher.add_handler(h)

for i in range(0, 100):
    h = CommandHandler('equip_a' + str(i), equip)
    dispatcher.add_handler(h)

updater.start_polling()
