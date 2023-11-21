from pyray import *


class Raylib:

    def __init__(self):
        init_window(640, 480, 'Clima RPG')

        self.logo = load_texture('res/clima_logo.png')

    def run(self):
        while not window_should_close():
            begin_drawing()
            clear_background(BLACK)
            self.render()
            end_drawing()

            self.update()

        self.dispose()

    def dispose(self):
        close_window()

    def render(self):
        draw_texture(self.logo, 0, 0, WHITE)
        pass

    def update(self):
        pass
