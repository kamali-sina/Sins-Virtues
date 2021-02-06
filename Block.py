from random import random
import Item
from Enemy import get_random_enemy

class Block:
    def __init__(self):
        self.name = ""
        self.tags = []
        self.rarity = 1
    
    def get_info(self):
        return 'default block'

    def __str__(self):
        return self.name

class CastleBlock(Block):
    def __init__(self):
        self.rarity = 9999
        self.name = "castle"
        self.tags = ['special']
    
    def get_info(self):
        return 'A castle in the middle of nowhere?!'

class DigableBlock(Block):
    def __init__(self):
        self.ITEM_CHANCE = 0.4
        self.tags = ['random', 'special', 'loot']
        self.name = "digable"
        self.rarity = 10
        self.contains_item = random() < self.ITEM_CHANCE
        if (self.contains_item):
            self.item_inside = Item.get_random_item(luck_factor=0)
    
    def get_info(self):
        return 'It looks like I can dig here with a shovel!'

class NormalBlock(Block):
    def __init__(self):
        self.ITEM_CHANCE = 0.04
        self.tags = ['random', 'loot']
        self.rarity = 1
        self.name = "normal"
        self.contains_item = random() < self.ITEM_CHANCE
        if (self.contains_item):
            self.item_inside = Item.get_random_item(luck_factor=0)

    def get_info(self):
        if (self.contains_item):
            return 'Wow there is a chest here!'
        else:
            return 'nothing special here.'

    def __str__(self):
        me = self.name
        if (self.contains_item):
            me += '*'
        return me

class HomeBlock(Block):
    def __init__(self):
        self.ENEMY_CHANCE = 0.3
        self.tags = ['random', 'special']
        self.rarity = 70
        self.name = "home"
        self.contains_enemy = random() < self.ENEMY_CHANCE
        if (self.contains_enemy):
            self.enemy = get_random_enemy()

    def get_info(self):
        return 'This looks like a place to rest.'

ALL_BLOCKS = [CastleBlock, DigableBlock, NormalBlock, HomeBlock]