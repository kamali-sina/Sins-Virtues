from random import random


ALL_TAGS = ['utility', 'attack', 'hp']

class Item:
    def __init__(self):
        self.name = "ite"
        self.tags = []

class Shovel(Item):
    def __init__(self):
        self.INITIAL_USES = 3
        self.tags = ["utility"]
        self.name = "shovel"
        self.uses = self.INITIAL_USES

class Compass(Item):
    def __init__(self):
        self.INITIAL_USES = 9999 #inf
        self.tags = ["utility"]
        self.name = "compass"
        self.uses = self.INITIAL_USES

class Knife(Item):
    def __init__(self):
        self.INITIAL_USES = 6
        self.tags = ["utility", 'attack']
        self.name = "knife"
        self.uses = self.INITIAL_USES
        self.damage = 5
        #TODO: think about this
        self.agile_mult = 1.5

class Sword(Item):
    def __init__(self):
        self.tags = ['attack']
        self.name = "sword"
        self.damage = 10
        #TODO: think about this
        self.agile_mult = 1

class Apple(Item):
    def __init__(self):
        self.tags = ["hp"]
        self.hp = 3

class Meat(Item):
    def __init__(self):
        self.tags = ['attack', 'hp']
        self.damage = 1
        self.hp = 6

ALL_ITEMS = [Shovel, Compass, Knife, Sword, Apple, Meat]
def get_random_item(luck_factor=0):
    """luck_factor is a number between 0 and 1"""
    index = int(random() * len(ALL_ITEMS))
    return ALL_ITEMS[index]()