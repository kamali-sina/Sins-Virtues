from random import random
from termcolor import colored, cprint

ALL_TAGS = ['utility', 'attack', 'hp', 'random']

class Item:
    def __init__(self):
        self.name = "ite"
        self.rarity = 1
        self.tags = []

    def __str__(self):
        return self.name

class UtilityItem(Item):
    def __init__(self):
        self.INITIAL_USES = 0
        self.name = 'utility'
        self.tags = ['utility']
        self.uses = self.INITIAL_USES
    
    def __str__(self):
        return colored(self.name, "blue") + ' ---- uses remaining: ' + str(self.uses)

class HpItem(Item):
    def __init__(self):
        self.name = 'hp'
        self.tags = ["hp"]
        self.hp = 0
    
    def __str__(self):
        return colored(self.name, "green") + ' ---- restores: ' + str(self.hp) + ' hp'

class AttackItem(Item):
    def __init__(self):
        self.tags = ['attack']
        self.name = "sword"
        self.speed = 0
        self.damage = 0

    def __str__(self):
        return colored(self.name, "red") + ' ---- damage: ' + str(self.damage)


class Shovel(UtilityItem):
    def __init__(self):
        self.INITIAL_USES = 4
        self.rarity = 3
        self.tags = ["utility", 'random', 'attack']
        self.damage = 3
        self.speed = 4
        self.name = "shovel"
        self.uses = self.INITIAL_USES

class Compass(UtilityItem):
    def __init__(self):
        self.rarity = 9
        self.INITIAL_USES = 9999 #inf
        self.tags = ["utility", 'random']
        self.name = "compass"
        self.uses = self.INITIAL_USES

class Fist(AttackItem):
    def __init__(self):
        self.tags = ['attack']
        self.rarity = 13
        self.name = "fist"
        self.damage = 1
        self.speed = 6

class Knife(AttackItem):
    def __init__(self):
        self.INITIAL_USES = 6
        self.rarity = 5
        self.tags = ["utility", 'attack', 'random']
        self.name = "knife"
        self.uses = self.INITIAL_USES
        self.damage = 5
        self.speed = 9

class Sword(AttackItem):
    def __init__(self):
        self.tags = ['attack', 'random']
        self.rarity = 13
        self.name = "sword"
        self.damage = 10
        self.speed = 7

class Apple(HpItem):
    def __init__(self):
        self.rarity = 3
        self.tags = ["hp", 'random']
        self.name = "apple"
        self.hp = 3

class Meat(HpItem):
    def __init__(self):
        self.rarity = 5
        self.name = "meat"
        self.tags = ['attack', 'hp', 'random']
        self.damage = 1
        self.speed = 1
        self.hp = 6

ALL_ITEMS = [Shovel, Compass, Knife, Sword, Apple, Meat]
ITEM_TENSOR = []

def make_item_tensor():
    for i in ALL_ITEMS:
        j = i()
        if ('random' not in j.tags):
            ITEM_TENSOR.append(0)
            continue
        ITEM_TENSOR.append(1 / j.rarity)
    s = sum(ITEM_TENSOR)
    for i in range(len(ITEM_TENSOR)):
        ITEM_TENSOR[i] = ITEM_TENSOR[i] / s

def get_random_item(luck_factor=0):
    """luck_factor is a number between 0 and 1"""
    if (len(ITEM_TENSOR) == 0):
        make_item_tensor()
    val = random()
    for i in range(len(ITEM_TENSOR)):
        if (val < ITEM_TENSOR[i]):
            return ALL_ITEMS[i]()
        val -= ITEM_TENSOR[i]