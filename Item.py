from random import random
from termcolor import colored, cprint

ALL_TAGS = ['utility', 'attack', 'hp']

class Item:
    def __init__(self):
        self.name = "ite"
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
        self.damage = 0
        #TODO: think about this
        self.agile_mult = 1

    def __str__(self):
        return colored(self.name, "red") + ' ---- damage: ' + str(self.damage)


class Shovel(UtilityItem):
    def __init__(self):
        self.INITIAL_USES = 3
        self.tags = ["utility"]
        self.name = "shovel"
        self.uses = self.INITIAL_USES

class Compass(UtilityItem):
    def __init__(self):
        self.INITIAL_USES = 9999 #inf
        self.tags = ["utility"]
        self.name = "compass"
        self.uses = self.INITIAL_USES

class Knife(AttackItem):
    def __init__(self):
        self.INITIAL_USES = 6
        self.tags = ["utility", 'attack']
        self.name = "knife"
        self.uses = self.INITIAL_USES
        self.damage = 5
        #TODO: think about this
        self.agile_mult = 1.5

class Sword(AttackItem):
    def __init__(self):
        self.tags = ['attack']
        self.name = "sword"
        self.damage = 10
        #TODO: think about this
        self.agile_mult = 1

class Apple(HpItem):
    def __init__(self):
        self.tags = ["hp"]
        self.name = "apple"
        self.hp = 3

class Meat(HpItem):
    def __init__(self):
        self.name = "meat"
        self.tags = ['attack', 'hp']
        self.damage = 1
        self.hp = 6

ALL_ITEMS = [Shovel, Compass, Knife, Sword, Apple, Meat]
def get_random_item(luck_factor=0):
    """luck_factor is a number between 0 and 1"""
    index = int(random() * len(ALL_ITEMS))
    return ALL_ITEMS[index]()