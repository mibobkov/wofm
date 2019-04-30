from locations import *
from User import User, UserStatus
from Monster import Monster
from Monster import rat_params
from copy import copy, deepcopy

class MessageProcessor:
    def __init__(self, entityManager, messageSender):
        self.entityManager = entityManager
        self.ms = messageSender

    def register_user(self, chat_id):
        user = User(chat_id)
        self.entityManager.add(user)
        self.ms.send_message(chat_id, "Enter your name:\n")

    def set_user_name(self, user, message):
        user.set_name(message)
        user.status = UserStatus.READY
        self.ms.send_message(user.chat_id, user.stats_text() + 'You are {} now\n'.format(message), keyboard=actionsin[user.location])

    def spawn_monsters(self, chat_id, location):
        r = random.random()
        acc = 0
        for i in range(0, len(monsterSpawnRates[location])):
            if acc + monsterSpawnRates[location][i] > r:
                mp = monsterParams[i]
                monster = Monster(chat_id, *mp)
                self.entityManager.add(monster)
                return monster
            else:
                acc += monsterSpawnRates[location][i]
        return None

    def delete_monster(self, chat_id):
        monster = self.entityManager.getEntityByField(Monster, 'user_id', chat_id)
        if monster != None:
            self.entityManager.delete(monster)

    def generateLocationActions(self, user):
        monster = self.entityManager.getEntityByField(Monster, 'user_id', user.chat_id)
        actions = deepcopy(actionsin[user.location])
        if user.status == UserStatus.FIGHTING or user.status == UserStatus.DUELLING:
            return fightactions
        if user.status == UserStatus.DUELLING_ATTACKED:
            return [[]]
        if monster != None:
            actions = [['Fight monster']] + actions
        if user.location == Location.ARENA and user.status == UserStatus.READY:
            actions += [['Duel']]
        return actions

    def go_to_location(self, user, message):
        if message in user.location.prettypaths:
            self.delete_monster(user.chat_id)
            user.location = Location.toEnum(message)
            user.status = UserStatus.READY
            spawned_monster = self.spawn_monsters(user.chat_id, user.location)
            actions = self.generateLocationActions(user)
            self.ms.send_message(user.chat_id, user.stats_text() + user.location.text +'\n' + ('' if not spawned_monster else spawned_monster.text), keyboard=actions)

    def choose_location(self, user, message):
        user.status = UserStatus.GOING
        self.ms.send_message(user.chat_id, 'Where do you want to go?\n', keyboard=pathkeyboards[user.location])


    def fight_monster(self, user, message):
        monster = self.entityManager.getEntityByField(Monster, 'user_id', user.chat_id)
        if not monster:
            self.ms.send_message(user.chat_id, 'There is no one to fight\n', keyboard=self.generateLocationActions(user))
            return
        user.status = UserStatus.FIGHTING
        self.ms.send_message(user.chat_id, 'You are fighting a {}\n'
                          '{}/{} hp\n'.format(monster.name, monster.health, monster.maxhealth), keyboard=fightactions)

    def attack(self, user, message):
        if message != 'Attack':
            self.ms.send_message(user.chat_id, "Invalid action", fightactions)
            return
        monster = self.entityManager.getEntityByField(Monster, 'user_id', user.chat_id)
        if not monster:
            user.status = UserStatus.READY
            return
        damage_dealt = user.get_damage()
        damage_received = monster.get_damage()
        user.receive_damage(damage_received)
        monster.receive_damage(damage_dealt)
        text = ('You dealt {} damage and received {} damage.\n' +
               'Remaining health: {}/{}\n' +
               '{}: {}/{}\n').format(damage_dealt, damage_received, user.health, user.max_health, monster.name, monster.health, monster.maxhealth)
        if user.health == 0:
            user.die()
            self.entityManager.delete(monster)
            self.ms.send_message(user.chat_id, 'You died, but were revived in the village by the hobo community.\n')
            keyboard = self.generateLocationActions(user)
        elif monster.health == 0:
            gold = monster.get_gold()
            exp = monster.get_exp()
            user.give_gold(gold)
            user.give_exp(exp)
            text = user.stats_text() + \
                   text + \
                   'You killed the monster and gained <b>{}</b> exp and <b>{}</b> gold!'.format(exp, gold)
            user.status = UserStatus.READY
            self.entityManager.delete(monster)
            keyboard = self.generateLocationActions(user)
        else:
            keyboard = fightactions
        self.ms.send_message(user.chat_id, text, keyboard=keyboard)
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
                text += u'{}. <b>{}</b>: {} lvl, {} exp, {}\n'.format(count, el.name, el.level, el.exp, el.location.cstring)
            else:
                text += u'{}. {}: {} lvl, {} exp, {}\n'.format(count, el.name, el.level, el.exp, el.location.cstring)
            count += 1
        self.ms.send_message(user.chat_id, text, keyboard=self.generateLocationActions(user))

    def choose_duel(self, user, message):
        if user.location != Location.ARENA:
            self.ms.send_message(user.chat_id, 'You must be in the arena to duel\n', keyboard=self.generateLocationActions(user))
            return
        users = self.entityManager.getAllByField(User, 'location', user.location)
        text = ''
        for u in users:
            if u.chat_id != user.chat_id:
                text += '{}: {}, id: {}'.format(u.name, u.level, u.chat_id)
        if text == '':
            self.ms.send_message(user.chat_id, 'No one in the arena\n')
        else:
            user.status = UserStatus.STARTING_DUEL
            self.ms.send_message(user.chat_id, 'Send the id of who you want to fight: \n' + text)

    def send_duel(self, user, message):
        target_user = self.entityManager.getEntityByField(User, 'chat_id', message)
        if not target_user:
            user.status = UserStatus.READY
            self.ms.send_message(user.chat_id, 'Sorry, no such player\n')
        elif target_user.location != Location.ARENA:
            self.ms.send_message(user.chat_id, 'Sorry, this player has left the arena\n')
        elif target_user.status != UserStatus.READY:
            self.ms.send_message(user.chat_id, "Sorry, this player seems to be busy\n")
        else:
            self.ms.send_message(user.chat_id, "Sent the invitation to the user.\n")
            self.ms.send_message(target_user.chat_id, "You have received a duel invite from {}.".format(user.name), keyboard=self.generateLocationActions(target_user) + [["Duel {}".format(user.chat_id)]])

    def accept_duel(self, user, message):
        target_id = int(message.split(' ')[1])
        target_user = self.entityManager.getEntityByField(User, 'chat_id', target_id)
        if not target_user:
            user.status = UserStatus.READY
            self.ms.send_message(user.chat_id, 'Sorry, no such player\n', self.generateLocationActions(user))
        elif target_user.location != Location.ARENA:
            user.status = UserStatus.READY
            self.ms.send_message(user.chat_id, 'Sorry, this player has left the arena\n', self.generateLocationActions(user))
        elif target_user.status != UserStatus.STARTING_DUEL:
            user.status = UserStatus.READY
            self.ms.send_message(user.chat_id, 'Sorry this player seems to no longer want a duel\n', self.generateLocationActions(user))
        else:
            user.status = UserStatus.DUELLING
            user.opponent = target_user.chat_id
            target_user.opponent = user.chat_id
            target_user.status = UserStatus.DUELLING
            self.ms.send_message(user.chat_id, user.stats_text() + target_user.stats_text(), keyboard=fightactions)
            self.ms.send_message(target_user.chat_id, target_user.stats_text() + user.stats_text(), keyboard=fightactions)

    def duel(self, user, message):
        if message != 'Attack':
            self.ms.send_message(user.chat_id, 'Invalid action', fightactions)
            return
        opponent = self.entityManager.getEntityByField(User, 'chat_id', user.opponent)
        if opponent.status == UserStatus.DUELLING:
            user.status = UserStatus.DUELLING_ATTACKED
            self.ms.send_message(user.chat_id, 'Attacked, waiting for opponent', keyboard=[[]])
        else:
            user.status = UserStatus.DUELLING
            opponent.status = UserStatus.DUELLING
            user_damage = user.get_damage()
            opponent_damage = opponent.get_damage()
            user.receive_damage(opponent_damage)
            opponent.receive_damage(user_damage)
            user_text = 'You dealt {} damage and received {} damage\n'.format(user_damage, opponent_damage)
            opponent_text = 'You dealt {} damage and received {} damage\n'.format(opponent_damage, user_damage)

            if user.health == 0 and opponent.health == 0:
                user_text += '<b>Its a draw</b>\n'
                opponent_text += '<b>Its a draw</b>\n'
            elif user.health == 0:
                user_text += '<b>You lost</b>!\n'
                opponent_text += '<b>You won</b>!\n'
            elif opponent.health == 0:
                user_text += '<b>You won!</b>\n'
                opponent_text += '<b>You lost!</b>\n'
            finished = user.health == 0 or opponent.health == 0
            if finished:
                user.status = UserStatus.READY
                opponent.status = UserStatus.READY
                user.opponent = None
                opponent.opponent = None

            self.ms.send_message(user.chat_id, user.battle_text() + opponent.battle_text() + user_text, keyboard=fightactions if not finished else self.generateLocationActions(user))
            self.ms.send_message(opponent.chat_id, opponent.battle_text() + user.battle_text() + opponent_text, keyboard=fightactions if not finished else self.generateLocationActions(opponent))

    #######################
    ## Command handlers: ##
    #######################

    def message(self, chat_id, message):
        user = self.entityManager.getEntityByField(User, 'chat_id', chat_id)
        if not user:
            self.register_user(chat_id)
            self.entityManager.commit()
            return

        if   user.status == UserStatus.SET_NAME:      self.set_user_name(user, message)
        elif user.status == UserStatus.STARTING_DUEL: self.send_duel(user, message)
        elif user.status == UserStatus.GOING:         self.go_to_location(user, message)
        elif user.status == UserStatus.FIGHTING:      self.attack(user, message)
        elif user.status == UserStatus.DUELLING:      self.duel(user, message)
        elif user.status == UserStatus.READY:
            if   message == 'Duel':                   self.choose_duel(user, message)
            elif message == 'Go somewhere':           self.choose_location(user, message)
            elif message == 'Fight monster':          self.fight_monster(user, message)
            elif len(message.split(' ')) == 2 \
                 and message.split(' ')[0] == 'Duel': self.accept_duel(user, message)
            elif message == 'Leaderboard':            self.show_leaderboard(user, message)
        else:
            self.ms.send_message(user.chat_id, user.stats_text(), keyboard=self.generateLocationActions(user))
        self.entityManager.commit()

    def broadcast(self, chat_id, message):
        user = self.entityManager.getEntityByField(User, 'chat_id', chat_id)
        if not user:
            self.register_user(chat_id)
            self.entityManager.commit()
            return

        users = self.entityManager.getAll(User)
        for u in users:
            self.ms.send_message(u.chat_id, text='Broadcast from ' + user.name + ': ' + message, keyboard=self.generateLocationActions(user))


    def start(self, chat_id, message):
        self.ms.send_message(chat_id=chat_id, text="Welcome to the World of Magic!")
        user = self.entityManager.getEntityByField(User, 'chat_id', chat_id)
        if not user:
            self.register_user(chat_id)
        else:
            self.ms.send_message(user.chat_id, user.stats_text(), keyboard=self.generateLocationActions(user))
        self.entityManager.commit()
