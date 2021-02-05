from Block import *
from termcolor import colored
from random import random


MAP_SIZE = 13
DEFAULT_VALUES = [(DigableBlock,4, (0,0)),
                    (HomeBlock,2, (2,2)),
                    (CastleBlock, 1, (5,5))]
class Map:
    def __init__(self, path_to_save=None):
        self.map = []
        self.__init_map()
        self.__spawn_special_blocks()
        self.__complete_map()

    def __init_map(self):
        for i in range(MAP_SIZE):
            line = [None] * MAP_SIZE
            self.map.append(line)
    
    def __spawn_special_blocks(self):
        for item in DEFAULT_VALUES:
            self.__spawn_blocks(item)
    
    def __complete_map(self):
        tensor = self.__make_tensor()
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                if (self.map[i][j] == None):
                    self.map[i][j] = self.get_random_block(tensor)

    def __spawn_blocks(self, tup):
        i = tup[1]
        while (i != 0):
            raw_index = int(MAP_SIZE * MAP_SIZE * random())
            index = (raw_index//MAP_SIZE, raw_index%MAP_SIZE)
            val = (MAP_SIZE - 1)//2
            cords = (val - index[0],index[1] - val)
            if (self.map[index[0]][index[1]] != None):
                continue
            if (abs(cords[0]) < tup[2][0] and abs(cords[1]) < tup[2][1]):
                continue
            self.map[index[0]][index[1]] = tup[0]()
            if (tup[0].__name__ == 'CastleBlock'):
                self.castle_location = index
            i -= 1
    
    def get_random_block(self, tensor):
        val = random()
        for i in range(len(tensor)):
            if (val < tensor[i]):
                return ALL_BLOCKS[i]()
            val -= tensor[i]
        raise('what the fuck just happened?')
    
    def __make_tensor(self):
        tensor = []
        for i in ALL_BLOCKS:
            j = i()
            if ('random' not in j.tags):
                tensor.append(0)
                continue
            tensor.append(1 / j.rarity)
        s = sum(tensor)
        for i in range(len(tensor)):
            tensor[i] = tensor[i] / s
        return tensor

    def print_map(self):
        for i in range(13):
            for j in range(13):
                print(self.map[i][j], end = "  ")
            print()
    
    def tup_to_index(self, tup):
        val = (MAP_SIZE - 1)//2
        indexes = (val - tup[0],tup[1] + val)
        return indexes
    
    def is_location_valid(self, tup):
        indexes = self.tup_to_index(tup)
        if (indexes[0] < MAP_SIZE and indexes[1] < MAP_SIZE and indexes[0] >= 0 and indexes[1] >= 0):
            return True
        return False

    def get(self, tup):
        indexes = self.tup_to_index(tup)
        return self.map[indexes[0]][indexes[1]]

    def compass(self, tup):
        vector = (self.castle_location[0] - tup[0], self.castle_location[1] - tup[1])
        if (vector[0] == 0 and vector[1] == 0):
            return 'This is the castle block!'
        direction = ''
        if (vector[0] > 0):
            direction += 'north'
        elif (vector[0] < 0):
            direction += 'south'
        if (vector[1] > 0):
            direction += 'east'
        elif (vector[1] < 0):
            direction += 'west'
        return f'The castle is {colored(direction, "cyan")} from here'