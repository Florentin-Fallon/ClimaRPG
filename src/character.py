from __future__ import annotations

import random

from pyray import *
from dice import Dice
from texture_cache import load_cached_texture


class Character:

    def __init__(self, name: str, max_hp: int, attack: int, defense: int, dice: Dice, logger_callback):
        self._name = name
        self._max_hp = max_hp
        self._current_hp = max_hp
        self._attack_value = attack
        self._defense_value = defense
        self._dice = dice
        self._logger = logger_callback
        self._position = Vector2(0, 0)
        self._texture = load_cached_texture(f"res/characters/{self.get_id()}.png")
        self._shadow = load_cached_texture(f"res/characters/shadow.png")
        self._yOffset = 0
        self._tilt: float = 0

    def is_dead(self):
        return self._current_hp <= 0

    def log_bonus(self, name: str):
        self._logger(f"{self._name} used {name} !", GREEN)

    def get_dice(self) -> Dice:
        return self._dice

    def get_position(self):
        return self._position

    def get_texture(self) -> Texture:
        return self._texture

    def get_id(self):
        return self.__class__.__name__.lower()

    def get_defense_value(self):
        return self._defense_value

    def get_name(self):
        return self._name

    def is_alive(self):
        return not self.is_dead()

    def regenerate(self):
        self._current_hp = self._max_hp

    def decrease_health(self, amount):
        if amount <= 0:
            self._logger(f"{self._name} had no damage", get_color(0xFF7F7FFF))
            return

        self._current_hp -= amount

        self._logger(f"{self._name}: -{amount} HP !", get_color(0xFF7F7FFF))

        if self._current_hp < 0:
            self._current_hp = 0
            self._logger(f"{self._name} is dead !", RED)

    def compute_damages(self, roll, target):
        return min(1, self._attack_value * roll / 2.5)

    def attack(self, target: Character):
        if not self.is_alive():
            return

        self._logger(f"{self._name} attacks {target.get_name()} !")

        roll = self._dice.roll()
        damages = self.compute_damages(roll, target)
        target.defense(damages, self)

    def compute_defense(self, damages, roll, attacker):
        return damages - self._defense_value // 10 - roll

    def defense(self, damages, attacker: Character):
        roll = self._dice.roll()
        wounds = self.compute_defense(damages, roll, attacker)
        self.decrease_health(wounds)

    def with_position(self, position: Vector2) -> Character:
        self._position = position
        return self

    def update(self):
        self._yOffset += get_frame_time() * 8

        if self._yOffset > 10:
            self._yOffset = 0

        if self.is_dead() and self._tilt < 1:
            self._tilt += get_frame_time() * 4

        current_character_index = 0

    def update_movements(self):
        if is_key_down(KeyboardKey.KEY_W):
            self._position.y -= get_frame_time()
        if is_key_down(KeyboardKey.KEY_S):
            self._position.y += get_frame_time()
        if is_key_down(KeyboardKey.KEY_A):
            self._position.x -= get_frame_time()
        if is_key_down(KeyboardKey.KEY_D):
            self._position.x += get_frame_time()

    def render(self, tile_size: int):
        x = int(self._position.x * tile_size)
        y = int(self._position.y * tile_size)

        draw_texture(self._shadow, x, y + 5, WHITE)
        draw_texture_ex(self._texture, Vector2(x + self._tilt * self._texture.width,
                                               y - int(self._yOffset / 5)), self._tilt * 90, 1, WHITE)

        self.render_hud(x, y)

    def render_bar(self, x: int, y: int, width: int, height: int, color: Color, value: float):
        draw_rectangle(x, y, width+2, height+2, BLACK)
        draw_rectangle(x, y, width, height, BLACK)
        draw_rectangle(x, y, int(width * value), 4, color)
        draw_rectangle_lines_ex(Rectangle(x-1, y-1, width+2, height+2), 1, WHITE)

    def render_hud(self, x: int, y: int):
        # Character's name
        text_y = y - 20
        draw_text(self._dice.__str__(), x - 1, text_y - 10, 10, WHITE)
        draw_text(self._name, x, text_y + 1, 10, BLACK)
        draw_text(self._name, x - 1, text_y, 10, WHITE)

        # Character's HP bar
        hp_bar_y = text_y + 12
        hp_percent = self._current_hp / self._max_hp
        self.render_bar(x, hp_bar_y, 32, 4, RED, hp_percent)


class Warrior(Character):
    def compute_damages(self, roll, target: Character):
        self.log_bonus('Axe')
        return super().compute_damages(roll, target) + 30 * (roll / 10)


class Mage(Character):

    def __init__(self, name: str, max_hp: int, attack: int, defense: int, dice: Dice, max_mana: float, logger_callback):
        super().__init__(name, max_hp, attack, defense, dice, logger_callback)

        self._mana = max_mana
        self._max_mana = max_mana

    def use_mana(self, cost: int):  # cost = coût du mana
        if self._mana - cost >= 0:
            self._mana -= cost
            return True
        else:
            return False

    def regain_mana(self, amount: int):
        self._mana = min(self._mana, self._mana + amount)

    def compute_defense(self, damages, roll, attacker: Character):
        if self.use_mana(1) and roll % 2 == 0:
            self.log_bonus('Magic Armor')
            return super().compute_defense(damages, roll, attacker) - 5
        else:
            return super().compute_defense(damages, roll, attacker)

    def compute_damages(self, roll, target):
        if self.use_mana(5):
            self.log_bonus('Magic Spell')
            return super().compute_damages(roll, target) * 10
        else:
            return super().compute_damages(roll, target) / 2

    def render_hud(self, x: int, y: int):
        super().render_hud(x, y - 10)

        mana_bar_y = y
        mana_percent = self._mana / self._max_mana
        self.render_bar(x, mana_bar_y - 10, 32, 4, SKYBLUE, mana_percent)


class Thief(Character):
    def compute_damages(self, roll, target: Character):
        self.log_bonus('Defense Steal')
        return super().compute_damages(roll, target) + target.get_defense_value() + roll * 2


class Majora(Character):
    def compute_damages(self, roll, target: Character):
        self.log_bonus("Majora's Mask")
        return super().compute_damages(roll, target) + 25

class Archer(Character):
  def compute_damages(self, roll, target: Character):
    self.log_bonus("Bows & Arrows")
    return super().compute_damages(roll, target) + 5

class Deadpool(Character):
  def compute_defense(self, damages, roll, attacker: Character):
    self.log_bonus("The Shield")
    return super().compute_defense(damages, roll, attacker) - 15

list_boss = [Warrior, Mage, Thief, Majora, Archer, Deadpool]
