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

        self.system_log('Battle started')

    def get_characters(self) -> list[Character]:
        return self._characters

    def any_character_dead(self) -> bool:
        for character in self._characters:
            if character.is_dead():
                return True

        return False

    def add(self, character: Character):
        self._characters += [character]

    def log(self, text: str, color: Color):
        self._logs += [ArenaLog(text, color).with_index(len(self._logs))]

    def system_log(self, text: str):
        self.log(text, SKYBLUE)

    def tick(self):
        c = self._characters[self._character_counter]
        self._character_counter += 1

        if self._character_counter >= len(self._characters):
            self._character_counter = 0

        for i in range(0, 10):
            target = self._characters[random.randint(0, len(self._characters) - 1)]
            if target == c:
                continue

            c.attack(target)

    def update(self):
        pass

    def render(self):
        latest_logs = self._logs[-5:]

        for i, log in enumerate(latest_logs):
            log.draw(20, 20 + i * 12)

        pass
