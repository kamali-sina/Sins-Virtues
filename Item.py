from random import random
from termcolor import colored, cprint
from sys import exit

ALL_TAGS = ['utility', 'attack', 'hp', 'random', 'coin']

class Item:
    def __init__(self):
        self.name = "ite"
        self.rarity = 1
        self.tags = []

    def __str__(self):
        return self.name
    
    def info(self):
        return 'info'

    def get_sell_price(self):
        MAX = 0.80
        MIN = 0.60
        price_multiplier = int((MAX - MIN) * random()) + MIN
        return int(self.rarity * price_multiplier)

class CoinItem(Item):
    def __init__(self):
        self.MAX = 0
        self.MIN = 0
        self.name = 'coin'
        self.tags = ['coin']
        self.amount = int((self.MAX - self.MIN + 1) * random()) + self.MIN
    
    def __str__(self):
        return colored(self.name, "yellow")

    def info(self):
        return 'amount: ' + str(self.amount)

class UtilityItem(Item):
    def __init__(self):
        self.INITIAL_USES = 0
        self.name = 'utility'
        self.tags = ['utility']
        self.uses = self.INITIAL_USES
    
    def __str__(self):
        return colored(self.name, "blue")
    
    def info(self):
        return 'uses remaining: ' + str(self.uses)
    
    def get_sell_price(self):
        MAX = 0.80
        MIN = 0.60
        price_multiplier = int((MAX - MIN + 1) * random()) + MIN
        return int(self.rarity * price_multiplier * (self.uses / self.INITIAL_USES))

    def use(self, game, inventory_index):
        print('this has to be re-writed')

class HpItem(Item):
    def __init__(self):
        self.name = 'hp'
        self.tags = ["hp"]
        self.hp = 0
    
    def __str__(self):
        return colored(self.name, "green")
    
    def info(self):
        return 'restores: ' + str(self.hp) + 'hp'

class AttackItem(Item):
    def __init__(self):
        self.tags = ['attack']
        self.name = "sword"
        self.speed = 0
        self.type = 'unknown'
        self.damage = 0

    def __str__(self):
        return colored(self.name, "red")
    
    def info(self):
        return 'damage: ' + str(self.damage) + ', speed: ' + str(self.speed)

class MeleeAttackItem(AttackItem):
    def __init__(self):
        self.tags = ['attack', 'melee']
        self.name = "sword"
        self.speed = 0
        self.type = 'melee'
        self.damage = 0
    
    def info(self):
        return 'damage: ' + str(self.damage) + ', speed: ' + str(self.speed) + ', type: ' + self.type

class RangedAttackItem(AttackItem):
    def __init__(self):
        self.MISS_CHANCE = 0
        self.tags = ['attack', 'ranged']
        self.name = "pistol"
        self.speed = 0
        self.type = 'ranged'
        self.damage = 0
    
    def info(self):
        return 'damage: ' + str(self.damage) + ', speed: ' + str(self.speed) + ', type: ' + self.type + ', misschance: ' + str(int(self.MISS_CHANCE*100)) + '%'


class Shovel(UtilityItem):
    def __init__(self):
        self.INITIAL_USES = 4
        self.rarity = 3
        self.tags = ["utility", 'random', 'attack']
        self.damage = 3
        self.speed = 4
        self.name = "shovel"
        self.uses = self.INITIAL_USES
    
    def use(self, game, inventory_index):
        game.dig_here(inventory_index)

class Compass(UtilityItem):
    def __init__(self):
        self.rarity = 9
        self.INITIAL_USES = 9999 #inf
        self.tags = ["utility", 'random']
        self.name = "compass"
        self.uses = self.INITIAL_USES

    def use(self, game, inventory_index):
        print(game.map.compass(game.player.location))
    
    def info(self):
        return 'infinite uses'

class Map(UtilityItem):
    def __init__(self):
        self.rarity = 8
        self.INITIAL_USES = 3
        self.tags = ["utility", 'random']
        self.name = "map"
        self.uses = self.INITIAL_USES

    def use(self, game, inventory_index):
        MAP_VISION = 2
        game.player.use_utility(inventory_index)
        game.map.print_partial_map(game.player.location, MAP_VISION)

class Steroid(UtilityItem):
    def __init__(self):
        self.rarity = 12
        self.INITIAL_USES = 1
        self.tags = ["utility", 'random']
        self.name = "steroid"
        self.uses = self.INITIAL_USES
    
    def use(self, game, inventory_index):
        game.player.use_utility(inventory_index)
        game.player.use_steroid(inventory_index)
        print(f'max hp is now {colored(game.player.max_hp, "red")}')

class Fist(MeleeAttackItem):
    def __init__(self):
        self.tags = ['attack']
        self.rarity = 999
        self.type = 'melee'
        self.name = "fist"
        self.damage = 1
        self.speed = 6

class Knife(MeleeAttackItem):
    def __init__(self):
        self.INITIAL_USES = 1
        self.rarity = 7
        self.tags = ["utility", 'attack', 'random', 'melee']
        self.name = "knife"
        self.type = 'melee'
        self.uses = self.INITIAL_USES
        self.damage = 3
        self.speed = 9

class Sword(MeleeAttackItem):
    def __init__(self):
        self.tags = ['attack', 'random', 'melee']
        self.rarity = 14
        self.name = "sword"
        self.type = 'melee'
        self.damage = 7
        self.speed = 6

class Axe(MeleeAttackItem):
    def __init__(self):
        self.tags = ['attack', 'random', 'melee']
        self.rarity = 10
        self.name = "axe"
        self.type = 'melee'
        self.damage = 10
        self.speed = 2

#TODO: handle ranged miss chance
class Peacemaker(RangedAttackItem):
    def __init__(self):
        self.MISS_CHANCE = 0.2
        self.tags = ['attack', 'random', 'ranged']
        self.rarity = 10
        self.type = 'ranged'
        self.name = "peacemaker"
        self.damage = 6
        self.speed = 7

class Apple(HpItem):
    def __init__(self):
        self.rarity = 3
        self.tags = ["hp", 'random']
        self.name = "apple"
        self.hp = 3

class Celery(HpItem):
    def __init__(self):
        self.rarity = 7
        self.tags = ["hp", 'random']
        self.name = "celery"
        self.hp = 11

class Meat(HpItem):
    def __init__(self):
        self.rarity = 5
        self.name = "meat"
        self.tags = ['attack', 'hp', 'random']
        self.damage = 1
        self.speed = 1
        self.hp = 6

class CoinStack(CoinItem):
    def __init__(self):
        self.MAX = 2
        self.MIN = 4
        self.rarity = 5
        self.name = 'coin_stack'
        self.tags = ['coin', 'random']
        self.amount = int((self.MAX - self.MIN + 1) * random()) + self.MIN

class CoinBag(CoinItem):
    def __init__(self):
        self.MAX = 3
        self.MIN = 8
        self.rarity = 10
        self.name = 'coin_stack'
        self.tags = ['coin', 'random']
        self.amount = int((self.MAX - self.MIN + 1) * random()) + self.MIN

ALL_ITEMS = [Shovel, Compass, Knife, Sword, CoinStack, CoinBag, Apple, Meat, Celery, Steroid, Axe, Peacemaker, Map]
ITEM_TENSOR = []

#TODO: use luck factor and make item generation better
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