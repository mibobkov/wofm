# Village - spawn point
# Forest - kill random things
# Arena - pvp
from enum import Enum


class Location(Enum):
    VILLAGE = 'village', 'You are in the village. Villagers bitch about weather and are ugly as fuck. Inbreeding?\n', ['arena', 'forest'], u'\U0001F3E0'
    FOREST = 'forest', 'You are in the forest. Villagers are following you. Why? Nobody knows.\n', ['village', 'lake'], u'\U0001F332'
    ARENA = 'arena', 'You are in the arena. You see a pair of gladiators fighting. You want to join but the desire to live stops you from such rash actions.\n', ['village'], u'\U0001F93A'
    LAKE = 'lake', 'You are near a giant fucking lake. The lake is so big, you can almost fit yo mama in it.\n', ['forest'], u'\U0001F4A7'
    def __init__(self, string, text, paths, emoji):
        self.emoji = emoji
        self.text = text
        self.string = string
        self.paths = paths
    @staticmethod
    def toEnum(string):
        string = string.encode('ascii', 'ignore').lower()
        for loc in Location:
            if loc.string == string:
                return loc
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
actionsin[Location.VILLAGE] = [['Stand in the middle of the village and do nothing'], ['Go somewhere']]
actionsin[Location.ARENA] = [['Look around'], ['Go somewhere'] ]
actionsin[Location.FOREST] = [['Bam bam, I am in the forest.'], ['Fight monsters'], ['Go somewhere']]

pathkeyboards = {}
for location in Location:
    path = location.prettypaths
    pathkeyboards[location] = []
    for place in path:
        pathkeyboards[location].append([place])
