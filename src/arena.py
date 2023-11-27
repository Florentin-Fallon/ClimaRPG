from __future__ import annotations

import random

from pyray import *
from character import Character


class ArenaLog:

    def __init__(self, text: str, color: Color):
        self._text = text
        self._color = color
        self._index = 0

    def with_index(self, index: int) -> ArenaLog:
        self._index = index
        return self

    def draw(self, x: int, y: int):
        draw_text(self._text, x + 1, y + 1, 10, BLACK)
        draw_text(self._text, x, y, 10, self._color)


class Arena:
    def __init__(self):
        self._characters: list[Character] = []
        self._logs: list[ArenaLog] = []
        self._character_counter = 0
        self._running = False

    def is_battle(self):
        return self._running

    def get_characters(self) -> list[Character]:
        return self._characters

    def any_character_dead(self) -> bool:
        for character in self._characters:
            if character.is_dead():
                return True

        return False

    def alive_count(self) -> int:
        count = 0

        for character in self._characters:
            if character.is_alive():
                count += 1

        return count

    def start_battle(self):
        if self._running:
            return

        self._running = True
        self.system_log('Battle started')
        self.system_log(f"First turn is for {self._characters[0].get_name()}")

    def add(self, character: Character):
        self._characters += [character]

    def log(self, text: str, color: Color):
        self._logs += [ArenaLog(text, color).with_index(len(self._logs))]

    def system_log(self, text: str):
        self.log(text, SKYBLUE)

    def end_battle(self):
        if not self._running:
            return

        self._running = False
        self.system_log('Battle ended')

    def tick(self):
        opponents: list[Character] = []

        for ch in self._characters:
            if ch.is_alive():
                opponents += [ch]

        c = opponents[self._character_counter]
        self._character_counter += 1

        while c.is_dead():
            c = opponents[self._character_counter]
            self._character_counter += 1

            if self._character_counter >= len(opponents):
                self._character_counter = 0

        if self._character_counter >= len(opponents):
            self._character_counter = 0

        target = None

        for i in range(0, 10):
            target = opponents[random.randint(0, len(opponents) - 1)]
            if target == c:
                continue

        if not target or target == c or target.is_dead():
            self.system_log(f"{c.get_name()} failed their attack !")
        else:
            c.attack(target)

        self.system_log(f"Next turn is for {opponents[self._character_counter].get_name()}")

    def update(self):
        pass

    def render(self):
        latest_logs = self._logs[-15:]

        for i, log in enumerate(latest_logs):
            log.draw(20, 20 + i * 12)

        pass
