from random import random
import Item
from Enemy import get_random_enemy

class Block:
    def __init__(self):
        self.name = ""

class CastleBlock(Block):
    def __init__(self):
        self.name = "castle"

class DigableBlock(Block):
    def __init__(self):
        self.name = "digable"
        self.item_inside = Item.get_random_item(luck_factor=0)

class NormalBlock(Block):
    def __init__(self):
        self.name = "normal"

class HomeBlock(Block):
    ENEMY_CHANCE = 0.3
    def __init__(self):
        self.name = "home"
        self.does_contain_enemy = random() < ENEMY_CHANCE
        if (self.does_contain_enemy):
            self.enemy = get_random_enemy()