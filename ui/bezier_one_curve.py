from kivy.app import App
from kivy.graphics import Line, Bezier, Color, Ellipse, InstructionGroup, ContextInstruction
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.config import Config

import random

Window.fullscreen = 'auto'

class BezierTest(FloatLayout):

    def __init__(self, **kwargs):
        super(BezierTest, self).__init__(**kwargs)
        self.loop = True
        self.clickOn = [0, 0]
        self.centercircle = []
        self.rayoncircle = (30, 30)
        self.isin = False
        self.points = []
        self.points.append((0, 0, 100, 100))
        self.line = []
        self.circle = []
        self.npoint = 4
        self.actcircle = None
        self.ncircleEncours = None
        self.demi_dr = []
        self.demi_dr_plt = []
        self.quart_dr = []
        self.quart_dr_plt = []
        self.c_bezier = None
        self.color_line = []
        self.color_circle =  []
        self.color_demi_line = []
        self.color_quart_line = []
        self.color_is_changed = False
        self.isClicked = False
        self.chrono_illumin = 0
        self.duree_illumin = 10
        self.duree_extinction = 10
        self.color_status = 3
        self.o = 1

        self.color_line_default = Color(0.7, 0.7, 0.7, 1)
        self.color_demi_line_default = Color(0.5, 0.5, 0.5, 1)
        self.color_quart_line_default = Color(0.2, 0.2, 0.2, 1)
        self.color_circle_default = Color(1, 1, 1, 1)

        for n in range(0, self.npoint, 1):
            if (n == 0) | (n == 3):
                h = 0
            else:
                h = Window.height/2
            self.centercircle.append((Window.width / (self.npoint + 1) * (n + 1), h))
            self.circle.append(None)
            self.color_circle.append(None)

        for n in range(0, self.npoint - 1):
            self.line.append(None)

        Clock.schedule_interval(self.update, 0)
        cld = self.color_line_default
        cdld = self.color_demi_line_default
        cqld = self.color_quart_line_default
        ccd = self.color_circle_default
        with self.canvas:
            for n in range(0, self.npoint):
                self.color_circle[n] = Color(ccd.rgba)
                self.circle[n] = Ellipse(pos=self.centercircle[n], size=self.rayoncircle)

            ry = rx = self.rayoncircle[0] / 2
            for n in range(0, self.npoint - 1):
                self.color_line.append(None)
                self.color_line[n] = Color(cld.r, cld.g, cld.b, cld.a)
                self.line[n] = Line(points=(
                    self.circle[n].pos[0] + rx,
                    self.circle[n].pos[1] + ry,
                    self.circle[n + 1].pos[0] + rx,
                    self.circle[n + 1].pos[1] + ry))
            dr = self.demi_droite()
            self.quart_droite()

            n = 0

            for d in dr:
                self.color_demi_line.append(None)
                self.color_demi_line[n] = Color(cdld.r, cdld.g, cdld.b, cdld.a)
                self.demi_dr.append(None)
                self.demi_dr[n] = Line(points=d)
                n += 1
            n = 0
            for q in self.quart_dr_plt:
                self.color_quart_line.append(None)
                self.color_quart_line[n] = Color(cqld.r, cqld.g, cqld.b, cqld.a)
                self.quart_dr.append(None)
                self.quart_dr[n] = Line(points=q)
                n += 1
            Color(1, 1, 1, 1)
            v = self.bezier_curve_create()
            self.c_bezier = Line(points=v)

    def creation_pointshalf(self):
        plts = []
        r = self.rayoncircle
        for n in range(0, self.npoint - 1):
            plts.append(((self.circle[n].pos[0] + self.circle[n + 1].pos[0]) / 2 + r[0] / 2,
                         (self.circle[n].pos[1] + self.circle[n + 1].pos[1]) / 2 + r[1] / 2))

        self.demi_dr_plt = plts
        return plts

    def demi_droite(self):
        demi_droite = []
        points = self.creation_pointshalf()
        for n in range(0, points.__len__() - 1):
            demi_droite.append((points[n], points[n + 1]))
        return demi_droite

    def update_demi_dr(self):
        dem = self.demi_droite()
        n = 0
        for d in dem:
            self.demi_dr[n].points = d
            n += 1

    def quart_droite(self):
        plts = []
        dplts = self.demi_dr_plt
        drplts = []

        for n in range(0, dplts.__len__() - 1):
            plts.append(((dplts[n][0] + dplts[n + 1][0]) / 2, (dplts[n][1] + dplts[n + 1][1]) / 2))
        for d in range(0, plts.__len__() - 1):
            drplts.append((plts[d], plts[d + 1]))
        self.quart_dr_plt = drplts

    def update_quart_droite(self):
        self.quart_droite()
        n = 0
        for q in self.quart_dr_plt:
            self.quart_dr[n].points = q
            n += 1

    def on_touch_down(self, touch):
        self.clickOn = Window.mouse_pos
        self.testcircle(self.clickOn)
        return super(BezierTest, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.isin:
            self.centercircle[self.ncircleEncours] = self.circle[self.ncircleEncours].pos
            self.actcircle = None
            self.ncircleEncours = None
            self.isin = False
        self.color_status = 2
        return super(BezierTest, self).on_touch_up(touch)

    def is_over_objet(self):
        pos = Window.mouse_pos
        for c in self.circle:
            if self.isincircle(pos, c):
                return True
        if self.issuralldroite(pos):
            return True
        return False

    def updateline(self):
        n = self.ncircleEncours
        ry = rx = self.rayoncircle[0] / 2

        if (n == 0) | (n == self.npoint - 1):
            pts = []
            t = n
            if n == self.npoint - 1:
                t = n - 1
            for c in (t, t + 1):
                pts.append(self.circle[c].pos[0] + rx)
                pts.append(self.circle[c].pos[1] + ry)
            self.line[t].points = pts
        elif (n > 0) & (n < self.npoint - 1):
            for t in range(n - 1, n + 1):
                pts = []
                for c in range(t, t + 2):
                    pts.append(self.circle[c].pos[0] + rx)
                    pts.append(self.circle[c].pos[1] + ry)
                self.line[t].points = pts

    def testcircle(self, coord):
        for n in range(0, self.npoint):
            if self.isincircle(coord, self.circle[n]):
                self.actcircle = self.circle[n]
                self.ncircleEncours = n
                self.isin = True

    def calculaxb(self, point1, point2):
        x1 = point1[0]
        y1 = point1[1]
        x2 = point2[0]
        y2 = point2[1]
        if x2-x1 !=0:
            a = (y2-y1)/(x2-x1)
            b = (y1*x2-y2*x1)/(x2-x1)
            return a, b
        return None, None

    def issuralldroite(self, mousepos):
        dr = [self.line, self.demi_dr, self.quart_dr]
        cl = [self.color_line, self.color_demi_line, self.color_quart_line]
        cd = [self.color_line_default, self.color_demi_line_default, self.color_quart_line_default]
        c = 0
        for ds in dr:
            n = 0
            for d in ds:
                if self.issursegment(d, mousepos):
                    cl[c][n].r = 1
                    cl[c][n].g = 0
                    cl[c][n].b = 0
                    return True
                else:
                    if cl[c][n].r != cd[c].r:
                        cl[c][n].rgba = cd[c].rgba
                n += 1
            c += 1
        return False

    def issurladroite(self, dr: Line, pointv):
        pt1 = Vector(dr.points[0:2])
        pt2 = Vector(dr.points[2:4])

        ab = pt2-pt1
        ac = Vector(pointv)-pt2
        r = ab.x*ac.y-ab.y*ac.x

        if round(r/1000) == 0:
            return True
        return False

    def issursegment(self, dr: Line, pointv):
        if self.issurladroite(dr, pointv):
            pt1 = Vector(dr.points[0:2])
            pt2 = Vector(dr.points[2:4])
            ptv = Vector(pointv)
            if ((ptv.x >= pt1.x) & (ptv.x <= pt2.x)) | ((ptv.x <= pt1.x) & (ptv.x >= pt2.x)):
                if ((ptv.y >= pt1.y) & (ptv.y <= pt2.y)) | ((ptv.y <= pt1.y) & (ptv.y >= pt2.y)):
                    return True
        return False

    def isincircle(self, coord, xcircle):
        xc = xcircle.pos[0]+self.rayoncircle[0]/2
        yc = xcircle.pos[1]+self.rayoncircle[1]/2
        rc = self.rayoncircle[0]
        x = coord[0]
        y = coord[1]

        h = ((x - xc) ** 2 + (y - yc) ** 2) ** 0.5

        if h <= rc:
            return True
        return False

    def bezier_curve_create(self):
        v = []
        ra = self.rayoncircle
        A = self.circle
        precision = 50
        for l in range(0, precision + 1):
            t = l / precision
            r = (1 - t) ** 3 * (Vector(A[0].pos) + Vector(ra) / 2) + 3 * (1 - t) ** 2 * t * (
                        Vector(A[1].pos) + Vector(ra) / 2) + 3 * (1 - t) * t ** 2 * (
                            Vector(A[2].pos) + Vector(ra) / 2) + t ** 3 * (Vector(A[3].pos) + Vector(ra) / 2)
            v.append(r)
        return v

    def updatec_bezier(self):
        self.c_bezier.points = self.bezier_curve_create()

    def update_color_status(self, dt):
        if self.color_status == 0:
            # la couleur de l'armature s'eteind
            # check du rafraichement
            vdim = self.duree_extinction*dt/10
            self.o -= 0.1
            if self.o <= 0.05:
                self.o = 0.05
        elif self.color_status == 1:
            self.chrono_illumin = self.duree_illumin
            # la couleur s'illummine puis reste
            self.o = 1
        elif self.color_status == 2:
            # pause avant delcin
            vdim = self.duree_illumin*dt
            self.chrono_illumin -= vdim
            if self.chrono_illumin <= 0:
                self.color_status = 0
        elif self.color_status == 4:
            vdim = self.duree_extinction*dt/10
            self.o += 0.05
            if self.o > 1:
                self.o = 1

    def update_color_transparency(self):
        cls = [self.color_circle, self.color_line, self.color_demi_line, self.color_quart_line]
        for cl in cls:
            for c in cl:
                c.a = self.o

    def update(self, dt):
        actual = Window.mouse_pos
        if self.isin:
            self.color_status = 1
            self.circle[self.ncircleEncours].pos = Vector(actual) - Vector(self.rayoncircle) / 2
            self.centercircle[self.ncircleEncours] = self.circle[self.ncircleEncours].pos
            self.updateline()
            self.update_demi_dr()
            self.update_quart_droite()
            self.updatec_bezier()
        elif self.is_over_objet():
            self.color_status = 4
        else:
            if self.color_status != 0:
                self.color_status = 2
        self.update_color_status(dt)
        self.update_color_transparency()

class Main(App):
    def build(self):
        return BezierTest()


if __name__ == '__main__':
    Main().run()