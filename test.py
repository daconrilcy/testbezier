from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from class_extend.quadri_bezier import Quadribezier
from kivy.graphics import Color, Line
from polybezier.casteljau2 import Casteljau2
import numpy as np

class Game(FloatLayout):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.zoommode = False
        self.r_defaut = 20

        self.pressed_keys = {
            'w': False,
            's': False,
            'up': False,
            'down': False,
            'shift': True
        }
        self.points = [[0, 200], [200, 400], [400, 400], [600, 200], [800, 0], [1000, 0], [1200, 200],[1400,400], [1600,600],[1800, 600]]
        self.bezier = Casteljau2(points=self.points, precision=50)
        self.coord = self.bezier.coord.tolist()

        self.lf = []
        with self.canvas:
            Color(1, 1, 1, 1)
            for n in range(0, len(self.coord)-1):
                self.lf.append(Line(points=(self.coord[n], self.coord[n+1])))

        self.q = Quadribezier(points=self.points, rayon=self.r_defaut)
        self.add_widget(self.q)
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
        pt = self.q.get_points()
        self.bezier.set_points_aslist(pt)
        pt2 = self.bezier.coord.tolist()
        self.update_line(pt2)
        pass

    def update_line(self, points):
        for n in range(0, len(points) - 1):
            self.lf[n].points = (points[n], points[n+1])

class PongApp(App):
    def build(self):
        return Game()


if __name__ == '__main__':
    PongApp().run()
