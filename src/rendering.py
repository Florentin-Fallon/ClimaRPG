from pyray import *
import pytmx

class Raylib:

    def __init__(self):
        init_window(640, 480, 'Clima RPG')

    def run(self, render, update):
        while not window_should_close():
            begin_drawing()
            clear_background(BLACK)
            self.render()
            render()
            end_drawing()

            self.update()
            update()

        self.dispose()

    def dispose(self):
        close_window()

    def render(self):
        pass

    def update(self):
        pass
