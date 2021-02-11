from random import random
from termcolor import colored
from time import sleep
import sys

class Enemy:
    def __init__(self):
        self.name = ""
        self.hp = 0
        self.speed = 0
        self.damage = 0

class Guy(Enemy):
    """you can 'talk' with to end fight"""
    def __init__(self):
        self.name = "guy"
        self.hp = 1
        self.speed = 1
        self.damage = 2

class Wolf(Enemy):
    """can be given a single meat to end fight"""
    def __init__(self):
        self.name = "wolf"
        self.hp = 4
        self.damage = 3
        self.speed = 7

class BloatedBoss(Enemy):
    def __init__(self):
        self.name = "bloated"
        self.hp = 20
        self.healing = 1
        self.damage = 8
        self.speed = 6

    def get_damaged(self, damage):
        self.hp -= damage
        if (self.hp <= 10 and self.healing == 1):
            self.healing = 0
            print(f'{colored("bloated", "red")} is healing it self...', end='')
            sys.stdout.flush()
            sleep(1.5)
            self.hp += 7
            print(f'bloated now has {colored(self.hp, "red")} hp')

normal_enemys = [Guy, Wolf]
endgame_bosses = [BloatedBoss]

def get_random_enemy():
    index = int(random() * len(normal_enemys))
    return normal_enemys[index]()

def get_endgame_boss():
    index = int(random() * len(endgame_bosses))
    return endgame_bosses[index]()