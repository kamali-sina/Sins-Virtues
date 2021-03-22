from ConsoleHandler import slow, intro_cutscene, dialog, error, notification
import ConsoleHandler
from Block import DigableBlock, NormalBlock, ShopBlock
import Block
from termcolor import colored
from Item import AttackItem
from time import sleep
from random import random
from Enemy import get_random_enemy
from sys import exit
from Player import Player
from Map import Map
from os import path
import os
import pickle

class Game:
    def __init__(self,path_to_savefiles=None, newgame=True, devmode=False):
        self.NORMAL_COMMANDS = ['move', 'inventory', 'use', 'info', 'commands', 'devmap', 'equip']
        self.NORMAL_COMMANDS_HANDLER = [self.move, self.inventory, self.use, self.info, self.commands, self.pmap, self.equip]
        self.FIGHT_COMMANDS = ['inventory', 'info', 'use', 'attack', 'commands', 'equip']
        self.FIGHT_COMMANDS_HANDLER = [self.inventory, self.info, self.use, self.attack, self.commands, self.equip]
        self.PROMPT_COMMANDS = ['yes', 'no', 'y', 'n']
        self.PROMPT_COMMANDS_HANDLER = [self.prompt_handler, self.prompt_handler, self.prompt_handler, self.prompt_handler]
        self.SHOP_COMMANDS = ['inventory', 'info', 'commands', 'stock', 'buy', 'sell', 'exit']
        self.SHOP_COMMANDS_HANDLER = [self.inventory, self.info, self.commands, self.stock, self.buy, self.sell, self.exit_shop]
        self.BLACKSMITH_COMMANDS = ['inventory', 'info', 'commands', 'upgrade', 'scrap', 'exit']
        self.BLACKSMITH_COMMANDS_HANDLER = [self.inventory, self.info, self.commands, self.upgrade, self.scrap, self.exit_shop]
        self.world_timer = float(0)
        self.available_times = ['morning', 'noon', 'night']
        self.NIGHT_ENEMY_CHANCE = 0.51
        self.time_of_day = self.available_times[0]
        self.my_time = float(0)
        self.enemy_time = float(0)
        if (newgame):
            if (not path.exists(path_to_savefiles)):
                os.makedirs(path_to_savefiles)
            self.player = Player(path_to_savefiles)
            self.map = Map(path_to_savefiles)
            if (not devmode):
                intro_cutscene()
            else:
                self.player._fill_inventory()
            self.save()
        else:
            if (not self.check_save_exists(path_to_savefiles)):
                error('No save file exists in the selected path! exitting...')
                exit()
            self.load_classes(path_to_savefiles)
            print('load successful!')

    def save(self):
        self.player.save()
        self.map.save()

    def load_classes(self, path_to_savefiles):
        file_name = path_to_savefiles + 'player.pkl'
        open_file = open(file_name, "rb")
        self.player = pickle.load(open_file)
        open_file.close()
        file_name = path_to_savefiles + 'map.pkl'
        open_file = open(file_name, "rb")
        self.map = pickle.load(open_file)
        open_file.close()

    def check_save_exists(self, path_to_savefiles):
        files = ['player', 'map']
        for file in files:
            if (not path.exists(path_to_savefiles + file + '.pkl')):
                return False
        return True

    def run(self):
        self.idiot_counter = 0
        self.state = 'normal'
        while(True):
            self.set_command_set()
            self.update_time_of_day()
            input_str = input("> ").strip().lower()
            validity = self.process_input(input_str)
            self.spawn_random_enemy_if_needed(validity)
    
    def spawn_random_enemy_if_needed(self, validity):
        if (self.time_of_day == self.available_times[-1] and self.state == 'normal' and validity):
            if (random() < self.NIGHT_ENEMY_CHANCE):
                enemy = get_random_enemy()
                ConsoleHandler.encountered_enemy_at_night_dialog(enemy.name)
                self.fight_enemy(enemy)
    
    def set_command_set(self):
        if (self.state == 'normal'):
            self.current_commandset = self.NORMAL_COMMANDS
            self.current_commandset_handler = self.NORMAL_COMMANDS_HANDLER
        elif (self.state == 'fight'):
            self.current_commandset = self.FIGHT_COMMANDS
            self.current_commandset_handler = self.FIGHT_COMMANDS_HANDLER
        elif (self.state == 'prompt'):
            self.current_commandset = self.PROMPT_COMMANDS
            self.current_commandset_handler = self.PROMPT_COMMANDS_HANDLER
        elif (self.state == 'shop'):
            self.current_commandset = self.SHOP_COMMANDS
            self.current_commandset_handler = self.SHOP_COMMANDS_HANDLER
        elif (self.state == 'blacksmith'):
            self.current_commandset = self.BLACKSMITH_COMMANDS
            self.current_commandset_handler = self.BLACKSMITH_COMMANDS_HANDLER
    
    def update_world_timer(self, time):
        Multi = 1
        self.world_timer += time * Multi
    
    def reset_world_timer(self):
        self.world_timer = float(0)
        self.time_of_day = self.available_times[0]

    def update_time_of_day(self):
        self.world_timer = self.world_timer % 24
        time = -1
        if (self.world_timer < 14):
            time = 0
        elif (self.world_timer < 16):
            time = 1
        else:
            time = 2
        if (self.time_of_day != self.available_times[time]):
            ConsoleHandler.new_time_dialog(time)
        self.time_of_day = self.available_times[time]
    
    def process_input(self, input_str):
        if (not self.validate_input(input_str)): return False
        print()
        dupped_str = input_str.split()
        command = dupped_str[0]
        index = self.current_commandset.index(command)
        self.current_commandset_handler[index](dupped_str)
        print()
        return True
    
    def validate_input(self, input_str):
        dupped_str = input_str.split()
        if (len(dupped_str) == 0):
            self.unknown_command_dialog()
            return False
        if (dupped_str[0] in self.current_commandset):
            self.idiot_counter = 0
            return True
        self.unknown_command_dialog()
        return False
    
    def unknown_command_dialog(self):
        self.idiot_counter += 1
        if (self.idiot_counter > 2):
            dialog('You', "I am bec oming bo bo idiot m an! maybe I should study the to turial?", 'yellow', speed=12)
            return
        dialog('You', "I do not know how to do that!", 'yellow', speed=15)
        return
    
    def move(self, dupped_str):
        moveset = ['north', 'south', 'east', 'west', 'up', 'down', 'left', 'right']
        moveset_handler = [(1,0), (-1,0), (0,1), (0,-1), (1,0), (-1,0), (0,-1), (0,1)]
        if (len(dupped_str) < 2):
            self.unknown_command_dialog()
            return
        try:
            index = moveset.index(dupped_str[1])
        except:
            self.unknown_command_dialog()
            return
        tup = (self.player.location[0] + moveset_handler[index][0] ,self.player.location[1] + moveset_handler[index][1])
        if (not self.map.is_location_valid(tup)):
            ConsoleHandler.out_of_bounds_dialog()
            return
        self.player.move(moveset_handler[index])
        self.new_block_dialog()
        self.update_world_timer(0.30)
        return
    
    def inventory(self, dupped_str):
        if (len(dupped_str) != 1):
            self.unknown_command_dialog()
            return
        self.my_time += 0.5
        self.update_world_timer(0.15)
        self.player.print_inventory()
    
    def stock(self, dupped_str):
        block = self.map.get(self.player.location)
        assert isinstance(block, ShopBlock), 'fuck'
        print('==========Shop Stock==========')
        print('  name                price')
        print('------------------------------')
        for i in range(len(block.stock[0])):
            print(f' {block.stock[0][i]}', end="")
            spaces = 21 - len(block.stock[block.NAME][i])
            print(f'{" " * spaces}{colored(block.stock[block.PRICE][i],"yellow")}')
        self.update_world_timer(0.18)
    
    def buy(self, dupped_str):
        if (len(dupped_str) < 2):
            self.unknown_command_dialog()
            return
        block = self.map.get(self.player.location)
        assert isinstance(block, ShopBlock), 'fuck'
        index = block.index_item(dupped_str[1])
        if (index == -1):
            ConsoleHandler.item_not_in_stock_dialog()
            return
        price = block.stock[block.PRICE][index]
        if (self.player.coin < price):
            ConsoleHandler.not_enough_coins_dialog()
            return
        item = block.buy_item(index)
        self.player.coin -= price
        self.player.add_item(item)
        self.update_world_timer(0.1)       
        print(f'buyed {dupped_str[1]} for {price} coins')
    
    def sell(self, dupped_str):
        if (len(dupped_str) < 2):
            self.unknown_command_dialog()
            return
        index = self.player.index_item(dupped_str[1])
        if (index == -1):
            ConsoleHandler.dont_have_items_dialog()
            return
        price = self.player.inventory[index].get_sell_price()
        self.update_world_timer(0.11)
        ans = ConsoleHandler.prompt(f'sell item for {price} coins?')
        if (ans != 0):
            print(f'{dupped_str[1]} sold for {colored(self.player.sell(index),"yellow")}')
    
    def exit_shop(self, dupped_str):
        print(f'exiting {self.state}...')
        self.update_world_timer(0.03)
        self.state = 'normal'
    
    def equip(self, dupped_str):
        if (len(dupped_str) < 2):
            self.unknown_command_dialog()
            return
        index = self.player.index_item(dupped_str[1])
        if (index == -1):
            ConsoleHandler.dont_have_items_dialog()
            return
        self.update_world_timer(0.13)
        if('attack' in self.player.inventory[index].tags):
            self.my_time += 1.5
            self.player.equip_item(self.player.inventory[index])
            print(f'equipped item is now {colored(self.player.equipped,"red")}')
        else:
            ConsoleHandler.cant_attack_with_item_dialog()

    def use(self, dupped_str):
        if (len(dupped_str) < 2):
            self.unknown_command_dialog()
            return
        index = self.player.index_item(dupped_str[1])
        if (index == -1):
            ConsoleHandler.dont_have_items_dialog()
            return
        self.update_world_timer(0.1)        
        if('utility' in self.player.inventory[index].tags):
            self.player.inventory[index].use(self, index)
        elif ('hp' in self.player.inventory[index].tags):
            self.player.heal(index)
        else:
            ConsoleHandler.cant_use_item_dialog()
            return
        self.update_world_timer(0.20)
        self.my_time += 1
    
    def get_clock_time(self):
        t =  (self.world_timer + 5) % 24
        h = int(t)
        m = int((t - h) * 60)
        return f'{h}:{m}'
        

    def info(self, dupped_str):
        if (len(dupped_str) != 1):
            self.unknown_command_dialog()
            return
        self.update_world_timer(0.1)        
        self.player.print_info()
        block = self.map.get(self.player.location)
        print(f'time: {self.get_clock_time()}')
        if (self.state == 'normal'): print(f'current block is {colored(block.name,"magenta")}')
        elif (self.state == 'fight'): print(f'enemy has {colored(self.enemy.hp,"red")} hp left')

    def upgrade(self, dupped_str):
        if (len(dupped_str) < 2):
            self.unknown_command_dialog()
            return
        index = self.player.index_item(dupped_str[1])
        if (index == -1):
            ConsoleHandler.dont_have_items_dialog()
            return
        if (not isinstance(self.player.inventory[index], AttackItem)):
            ConsoleHandler.item_not_upgradble_dialog()
            return
        price = self.player.inventory[index].get_upgrade_price()
        level = self.player.inventory[index].lvl + 1
        if (level > 3):
            ConsoleHandler.cant_upgrade_maxitem_dialog()
            return
        ans = ConsoleHandler.prompt(f'upgrading the {self.player.inventory[index]} to level {level} costs {price} scraps, upgrade?')
        if (ans == 0):
            ConsoleHandler.dont_waste_my_time_dialog()
            return
        if (self.player.scrap < price):
            ConsoleHandler.not_enough_scraps_dialog()
            return
        result = self.player.inventory[index].upgrade()
        self.player.scrap -= price
        self.update_world_timer(0.5)        
        print(f'upgraded {dupped_str[1]} for {price} parts. {result}')
    
    def scrap(self, dupped_str):
        if (len(dupped_str) < 2):
            self.unknown_command_dialog()
            return
        index = self.player.index_item(dupped_str[1])
        if (index == -1):
            ConsoleHandler.dont_have_items_dialog()
            return
        if (not isinstance(self.player.inventory[index], AttackItem)):
            ConsoleHandler.item_not_scrappable_dialog()
            return
        price = self.player.inventory[index].get_scrap_parts()
        self.update_world_timer(0.1)       
        ans = ConsoleHandler.prompt(f'scrap {self.player.inventory[index]} for {price} scraps?')
        if (ans != 0):
            print(f'{dupped_str[1]} scrapped for {colored(self.player.scrap_item(index),"grey")} scraps.')
            self.update_world_timer(0.6)

    def attack(self, dupped_str):
        self.attacked = True
        self.my_time += self.enemy.speed
        self.update_world_timer(0.05)
        self.player.attack(self.enemy)

    def commands(self, dupped_str):
        if (len(dupped_str) != 1):
            self.unknown_command_dialog()
            return
        exclude = ['devmap']
        print('Available commands:')
        for x in self.current_commandset:
            if (x not in exclude):
                print(f'                  {colored("-", "cyan")}{x}')
    
    def pmap(self, dupped_str):
        self.map.print_full_map(self.player.location)
    
    def prompt_handler(self, dupped_str):
        if (len(dupped_str) != 1):
            self.unknown_command_dialog()
            return
        ans = 0
        if (dupped_str[0] in ['yes', 'y']):
            ans = 1
        response = self.map.get(self.player.location).prompt_handler(ans, self)
        if (response != ''): print(response)
        self.state = 'normal'
    
    def dig_here(self, inventory_index):
        block = self.map.get(self.player.location)
        if (not isinstance(block, DigableBlock)):
            ConsoleHandler.cant_dig_here_dialog()
            return
        self.player.use_utility(inventory_index)
        if (block.contains_item):
            block.contains_item = False
            item = block.item_inside
            ConsoleHandler.found_item_dialog(item.name)
            self.player.add_item(item)
        else:
            ConsoleHandler.didnt_find_item_dialog()
        self.map.set(self.player.location, NormalBlock(no_chest=True))
    
    def new_block_dialog(self):
        current_block = self.map.get(self.player.location)
        ConsoleHandler.new_block_reached_dialog(current_block)
        self.print_adjacent_dialogs()
        if (current_block.has_special_prompt):
            slow(current_block.get_prompt() + '\n')
            self.state = 'prompt'
    
    def print_adjacent_dialogs(self):
        s = self.map.get_adjacent_dialogs(self.player.location)
        for item in s:
            dialog("You",item, "yellow", speed=30)
    
    def fight_enemy(self, enemy):
        print(colored('\n--Entered Battle--\n','red'))
        notification('enemy info:\n' + str(enemy), speed=18)
        print()
        save_state = self.state
        self.state = 'fight'
        self.set_command_set()
        self.enemy = enemy
        self.my_time = float(enemy.speed)
        self.enemy_time = float(self.player.equipped.speed)
        self.attacked = False
        while(True):
            if (self.enemy_time < self.my_time):
                #Enemy's turn to attack!
                notification(self.enemy.attack(self.player), speed=26)
                self.enemy_time += self.player.equipped.speed
            else:
                #our turn to attack
                if (self.attacked):
                    self.attacked = False
                    self.player.update_status_effects()
                print(colored("Your hp",'green') + f': {self.player.hp}')
                print(colored("Enemy's hp",'red') + f': {self.enemy.hp}\n')
                self.player.print_affected_effects()
                input_str = input(colored("> ",'red')).strip().lower()
                self.process_input(input_str)
            if (self.player.hp <= 0):
                ConsoleHandler.death_dialog()
                exit()
            elif(self.enemy.hp <= 0):
                notification(f'the {colored(self.enemy.name, "red")} is dead.', speed=20)
                print()
                dialog("You", self.enemy.get_kill_dialog(), "yellow", speed=18)
                self.player.coin += self.enemy.bounty
                break
        self.player.reset_status_effects()
        self.state = save_state
    
    def is_block_closed(self, block_name):
        if (self.time_of_day == 'night'): 
            ConsoleHandler.shop_is_closed_dialog(block_name)
            return True
        return False

    def enter_shop(self):
        if (self.is_block_closed('shop')): return
        print(colored('--Entered Shop--\n','yellow'))
        ConsoleHandler.welcome_to_shop_dialog()
        self.state = 'shop'
        while(self.state == 'shop'):
            self.set_command_set()
            input_str = input(colored("> ",'yellow')).strip().lower()
            self.process_input(input_str)
        self.set_command_set()
    
    def enter_blacksmith(self):
        if (self.is_block_closed('blacksmith')): return
        print(colored('--Entered Blacksmith--\n','grey'))
        ConsoleHandler.welcome_to_blacksmith_dialog()
        self.state = 'blacksmith'
        while(self.state == 'blacksmith'):
            self.set_command_set()
            input_str = input(colored("> ",'grey')).strip().lower()
            self.process_input(input_str)
        self.set_command_set()