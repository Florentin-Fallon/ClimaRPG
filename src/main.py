import pytmx
from pyray import *
from arena import Arena
from character import Mage, Warrior
from dice import Dice
from map_renderer import MapRenderer
from rendering import Raylib

arena = Arena()
raylib = Raylib()
rend = MapRenderer(pytmx.TiledMap('res/maps/map.tmx'), 16)


def setup_characters():
    arena.add(Mage('Frank', 20, 10, 15, Dice(2), 10)
              .with_position(Vector2(16, 15)))
    arena.add(Warrior('Claude', 20, 15, 10, Dice(2), 0)
              .with_position(Vector2(22, 15)))


def main():
    setup_characters()
    raylib.run(render, update)


def update():
    pass


def render():
    # Render the map
    rend.render()

    # Render the characters
    for character in arena.get_characters():
        character.render(rend.get_tile_size())


if __name__ == '__main__':
    main()
