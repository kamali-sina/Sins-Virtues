from Block import *
from termcolor import colored
from random import random


MAP_SIZE = 13
DEFAULT_VALUES = [(DigableBlock,4, (0,0)),
                    (HomeBlock,2, (2,2)),
                    (CastleBlock, 1, (5,5)),
                    (ShopBlock, 1, (3,3))]
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
                self.castle_location = cords
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

    def print_map(self, tup):
        indexes = self.tup_to_index(tup)
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                if (indexes[0] == i and indexes[1] == j):
                    print(colored(self.map[i][j], 'blue'), end = "  ")
                    continue
                print(self.map[i][j], end = "  ")
            print()
    
    def tup_to_index(self, tup):
        val = (MAP_SIZE - 1)//2
        indexes = (val - tup[0],tup[1] + val)
        return indexes

    def index_to_tup(self, index):
        val = (MAP_SIZE - 1)//2
        indexes = (val - index[0],index[1] - val)
        return indexes
    
    def is_location_valid(self, tup):
        indexes = self.tup_to_index(tup)
        if (indexes[0] < MAP_SIZE and indexes[1] < MAP_SIZE and indexes[0] >= 0 and indexes[1] >= 0):
            return True
        return False

    def get(self, tup):
        indexes = self.tup_to_index(tup)
        return self.map[indexes[0]][indexes[1]]
    
    def set(self, tup, block):
        indexes = self.tup_to_index(tup)
        self.map[indexes[0]][indexes[1]] = block

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

    def get_adjacent_blocks(self, tup):
        x = set()
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                l = (tup[0] + i, tup[1] + j)
                if (not self.is_location_valid(l)): continue
                indexes = self.tup_to_index(l)
                if (not(i == 0 and j == 0)): x.add(type(self.map[indexes[0]][indexes[1]]))
        return x
    
    def get_adjacent_dialogs(self, tup):
        x = set()
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                l = (tup[0] + i, tup[1] + j)
                if (not self.is_location_valid(l)): continue
                indexes = self.tup_to_index(l)
                block = self.map[indexes[0]][indexes[1]]
                if (not block.has_adjacent_dialog): continue
                if (not(i == 0 and j == 0)): x.add(self.map[indexes[0]][indexes[1]].get_adjacent_dialog())
        return x