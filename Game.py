from ConsoleHandler import slow, intro_cutscene

NORMAL_COMMANDS = ['move', 'inventory', 'use', 'info']
FIGHT_COMMANDS = ['inventory', 'info', 'use', 'attack', 'counter', 'sneak']

class Game:
    def __init__(self,path_to_savefiles=None, newgame=True):
        intro_cutscene()
        self.run()

    def run(self):
        print('running game!')