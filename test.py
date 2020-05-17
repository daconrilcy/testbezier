from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from class_extend.circle import Circle


class Game(FloatLayout):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.zoommode = False
        self.a = Circle(size=(50, 50), pos=(100, 100), color=Color(0, 0, 1, 1))
        self.b = Circle(size=(50, 50), pos=(200, 100), color=Color(0, 1, 0, 1))
        self.l = Mline(circle1=self.a, circle2=self.b, color=Color(1, 1, 1, 1))
        self.e = None

        self.add_widget(self.a)
        self.add_widget(self.b)
        self.add_widget(self.l)

        self.pressed_keys = {
            'w': False,
            's': False,
            'up': False,
            'down': False,
            'shift': True
        }

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
        if self.a.touched:
            self.a.zoommode = self.zoommode
        elif self.b.touched:
            self.b.zoommode = self.zoommode


class Mline(Widget):
    def __init__(self, color: Color = None, circle1:Circle= None, circle2:Circle= None, **kwargs):
        super().__init__(**kwargs)
        self.mline = None
        if color is None:
            color = Color(1, 1, 1, 1)
        self.color = None
        self.color_default = color
        self.mouse_pos = None
        self.noeud1 = circle1
        self.noeud2 = circle2
        self.poids = 1
        self.is_overed = False
        self.timer_extinction = 2
        self.is_eteind = False
        self.is_en_cours_extinction = False
        self.duree_extinction_default = 2
        self.duree_extinction = self.duree_extinction_default


        with self.canvas:
            self.color = Color(color.r, color.g, color.b, color.a)
            self.mline = Line(points=(circle1.get_center()[0], circle1.get_center()[1], circle2.get_center()[0], circle2.get_center()[1]))

        Clock.schedule_interval(self.update, 0)

    def set_color(self, r=1, g=1, b=1, a=1):
        self.color.r = r
        self.color.g = g
        self.color.b = b
        self.color.a = a

    def set_opacity(self, o=1):
        self.color.a = o

    def is_on_over(self):
        a = Vector(self.mline.points[0:2])
        b = Vector(self.mline.points[2:4])
        c = Vector(self.mouse_pos)
        d = round(a.distance(c) + c.distance(b) - a.distance(b))
        if d == 0:
            self.is_overed = True
        else:
            self.is_overed = False

    def update_pos(self):
        self.mline.points = (self.noeud1.get_center(), self.noeud2.get_center())

    def illumine(self):
        o = self.color.a
        if o < 1:
            o += 0.15
        if o > 1:
            o = 1
        self.set_opacity(o)
        self.timer_extinction = 2
        self.is_eteind = False
        self.is_en_cours_extinction = False
        self.duree_extinction = self.duree_extinction_default

    def eteind(self):
        if not self.is_eteind:
            if self.timer_extinction <= 0:
                o = self.color.a
                if o > 0.15:
                    self.is_en_cours_extinction = True
                    ratio = self.duree_extinction/self.duree_extinction_default
                    if o > ratio:
                        o = ratio
                if o <= 0.15:
                    o = 0.15
                    self.is_eteind = True
                    self.is_en_cours_extinction = False
                self.set_opacity(o)

    def update_color(self):
        if self.is_overed:
            self.set_color(1, 0, 0, 1)
            self.illumine()
        else:
            self.set_color(self.color_default.r, self.color_default.g, self.color_default.b, self.color.a)
            self.eteind()

    def update(self, dt):
        self.mouse_pos = Window.mouse_pos
        self.is_on_over()
        self.update_pos()
        self.update_color()
        self.timer_extinction -= dt
        if self.is_en_cours_extinction:
            self.duree_extinction -= dt



class PongApp(App):
    def build(self):
        return Game()


if __name__ == '__main__':
    PongApp().run()
