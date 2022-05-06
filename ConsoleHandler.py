GAMEVERSION = "1.2.1"

from getpass import getpass
from termcolor import colored, cprint
import sys
from time import sleep
import os
import threading

# import pyautogui
from random import random

DELIM = ""
try:
    import msvcrt

    DELIM = "\\"
except:
    import getch

    DELIM = "/"
from sys import exit

#TODO: Fix output system

data_ready = threading.Event()


class KeyboardPoller(threading.Thread):
    def run(self):
        getpass("")
        data_ready.set()
        return


HELPS = ["-h", "--help"]
INFOS = ["-i", "--info"]
NEWGAME = "-n"
LOADGAME = "-l"
DEVMODE = "--dev"
TOTURIALS = ["-t", "--toturial"]


def error(string):
    cprint(f"ERROR: {string}", "red")


def warning(string):
    cprint(f"WARNING: {string}", "yellow")


def dialog(name, text, color, speed=13):
    text = colored(f"{name}: ", color) + text.strip()
    slow(text, speed=speed)
    print()


def notification(text, speed=13):
    text = text.strip()
    slow(text, speed=speed)
    print()


def help_if_needed(string):
    if string in HELPS:
        print("Usage: Python3 VnS.py <options>\n")
        cprint("=== welcome to Sins & Virtues! ===\n", "green")
        print("use the following options to play the game:\n")
        new = colored(f'"{NEWGAME}"', "yellow")
        load = colored(f'"{LOADGAME}"', "yellow")
        toturial = colored(f'"{TOTURIALS[0]}"', "yellow")
        helps = colored(f'"{HELPS[0]}"', "yellow")
        infos = colored(f'"{INFOS[0]}"', "yellow")
        print(
            f"  {new}: for starting a new game. \n    can be followed by the path to save the game. saves in the current directory as default\n"
        )
        print(
            f"  {load}: for resuming from a save file.\n    can be be followed by the path to the save directory"
        )
        print(f"  {toturial}: for learning the game. \n")
        print(f"  {infos}: for getting version info of the game \n")
        print(f"  {helps}: for seeing the page you are reading now. \n")
        exit()


def info_if_needed(string):
    if string in INFOS:
        print(
            f"VnS version {GAMEVERSION}\nmore info at: https://github.com/PapaSinku/Sins-Virtues"
        )
        exit()


def toturial_if_needed(string):
    if string in TOTURIALS:
        cprint("\n=== welcome to Sins & Virtues! ===\n", "blue")
        print(
            "This game is completely text based. There are no maps(yet), no hints, no eagle vision, no nothing."
        )
        print(
            "But that does not mean that you are completely blind! The protagonist constantly talks about his surroundings, everything he says is there for a reason, so don't skip all the dialogs!"
        )
        cprint("\n===HOW TO PLAY THE GAME===\n", "green")
        print(
            'Everytime you see a little ">" on the screen it\'s your turn to play the game. You have a handful of commands that you can use in every situation that you can review by typing "commands".'
        )
        print(
            "Each of the commands that you can use do use some time, this becomes important specially in the fights where losing time could mean death."
        )
        print(
            "We suggest testing and exploring the commnads by yourself, but if you want more info on some commands you can:"
        )
        print(
            "\tGo to our github page and read the complete readme: https://github.com/PapaSinku/Sins-Virtues"
        )
        cprint("\n===Shops===\n", "yellow")
        print(
            'There are some shops located in the game that you can use to sell your unwanted items and buy the things you want. The currencies in this game are "coins".'
        )
        print(
            "Not all shopkeepers are the same, some have higher prices, some buy your items at a higher price. explore and find the shopkeeper that suits you the best."
        )
        cprint("\n===Homes===\n", "green")
        print(
            "Homes can be used to rest the night and restore your hp. They also usualy contains a good item inside."
        )
        print("But not all homes are empty. Enter with caution.")
        cprint("\n===Fights===\n", "red")
        print(
            'Fights in this game are text based also. The only command for attacking that you have is "attack" that uses the equipped item to attack the enemy.'
        )
        print(
            "Each move you or your enemy make in a fight uses some time, the turns in the fights are calculated by using that time."
        )
        print(
            'Always make sure to have equipped your best weapon before exploring into the unknown. You never know when the next enemy is going to fight you and that extra "equip" might be what saves or kills you in the end.'
        )
        cprint("\n===Castle===", "magenta")
        print(
            "To finish the game, you need to find the castle and explore it completely to the end. You have 2 options to find the castle:"
        )
        print("\texplore blindly untill you come across the castle block")
        print(
            "\tfind a compass. by using a compass the compass directs you to the castle location."
        )
        cprint(
            "*Always go into the castle prepared. The enemies in there will kill you easily if you are not well prepared.*",
            "red",
        )
        print("\n\n===============\nHappy Exploring, goodnight!")
        exit()


