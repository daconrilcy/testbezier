from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.vector import Vector
from kivy.core.window import Window
from kivy.clock import Clock


class Circle(Widget):
    def __init__(self, color: Color = None, rayon=None, **kwargs):
        super().__init__(**kwargs)
        self.player = None
        self.touched = False
        self.zoommode = False
        if color is None:
            color = Color(1, 1, 1, 1)
        self.color = None
        self.activeweigth = False
        self.clickon = None
        self.d_clic = None
        if rayon is None:
            rayon = 30
        self.size = (rayon, rayon)
        self.sizeclicked = None
        self.player_pos_clicked = None
        self.mouse_pos = None
        self.poids = rayon
        with self.canvas:
            self.color = Color(color.r, color.g, color.b, color.a)
            self.player = Ellipse(pos=self.pos, size=(rayon, rayon))

        Clock.schedule_interval(self.update, 0)

    def set_pos(self, pos):
        self.pos = pos
        self.player.pos = pos

    def set_color(self, r=1, g=1, b=1, a=1):
        self.color.r = r
        self.color.g = g
        self.color.b = b
        self.color.a = a

    def set_opacity(self, o=1):
        self.color.a = o

    def set_rayon(self, rayon=30):
        self.player.size = (rayon, rayon)

    def zoommify(self):
        if self.zoommode & self.touched:
            d = self.mouse_pos[0]-(self.player_pos_clicked[0]+self.player.size[0]/2)
            si = 1
            if d < 0:
                si = -1
            if abs(d) < 10:
                d = 10 * si
            if abs(d) > 100:
                d = 100 * si

            r = self.player.size[0]*(1+d/1000)
            if r < 10:
                r = 10
            if r > 200:
                r = 200
            self.set_rayon(r)

            self.player.pos = Vector(self.player_pos_clicked)-Vector(self.player.size)/2+Vector(self.sizeclicked)/2
            self.pos = Vector(self.player.pos)
            self.poids = self.player.size[0]
            self.size = self.player.size

    def on_touch_down(self, touch):
        if Vector(touch.pos).distance(Vector(self.player.pos)+Vector(self.player.size)/2) <= self.player.size[0]/2:
            self.touched = True
            self.clickon = touch.pos
            self.d_clic = Vector(self.pos)-Vector(self.clickon)
            self.sizeclicked = self.player.size
            self.player_pos_clicked = self.player.pos

    def on_touch_move(self, touch):
        self.size = self.player.size
        if self.touched:
            if not self.zoommode:
                self.set_pos(Vector(touch.pos)+self.d_clic)

    def on_touch_up(self, touch):
        self.touched = False
        self.clickon = None
        self.size = self.player.size

    def get_center(self):
        return Vector(self.player.pos) + Vector(self.player.size)/2

    def update(self):
        self.mouse_pos = Window.mouse_pos
        self.zoommify()
