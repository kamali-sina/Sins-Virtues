from ConsoleHandler import slow, intro_cutscene, dialog, error
import ConsoleHandler
from Block import DigableBlock, NormalBlock
import Block
from termcolor import colored
from Player import Player
from Map import Map
#TODO: add shop blocks and gold

class Game:
    def __init__(self,path_to_savefiles=None, newgame=True):
        self.NORMAL_COMMANDS = ['move', 'inventory', 'use', 'info', 'commands', 'map', 'equip']
        self.NORMAL_COMMANDS_HANDLER = [self.move, self.inventory, self.use, self.info, self.commands, self.pmap, self.equip]
        self.FIGHT_COMMANDS = ['inventory', 'info', 'use', 'attack', 'counter', 'sneak', 'commands', 'equip']
        self.FIGHT_COMMANDS_HANDLER = [self.inventory, self.info, self.use, self.attack, self.counter, self.sneak, self.commands, self.equip]
        self.PROMPT_COMMANDS = ['yes', 'no', 'y', 'n']
        self.PROMPT_COMMANDS_HANDLER = [self.prompt_handler, self.prompt_handler, self.prompt_handler, self.prompt_handler]
        self.my_time = float(0)
        self.enemy_time = float(0)
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
        elif (self.state == 'prompt'):
            self.current_commandset = self.PROMPT_COMMANDS
            self.current_commandset_handler = self.PROMPT_COMMANDS_HANDLER
    
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
        except:
            self.unknown_command_dialog()
            return
        tup = (self.player.location[0] + moveset_handler[index][0] ,self.player.location[1] + moveset_handler[index][1])
        if (not self.map.is_location_valid(tup)):
            ConsoleHandler.out_of_bounds_dialog()
            return
        self.player.move(moveset_handler[index])
        self.new_block_dialog()
        return
    
    def inventory(self, dupped_str):
        if (len(dupped_str) != 1):
            self.unknown_command_dialog()
            return
        self.my_time += 0.5
        self.player.print_inventory()
    
    def equip(self, dupped_str):
        if (len(dupped_str) < 2):
            self.unknown_command_dialog()
            return
        index = self.player.index_item(dupped_str[1])
        if (index == -1):
            ConsoleHandler.dont_have_items_dialog()
            return
        if('attack' in self.player.inventory[index].tags):
            self.my_time += 1.5
            self.player.equip_item(self.player.inventory[index])
            print(f'\nequipped item is now {colored(self.player.equipped,"red")}\n')
        else:
            ConsoleHandler.cant_attack_with_item_dialog()

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
        self.my_time += 1
    
    def info(self, dupped_str):
        if (len(dupped_str) != 1):
            self.unknown_command_dialog()
            return
        print()
        self.player.print_info()
        block = self.map.get(self.player.location)
        if (self.state == 'normal'): print(f'current block is {colored(block.name,"magenta")}')
        elif (self.state == 'fight'): print(f'enemy has {colored(self.enemy.hp,"red")} hp left')
        print()
    
    def attack(self, dupped_str):
        # if (len(dupped_str) != 1):
        #     self.unknown_command_dialog()
        #     return
        self.enemy.hp -= self.player.equipped.damage
        self.my_time += self.enemy.speed
        print(f'attacked {colored(self.enemy.name, "magenta")} for {colored(self.player.equipped.damage,"red")} damage!')
    
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
    
    def pmap(self, dupped_str):
        self.map.print_map(self.player.location)
    
    def prompt_handler(self, dupped_str):
        if (len(dupped_str) != 1):
            self.unknown_command_dialog()
            return
        ans = 0
        if (dupped_str[0] in ['yes', 'y']):
            ans = 1
        print()
        response = self.map.get(self.player.location).prompt_handler(ans, self)
        print(response)
        print()
        self.state = 'normal'
    
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
        adjacent_dialog = self.adjacent_dialogs().strip()
        print()
        ConsoleHandler.new_block_reached_dialog(current_block)
        if (len(adjacent_dialog) > 0):
            dialog("You",adjacent_dialog, "yellow", speed=30)
        if (current_block.has_special_prompt):
            slow(current_block.get_prompt() + '\n')
            self.state = 'prompt'
        print()
    
    def adjacent_dialogs(self):
        #FIXME: complete mojaver blocks
        blocks = [Block.HomeBlock]
        blocks_dialog = ['I can see a faint light emitting nearby...']
        full_dialog = ''
        s = self.map.get_adjacent_blocks(self.player.location)
        for item in s:
            try:
                index = blocks.index(item)
                full_dialog += blocks_dialog[index] + '\n'
            except:
                continue
        return full_dialog
    
    def enemy_attack(self):
        self.player.hp -= self.enemy.damage
        print(f'\n{self.enemy.name} attacks you for {colored(str(self.enemy.damage), "red")} damage!\n')
    
    def fight_enemy(self, enemy):
        self.state = 'fight'
        self.set_command_set()
        self.enemy = enemy
        self.my_time = float(enemy.speed)
        self.enemy_time = float(self.player.equipped.speed)
        while(True):
            if (self.enemy_time < self.my_time):
                #Enemy's turn to attack!
                self.enemy_attack()
                self.enemy_time += self.player.equipped.speed
            else:
                #our turn to attack
                input_str = input(colored("> ",'red')).strip().lower()
                self.process_input(input_str)
            if (self.player.hp <= 0):
                ConsoleHandler.death_dialog()
                exit()
            elif(self.enemy.hp <= 0):
                print(f'the {colored(self.enemy.name, "red")} is dead.')
                break
        self.state = 'normal'