def get_file_path(argv1):
    splitted = argv1.split("/")
    if len(splitted) != 1:
        return "/".join(splitted[:-1]) + "/"
    splitted = argv1.split("\\")
    if len(splitted) != 1:
        return "\\".join(splitted[:-1]) + "\\"
    return "./"


def slow(text, speed=13):
    """function which displays characters one at a time"""
    poller = KeyboardPoller()
    poller.start()
    second = False
    charge = 0
    for i in range(len(text)):
        if charge > 0:
            print(text[i], end="")
            charge -= 1
            continue
        if text[i] == "\n":
            print()
        elif ord(text[i]) == 27:
            if second:
                charge = 4
                second = False
            else:
                charge = 5
                second = True
            print(text[i], end="")
            charge -= 1
            continue
        else:
            print(text[i], end="")
        if data_ready.isSet():
            sys.stdout.write("\033[F")
            data_ready.clear()
            poller.join()
            print(text, end="")
            sys.stdout.flush()
            return
        sys.stdout.flush()
        x = 1 + ((random() - 0.5) * 0.4)
        sleep(1 / (speed * x * 1.4))
    i = 0
    do_once = True
    while not data_ready.isSet():
        if i > 60 and do_once:
            do_once = False
            print("-press return key to continue-", end="")
            sys.stdout.flush()
        i += 1
        sleep(0.05)
    data_ready.clear()
    poller.join()
    return


def intro_cutscene():
    cprint("\n======== Sins & Virtues ========", "blue")
    cprint("=== A game made by PapaSinku ===\n", "yellow")
    dialog("Unknown", "Have you ever been to the SinkuLand?\n", "red", speed=8)
    dialog("You", "No I can't recall...", "yellow", speed=4)
    dialog("Unknown", "Close your eyes, and just imagine SinkuLand...", "red", speed=10)
    sleep(1)
    cprint("\n> A white light fills the room\n", "magenta")
    sleep(0.5)
    dialog(
        "You",
        "Where the hell am I? It's getting dark, better find shelter.",
        "yellow",
        speed=7,
    )


def out_of_bounds_dialog():
    dialog(
        "You",
        "Ohoh!!! there is a cliff here! I can't move this direction.",
        "yellow",
        speed=20,
    )


def dont_have_items_dialog():
    dialog("You", "I do not have that item!", "yellow", speed=18)


def item_not_in_stock_dialog():
    dialog("Shopkeeper", "I do not have that item in stock!", "green", speed=18)


def not_enough_coins_dialog():
    dialog("Shopkeeper", "You do not have enough coins to buy that!", "green", speed=18)


def not_enough_scraps_dialog():
    dialog(
        "Blacksmith",
        "You do not have enough scraps to upgrade that!",
        "green",
        speed=18,
    )


def welcome_to_shop_dialog():
    dialog(
        "Shopkeeper",
        "Welcome stranger! Whatever you want, I got it.",
        "green",
        speed=18,
    )


def welcome_to_blacksmith_dialog():
    dialog(
        "Blacksmith",
        "Welcome stranger! You want stronger weapons? I have it.",
        "green",
        speed=22,
    )


def item_not_scrappable_dialog():
    dialog("Blacksmith", "I can't scrap that item! it's worthless.", "green", speed=22)


def item_not_upgradble_dialog():
    dialog(
        "Blacksmith",
        "I can't upgrade that item! it's not an attack item.",
        "green",
        speed=22,
    )


