from enum import Enum

class Location(Enum):
    VILLAGE  = 'village', \
               'You are in the village. It seems like the orcs have driven the villagers away and occupied the village\n', \
               {'S': None, 'N': None, 'W': 'arena', 'E': 'forest'}, \
               u'\U0001F3E0', \
               1
    FOREST   = 'forest', \
               'You are in the forest. Orcs are following you. Why? Cause they don\'t like you.\n', \
               {'S': 'deep forest', 'N': None, 'W': 'village', 'E': 'lake'}, \
               u'\U0001F332', \
               2
    ARENA    = 'arena', \
               'You are in the arena. You see a pair of gladiators fighting. You want to join but the desire to live stops you from such rash actions.\n', \
               {'S': None, 'N': None, 'W': None, 'E': 'village'}, \
               u'\U0001F93A', \
               3
    LAKE     = 'lake', \
               'You are near a giant lake.\n',\
               {'S': None, 'N': None, 'W': 'forest', 'E': 'town'}, \
               u'\U0001F4A7', \
               4
    TOWN     = 'town', \
               'You are in a small town.\n',\
               {'S': 'fountain', 'N': 'Mielee forest', 'W': 'lake', 'E': 'Weapon shop'}, \
               u'\U0001F3E0', \
               5
    FOUNTAIN = 'fountain', \
               'You are near a small magical fountain. They say if you drink from it, your strength will be restored.\n', \
               {'S': None, 'N': 'town', 'W': None, 'E': None}, \
               u'\U0001F4A7', \
               6
    MIELEE_FOREST = 'Mielee forest', \
                    'You are in the Mielee forest. Its nice and fresh and it seems like one can stay here forever.\n', \
                    {'S': 'town', 'N': 'Mielee forest hut', 'W': None, 'E': None}, \
                    u'\U0001F332', \
                    7
    MIELEE_FOREST_HUT = 'Mielee forest hut', \
                      'Abandoned hut, where travellers can stay and relax.\n', \
                        {'S': 'Mielee forest', 'N': 'Dogo village', 'W': None, 'E': None}, \
                        u'\U0001F3E0', \
                      8
    DOGO_VILLAGE = 'Dogo village', \
                   'You are in a dogo village. Dogos seem to be very friendly creatures and quite hardworking.\n', \
                   {'S': 'Mielee forest hut', 'N': None, 'W': 'Dogo pond', 'E': 'House of the Great Dogo'}, \
                   u'\U0001F3E0', \
                   9
    HOUSE_OF_THE_GREAT_DOGO = 'House of the Great Dogo', \
                                'You are in a house of the Great Dogo, the most respected and influential figure in this town.\n', \
                              {'S': None, 'N': None, 'W': 'Dogo village', 'E': None}, \
                              u'\U0001F3E0', \
                                10
    DOGO_POND = 'Dogo Pond', \
                'You approach an oddly shaped dark pond, that dogos seem to avoid and never look at.\n', \
                {'S': None, 'N': None, 'W': None, 'E': 'Dogo village'}, \
                u'\U0001F4A7', \
                11
    WEAPON_SHOP = 'Weapon shop', \
                  'You are in a weapon shop, preparing to spend your last money on exorbitantly overpriced iWeapons.\n', \
                  {'S': None, 'N': None, 'W': 'town', 'E': None}, \
                  u'\U0001F5E1', \
                  12
    DEEP_FOREST   = 'deep forest', \
               'You went deeper into the forest. It became darker and more menacing\n', \
               {'S': 'ancient ruins', 'N': 'forest', 'W': None, 'E': None}, \
               u'\U0001F332', \
               13
    ANCIENT_RUINS  = 'ancient ruins', \
               'You approached ruins of an ancient fort. You feel uneasy.\n', \
               {'S': None, 'N': 'deep forest', 'W': None, 'E': 'cemetry'}, \
               u'\U0001F3DB', \
               14
    CEMETRY   = 'cemetry', \
               'You see a vast cemetry and feel an aura of evil and malevolence.\n', \
               {'S': 'tomb', 'N': None, 'W': 'ancient ruins', 'E': None}, \
               u'\U000026B0', \
               15
    TOMB      = 'tomb', \
               'You see a tomb. Evil beings seem to occupy it.\n', \
               {'S': None, 'N': 'cemetry', 'W': None, 'E': None}, \
               u'\U000026B0', \
               16
    def __init__(self, string, text, paths, emoji, id):
        self.emoji = emoji
        self.text = text
        self.string = string
        self.paths = paths
        self.id = id
        self.monsterSpawnRates = {}
        self.actions = []

    @staticmethod
    def idToEnum(id):
        for loc in Location:
            if loc.id == id:
                return loc

    @staticmethod
    def toEnum(string):
        def delEmoji(s):
            if ord(s[0]) > 255:
                return s[1:]
            else:
                return s

        string = delEmoji(string).lower()
        for loc in Location:
            if loc.string.lower() == string:
                return loc
        else:
            print('No proper enums for string ' + string)

    @property
    def prettypaths(self):
        prettypaths = []
        for p in self.paths:
            path = self.paths[p]
            if self.paths[p] != None:
                prettypaths.append(self.toEnum(path).emoji+path.capitalize())
        return prettypaths

    @property
    def pathKeyboard(self):
        path = self.prettypaths
        pathKeyboard = []
        for place in path:
            pathKeyboard.append([place])
        return pathKeyboard

    @property
    def cstring(self):
        return self.string[0].capitalize()+self.string[1:]

Location.FOUNTAIN.actions = [['Drink from the fountain']]
Location.HOUSE_OF_THE_GREAT_DOGO.actions = [['Speak to the Great Dogo']]
Location.WEAPON_SHOP.actions = [['Trade']]
for loc in Location:
    loc.actions = loc.actions + [['Stats', 'Inventory', 'Leaderboard']]


from monster import MonsterType
Location.VILLAGE.monsterSpawnRates = {MonsterType.GOBLIN: 0.2, MonsterType.ORC: 0.6}
Location.FOREST.monsterSpawnRates = {MonsterType.RAT: 0.2,  MonsterType.SPIDER: 0.2, MonsterType.WOLF: 0.1, MonsterType.ORC: 0.2}
Location.LAKE.monsterSpawnRates = {MonsterType.GOBLIN: 0.3, MonsterType.SPIDER: 0.2, MonsterType.WOLF: 0.05, MonsterType.ORC: 0.1}
Location.MIELEE_FOREST.monsterSpawnRates = {MonsterType.SPIDER:0.1, MonsterType.WOLF:0.05}
Location.DEEP_FOREST.monsterSpawnRates = {MonsterType.BEAR: 0.3, MonsterType.TROLL: 0.1, MonsterType.WOLF: 0.3}
Location.ANCIENT_RUINS.monsterSpawnRates = {MonsterType.TROLL: 0.3, MonsterType.SKELETON: 0.2, MonsterType.BEAR: 0.2}
Location.CEMETRY.monsterSpawnRates = {MonsterType.SKELETON: 0.3, MonsterType.ZOMBIE: 0.3}
Location.TOMB.monsterSpawnRates = {MonsterType.ZOMBIE: 0.4, MonsterType.SKELETON: 0.5, MonsterType.LICH: 0.1}

fightactions = [['Attack']]
