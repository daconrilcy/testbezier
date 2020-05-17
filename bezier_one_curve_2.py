from kivy.app import App
from kivy.graphics import Line, Color, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from polybezier import Polybezier
from kivy.config import Config
from class_extend.circle import Circle
import random
poly = Polybezier(precision=200)

Window.fullscreen = 'auto'
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class BezierTest(FloatLayout):
    def __init__(self, **kwargs):
        super(BezierTest, self).__init__(**kwargs)
        self.circle = [Circle()]
        self.rayondefault = 30
        self.npoints = 4

        #Clock.schedule_interval(self.update, 0)

        self.create_circle()

    def create_circle(self):
        l = Window.width/(self.npoints-1)
        points = []
        for n in range(self.npoints):
            h = Window.height/2
            if n == 0:
                x = 0
                y = 0
            elif n == self.npoints-1:
                x = l*n-self.rayondefault
                y = 0
            else:
                x = l*n
                y = Window.height/2
            points.append([x, y])

        self.circle.clear()
        n=0

        for p in points:
            r = random.randint(0, 100)/100
            v = random.randint(0, 100)/100
            b = random.randint(0, 100)/100
            self.circle.append(Circle(pos=p, color=Color(r, v, b, 1), rayon=20, nom=str(n)))
            n += 1

        for c in self.circle:
            self.add_widget(c)

    def update(self, dt):
        pass


class Main(App):
    def build(self):
        return BezierTest()


if __name__ == '__main__':
    Main().run()
