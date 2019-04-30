from enum import Enum

class Location(Enum):
    VILLAGE  = 'village', \
               'You are in the village. \n', \
               {'S': None, 'N': None, 'W': 'arena', 'E': 'forest'}, \
               u'\U0001F3E0', \
               1
    FOREST   = 'forest', \
               'You are in the forest. Villagers are following you. Why? Nobody knows.\n', \
               {'S': None, 'N': None, 'W': 'village', 'E': 'lake'}, \
               u'\U0001F332', \
               2
    ARENA    = 'arena', \
               'You are in the arena. You see a pair of gladiators fighting. You want to join but the desire to live stops you from such rash actions.\n', \
               {'S': None, 'N': None, 'W': None, 'E': 'village'}, \
               u'\U0001F93A', \
               3
    LAKE     = 'lake', \
               'You are near a giant lake.',\
               {'S': None, 'N': None, 'W': 'forest', 'E': 'town'}, \
               u'\U0001F4A7', \
               4
    TOWN     = 'town', \
               'You are in a small town.',\
               {'S': 'fountain', 'N': 'Mielee forest', 'W': 'lake', 'E': None}, \
               u'\U0001F3E0', \
               5
    FOUNTAIN = 'fountain', \
               'You are near a small magical fountain. They say if you drink from it, your strength will be restored.', \
               {'S': None, 'N': 'town', 'W': None, 'E': None}, \
               u'\U0001F4A7', \
               6
    MIELEE_FOREST = 'Mielee forest', \
                    'You are in the Mielee forest. Its nice and fresh and it seems like one can stay here forever.', \
                    {'S': 'town', 'N': 'Mielee forest hut', 'W': None, 'E': None}, \
                    u'\U0001F332', \
                    7
    MIELEE_FOREST_HUT = 'Mielee forest hut', \
                      'Abandoned hut, where travellers can stay and relax.', \
                        {'S': 'Mielee forest', 'N': 'Dogo village', 'W': None, 'E': None}, \
                        u'\U0001F3E0', \
                      8
    DOGO_VILLAGE = 'Dogo village', \
                   'You are in a dogo village. Dogos seem to be very friendly creatures and quite hardworking.', \
                   {'S': 'Mielee forest hut', 'N': None, 'W': 'Dogo pond', 'E': 'House of the Great Dogo'}, \
                   u'\U0001F3E0', \
                   9
    HOUSE_OF_THE_GREAT_DOGO = 'House of the Great Dogo', \
                                'You are in a house of the Great Dogo, the most respected and influential figure in this town.', \
                              {'S': None, 'N': None, 'W': 'Dogo village', 'E': None}, \
                              u'\U0001F3E0', \
                                10
    DOGO_POND = 'Dogo Pond', \
                'You approach an oddly shaped dark pond, that dogos seem to avoid and never look at.', \
                {'S': None, 'N': None, 'W': None, 'E': 'Dogo village'}, \
                u'\U0001F3E0', \
                11

    def __init__(self, string, text, paths, emoji, id):
        self.emoji = emoji
        self.text = text
        self.string = string
        self.paths = paths
        self.id = id

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
    def cstring(self):
        return self.string[0].capitalize()+self.string[1:]

actionsin = {}
actionsin[Location.VILLAGE] = []
actionsin[Location.ARENA] = []
actionsin[Location.FOREST] = []
actionsin[Location.LAKE] = []
actionsin[Location.TOWN] = []
actionsin[Location.FOUNTAIN] = [['Drink from the fountain']]
actionsin[Location.MIELEE_FOREST] = []
actionsin[Location.MIELEE_FOREST_HUT] = []
actionsin[Location.DOGO_VILLAGE] = []
actionsin[Location.HOUSE_OF_THE_GREAT_DOGO] = [['Speak to the Great Dogo']]
actionsin[Location.DOGO_POND] = []
for place in actionsin:
    actionsin[place] += ['Inventory'], ['Leaderboard']


from monster import *
monsterParams = [rat_params, goblin_params, spider_params, wolf_params, devil_params]
monsterSpawnRates = {}
monsterSpawnRates[Location.VILLAGE] = [0, 0, 0, 0, 0]
monsterSpawnRates[Location.ARENA] = [0, 0, 0, 0, 0]
monsterSpawnRates[Location.FOREST] = [0.3, 0.05, 0.3, 0.1, 0]
monsterSpawnRates[Location.LAKE] = [0, 0.3, 0.2, 0.05, 0]
monsterSpawnRates[Location.TOWN] = [0, 0, 0, 0, 0]
monsterSpawnRates[Location.FOUNTAIN] = [0, 0, 0, 0, 0]
monsterSpawnRates[Location.MIELEE_FOREST] = [0, 0, 0.1, 0.05, 0]
monsterSpawnRates[Location.MIELEE_FOREST_HUT] = [0, 0, 0, 0, 0]
monsterSpawnRates[Location.DOGO_VILLAGE] = [0, 0, 0, 0, 0]
monsterSpawnRates[Location.HOUSE_OF_THE_GREAT_DOGO] = [0, 0, 0, 0, 0]
monsterSpawnRates[Location.DOGO_POND] = [0, 0, 0, 0, 1]

pathkeyboards = {}
for location in Location:
    path = location.prettypaths
    pathkeyboards[location] = []
    for place in path:
        pathkeyboards[location].append([place])

fightactions = [['Attack']]
