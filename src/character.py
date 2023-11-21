from __future__ import annotations

from dice import Dice


class MessageManager():
    pass


class Character:

    def __init__(self, name: str, max_hp: int, attack: int, defense: int, dice: Dice, max_mana: int):
        self._name = name
        self._max_hp = max_hp
        self._current_hp = max_hp
        self._attack_value = attack
        self._defense_value = defense
        self._dice = dice
        self._max_mana = max_mana
        self._current_mana = max_mana

    def __str__(self):
        return f"""{self._name} the Character enter the arena with :
    ■ attack: {self._attack_value} 
    ■ defense: {self._defense_value}
    ■ mana : {self._current_mana}"""

    def get_defense_value(self):
        return self._defense_value

    def get_name(self):
        return self._name

    def is_alive(self):
        return self._current_hp > 0

    def show_healthbar(self):
        missing_hp = self._max_hp - self._current_hp
        healthbar = f"[{"♥" * self._current_hp}{"♡" * missing_hp}] {self._current_hp}/{self._max_hp}hp"
        print(healthbar)

    def regenerate(self):
        self._current_hp = self._max_hp

    def decrease_health(self, amount):
        if amount > 0:
            self._current_hp -= amount
            if self._current_hp < 0:
                self._current_hp = 0
        self.show_healthbar()

    def compute_damages(self, roll, target):
        return self._attack_value + roll

    def attack(self, target: Character):
        if not self.is_alive():
            return
        roll = self._dice.roll()
        damages = self.compute_damages(roll, target)
        print(
            f"⚔️ {self._name} attack {target.get_name()} with {damages} damages (attack: {self._attack_value} + roll: {roll})")
        target.defense(damages, self)

    def compute_defense(self, damages, roll, attacker):
        return damages - self._defense_value - roll

    def defense(self, damages, attacker: Character):
        roll = self._dice.roll()
        wounds = self.compute_defense(damages, roll, attacker)
        print(
            f"🛡️ {self._name} take {wounds} wounds from {attacker.get_name()} (damages: {damages} - defense: {self._defense_value} - roll: {roll})")
        self.decrease_health(wounds)


class Warrior(Character):
    def compute_damages(self, roll, target: Character):
        # print("🪓 Bonus: Axe in your face (+3 attack)")
        return super().compute_damages(roll, target) + 3


class Mage(Character):

    def use_mana(self, cost: int):  # cost = coût du mana
        if self._current_mana - cost >= 0:
            self._current_mana -= cost
            return True
        else:
            print("not enough mana !")
            return False

    def regain_mana(self, amount: int):
        self._current_mana = min(self._max_mana, self._current_mana + amount)

    def compute_defense(self, damages, roll, attacker: Character):
        print("🧙 Bonus: Magic armor (-3 damages)")
        if self.use_mana(3):
            return super().compute_defense(damages, roll, attacker) - 3
        else:
            return super().compute_defense(damages, roll, attacker)

    def attack(self, target: Character):
        if not self.is_alive():
            return
        spell_cost = 5
        if self.use_mana(spell_cost):
            roll = self._dice.roll()
            damages = self.compute_damages(roll, target)
            print(f"🔮 {self._name} casts a spell on {target.get_name()} dealing {damages} damages (attack: {self._attack_value} + roll: {roll})")
            target.defense(damages, self)
        else:
            print("not enough mana to cast the spell")
            print(f"■ mana : {self._current_mana}")

    def show_healthbar(self):
        super().show_healthbar()
        print(f"mana = {self._current_mana}")


class Thief(Character):
    def compute_damages(self, roll, target: Character):
        print(f"🔪 Bonus: Sneacky attack (+{target.get_defense_value()} damages)")
        return super().compute_damages(roll, target) + target.get_defense_value()


if __name__ == "__main__":
    character1 = Warrior("Salim", 20, 0, 3, Dice(6), 0)
    character2 = Mage("Lisa", 20, 0, 3, Dice(6), 100)
    print(character1)
    print(character2)

    while (character1.is_alive() and character2.is_alive()):
        character1.attack(character2)
        character2.attack(character1)

