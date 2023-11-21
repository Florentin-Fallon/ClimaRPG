import pytmx

import engine
from map_renderer import MapRenderer
from rendering import Raylib

raylib = Raylib()
rend = MapRenderer(pytmx.TiledMap('res/maps/map.tmx'))


def main():
    raylib.run(render, update)


def update():
    pass


def render():
    rend.render()
    pass


if __name__ == '__main__':
    main()
