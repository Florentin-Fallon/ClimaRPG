from pyray import *

cached_textures = {}


def load_cached_texture(filename) -> Texture2D:
    if cached_textures.get(filename):
        return cached_textures[filename]

    texture = load_texture(filename)
    cached_textures[filename] = texture

    return texture