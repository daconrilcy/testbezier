from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from class_extend.quadri_bezier import Quadribezier


class Game(FloatLayout):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.zoommode = False
        self.r_defaut = 30

        self.pressed_keys = {
            'w': False,
            's': False,
            'up': False,
            'down': False,
            'shift': True
        }

        q = Quadribezier(nbpoints=12)
        self.add_widget(q)
        Clock.schedule_interval(self.update, 0)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # pressed_key = self._keyboard.keycode_to_string(keycode) # this does not work somehow
        pressed_key = keycode[1]
        #print('You pressed the key', pressed_key, '.', sep=' ', end='\n')

        self.pressed_keys[pressed_key] = True
        if self.pressed_keys["shift"]:
            self.zoommode = True
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        released_key = keycode[1]
        # print('You released the key', released_key, '.', sep=' ', end='\n')
        self.pressed_keys[released_key] = False
        self.zoommode = False
        return True

    def update(self, dt):
        pass


class PongApp(App):
    def build(self):
        return Game()


if __name__ == '__main__':
    PongApp().run()
