from random import random
import Item
from Enemy import get_random_enemy

class Block:
    def __init__(self):
        self.name = ""
        self.tags = []
        self.rarity = 1
        self.has_special_prompt = False
    
    def get_info(self):
        return 'default block'

    def __str__(self):
        return self.name


class CastleBlock(Block):
    def __init__(self):
        self.rarity = 9999
        self.name = "castle"
        self.has_special_prompt = True
        self.tags = ['special']
    
    def get_info(self):
        return 'A castle in the middle of nowhere?!'
    
    def get_prompt(self):
        return 'There is no turning back now, Do you want to enter the castle?(y,n)'


class DigableBlock(Block):
    def __init__(self):
        self.ITEM_CHANCE = 0.4
        self.tags = ['random', 'special', 'loot']
        self.name = "digable"
        self.has_special_prompt = False
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
        self.has_special_prompt = self.contains_item
        if (self.contains_item):
            self.item_inside = Item.get_random_item(luck_factor=0)


    def get_info(self):
        if (self.contains_item):
            return 'Wow there is a chest here!'
        else:
            return 'nothing special here.'
    
    def get_prompt(self):
        return 'Open the chest?(y,n)'

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
        self.has_special_prompt = True
        self.contains_enemy = random() < self.ENEMY_CHANCE
        if (self.contains_enemy):
            self.enemy = get_random_enemy()

    def get_info(self):
        return 'This looks like a place to rest.'
    
    def get_prompt(self):
        return 'Enter the home?(y,n)'


ALL_BLOCKS = [CastleBlock, DigableBlock, NormalBlock, HomeBlock]