def cant_upgrade_maxitem_dialog():
    dialog(
        "Blacksmith",
        "I can't upgrade that item anymore! it's at max level.",
        "green",
        speed=22,
    )


def dont_waste_my_time_dialog():
    dialog(
        "Blacksmith",
        "Don't waste my time. either upgrade or get out!",
        "green",
        speed=22,
    )


def cant_use_item_dialog():
    dialog("You", "I can't use that item!", "yellow", speed=17)


def new_time_dialog(time):
    dia = ""
    if time == 0:
        dia = "The sun is rising! I was up all night god damn. Can't stop now..."
    elif time == 1:
        dia = "It's evening, getting dark soon, better find shelter fast."
    else:
        dia = "It's night. Shops are closed. the night is dark and full of terrors..."
    dialog("You", dia, "yellow", speed=18)


def encountered_enemy_at_night_dialog(enemy_name):
    dialog("You", f"Shit there is a {enemy_name} here, Shit!", "yellow", speed=18)


def shop_is_closed_dialog(block):
    dialog(
        "You",
        f"The {block} is closed at nights, better find another shelter.",
        "yellow",
        speed=18,
    )


def cant_dig_here_dialog():
    dialog("You", "This is not a digable block!", "yellow", speed=17)


def stop_doing_that():
    dialog("You", "dude ffs just stop doing that!", "yellow", speed=17)


def found_item_dialog(item_name):
    dialog("You", f"I found a {item_name}!", "yellow", speed=17)


def didnt_find_item_dialog():
    dialog("You", "There was nothing here!", "yellow", speed=17)


def new_block_reached_dialog(block):
    print(
        f'{colored("You","yellow")}: reached a {block.name} block. {block.get_info()}'
    )


def death_dialog():
    dialog(
        "You",
        "fuck, is this what death is? god damn it hurts...\nI'm just gonna close my eyes for a little bit...\n\ngoodbye...",
        "yellow",
        speed=6,
    )


def default_kill_dialog(enemy_name):
    dialog("You", "It's over, time to move on...", "yellow", speed=17)


def cant_attack_with_item_dialog():
    dialog("You", "I can't attack with that item!", "yellow", speed=23)


def miss_dialog():
    dialog("You", "Oh shit I missed!!!", "yellow", speed=23)


def into_the_castle_dialog(number_of_enemies, boss_name):
    dialog(
        "You",
        f"Here goes nothing...\nThere are {number_of_enemies} enemies here and a {boss_name} boss!",
        "yellow",
        speed=23,
    )


def boss_dialog():
    dialog("You", "Ok time to fight this big bitch!", "yellow", speed=23)


def outro_dialog():
    dialog(
        "You",
        " *panting* holy shit it's over... what is that over there?",
        "yellow",
        speed=15,
    )
    sleep(1)
    dialog("You", "what the hell? is that... me? hey you ok man?", "yellow", speed=15)
    print("*you try to wake yourself up*")
    sleep(1)
    cprint("\n> A white light fills the room\n", "magenta")
    sleep(1)
    dialog(
        "Unknown", "Open your eyes, do you know where you just went?", "red", speed=15
    )
    dialog("You", "*trying to open eyes* what? no. where am I?", "yellow", speed=15)
    dialog(
        "Unknown", "You are back in your room. The simulation is over.", "red", speed=15
    )
    dialog(
        "You", "Is this real? was that real? what just happened?", "yellow", speed=15
    )
    dialog(
        "Unknown",
        "A thought that shapes in your head has found meaning. No one knows where is SinkuLand and what are the creatures that live there, but each time you go inside, we learn a bit more! We'll be waiting for you on the other side. ",
        "red",
        speed=15,
    )
    dialog("You", "*you turn off the computer*", "yellow", speed=15)
    print("\nThe End\n")


def prompt(prom):
    print(f"{prom}(y,n)")
    YES = ["yes", "y"]
    NO = ["no", "n"]
    while True:
        input_str = input("> ").strip().lower()
        if input_str in YES:
            return 1
        if input_str in NO:
            return 0
        print("answer with y or n")
