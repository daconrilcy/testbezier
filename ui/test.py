from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.lang import Builder


class Planet(Widget):
    # velocity of the ball on x and y axis
    dx = NumericProperty(0)
    dy = NumericProperty(0)

    def init(self, pos=(50, 50), **kwargs):
        """ Initialize the planet"""
        self.pos = pos
        #print("Init planet. pos:", self.pos)
        # These shapes do not move with the widget.
        # Why?
        # Only the white circle in .kv lang moves with it.
        self.canvas.add(Color(0.8, 0, 0))
        self.canvas.add(Ellipse(pos=self.pos, size=(50, 50)))

    def move(self):
        """ Move the planet. """
        self.pos = Vector(self.velocity) + self.pos
        #print("Planet now at", self.pos)


class System(Widget):
    mars = ObjectProperty(None)

    def update(self, dt):
        #print("Update! ", dt)
        if self.mars:
            self.mars.move()

    def spawn(self, dt):
        print("Insert!", dt)
        self.mars = Planet()
        self.mars.init()
        self.add_widget(self.mars)
        self.mars.velocity = (0.1, 0.1)


class PlanetApp(App):
    def build(self):
        sys = System()
        Clock.schedule_interval(sys.update, 1 / 60)
        Clock.schedule_once(sys.spawn, 3)
        return sys


if __name__ == '__main__':
    Builder.load_string(""" 
#:kivy 1.0.9 
<Planet> 
    canvas: 
        Ellipse: 
            pos: self.pos 
            size: self.size 
""")

    PlanetApp().run()
