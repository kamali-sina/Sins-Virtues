from ConsoleHandler import slow, intro_cutscene, dialog
import ConsoleHandler
from Player import Player
from Map import Map


class Game:
    def __init__(self,path_to_savefiles=None, newgame=True):
        self.NORMAL_COMMANDS = ['move', 'inventory', 'use', 'info']
        self.NORMAL_COMMANDS_HANDLER = [self.move, self.inventory, self.use, self.info]
        self.FIGHT_COMMANDS = ['inventory', 'info', 'use', 'attack', 'counter', 'sneak']
        self.FIGHT_COMMANDS_HANDLER = [self.inventory, self.info, self.use, self.attack, self.counter, self.sneak]
        # intro_cutscene()
        self.player = Player(path_to_savefiles)
        self.map = Map(path_to_savefiles)

    def run(self):
        self.idiot_counter = 0
        self.state = 'normal'
        while(True):
            #TODO: dialog after reaching new block
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
        if (self.idiot_counter > 3):
            dialog('You', "I am bec oming bo bo idiot m an! maybe I should study the to turial?", 'yellow', speed=12)
            return
        dialog('You', "I do not know how to do that!", 'yellow', speed=15)
        return
    
    def move(self, dupped_str):
        moveset = ['north', 'south', 'east', 'west', 'up', 'down', 'left', 'right']
        moveset_handler = [(1,0), (-1,0), (0,1), (-1,0), (1,0), (-1,0), (0,1), (-1,0)]
        if (len(dupped_str) < 2):
            print(2)
            self.unknown_command_dialog()
        try:
            index = moveset.index(dupped_str[1])
            tup = (self.player.location[0] + moveset_handler[index][0] , self.player.location[1] + moveset_handler[index][1])
            if (not self.map.is_location_valid(tup)):
                ConsoleHandler.out_of_bounds_dialog()
                return
            self.player.move(moveset_handler[index])
        except:
            print(1)
            print(dupped_str[1])
            self.unknown_command_dialog()
        return
    
    def inventory(self, dupped_str):
        #TODO:complete
        print('base')
    
    def use(self, dupped_str):
        #TODO:complete
        print('base')
    
    def info(self, dupped_str):
        #TODO:complete
        print(f'cords: {self.player.location[0]}, {self.player.location[1]}')
    
    def attack(self, dupped_str):
        #TODO:complete
        print('base')
    
    def sneak(self, dupped_str):
        #TODO:complete
        print('base')
    
    def counter(self, dupped_str):
        #TODO:complete
        print('base')