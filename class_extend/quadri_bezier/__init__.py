from class_extend.circle import Circle
from class_extend.line.Cline2 import Cline
from class_extend.line.Mline import Mline
from kivy.uix.widget import Widget
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.vector import Vector
import math


class Quadribezier(Widget):
    def __init__(self, nbpoints: [float] = 4, points=None, rayon:float = 20, **kwargs):
        super().__init__(**kwargs)
        self.circles = []
        self.lines = []
        self.line_support = []
        self.demi_lignes = []
        self.quart_lines = []
        self.pos = (0, 0)
        self.width = Window.width
        self.height = Window.height
        self.rayon = rayon
        if points is None:
            if nbpoints is None:
                self.npoints = 4
            else:
                self.npoints = nbpoints
            self.pos_circle = self.positionne_circle_auto()
        else:
            self.pos_circle = self.transf_listtuple_tolist(points)
            self.npoints = len(points)
        self.beziers_lines_obj: BezierLine

        self.creer_circles()
        self.beziers_lines_obj = BezierLine(self.circles)
        self.jonction_lines()
        self.affiche_lines()

    def transf_listtuple_tolist(self, points):
        t = None
        if isinstance(points, list):
            if isinstance(points[0], int) | isinstance(points[0], float):
                return points
            elif isinstance(points[0], tuple) | isinstance(points[0], list):
                x = []
                for nts in points:
                    for n in nts:
                        x.append(n)
                return x
            else:
                return [0, 0]

    def positionne_circle_auto(self):
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
            pos.append(x[n])
            pos.append(y[n])
        print(pos)
        return pos

    def creer_circles(self):
        pos = self.pos_circle
        for n in range(0, self.npoints):
            self.circles.append(Circle(color=Color(1, 1, 1, 1), rayon=self.rayon, pos=pos[n*2:(n*2)+2]))
            self.add_widget(self.circles[n])

    def jonction_lines(self):
        self.lines = self.beziers_lines_obj.lines
        self.line_support = self.beziers_lines_obj.lines_support
        pass

    def affiche_lines(self):
        for ls in self.lines:
            for li in ls:
                self.add_widget(li)

    def get_points(self):
        pt= []
        for c in self.circles:
            pt.append(c.get_center())
        return pt

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
        self.creer_demi_lines()
        self.creer_quart_lines()

