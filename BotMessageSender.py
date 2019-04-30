import telegram

class BotMessageSender:
    def __init__(self, bot):
        self.bot = bot

    def send_message(self, chat_id, text, keyboard=None):
        if keyboard != None:
            markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True,)
        else:
            markup = telegram.ReplyKeyboardRemove()
        self.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)
