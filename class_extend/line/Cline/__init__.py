from kivy.graphics import Line, Color
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.core.window import Window
from class_extend.circle import Circle


class Cline(Widget):
    def __init__(self, color: Color = None, circle1: Circle = None, circle2: Circle = None, **kwargs):
        super().__init__(**kwargs)
        self.cline = None
        if color is None:
            color = Color(1, 1, 1, 1)
        self.color = None
        self.color_default = color
        self.mouse_pos = None
        self.noeud1 = circle1
        self.noeud2 = circle2
        self.poids = 1
        self.points = None
        self.is_overed = False
        self.timer_extinction = 2
        self.is_eteind = False
        self.is_en_cours_extinction = False
        self.duree_extinction_default = 2
        self.duree_extinction = self.duree_extinction_default

        with self.canvas:
            self.color = Color(color.r, color.g, color.b, color.a)
            self.cline = Line(points=(circle1.get_center()[0], circle1.get_center()[1],
                                      circle2.get_center()[0], circle2.get_center()[1]))

        self.points = self.cline.points

        Clock.schedule_interval(self.update, 0)

    def set_color(self, r=1, g=1, b=1, a=1):
        self.color.r = r
        self.color.g = g
        self.color.b = b
        self.color.a = a

    def set_opacity(self, o=1):
        self.color.a = o

    def is_on_over(self):
        a = Vector(self.cline.points[0:2])
        b = Vector(self.cline.points[2:4])
        c = Vector(self.mouse_pos)
        d = round(a.distance(c) + c.distance(b) - a.distance(b))
        if d == 0:
            self.is_overed = True
        else:
            self.is_overed = False

    def update_pos(self):
        self.cline.points = (self.noeud1.get_center(), self.noeud2.get_center())
        self.points = self.cline.points

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
