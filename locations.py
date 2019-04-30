from enum import Enum

class Location(Enum):
    VILLAGE  = 'village', \
               'You are in the village. \n', \
               ['arena', 'forest'], \
               u'\U0001F3E0'
    FOREST   = 'forest', \
               'You are in the forest. Villagers are following you. Why? Nobody knows.\n',\
               ['village', 'lake'],\
               u'\U0001F332'
    ARENA    = 'arena', \
               'You are in the arena. You see a pair of gladiators fighting. You want to join but the desire to live stops you from such rash actions.\n', \
               ['village'], \
               u'\U0001F93A'
    LAKE     = 'lake', \
               'You are near a giant lake.',\
               ['forest', 'town'],\
               u'\U0001F4A7'
    TOWN     = 'town', \
               'You are in a small town.',\
               ['lake', 'fountain', 'Mielee forest'], \
               u'\U0001F3E0'
    FOUNTAIN = 'fountain', \
               'You are near a small magical fountain. They say if you drink from it, your strength will be restored.', \
               ['town'], \
               u'\U0001F3E0' # TODO: this is placeholder emoji
    MIELEE_FOREST = 'Mielee forest', \
                    'You are in the Mielee forest. Its nice and fresh and it seems like one can stay here forever.', \
                    ['town', 'Mielee forest hut'], \
                    u'\U0001F3E0' # TODO: this is placeholder emoji
    MIELEE_FOREST_HUT = 'Mielee forest hut', \
                      'Abandoned hut, where travellers can stay and relax.', \
                      ['Mielee forest', 'Dogo village'], \
                      u'\U0001F3E0' # TODO: this is placeholder emoji
    DOGO_VILLAGE = 'Dogo village', \
                   'You are in a dogo village. Dogos seem to be very friendly creatures and quite hardworking.', \
                   ['Mielee forest hut', 'House of the Greater Dogo', 'Dogo Pond'], \
                   u'\U0001F3E0'
    HOUSE_OF_THE_GREATER_DOGO = 'House of the Greater Dogo', \
                                'You are in a house of the Greater Dogo, the most respected and influential figure in this town.', \
                                ['Dogo village'], \
                                u'\U0001F3E0'
    DOGO_POND = 'Dogo Pond', \
                'You approach an oddly shaped dark pond, that dogos seem to avoid and never look at.', \
                ['Dogo village'], \
                u'\U0001F3E0' # TODO: this is placeholder emoji

    def __init__(self, string, text, paths, emoji):
        self.emoji = emoji
        self.text = text
        self.string = string
        self.paths = paths

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
        for path in self.paths:
            prettypaths.append(self.toEnum(path).emoji+path.capitalize())
        return prettypaths

    @property
    def cstring(self):
        return self.string.capitalize()

actionsin = {}
actionsin[Location.VILLAGE] = []
actionsin[Location.ARENA] = []
actionsin[Location.FOREST] = []
actionsin[Location.LAKE] = []
actionsin[Location.TOWN] = []
actionsin[Location.FOUNTAIN] = []
actionsin[Location.MIELEE_FOREST] = []
actionsin[Location.MIELEE_FOREST_HUT] = []
actionsin[Location.DOGO_VILLAGE] = []
actionsin[Location.HOUSE_OF_THE_GREATER_DOGO] = []
actionsin[Location.DOGO_POND] = []
for place in actionsin:
    actionsin[place] += ['Go somewhere'], ['Leaderboard']


from monster import *
monsterParams = [rat_params, goblin_params, spider_params, wolf_params, devil_params]
monsterSpawnRates = {}
monsterSpawnRates[Location.VILLAGE] = [0, 0, 0, 0, 0]
monsterSpawnRates[Location.ARENA] = [0, 0, 0, 0, 0]
monsterSpawnRates[Location.FOREST] = [0.1, 0.05, 0.2, 0.1, 0]
monsterSpawnRates[Location.LAKE] = [0, 0, 0.2, 0.05, 0]
monsterSpawnRates[Location.TOWN] = [0, 0, 0, 0, 0]
monsterSpawnRates[Location.FOUNTAIN] = [0, 0, 0, 0, 0]
monsterSpawnRates[Location.MIELEE_FOREST] = [0, 0, 0.1, 0, 0]
monsterSpawnRates[Location.MIELEE_FOREST_HUT] = [0, 0, 0, 0, 0]
monsterSpawnRates[Location.DOGO_VILLAGE] = [0, 0, 0, 0, 0]
monsterSpawnRates[Location.HOUSE_OF_THE_GREATER_DOGO] = [0, 0, 0, 0, 0]
monsterSpawnRates[Location.DOGO_POND] = [0, 0, 0, 0, 1]

pathkeyboards = {}
for location in Location:
    path = location.prettypaths
    pathkeyboards[location] = []
    for place in path:
        pathkeyboards[location].append([place])

fightactions = [['Attack']]
