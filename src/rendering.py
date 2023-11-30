from pyray import *
import pytmx


class Raylib:

    def __init__(self, fps: int):
        set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
        init_window(640, 480, 'Clima RPG')
        self.width = 640
        self.height = 480
        self.render_texture: RenderTexture = load_render_texture(self.width, self.height)

        set_target_fps(fps)

    def run(self, render, update):
        while not window_should_close():
            begin_drawing()

            clear_background(BLACK)
            begin_texture_mode(self.render_texture)
            clear_background(BLACK)
            self.render()
            render()
            end_texture_mode()

            renderWidth = get_render_height() / self.height * self.width

            draw_texture_pro(self.render_texture.texture,
                             Rectangle(0, 0, self.width, -self.height),
                             Rectangle(get_render_width() / 2 - renderWidth / 2,
                                       0,
                                       renderWidth,
                                       get_screen_height()),
                             Vector2(0, 0),
                             0,
                             WHITE)

            end_drawing()

            self.update()
            update()

        self.dispose()

    def dispose(self):
        unload_render_texture(self.render_texture)
        close_window()

    def render(self):
        pass

    def update(self):
        pass
