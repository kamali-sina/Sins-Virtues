from random import random
from termcolor import colored
from time import sleep
import sys
from ConsoleHandler import dialog

#TODO: add poison damage
class Enemy:
    def __init__(self):
        self.name = ""
        self.hp = 0
        self.bounty = 0
        self.speed = 0
        self.damage = 0

    def get_damaged(self, damage):
        self.hp -= damage
    
    def get_kill_dialog(self):
        return f"Found {colored(self.bounty,'yellow')} coin(s) on the {self.name}"
    
    def __str__(self):
        return f"name: {self.name} - hp: {self.hp} - speed: {self.speed} - damage: {self.damage}"

class Boss(Enemy):
    def __init__(self):
        self.name = ""
        self.hp = 0
        self.speed = 0
        self.damage = 0

    def intro_dialog(self):
        dialog(self.name, "I am a boss", "red")

class Guy(Enemy):
    """you can 'talk' with to end fight"""
    def __init__(self):
        self.name = "guy"
        self.hp = 1
        self.bounty = 1
        self.speed = 1
        self.damage = 2

class Wolf(Enemy):
    """can be given a single meat to end fight"""
    def __init__(self):
        self.name = "wolf"
        self.hp = 4
        self.bounty = 2
        self.damage = 3
        self.speed = 7
    
    def get_kill_dialog(self):
        return f"Found {colored(self.bounty,'yellow')} coin(s) on the wolf, how does a wolf have money?"

class BigBob(Enemy):
    def __init__(self):
        self.name = "big bob"
        self.hp = 12
        self.bounty = 2
        self.damage = 6
        self.speed = 3

class BloatedBoss(Boss):
    def __init__(self):
        self.name = "bloated"
        self.hp = 20
        self.bounty = 20
        self.healing = 1
        self.damage = 7
        self.speed = 4

    def get_damaged(self, damage):
        self.hp -= damage
        if (self.hp <= 10 and self.healing == 1):
            self.healing = 0
            print(f'{colored("bloated", "red")} is healing it self...', end='')
            sys.stdout.flush()
            sleep(1.5)
            self.hp += 5
            print(f'bloated now has {colored(self.hp, "red")} hp')
    
    def intro_dialog(self):
        dialog(self.name, "Acid goes brrrrrrr...", "red")
    
    def get_kill_dialog(self):
        return f"Acid does no go brrrrrrrr anymore..."

normal_enemys = [Guy, Wolf, BigBob]
endgame_bosses = [BloatedBoss]

def get_random_enemy():
    index = int(random() * len(normal_enemys))
    return normal_enemys[index]()

def get_endgame_boss():
    index = int(random() * len(endgame_bosses))
    return endgame_bosses[index]()