from __future__ import annotations

from pyray import *
from dice import Dice
from texture_cache import load_cached_texture


class Character:

    def __init__(self, name: str, max_hp: int, attack: int, defense: int, dice: Dice, max_mana: int, logger_callback):
        self._name = name
        self._max_hp = max_hp
        self._current_hp = max_hp
        self._attack_value = attack
        self._defense_value = defense
        self._dice = dice
        self._max_mana = max_mana
        self._current_mana = max_mana
        self._logger = logger_callback
        self._position = Vector2(0, 0)
        self._texture = load_cached_texture(f"res/characters/{self.get_id()}.png")
        self._shadow = load_cached_texture(f"res/characters/shadow.png")
        self._yOffset = 0

    def is_dead(self):
        return self._current_hp <= 0

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
        return self._current_hp > 0

    def regenerate(self):
        self._current_hp = self._max_hp

    def decrease_health(self, amount):
        if amount <= 0:
            return

        self._current_hp -= amount
        if self._current_hp < 0:
            self._current_hp = 0
            self._logger(f"{self._name} is dead !", RED)

    def compute_damages(self, roll, target):
        return self._attack_value + roll

    def attack(self, target: Character):
        if not self.is_alive():
            return
        roll = self._dice.roll()
        damages = self.compute_damages(roll, target)
        self._logger(
            f"{self._name} attacks {target.get_name()} ! -{damages} HP (attack: {self._attack_value} + roll: {roll})")
        target.defense(damages, self)

    def compute_defense(self, damages, roll, attacker):
        return damages - self._defense_value - roll

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

        # Raylib specific methods
    def render(self, tile_size: int):
        x = int(self._position.x * tile_size)
        y = int(self._position.y * tile_size)

        draw_texture(self._shadow, x, y + 5, WHITE)
        draw_texture(self._texture, x, y - int(self._yOffset / 5), WHITE)

        self.render_hud(x, y)

    def render_bar(self, x: int, y: int, width: int, height: int, color: Color, value: float):
        draw_rectangle(x + 1, y + 1, width, height, BLACK)
        draw_rectangle(x, y, width, height, BLACK)
        draw_rectangle(x, y, int(width * value), 4, color)

    def render_hud(self, x: int, y: int):
        # Character's name
        text_y = y - 20
        draw_text(self._name, x + 1, text_y + 1, 10, BLACK)
        draw_text(self._name, x, text_y, 10, WHITE)

        # Character's HP bar
        hp_bar_y = text_y + 12
        hp_percent = self._current_hp / self._max_hp
        self.render_bar(x, hp_bar_y, 32, 4, RED, hp_percent)


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
            self._logger("not enough mana !")
            return False

    def regain_mana(self, amount: int):
        self._current_mana = min(self._max_mana, self._current_mana + amount)

    def compute_defense(self, damages, roll, attacker: Character):
        self._logger("🧙 Bonus: Magic armor (-3 damages)")
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
            self._logger(
                f"{self._name} casts a spell on {target.get_name()} dealing {damages} damages (attack: {self._attack_value} + roll: {roll})")
            target.defense(damages, self)
        else:
            self._logger(f"not enough mana to cast the spell ({self._current_mana} mana)")

    def show_healthbar(self):
        super().show_healthbar()
        self._logger(f"mana = {self._current_mana}")

    def render_hud(self, x: int, y: int):
        super().render_hud(x, y - 10)

        mana_bar_y = y
        mana_percent = self._current_mana / self._max_mana
        self.render_bar(x, mana_bar_y - 10, 32, 4, SKYBLUE, mana_percent)

class Thief(Character):
    def compute_damages(self, roll, target: Character):
        self._logger(f"Bonus: Sneacky attack (+{target.get_defense_value()} damages)")
        return super().compute_damages(roll, target) + target.get_defense_value()

class Majora(Character):
  def compute_damages(self, roll, target: Character):
    print(f"Bonus: if you're wearing Majora's mask, you're entitled to (+5 damages)")
    return super().compute_damages(roll, target) + 5

list_boss = [Warrior, Mage, Thief, Majora]