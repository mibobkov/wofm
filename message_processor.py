from locations import *
from user import User, UserStatus
from monster import Monster
from copy import copy, deepcopy
from resource_entry import ResourceEntry
from quotes import Quotes
from weapon_entry import Weapon, WeaponEntry
import random

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
        self.ms.send_message(user.chat_id, user.stats_text() + 'You are {} now\n'.format(message), keyboard=user.location.actions)

    def spawn_monsters(self, chat_id, location):
        r = random.random()
        acc = 0
        for mon in location.monsterSpawnRates:
            if acc + location.monsterSpawnRates[mon] > r:
                monster = Monster(chat_id, mon)
                self.entityManager.add(monster)
                return monster
            else:
                acc += location.monsterSpawnRates[mon]
        return None

    def delete_monster(self, chat_id):
        monster = self.entityManager.getEntityByField(Monster, 'user_id', chat_id)
        if monster != None:
            self.entityManager.delete(monster)

    def generateLocationActions(self, user):
        monster = self.entityManager.getEntityByField(Monster, 'user_id', user.chat_id)
        actions = deepcopy(user.location.actions)
        if user.status == UserStatus.FIGHTING or user.status == UserStatus.DUELLING:
            return fightactions
        if user.status == UserStatus.DUELLING_ATTACKED:
            return [[]]
        if monster:
            actions = [['Fight monster']] + actions
        if user.location == Location.ARENA and user.status == UserStatus.READY:
            actions += [['Duel']]
        return actions

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
        text = ( u'\U00002764''{} Health: {}/{}\n\n'.format(monster.name, monster.health, monster.maxhealth) +
                'You dealt <b>{} damage</b> and received <b>{} damage</b>.\n').format(damage_dealt, damage_received)
        if user.health == 0:
            user.die()
            self.entityManager.delete(monster)
            self.ms.send_message(user.chat_id, 'You died, but were revived in the village by the hobo community.\n')
            keyboard = self.generateLocationActions(user)
            self.ms.send_message(user.chat_id, user.stats_text(), keyboard=keyboard)
        elif monster.health == 0:
            gold = monster.get_gold()
            exp = monster.get_exp()
            user.give_gold(gold)
            user.give_exp(exp)
            resources = monster.get_loot()
            loot_text = ''
            for r in resources:
                loot_text += '<b>{}: {}</b>\n'.format(str(r), resources[r])
                current_res = self.entityManager.getEntityByTwoFields(ResourceEntry, 'user_id', user.chat_id, 'resource', r)
                if current_res != None:
                    current_res.quantity += resources[r]
                else:
                    current_res = ResourceEntry(user.chat_id, r, resources[r])
                    self.entityManager.add(current_res)
            if loot_text != '':
                loot_text = '\nLoot:\n\n' + loot_text
            text = text + \
                   ('You killed the monster and gained'+ u'\U0001F4A1''<b>{} exp</b> and ' + u'\U0001F4B0''<b>{} gold</b>!\n').format(exp, gold) + \
                   loot_text
            user.status = UserStatus.READY
            self.entityManager.delete(monster)
            self.ms.send_message(user.chat_id, text, keyboard=[])
            keyboard = self.generateLocationActions(user)
            self.ms.send_message(user.chat_id, user.stats_text(), keyboard=keyboard)
        else:
            text = user.battle_text() + text
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
            self.ms.send_message(user.chat_id, 'Sorry, no such player\n', self.generateLocationActions(user))
        elif target_user.location != Location.ARENA:
            user.status = UserStatus.READY
            self.ms.send_message(user.chat_id, 'Sorry, this player has left the arena\n', self.generateLocationActions(user))
        elif target_user.status != UserStatus.READY:
            user.status = UserStatus.READY
            self.ms.send_message(user.chat_id, "Sorry, this player seems to be busy\n", self.generateLocationActions(user))
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
            self.ms.send_message(user.chat_id, user.battle_text() + target_user.battle_text(), keyboard=fightactions)
            self.ms.send_message(target_user.chat_id, target_user.battle_text() + user.battle_text(), keyboard=fightactions)

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
            self.ms.send_message(user.chat_id, user.battle_text() + opponent.battle_text() + user_text, keyboard=fightactions)
            self.ms.send_message(opponent.chat_id, opponent.battle_text() + user.battle_text() + opponent_text, keyboard=fightactions)
            if finished:
                user.status = UserStatus.READY
                opponent.status = UserStatus.READY
                user.opponent = None
                opponent.opponent = None
                self.ms.send_message(user.chat_id, user.stats_text() + user_text, keyboard=self.generateLocationActions(user))
                self.ms.send_message(opponent.chat_id, opponent.stats_text() + opponent_text, keyboard=self.generateLocationActions(opponent))

    def show_inventory(self, user, message):
        resources = self.entityManager.getAllByField(ResourceEntry, 'user_id', user.chat_id)
        weapons = self.entityManager.getAllByField(WeaponEntry, 'user_id', user.chat_id)
        text = 'Resources:\n'
        for r in resources:
            text += '{} x {}\n'.format(str(r.resource), r.quantity)
        text += '------------\n\n'
        text += 'Weapons:\n'
        for w in weapons:
            text += '/equip_w{} {} x {}\n'.format(Weapon.toEnum(w.name).id, w.name, w.quantity)
        text += '------------\n'
        self.ms.send_message(user.chat_id, user.stats_text() + text, keyboard=self.generateLocationActions(user))

    def speak_to_great_dogo(self, user, message):
        if user.location != Location.HOUSE_OF_THE_GREAT_DOGO:
            return
        quotes = Quotes()
        quote = quotes.random()
        text = '<b>The Great Dogo says:</b>\n\nMy old friend, {}, once said:\n<i>{}</i>.\nI suggest you follow this advice!\n'.format(quote[0], quote[1])
        self.ms.send_message(user.chat_id, user.stats_text() + text, keyboard=self.generateLocationActions(user))

    def drink_from_the_fountain(self, user, message):
        if user.location != Location.FOUNTAIN:
            return
        user.health = user.max_health
        user.mana = user.max_mana
        text = 'Drink! Drink! Drink! Piracy\'s a crime, but drinking from the fountain of youth is not. You restored you health and mana.\n'
        self.ms.send_message(user.chat_id, user.stats_text() + text, keyboard=self.generateLocationActions(user))

    def trade(self, user, message):
        if user.location != Location.WEAPON_SHOP:
            return
        items = {Weapon.DAGGER, Weapon.SCIMITAR, Weapon.SWORD, Weapon.SWORD_OF_DAWN}
        text = 'Greetings traveller, what do you wanna buy?\n'
        for i in items:
            text += '/buy_w{} {}: {} gold\n'.format(i.id, i.cstring, i.base_cost)
        self.ms.send_message(user.chat_id, user.stats_text() + text, keyboard=self.generateLocationActions(user))

    #######################
    ## Command handlers: ##
    #######################

    def buy(self, chat_id, message):
        user = self.entityManager.getEntityByField(User, 'chat_id', chat_id)
        if not user:
            self.register_user(chat_id)
            self.entityManager.commit()
            return
        if user.status != UserStatus.READY:
            return
        item_type = message.split(' ')[0].split('_')[1][0]
        if item_type != 'w':
            return
        else:
            weapon_id = message.split(' ')[0].split('_')[1][1:]
            print(weapon_id)
            weapon = Weapon.idToEnum(weapon_id)
            print(weapon)
            if weapon == None:
                return
            if user.gold > weapon.base_cost:
                user.gold -= weapon.base_cost
                weapon_entry = self.entityManager.getEntityByTwoFields(WeaponEntry, 'user_id', user.chat_id, 'name', weapon.cstring)
                if weapon_entry == None:
                    weapon_entry = WeaponEntry(weapon.cstring, user.chat_id, 1)
                    self.entityManager.add(weapon_entry)
                else:
                    weapon_entry.quantity += 1
                self.ms.send_message(user.chat_id, user.stats_text() + 'You have bought {}!\n'.format(weapon.cstring), self.generateLocationActions(user))
            else:
                self.ms.send_message(user.chat_id, 'Need more gold!\n', self.generateLocationActions(user))
        self.entityManager.commit()

    def equip(self, chat_id, message):
        user = self.entityManager.getEntityByField(User, 'chat_id', chat_id)
        if not user:
            self.register_user(chat_id)
            self.entityManager.commit()
            return
        if user.status != UserStatus.READY:
            return
        item_type = message.split(' ')[0].split('_')[1][0]
        if item_type != 'w':
            return
        else:
            weapon_id = message.split(' ')[0].split('_')[1][1:]
            weapon = Weapon.idToEnum(weapon_id)
            if weapon == None:
                return
            user.equipped_weapon = weapon_id
            self.ms.send_message(user.chat_id, 'You equipped {}!\n'.format(weapon.cstring), self.generateLocationActions(user))
            self.entityManager.commit()

    def message(self, chat_id, message):
        print(message)
        user = self.entityManager.getEntityByField(User, 'chat_id', chat_id)
        if not user:
            self.register_user(chat_id)
            self.entityManager.commit()
            return

        if   user.status == UserStatus.SET_NAME:       self.set_user_name(user, message)
        elif user.status == UserStatus.STARTING_DUEL:  self.send_duel(user, message)
        elif user.status == UserStatus.FIGHTING:       self.attack(user, message)
        elif user.status == UserStatus.DUELLING:       self.duel(user, message)
        elif user.status == UserStatus.READY:
            if   message == 'Duel':                    self.choose_duel(user, message)
            elif message == 'Fight monster':           self.fight_monster(user, message)
            elif len(message.split(' ')) == 2 \
                 and message.split(' ')[0] == 'Duel':  self.accept_duel(user, message)
            elif message == 'Leaderboard':             self.show_leaderboard(user, message)
            elif message == 'Inventory':               self.show_inventory(user, message)
            elif message == 'Speak to the Great Dogo': self.speak_to_great_dogo(user, message)
            elif message == 'Drink from the fountain': self.drink_from_the_fountain(user, message)
            elif message == 'Trade':                   self.trade(user, message)
        else:
            self.ms.send_message(user.chat_id, user.stats_text(), keyboard=self.generateLocationActions(user))
        self.entityManager.commit()

        # elif user.status == UserStatus.GOING:          self.go_to_location(user, message)
        # elif message == 'Go somewhere':            self.choose_location(user, message)
    def broadcast(self, chat_id, message):
        user = self.entityManager.getEntityByField(User, 'chat_id', chat_id)
        if not user:
            self.register_user(chat_id)
            self.entityManager.commit()
            return

        users = self.entityManager.getAll(User)
        for u in users:
            self.ms.send_message(u.chat_id, text='Broadcast from ' + user.name + ': ' + message, keyboard=self.generateLocationActions(user))

    def go(self, chat_id, message):
        user = self.entityManager.getEntityByField(User, 'chat_id', chat_id)
        if not user:
            self.register_user(chat_id)

        if user.status != UserStatus.READY:
            return
        location_id = message.split(' ')[0].split('_')[1]
        location = Location.idToEnum(int(location_id))
        if location in [Location.toEnum(user.location.paths[x]) for x in user.location.paths if user.location.paths[x] != None]:
            self.delete_monster(user.chat_id)
            user.location = location
            user.status = UserStatus.READY
            spawned_monster = self.spawn_monsters(user.chat_id, user.location)
            actions = self.generateLocationActions(user)
            self.ms.send_message(user.chat_id, user.stats_text() + user.location.text +'\n' + ('' if not spawned_monster else spawned_monster.text), keyboard=actions)
        else:
            print('some error')
        self.entityManager.commit()

    def start(self, chat_id, message):
        self.ms.send_message(chat_id=chat_id, text="Welcome to the World of Magic!")
        user = self.entityManager.getEntityByField(User, 'chat_id', chat_id)
        if not user:
            self.register_user(chat_id)
        else:
            self.ms.send_message(user.chat_id, user.stats_text(), keyboard=self.generateLocationActions(user))
        self.entityManager.commit()
