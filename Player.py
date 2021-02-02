
STARTING_MAX_HEALTH = 10
STARTING_GOLD = 0
STARTING_LOCATION = [0,0]
class Player:
    def __init__(self, path_to_save=None):
        self.inventory = []
        self.health = STARTING_MAX_HEALTH
        self.gold = STARTING_GOLD
        self.location = STARTING_LOCATION
        if (path_to_save):
            self.load_from_save(path_to_save)

    def load_from_save(self, path_to_save):
        print('loading from save!')