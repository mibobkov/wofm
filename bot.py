from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
import logging
from configuration import TOKEN, db_param
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from MessageProcessor import MessageProcessor
from EntityManager import EntityManager

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

mp = MessageProcessor(entity_manager)

def start(bot, update):
    mp.start(bot, update)

def message(bot, update):
    mp.message(bot, update)

start_handler = CommandHandler('start', start)
message_handler = MessageHandler([Filters.text], message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
