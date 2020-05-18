from class_extend.circle import Circle
from class_extend.line.Cline2 import Cline
from class_extend.line.Mline import Mline
from kivy.uix.widget import Widget
from kivy.graphics import Color
from kivy.core.window import Window
import math


class Quadribezier(Widget):
    def __init__(self, nbpoints=4, **kwargs):
        super().__init__(**kwargs)
        self.npoints = nbpoints
        self.circles = []
        self.lines = []
        self.line_support = []
        self.demi_lignes = []
        self.quart_lines = []
        self.pos = (0, 0)
        self.width = Window.width
        self.height = Window.height
        self.rayon = 20
        self.beziers_lines_obj: BezierLine

        self.creer_circles()
        self.beziers_lines_obj = BezierLine(self.circles)
        self.jonction_lines()
        self.affiche_lines()

    def positionne_circle(self):
        pos = []
        y = []
        x = []
        hauteur = Window.height / 2
        delta_x = Window.width / (self.npoints - 1)
        for n in range(0, self.npoints):
            y.append(abs(round(math.sin(n * math.pi / 3)) * hauteur))
            x.append(n * delta_x)
        x[self.npoints - 1] -= self.rayon
        for n in range(self.npoints):
            pos.append((x[n], y[n]))

        return pos

    def creer_circles(self):
        pos = self.positionne_circle()
        for n in range(0, self.npoints):
            self.circles.append(Circle(color=Color(1, 1, 1, 1), rayon=self.rayon, pos=pos[n]))
            self.add_widget(self.circles[n])

    def jonction_lines(self):
        self.lines = self.beziers_lines_obj.lines
        self.line_support = self.beziers_lines_obj.lines_support
        pass

    def affiche_lines(self):
        for ls in self.lines:
            for l in ls:
                self.add_widget(l)


class BezierLine:
    def __init__(self, circles: list = None):

        if circles is None:
            circles = []
        self.circles = circles
        self.lines = []
        self.lines_support = []
        self.lines_demi = []
        self.lines_quart = []

        self.creer_all_lines()

    def creer_lines_support(self):
        for n in range(1, len(self.circles)):
            self.lines_support.append(Cline(obj_1=self.circles[n - 1],
                                            obj_2=self.circles[n],
                                            color=Color(0.5, 0.5, 0.5, 1)
                                            ))

        self.lines.append(self.lines_support)

    def creer_demi_lines(self):
        for n in range(1, len(self.lines_support)):
            self.lines_demi.append(Mline(line1=self.lines_support[n - 1],
                                         line2=self.lines_support[n],
                                         color=Color(0.25, 0.25, 0.25, 1)
                                         ))
        self.lines.append(self.lines_demi)

    def creer_quart_lines(self):
        for n in range(1, len(self.lines_demi)):
            self.lines_quart.append(Mline(line1=self.lines_demi[n - 1],
                                          line2=self.lines_demi[n],
                                          color=Color(0.12, 0.12, 0.12, 1)
                                          ))
        self.lines.append(self.lines_quart)

    def creer_all_lines(self):
        self.creer_lines_support()
        #self.creer_demi_lines()
        #self.creer_quart_lines()
