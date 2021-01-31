

class Map:
    MAP_SIZE = (13,13)
    def __init__(self, path_to_save=None):
        self.map = []
        for i in range(MAP_SIZE[0]):
            for j in range(MAP_SIZE[1]):
                