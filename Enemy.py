from random import random

class Enemy:
    def __init__(self):
        self.name = ""
        self.hp = 0
        self.att_dmg = 0

class Guy(Enemy):
    """you can 'talk' with to end fight"""
    def __init__(self):
        self.name = "guy"
        self.hp = 1
        self.att_dmg = 1

class Wolf(Enemy):
    """can be given a single meat to end fight"""
    def __init__(self):
        self.name = "wolf"
        self.hp = 4
        self.att_dmg = 3

class BloatedBoss(Enemy):
    def __init__(self):
        self.name = "bloated"
        self.hp = 20
        self.att_dmg = 8

normal_enemys = [Guy, Wolf]

def get_random_enemy():
    index = int(random() * len(normal_enemys))
    return normal_enemys[index]()