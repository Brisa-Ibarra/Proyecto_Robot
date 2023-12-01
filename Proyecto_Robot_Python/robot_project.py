# -*- coding: utf-8 -*-

robot_art = r"""
      0: {head_name}
      Is available: {head_status}
      Attack: {head_attack}
      Defense: {head_defense}
      Energy consumption: {head_energy_consump}
              ^
              |                  |1: {weapon_name}
              |                  |Is available: {weapon_status}
     ____     |    ____          |Attack: {weapon_attack}
    |oooo|  ____  |oooo| ------> |Defense: {weapon_defense}
    |oooo| '    ' |oooo|         |Energy consumption: {weapon_energy_consump}
    |oooo|/\_||_/\|oooo|
    `----' / __ \  `----'           |2: {left_arm_name}
   '/  |#|/\/__\/\|#|  \'           |Is available: {left_arm_status}
   /  \|#|| |/\| ||#|/  \           |Attack: {left_arm_attack}
  / \_/|_|| |/\| ||_|\_/ \          |Defense: {left_arm_defense}
 |_\/    O\=----=/O    \/_|         |Energy consumption: {left_arm_energy_consump}
 <_>      |=\__/=|      <_> ------> |
 <_>      |------|      <_>         |3: {right_arm_name}
 | |   ___|======|___   | |         |Is available: {right_arm_status}
// \\ / |O|======|O| \  //\\        |Attack: {right_arm_attack}
|  |  | |O+------+O| |  |  |        |Defense: {right_arm_defense}
|\/|  \_+/        \+_/  |\/|        |Energy consumption: {right_arm_energy_consump}
\__/  _|||        |||_  \__/
      | ||        || |          |4: {left_leg_name}
     [==|]        [|==]         |Is available: {left_leg_status}
     [===]        [===]         |Attack: {left_leg_attack}
      >_<          >_<          |Defense: {left_leg_defense}
     || ||        || ||         |Energy consumption: {left_leg_energy_consump}
     || ||        || || ------> |
     || ||        || ||         |5: {right_leg_name}
   __|\_/|__    __|\_/|__       |Is available: {right_leg_status}
  /___n_n___\  /___n_n___\      |Attack: {right_leg_attack}
                                |Defense: {right_leg_defense}
                                |Energy consumption: {right_leg_energy_consump}

"""

class Part:
    def __init__(self, name, attack_level=0, defense_level=0, energy_consumption=0):
        self.name = name
        self.attack_level = attack_level
        self.defense_level = defense_level
        self.energy_consumption = energy_consumption
        self.initial_defense = defense_level

    def get_status_dict(self):
        formatted_name = self.name.replace(" ","_").lower()
        return {
            "{}_name".format(formatted_name): self.name.upper(),
            "{}_status".format(formatted_name): self.is_available(),
            "{}_attack".format(formatted_name): self.attack_level,
            "{}_defense".format(formatted_name):  self.defense_level,
            "{}_energy_consump".format(formatted_name):  self.energy_consumption
        }

    def is_available(self):
        return not self.defense_level <= 0

class RepairCard:
    def __init__(self):
        self.name = "Repair Card"

    def use(self, robot, part_index):
        robot.parts[part_index].defense_level = robot.parts[part_index].initial_defense

class ChangePartsCard:
    def __init__(self):
        self.name = "Change Parts Card"

    def use(self, robot):
        print("Changing parts...")
        for part in robot.parts:
            new_defense = int(input(f"Enter new defense level for {part.name}: "))
            part.defense_level = new_defense

class SacrificeCard:
    def __init__(self):
        self.name = "Sacrifice Card"

    def use(self, robot, sacrifice_index, target_index):
        sacrificed_defense = robot.parts[sacrifice_index].defense_level
        robot.parts[sacrifice_index].defense_level = 0
        robot.parts[target_index].defense_level += sacrificed_defense

colors = {
    "Black": '\x1b[90m',
    "Blue": '\x1b[94m',
    "Cyan": '\x1b[96m',
    "Green": '\x1b[92m',
    "Magenta": '\x1b[95m',
    "Red": '\x1b[91m',
    "White": '\x1b[97m',
    "Yellow": '\x1b[93m'
}

