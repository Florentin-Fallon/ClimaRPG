from pyray import *


class Raylib:

    def __init__(self):
        init_window(640, 480, 'Clima RPG')

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
        pass

    def update(self):
        pass
