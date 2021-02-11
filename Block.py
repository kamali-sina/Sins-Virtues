from random import random
import Item
from Enemy import get_random_enemy
from termcolor import colored
from time import sleep

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
    
    def prompt_handler(self, ans, game):
        if (ans == 0):
            response = 'Oh thank god! This place looks scary af!'
        else:
            response = 'Here goes nothing...'
            # TODO: I still dont know what to do here, have an array of enemies and fight every signle one of them!
        return response


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

    def __str__(self):
        return colored(self.name, 'blue')


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
    
    def prompt_handler(self, ans, game):
        if (ans == 0):
            response = "Ok I'll play it safe"
        else:
            self.contains_item = False
            self.has_special_prompt = False
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
        self.has_special_prompt = True
        self.contains_item = True
        self.contains_enemy = random() < self.ENEMY_CHANCE
        if (self.contains_enemy):
            self.enemy = get_random_enemy()
        self.item_inside = Item.get_random_item(luck_factor=0)

    def get_info(self):
        return 'This looks like a place to rest.'
    
    def get_prompt(self):
        return 'Enter the home?(y,n)'

    def prompt_handler(self, ans, game):
        response = ''
        if (ans == 0):
            response = 'Good idea, there might be people in there'
        else:
            if self.contains_enemy:
                print(f'there is a {colored(self.enemy.name,"red")} here, I have to fight it!')
                print(colored('--Entered Battle--','red') + '\n')
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


ALL_BLOCKS = [CastleBlock, DigableBlock, NormalBlock, HomeBlock]