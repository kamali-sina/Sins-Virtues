from termcolor import colored, cprint

class StatusEffect():
    def __init__(self):
        self.name = 'statuseffect'
        self.color = 'magenta'
        #HP change: Has to be - for damage and + for healing
        self.hpc = 0
        self.turns = 0
        self.init()
        if (self.hpc > 0): self.color = 'green'
        elif (self.hpc < 0): self.color = 'red'

    def apply(self, target):
        target.hp += self.hpc
        self.turns -= 1
        print(self.apply_dialog())
    
    def apply_dialog(self):
        if (self.hpc < 0):
            return f"I got damaged for {self.hpc}hp by the {self.name}"
        elif(self.hpc > 0):
            return f"I got healed for {self.hpc}hp by the {self.name}"
        else:
            return f"Still affected by the {self.name}"

    def init(self):
        self.name = 'status'
    
    def description(self):
        word = ''
        if (self.hpc < 0): word = 'damage'
        elif(self.hpc > 0): word = 'heal'
        else: 
            return f'{colored(self.name, self.color)} will affect you for the next {self.turns} turns'
        return f'{colored(self.name, self.color)} will {word} you for {abs(self.hpc)}hp for the next {self.turns} turns'
    
    def __str__(self):
        return colored(self.name, self.color)

class PoisonEffect(StatusEffect):
    def init(self):
        self.name = 'poison'
        self.hpc = -2
        self.turns = 2