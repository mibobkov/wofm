import telegram

class User:
    location = 'village'
    mana = 100
    max_mana = 100
    name= ""
    status= 'set_name'

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
