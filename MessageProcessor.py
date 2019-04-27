from locations import *
from User import User
from Monster import Monster
from Monster import rat_params

class MessageProcessor:
    def __init__(self, entityManager):
        self.entityManager = entityManager

    def register_user(self, bot, chat_id):
        user = User(chat_id)
        user.set_bot(bot)
        self.entityManager.add(user)
        user.send_message("Enter your name:\n")

    def set_user_name(self, user, message):
        user.set_name(message)
        user.status = 'ready'
        user.send_message(user.stats_text() + 'You are {} now\n'.format(message), keyboard=actionsin[user.location])

    def go_to_location(self, user, message):
        if message in user.location.prettypaths:
            user.location = Location.toEnum(message)
            user.status = 'ready'
            user.send_message(user.stats_text() + user.location.text, keyboard=actionsin[user.location])

    def choose_location(self, user, message):
        user.status = 'going'
        user.send_message('Where do you want to go?\n', keyboard=pathkeyboards[user.location])


    def fight_monsters(self, user, message):
        monster = Monster(user.chat_id, *rat_params)
        self.entityManager.add(monster)
        user.status = 'fighting'
        user.send_message('You are fighting a {}\n'
                          '{}/{} hp\n'
                          '{}'.format(monster.name, monster.health, monster.maxhealth, monster.text), keyboard=fightactions)

    def attack(self, user, message):
        monster = self.entityManager.getEntityByField(Monster, 'user_id', user.chat_id)
        if not monster:
            user.status = 'ready'
            return
        damage_dealt = user.get_damage()
        damage_received = monster.get_damage()
        user.receive_damage(damage_received)
        monster.receive_damage(damage_dealt)
        text = 'You attacked and were attacked (3rd Law of Newton)!\n' + \
               'You dealt {} damage and received {} damage.\n'.format(damage_dealt, damage_received)
        if user.health == 0:
            user.die()
            self.entityManager.delete(monster)
            user.send_message('You died, but were revived in the village by the hobo community.\n')
        if monster.health == 0:
            gold = monster.get_gold()
            exp = monster.get_exp()
            user.give_gold(gold)
            user.give_exp(exp)
            text = user.stats_text() + \
                   text + \
                   'You killed the monster!\n' + \
                   'You have gained <b>{}</b> exp and <b>{}</b> gold!'.format(exp, gold)
            user.status = 'ready'
            self.entityManager.delete(monster)
            keyboard = actionsin[user.location]
        else:
            keyboard = fightactions
        user.send_message(text, keyboard=keyboard)
        #else:
        #    user.send_message('You are not fighting anyone\n', keyboard=actionsin[user.location])

    def show_leaderboard(self, user, message):
        userlist = []
        for u in self.entityManager.getAll(User):
            userlist.append(u)
        sortedList = sorted(userlist, key=lambda x: x.exp, reverse=True)
        text = 'Leaderboard: \n'
        count = 1
        for el in sortedList:
            if el.chat_id == user.chat_id:
                text += u'{}. <b>{}</b>: {} lvl, {} exp\n'.format(count, el.name, el.level, el.exp)
            else:
                text += u'{}. {}: {} lvl, {} exp\n'.format(count, el.name, el.level, el.exp)
            count += 1
        user.send_message(text, keyboard=actionsin[user.location])

    def message(self, bot, update):
        user = self.entityManager.getEntityByField(User, 'chat_id', update.message.chat_id)
        if not user:
            self.register_user(bot, update.message.chat_id)
            return
        else:
            user.set_bot(bot)

        message = update.message.text

        if user.status == 'set_name':
            self.set_user_name(user, message)
        elif user.status == 'going':
            self.go_to_location(user, message)
        elif user.status == 'ready' and message == 'Go somewhere':
            self.choose_location(user, message)
        elif user.status == 'ready' and message == 'Fight monsters' and user.location == Location.FOREST:
            self.fight_monsters(user, message)
        elif message == 'Attack' and user.status == 'fighting':
            self.attack(user, message)
        elif message == 'Leaderboard':
            self.show_leaderboard(user, message)
        else:
            user.send_message(user.stats_text(), keyboard=actionsin[user.location])
        self.entityManager.commit()

    def start(self, bot, update):
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, text="Welcome to the World of Magic!")
        user = self.entityManager.getEntityByField(User, 'chat_id', chat_id)
        if not user:
            self.register_user(bot, chat_id)
        else:
            user.send_message(user.stats_text(), keyboard=actionsin[user.location])
        self.entityManager.commit()
