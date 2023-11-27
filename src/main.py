import pytmx
from pyray import *
from arena import Arena
from character import Mage, Warrior, Majora, Thief, Archer, Deadpool
from dice import Dice
from map_renderer import MapRenderer
from rendering import Raylib

arena = Arena()
raylib = Raylib()
rend = MapRenderer(pytmx.TiledMap('res/maps/map.tmx'), 16)
camera = Camera2D(Vector2(0, 0), Vector2(0, 0), 0, 1)


def logger_callback(message, color: Color = WHITE):
    arena.log(message, color)


def setup_characters():
    arena.add(Mage('Frank', 50, 10, 15, Dice(10), 10, logger_callback)
              .with_position(Vector2(16, 14)))
    arena.add(Warrior('Claude', 50, 15, 10, Dice(10), logger_callback)
              .with_position(Vector2(22, 14)))
    arena.add(Majora('Legend', 50, 25, 20, Dice(10), logger_callback)
              .with_position(Vector2(16, 18)))
    arena.add(Thief('Garro', 15, 9, 20, Dice(10), logger_callback)
              .with_position(Vector2(22, 18)))
    arena.add(Archer('Trevize', 50, 15, 20, Dice(10), logger_callback)
              .with_position(Vector2(16, 23)))
    arena.add(Deadpool('Ryan', 50, 20, 20, Dice(10), logger_callback)
              .with_position(Vector2(22, 23)))

    arena.start_battle()


def main():
    setup_characters()
    raylib.run(render, update)


def update():
    if not arena.is_battle():
        return

    for character in arena.get_characters():
        character.update()

    arena.update()

    if arena.alive_count() == 1:
        arena.end_battle()
        return

    if is_key_pressed(KeyboardKey.KEY_SPACE):
        arena.tick()


def render():
    begin_mode_2d(camera)

    # Render the map
    rend.render()

    # Render the characters
    for character in arena.get_characters():
        character.render(rend.get_tile_size())

    arena.render()

    end_mode_2d()


if __name__ == '__main__':
    main()
