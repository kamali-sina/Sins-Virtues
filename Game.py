from ConsoleHandler import slow, intro_cutscene, dialog, error
import ConsoleHandler
from Block import DigableBlock
from termcolor import colored
from Player import Player
from Map import Map


class Game:
    def __init__(self,path_to_savefiles=None, newgame=True):
        self.NORMAL_COMMANDS = ['move', 'inventory', 'use', 'info', 'commands', 'map']
        self.NORMAL_COMMANDS_HANDLER = [self.move, self.inventory, self.use, self.info, self.commands, self.map]
        self.FIGHT_COMMANDS = ['inventory', 'info', 'use', 'attack', 'counter', 'sneak', 'commands']
        self.FIGHT_COMMANDS_HANDLER = [self.inventory, self.info, self.use, self.attack, self.counter, self.sneak, self.commands]
        # intro_cutscene()
        self.player = Player(path_to_savefiles)
        self.map = Map(path_to_savefiles)

    def run(self):
        self.idiot_counter = 0
        self.state = 'normal'
        while(True):
            self.set_command_set()
            input_str = input("> ").strip().lower()
            self.process_input(input_str)
    
    def set_command_set(self):
        if (self.state == 'normal'):
            self.current_commandset = self.NORMAL_COMMANDS
            self.current_commandset_handler = self.NORMAL_COMMANDS_HANDLER
        elif (self.state == 'fight'):
            self.current_commandset = self.FIGHT_COMMANDS
            self.current_commandset_handler = self.FIGHT_COMMANDS_HANDLER
    
    def process_input(self, input_str):
        if (not self.validate_input(input_str)): return
        dupped_str = input_str.split()
        command = dupped_str[0]
        index = self.current_commandset.index(command)
        self.current_commandset_handler[index](dupped_str)
    
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
        print()
        if (self.idiot_counter > 2):
            dialog('You', "I am bec oming bo bo idiot m an! maybe I should study the to turial?", 'yellow', speed=12)
            return
        dialog('You', "I do not know how to do that!", 'yellow', speed=15)
        print()
        return
    
    def move(self, dupped_str):
        moveset = ['north', 'south', 'east', 'west', 'up', 'down', 'left', 'right']
        moveset_handler = [(1,0), (-1,0), (0,1), (0,-1), (1,0), (-1,0), (0,-1), (0,1)]
        if (len(dupped_str) < 2):
            self.unknown_command_dialog()
            return
        try:
            index = moveset.index(dupped_str[1])
            tup = (self.player.location[0] + moveset_handler[index][0] ,self.player.location[1] + moveset_handler[index][1])
            if (not self.map.is_location_valid(tup)):
                ConsoleHandler.out_of_bounds_dialog()
                return
            self.player.move(moveset_handler[index])
            self.new_block_dialog()
        except:
            self.unknown_command_dialog()
        return
    
    def inventory(self, dupped_str):
        if (len(dupped_str) != 1):
            self.unknown_command_dialog()
            return
        self.player.print_inventory()
    
    def use(self, dupped_str):
        utility_items = ['shovel', 'compass']
        utility_handlers = [self.dig_here, self.use_compass]
        if (len(dupped_str) < 2):
            self.unknown_command_dialog()
            return
        index = self.player.index_item(dupped_str[1])
        if (index == -1):
            ConsoleHandler.dont_have_items_dialog()
            return
        if('utility' in self.player.inventory[index].tags):
            try:
                handler_index = utility_items.index(dupped_str[1])
            except:
                error('Unexpected error accured!')
                exit()
            utility_handlers[handler_index](index)
        elif ('hp' in self.player.inventory[index].tags):
            self.player.heal(index)
        else:
            ConsoleHandler.cant_use_item_dialog()
            return
    
    def info(self, dupped_str):
        if (len(dupped_str) != 1):
            self.unknown_command_dialog()
            return
        print()
        self.player.print_info()
        block = self.map.get(self.player.location)
        print(f'current block is {colored(block.name,"magenta")}')
        print()
    
    def attack(self, dupped_str):
        #TODO:complete
        print('base')
    
    def sneak(self, dupped_str):
        #TODO:complete
        print('base')
    
    def counter(self, dupped_str):
        #TODO:complete
        print('base')
    
    def commands(self, dupped_str):
        if (len(dupped_str) != 1):
            self.unknown_command_dialog()
            return
        print('\nAvailable commands:')
        for x in self.current_commandset:
            print(f'                  {colored("-", "cyan")}{x}')
        print()
    
    def map(self, dupped_str):
        self.map.print_map()
    
    def use_compass(self, inventory_index):
        print()
        print(self.map.compass(self.player.location))
        print()

    def dig_here(self, inventory_index):
        block = self.map.get(self.player.location)
        if (not isinstance(block, DigableBlock)):
            ConsoleHandler.cant_dig_here_dialog()
            return
        self.player.use_utility(inventory_index)
        print()
        if (block.contains_item):
            block.contains_item = False
            item = block.item_inside
            ConsoleHandler.found_item_dialog(item.name)
            self.player.add_item(item)
        else:
            ConsoleHandler.didnt_find_item_dialog()
        print()
    
    def new_block_dialog(self):
        current_block = self.map.get(self.player.location)
        print()
        ConsoleHandler.new_block_reached_dialog(current_block)
        print()