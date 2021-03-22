from termcolor import colored, cprint
from random import random
from Item import get_random_item, HpItem, Fist, CoinItem, ScrapBox
import ConsoleHandler
from sys import exit
import pickle

STARTING_MAX_hp = 10
STARTING_GOLD = 0
STARTING_SCRAP = 0
STARTING_LOCATION = [0,0]
STARTING_EQIPPED_ITEM = Fist()
#TODO: make a way to diffrenciate the items of the same name but different levels
class Player:
    def __init__(self, path_to_save):
        self.inventory = []
        self.max_hp = STARTING_MAX_hp
        self.hp = self.max_hp
        self.coin = STARTING_GOLD
        self.location = STARTING_LOCATION
        self.scrap = STARTING_SCRAP
        self.equipped = STARTING_EQIPPED_ITEM
        self.status_effects = []
        self.save_path = path_to_save
    
    def save(self):
        file_name = self.save_path + "player.pkl"
        open_file = open(file_name, "wb")
        pickle.dump(self, open_file)
        open_file.close()

    def _fill_inventory(self, count=20):
        for i in range(30):
            self.add_item(get_random_item())

    def load_from_save(self, path_to_save):
        print('player: loading from save!')
    
    def move(self, tup):
        self.location[0] += tup[0]
        self.location[1] += tup[1]
    
    def print_inventory(self):
        if (len(self.inventory) == 0): 
            print('There are no items in your inventory.')
            return
        print('==========Inventory==========')
        print('  name                 info  ')
        print('-----------------------------')
        for item in self.inventory:
            print(f' {item}', end="")
            spaces = 22 - len(item.name)
            print(f'{" " * spaces}{item.info()}')
    
    def print_info(self):
        print(colored("hp",'green') + f': {self.hp}')
        print(colored("coins",'yellow') + f': {self.coin}')
        print(colored("scraps",'grey') + f': {self.scrap}')
        print(colored("location",'blue') + f': {self.location}')
        print(colored("equipped item",'white') + f': {str(self.equipped)}')
        print(f'{len(self.inventory)} item(s) in ' + colored("inventory",'cyan'))
        self.print_affected_effects()
    
    def index_item(self, item_name):
        for i in range(len(self.inventory)):
            if (self.inventory[i].name == item_name):
                return i
        return -1
    
    def heal(self, index):
        assert isinstance(self.inventory[index], HpItem), 'trying to heal with not hp item'
        item = self.inventory.pop(index)
        self.hp = min(10, self.hp + item.hp)
        if (self.hp == self.max_hp):
            print(colored("hp",'green') + ' is now full at ' + str(self.hp))
        else:
            print(colored("hp",'green') + ' is now ' + str(self.hp))
    
    def use_utility(self, index):
        item = self.inventory[index]
        item.uses -= 1
        if (item.uses == 0):
            self.inventory.pop(index)
    
    def add_item(self, item):
        if (isinstance(item, CoinItem)):
            self.coin += item.amount
            return
        if (isinstance(item, ScrapBox)):
            self.scrap += item.amount
            return
        self.inventory.append(item)
    
    def refill_hp(self):
        self.hp = self.max_hp
    
    def equip_item(self, item):
        self.equipped = item
    
    def use_steroid(self, index):
        STEROID_ADD = 5
        self.max_hp += STEROID_ADD
        self.hp = self.max_hp
    
    def unequip_discarded_item(self, index):
        if (self.equipped is self.inventory[index]):
            self.equipped = STARTING_EQIPPED_ITEM

    def sell(self, index):
        price = self.inventory[index].get_sell_price()
        self.coin += price
        self.unequip_discarded_item(index)
        self.inventory.pop(index)
        return price
    
    def scrap_item(self, index):
        parts = self.inventory[index].get_scrap_parts()
        self.scrap += parts
        self.inventory.pop(index)
        return parts
    
    def attack(self, enemy):
        damage = self.equipped.damage
        if ('ranged' in self.equipped.tags):
            if (random() < self.equipped.MISS_CHANCE):
                damage =  0
        if (damage > 0):
            enemy.get_damaged(damage)
            text = f'attacked {colored(enemy.name, "magenta")} for {colored(self.equipped.damage,"red")} damage!'
            ConsoleHandler.notification(text, speed=30)
        else:
            ConsoleHandler.miss_dialog()
    
    def update_status_effects(self):
        for i in range(len(self.status_effects) - 1, -1, -1):
            effect = self.status_effects[i]
            effect.apply(self)
            if (effect.turns <= 0):
                self.status_effects.pop(i)
                print(f'status effect {effect} ended!')
    
    def reset_status_effects(self):
        self.status_effects = []
    
    def print_affected_effects(self):
        for effect in self.status_effects:
            ConsoleHandler.notification(effect.description(), speed=20)