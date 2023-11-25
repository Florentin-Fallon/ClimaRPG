import pytmx
from pyray import *

cached_textures = {}


def load_cached_texture(filename) -> Texture2D:
    if cached_textures.get(filename):
        return cached_textures[filename]

    texture = load_texture(filename)
    cached_textures[filename] = texture

    return texture


class MapTile:

    def __init__(self, filename, x, y, width, height):
        self._texture = load_cached_texture(filename)
        self._rect = Rectangle(x, y, width, height)

    def render(self, position: Vector2):
        draw_texture_rec(self._texture, self._rect, position, WHITE)


class MapTileLayer:
    def __init__(self, matrix: list[MapTile]):
        self._matrix = matrix

    def get_matrix(self):
        return self._matrix


class MapRenderer:

    def __init__(self, map: pytmx.TiledMap, tilesize: int):
        self._map: pytmx.TiledMap = map
        self._tiles: list[MapTile] = []
        self._width: int = map.width
        self._height: int = map.height
        self._layers: list[MapTileLayer] = []
        self._tile_size = tilesize

        for layer in map.layers:
            self._layers += [MapTileLayer(layer.data)]

        # Build tiles
        for image in map.images:
            if image is None:
                continue

            filename = image[0]
            bounds = image[1]

            self._tiles += [MapTile(filename, bounds[0], bounds[1], bounds[2], bounds[3])]

    def render_layer(self, layer: MapTileLayer):
        for y, line in enumerate(layer.get_matrix()):
            for x, tile_idx in enumerate(line):
                index = tile_idx - 1

                if index >= len(self._tiles):
                    continue

                self._tiles[index].render(Vector2(x * self._tile_size, y * self._tile_size))

    def render(self):
        for layer in self._layers:
            self.render_layer(layer)

    def get_tile_size(self):
        return self._tile_size
