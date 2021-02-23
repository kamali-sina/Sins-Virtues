from random import random
import Item
from Enemy import get_random_enemy, get_endgame_boss
from termcolor import colored
from time import sleep
import ConsoleHandler

class Block:
    def __init__(self):
        self.name = ""
        self.tags = []
        self.rarity = 1
        self.has_special_prompt = False
        self.has_adjacent_dialog = False
    
    def get_info(self):
        return 'default block'

    def __str__(self):
        return self.name


class CastleBlock(Block):
    def __init__(self):
        MAX_NUMBER_OF_ENEMIES = 4
        self.number_of_enemies = int(random() * MAX_NUMBER_OF_ENEMIES) + 1
        self.rarity = 9999
        self.name = "castle"
        self.enemies = []
        self.boss = None
        self.has_special_prompt = True
        self.has_adjacent_dialog = False
        self.tags = ['special']
        self.init_enemies()
    
    def init_enemies(self):
        for i in range(self.number_of_enemies):
            self.enemies.append(get_random_enemy())
        self.boss = get_endgame_boss()
    
    def get_info(self):
        return 'A castle in the middle of nowhere?!'
    
    def get_prompt(self):
        return 'There is no turning back now, get ready, have healing items, and equip your weapons. Do you want to enter the castle?(y,n)'
    
    def prompt_handler(self, ans, game):
        if (ans == 0):
            response = 'Oh thank god! This place looks scary af!'
        else:
            ConsoleHandler.into_the_castle_dialog(self.number_of_enemies, self.boss.name)
            for enemy in self.enemies:
                game.fight_enemy(enemy)
                self.number_of_enemies -= 1
                if (self.number_of_enemies > 0):
                    print(f'{self.number_of_enemies} enemies remaining...')
            ConsoleHandler.boss_dialog()
            self.boss.intro_dialog()
            game.fight_enemy(self.boss)
            print()
            ConsoleHandler.outro_dialog()
            exit()
        return response

    def __str__(self):
        return colored(self.name, 'yellow')

class DigableBlock(Block):
    def __init__(self):
        self.ITEM_CHANCE = 0.9
        self.tags = ['random', 'special', 'loot']
        self.name = "digable"
        self.has_special_prompt = False
        self.has_adjacent_dialog = False
        self.rarity = 10
        self.contains_item = random() < self.ITEM_CHANCE
        if (self.contains_item):
            self.item_inside = Item.get_random_item(luck_factor=0)
    
    def get_info(self):
        return 'It looks like I can dig here with a shovel!'

    def __str__(self):
        return colored(self.name, 'red')


class NormalBlock(Block):
    def __init__(self, no_chest=False):
        self.ITEM_CHANCE = 0.04
        self.tags = ['random', 'loot']
        self.rarity = 1
        self.name = "normal"
        if (no_chest):
            self.contains_item = False
        else:
            self.contains_item = random() < self.ITEM_CHANCE
        self.has_special_prompt = self.contains_item
        self.has_adjacent_dialog = self.contains_item
        if (self.contains_item):
            self.item_inside = Item.get_random_item(luck_factor=0)

    def get_info(self):
        if (self.contains_item):
            return 'Wow there is a chest here!'
        else:
            return 'nothing special here.'
    
    def get_adjacent_dialog(self):
        return 'I can see a chest over there on the ground!'
    
    def get_prompt(self):
        return 'Open the chest?(y,n)'
    
    def prompt_handler(self, ans, game):
        if (ans == 0):
            response = "Ok I'll play it safe"
        else:
            self.contains_item = False
            self.has_special_prompt = False
            self.has_adjacent_dialog = False
            game.player.add_item(self.item_inside)
            response = f'Found a {self.item_inside.name} in the chest!'
        return response

    def __str__(self):
        me = self.name
        if (self.contains_item):
            me += '*'
        return me


class HomeBlock(Block):
    def __init__(self):
        self.ENEMY_CHANCE = 0.6
        self.tags = ['random', 'special']
        self.rarity = 80
        self.name = "home"
        self.has_adjacent_dialog = True
        self.has_special_prompt = True
        self.contains_item = True
        self.contains_enemy = random() < self.ENEMY_CHANCE
        if (self.contains_enemy):
            self.enemy = get_random_enemy()
        self.item_inside = Item.get_random_item(luck_factor=0)

    def get_info(self):
        return 'This looks like a place to rest.'
    
    def get_adjacent_dialog(self):
        return 'I can see a faint light emitting nearby...'
    
    def get_prompt(self):
        return 'Enter the home?(y,n)'

    def prompt_handler(self, ans, game):
        response = ''
        if (ans == 0):
            response = 'Good idea, there might be people in there'
        else:
            if self.contains_enemy:
                ConsoleHandler.dialog("You", f'there is a {colored(self.enemy.name,"red")} here, I have to fight it!', "yellow", speed=20)
                game.fight_enemy(self.enemy)
                self.contains_enemy = False
                print('now I can rest here')
            print('resting...')
            sleep(2)
            game.player.refill_hp()
            response += f'health {colored("fully", "green")} restored'
            if (self.contains_item):
                self.contains_item = False
                game.player.add_item(self.item_inside)
                response += f'\nfound a {self.item_inside.name} here'
        return response

    def __str__(self):
        return colored(self.name, 'green')


class ShopBlock(Block):
    def __init__(self):
        self.NAME = 0
        self.PRICE = 1
        self.MAKER = 2
        self.tags = ['random', 'special']
        self.rarity = 100
        self.name = "shop"
        self.has_special_prompt = True
        self.has_adjacent_dialog = True
        self.stock = self.make_stock()
    
    def get_adjacent_dialog(self):
        return 'I can see a shop nearby.'
    
    def make_stock(self):
        ignored_tags = ['coin']
        stock = [[],[],[]]
        for item in Item.ALL_ITEMS:
            temp = item()
            if (self.check_tags(ignored_tags, temp)): continue
            name = temp.name
            stock[self.NAME].append(name)
            rarity_multiplier = self.get_random_multiplier()
            price = int(temp.rarity * rarity_multiplier)
            stock[self.PRICE].append(price)
            stock[self.MAKER].append(item)
        return stock

    def check_tags(self, ignored_tags, item):
        result = False
        for x in ignored_tags:
            if (x in item.tags):
                result = True
                break
        return result

    def index_item(self, item_name):
        for i in range(len(self.stock[self.NAME])):
            if (self.stock[self.NAME][i] == item_name):
                return i
        return -1
    
    def buy_item(self, index):
        self.stock[self.NAME].pop(index)
        self.stock[self.PRICE].pop(index)
        return self.stock[self.MAKER].pop(index)()

    def get_random_multiplier(self):
        x = random() - 0.5
        return 1 + (x * 0.4)
    
    def get_info(self):
        return 'I can spend the coins I found here and sell my extra stuff.'
    
    def get_prompt(self):
        return 'Enter the shop?(y,n)'

    def prompt_handler(self, ans, game):
        response = ''
        if (ans == 0):
            response = "I'll come back when I have more money"
        else:
            game.enter_shop()
        return response

    def __str__(self):
        return colored(self.name, 'yellow')

ALL_BLOCKS = [CastleBlock, DigableBlock, NormalBlock, HomeBlock, ShopBlock]