from termcolor import colored, cprint

HELPS = ['-h', '--help']
NEWGAME = '-n'
LOADGAME = '-s'
def error(string):
    cprint(f'ERROR: {string}','red')

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
