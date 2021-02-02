from random import random
import Item
from Enemy import get_random_enemy

class Block:
    def __init__(self):
        self.name = ""
        self.tags = []
        self.rarity = 1

    def __str__(self):
        return self.name

class CastleBlock(Block):
    def __init__(self):
        self.rarity = 9999
        self.name = "castle"
        self.tags = ['special']

class DigableBlock(Block):
    def __init__(self):
        self.ITEM_CHANCE = 0.4
        self.tags = ['random', 'special']
        self.name = "digable"
        self.rarity = 10
        self.contains_item = random() < self.ITEM_CHANCE
        if (self.contains_item):
            self.item_inside = Item.get_random_item(luck_factor=0)

class NormalBlock(Block):
    def __init__(self):
        self.tags = ['random']
        self.rarity = 1
        self.name = "normal"

class HomeBlock(Block):
    def __init__(self):
        self.ENEMY_CHANCE = 0.3
        self.tags = ['random', 'special']
        self.rarity = 70
        self.name = "home"
        self.contains_enemy = random() < self.ENEMY_CHANCE
        if (self.contains_enemy):
            self.enemy = get_random_enemy()

ALL_BLOCKS = [CastleBlock, DigableBlock, NormalBlock, HomeBlock]