import sys
import os
from ConsoleHandler import error,help_if_needed, toturial_if_needed, NEWGAME, LOADGAME
from Game import Game
from sys import exit

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        error('no arguments were provided.\n\nif you need help use -h or --help')
        exit()
    help_if_needed(sys.argv[1])
    toturial_if_needed(sys.argv[1])
    path = './'
    if (len(sys.argv) > 2):
        path = sys.argv[2]
    game_session = None
    if (sys.argv[1] == NEWGAME):
        game_session = Game(path_to_savefiles=path, newgame=True)
    elif(sys.argv[1] == LOADGAME):
        game_session = Game(path_to_savefiles=path, newgame=False)
    else:
        error('undefined option was provided!')
    
    game_session.run()