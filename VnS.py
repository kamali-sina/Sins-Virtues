import sys
import os
from ConsoleHandler import error,help_if_needed, toturial_if_needed, NEWGAME, LOADGAME, DEVMODE, info_if_needed, get_file_path, DELIM
from Game import Game
from sys import exit

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        error('no arguments were provided.\n\nif you need help use -h or --help')
        exit()
    help_if_needed(sys.argv[1])
    info_if_needed(sys.argv[1])
    toturial_if_needed(sys.argv[1])
    path = get_file_path(sys.argv[0]) + 'saves' + DELIM
    if (len(sys.argv) > 2):
        path = sys.argv[2]
        if (not path.endswith(DELIM)):
            path = path + DELIM
        path = path + 'saves' + DELIM
    game_session = None
    if (sys.argv[1] == NEWGAME):
        game_session = Game(path_to_savefiles=path, newgame=True)
    elif(sys.argv[1] == LOADGAME):
        game_session = Game(path_to_savefiles=path, newgame=False)
    elif(sys.argv[1] == DEVMODE):
        game_session = Game(path_to_savefiles=path, newgame=True, devmode=True)
    else:
        error('undefined option was provided!')
        exit(0)
    
    game_session.run()