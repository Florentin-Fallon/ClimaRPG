import random

from pyray import *

from texture_cache import load_cached_texture


class Dice:
    def __init__(self, faces=6):
        self._faces = faces
        self._texture = load_cached_texture(f'res/ui/dices/d{faces}.png')
        self._name = f"D{faces}"

    def __str__(self):
        return self._name

    def roll(self):
        return random.randint(1, self._faces)

    def draw(self, x: int, y: int):
        draw_texture(self._texture, x, y, WHITE)

class RiggedDice(Dice):

    def roll(self, rigged=False):
        # if rigged:
        #     return self._faces
        # else:
        #     return super().roll()

        return self._faces if rigged else super().roll()


if __name__ == "__main__":
    a_dice = Dice()
    print(a_dice)

    for _ in range(10):
        print(a_dice.roll())
