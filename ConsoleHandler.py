from termcolor import colored, cprint
import sys
from time import sleep
import os
import threading
import pyautogui
import getch
# from _Getch import getch

data_ready = threading.Event()

class KeyboardPoller( threading.Thread ) :
    def run( self ) :
        getch.getch()
        data_ready.set()
        return

HELPS = ['-h', '--help']
NEWGAME = '-n'
LOADGAME = '-s'
#TODO: make toturial
TOTURIALS = ['-t', '--toturial']

def error(string):
    cprint(f"ERROR: {string}",'red')

def dialog(name ,text, color, speed=13):
    cprint(f'{name}: ',color,end="")
    text = text.strip()
    slow(text, speed=speed)
    print()

def help_if_needed(string):
    if (string in HELPS):
        print('Usage: Python3 VnS.py <options>\n')
        cprint('welcome to Sins & Virtues!\n', 'green')
        print('use the following options to play the game:\n')
        new = colored(f'"{NEWGAME}"','yellow')
        load = colored(f'"{LOADGAME}"','yellow')
        print(f'  {new}: for starting a new game. \n    can be followed by the path to save the game. saves in the current directory as default\n')
        print(f'  {load}: for resuming from a save file.\n    must be followed by the path to the save directory')
        exit()

def slow(text, speed=13):
    """function which displays characters one at a time"""
    poller = KeyboardPoller()
    poller.start()
    for i in range(len(text)):
        print(text[i], end="")
        if (data_ready.isSet()):
            data_ready.clear()
            poller.join()
            print(text[i+1:], end="")
            sys.stdout.flush()
            return
        sys.stdout.flush()
        sleep(1/speed)
    pyautogui.press('a')
    data_ready.clear()
    poller.join()

def intro_cutscene():
    dialog('Unknown', "Have you ever been to the SinkuLand?\n", 'red', speed=8)
    dialog('You', "No I can't recall...", 'yellow', speed=4)
    dialog('Unknown', "Close your eyes, and just imagine SinkuLand...", 'red', speed=10)
    sleep(1)
    cprint('\n> A white light fills the room\n','magenta')
    sleep(0.5)
    dialog('You', "Where the hell am I? It's getting dark, better find shelter.", 'yellow', speed=7)

def out_of_bounds_dialog():
    dialog('You', "Ohoh!!! there is a cliff here! I can't move this direction.", 'yellow', speed=20)

def dont_have_items_dialog():
    dialog('You', "I do not have that item!", 'yellow', speed=18)

def cant_use_item_dialog():
    dialog('You', "I can't use that item!", 'yellow', speed=17)

def cant_dig_here_dialog():
    dialog('You', "This is not a digable block!", 'yellow', speed=17)

def found_item_dialog(item_name):
    dialog('You', f"I found a {item_name}!", 'yellow', speed=17)

def didnt_find_item_dialog():
    dialog('You', "There was nothing here!", 'yellow', speed=17)

def new_block_reached_dialog(block):
    print(f'{colored("You","yellow")}: reached a {block.name} block. {block.get_info()}')

def death_dialog():
    dialog('You', "fuck, is this what death is? god damn it hurts...\nI'm just gonna close my eyes for a little bit...\n\ngoodbye...", 'yellow', speed=6)

def default_kill_dialog(enemy_name):
    dialog('You', "It's over, time to move on...", 'yellow', speed=17)

def cant_attack_with_item_dialog(item_name):
    dialog('You', "I can't attack with that item!", 'yellow', speed=23)

def into_the_castle_dialog(number_of_enemies, boss_name):
    dialog('You', f"Here goes nothing...\nThere are {number_of_enemies} enemies here and a {boss_name} boss!", 'yellow', speed=23)

def boss_dialog():
    dialog('You', "Ok time to fight this big bitch!", 'yellow', speed=23)

def outro_dialog():
    dialog('You', " *panting* holy shit it's over... what is that over there?", 'yellow', speed=15)
    sleep(1)
    dialog('You', "what the hell? is that... me? hey you ok man?", 'yellow', speed=15)
    print('*you try to wake yourself up*')
    sleep(1)
    cprint('\n> A white light fills the room\n','magenta')
    sleep(1)
    dialog('Unknown', "Open your eyes, did you know where you just went?", 'red', speed=15)
    dialog('You', "*trying to open eyes* what? no. where am I?", 'yellow', speed=15)
    dialog('Unknown', "You are back in your room. The simulation is over.", 'red', speed=15)
    dialog('You', "Is this real? was that real? what just happened?", 'yellow', speed=15)
    dialog('Unknown', "A thought that shapes in your head has found meaning. No one knows where is SinkuLand and what are the creatures that live there, but each time you go inside, we learn a bit more! We'll be waiting for you on the other side. ", 'red', speed=15)
    dialog('You', "*you turn of the computer*", 'yellow', speed=15)
    print('\nThe End\n')