class Robot:
    def __init__(self, name, color_code):
        self.name = name
        self.color_code = color_code
        self.energy = 100
        self.parts = [
            Part("Head", attack_level=5, defense_level=10, energy_consumption=5),
            Part ("Weapon", attack_level=15, defense_level=0, energy_consumption=10),
            Part("Left Arm", attack_level=3, defense_level=20, energy_consumption=10),
            Part("Right Arm", attack_level=6, defense_level=20, energy_consumption=10),
            Part("Left Leg", attack_level=4, defense_level=20, energy_consumption=15),
            Part("Right Leg", attack_level=4, defense_level=20, energy_consumption=15),
        ]
        self.repair_cards = [RepairCard() for _ in range(3)]
        self.change_parts_cards = [ChangePartsCard() for _ in range(3)]
        self.sacrifice_cards = [SacrificeCard() for _ in range(3)]

    def greet(self):
        print("My name is: ", self.name)

    def show_energy(self):
        print("We have", self.energy, " percent energy left")

    def attack(self, enemy_robot, part_to_use, part_to_attack):
        enemy_robot.parts[part_to_attack].defense_level -= self.parts[part_to_use].attack_level
        self.energy -= self.parts[part_to_use].energy_consumption

    def is_on(self):
        return self.energy >= 0

    def is_there_available_parts(self):
        for part in self.parts:
            if part.is_available():
                return True
        return False

    def use_repair_card(self):
        if self.repair_cards:
            print("Using Repair Card...")
            self.print_available_cards(self.repair_cards)
            card_index = int(input("Choose a Repair Card: "))
            part_index = int(input("Choose a part to repair: "))
            self.repair_cards.pop(card_index - 1).use(self, part_index)
            print("Part repaired successfully!")
        else:
            print("No Repair Cards available.")

    def use_change_parts_card(self):
        if self.change_parts_cards:
            print("Using Change Parts Card...")
            self.print_available_cards(self.change_parts_cards)
            card_index = int(input("Choose a Change Parts Card: "))
            self.change_parts_cards.pop(card_index - 1).use(self)
            print("Parts changed successfully!")
        else:
            print("No Change Parts Cards available.")

    def use_sacrifice_card(self):
        if self.sacrifice_cards:
            print("Using Sacrifice Card...")
            self.print_available_cards(self.sacrifice_cards)
            card_index = int(input("Choose a Sacrifice Card: "))
            sacrifice_index = int(input("Choose a part to sacrifice: "))
            target_index = int(input("Choose a target part: "))
            self.sacrifice_cards.pop(card_index - 1).use(self, sacrifice_index, target_index)
            print("Sacrifice performed successfully!")
        else:
            print("No Sacrifice Cards available.")

    def print_status(self):
        print(self.color_code)
        str_robot = robot_art.format(**self.get_part_status())
        self.greet()
        self.show_energy()
        print(str_robot)
        print(colors["White"])

    def get_part_status(self):
        part_status = {}
        for part in self.parts:
            status_dict = part.get_status_dict()
            part_status.update(status_dict)
        return part_status

    def print_available_cards(self, cards):
        print("Available Cards:")
        for i, card in enumerate(cards, start=1):
            print(f"{i}. {card.name}")


def play():
    playing = True
    print("Welcome to the game")
    robot_one = Robot("Alan", colors["Yellow"])
    robot_two = Robot("Brisa", colors["Red"])
    rount = 0

    while playing:
        current_robot, enemy_robot = (robot_one, robot_two) if rount % 2 == 0 else (robot_two, robot_one)

        current_robot.print_status()

        if current_robot.is_there_available_parts():
            print("What do you want to do?")
            print("1. Attack enemy")
            print("2. Go to the mechanic workshop")
            choice = int(input("Choose an option: "))

            if choice == 1:
                print("Enemy Robot:")
                enemy_robot.print_status()
                print("Which part of the enemy should we attack?")
                part_to_use = int(input("Choose a part to use for the attack: "))
                part_to_attack = int(input("Choose an enemy part to attack: "))
                current_robot.attack(enemy_robot, part_to_use, part_to_attack)
                print("Attack successful!")

            elif choice == 2:
                current_robot.print_status()
                print("Mechanic Workshop:")
                print("1. Use Repair Card")
                print("2. Use Change Parts Card")
                print("3. Use Sacrifice Card")
                workshop_choice = int(input("Choose an option: "))

                if workshop_choice == 1:
                    current_robot.use_repair_card()
                elif workshop_choice == 2:
                    current_robot.use_change_parts_card()
                elif workshop_choice == 3:
                    current_robot.use_sacrifice_card()
        else:
            print("No available parts to attack. Skipping turn.")

        if not enemy_robot.is_on() or enemy_robot.is_there_available_parts() == False:
            playing = False
            print(current_robot.name)

        rount += 1

play()