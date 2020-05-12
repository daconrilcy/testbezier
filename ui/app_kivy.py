from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Line, Color, Bezier
from kivy.config import Config
from kivy.core.window import Window

from random import randint


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1
        self.xmax = int(Window.system_size[0])
        self.ymax = int(Window.system_size[1])
        #self.inside = GridLayout()
        #self.inside.cols = 2

        #self.inside.add_widget(Label(text="Name : "))
        #self.name = TextInput(multiline=False)
        #self.inside.add_widget(self.name)

        #self.inside.add_widget(Label(text="Last Name : "))
        #self.lastname = TextInput(multiline=False)
        #self.inside.add_widget(self.lastname)

        #self.inside.add_widget(Label(text="Email : "))
        #self.email = TextInput(multiline=False)
        #self.inside.add_widget(self.email)

        #self.add_widget(self.inside)

        #self.submit = Button(text="Submit", font_size=40)
        #self.submit.bind(on_press=self.pressed)
        #self.add_widget(self.submit)

        nbpiece = 200
        difx, dify, nx, ny = calc_nb_piece(npiece=nbpiece)
        print(dify)
        # creation des lignes de separations horizontales
        iter = 4
        for t in range(0, ny+1):
            y0 = int(t * dify)
            if t == ny:
                y0 = self.ymax
            x = [0]
            y = [y0]
            r, v, b = (0, 0, 1.)
            vary = 0

            listpoint = [x[0], y[0]]
            with self.canvas:
                Color(0.6, 0.6, 1.)
                Line(circle=(x[0], y[0], 5))
            for n in range(1, nx+1):
                vary1ast = vary
                x.append(int(x[n - 1] + difx))
                if vary1ast == 0:
                    vary = int(randint(0, int(dify/2)) - dify/4)
                elif vary1ast < 0:
                    vary = randint(0, int(dify/4))
                else:
                    vary = 0 - randint(0, int(dify/4))
                y.append(y0 + vary)
                if t == 0:
                    y[n] = 0
                if t == ny:
                    y[n] = self.ymax

                listpoint.append(x[n])
                listpoint.append(y[n])
                with self.canvas:
                    Color(0.6, 0.6, 1.)
                    Line(circle=(x[n], y[n], 5))

            with self.canvas:
                Color(r, v, b)
                Bezier(points=listpoint, segment=150, dash_length=10, dash_offset=10)
                #r, v, b = rnd_rvb()
                #Color(r, v, b)
                #Line(points=[0, y0, self.xmax, y0])

        # creation des lignes de separations verticales
        for t in range(0, nx+1):
            x0 = int(t * difx)
            if t == nx:
                x0 = self.xmax
            x = [x0]
            y = [0]
            r, v, b = (0, 1., 0)
            varx = 0
            listpoint = [x[0],y[0]]
            with self.canvas:
                Color(0.5,0.8,0.5)
                Line(points=(x0 , 0 , x0, self.ymax))
            with self.canvas:
                Color(0.6, 1., 0.6)
                Line(circle=(x[0], y[0], 5))
            for n in range(1, ny*iter + 1, iter):
                for i in range(0, iter):
                    z = n + i
                    #print("n:", n, "i:",i, 'z:',z)
                    varxlast = varx
                    y.append(int(y[z-1] + dify/iter))
                    varx = int(randint(0, int(difx))-difx/2)
                    x.append(x0+varx)
                    print("x:", x[n], "y:", y[n])
                    if t == 0:
                        x[z] = 0
                    if t == nx:
                        x[z] = self.xmax
                    with self.canvas:
                        Color(0.6, 1., 0.6)
                        Line(circle=(x[z], y[z], 5))
                    listpoint.append(x[z])
                    listpoint.append(y[z])
            with self.canvas:
                Color(r, 1, b)
                Line(bezier=listpoint)


    def pressed(self, instance):
        print("enregistrement de : " + self.name.text + " " + self.lastname.text + " - " + self.email.text)
        print(self.xmax)
        self.name.text = ""
        self.lastname.text = ""
        self.email.text = ""
        xfin = self.width
        yfin = self.height
        with self.canvas:
            Color(1., 1., 0)
            Line(bezier=(0, 200, 100, 300, 200, 200))
            Color(1., 0, 0)
            Line(points=[300, 400, xfin, 200])


class MyApp(App):
    def build(self):
        return MyGrid()


def rnd_rvb():
    r = randint(0, 100) / 100
    v = randint(0, 100) / 100
    b = randint(0, 100) / 100
    return r, v, b

def calc_nb_piece(npiece = 250, width= 1920, height = 1080, type=0):
    surface_tot = width * height
    surface_unit = surface_tot/npiece

    if type == 0:
        l = surface_unit ** 0.5
        print("longueur unit", l)
        nbpiece_width = int(width/l) + 1
        lwidth = width/nbpiece_width
        nbpiece_height = int(height/l) + 1
        lheight = height/nbpiece_height
        nbpiece_tot = nbpiece_width * nbpiece_height

        print("nb piece long:", nbpiece_width, "nbpiece_height:", nbpiece_height, "nbpiece_tot:", nbpiece_tot)
        return lwidth, lheight, nbpiece_width, nbpiece_height

if __name__ == "__main__":
    print(Window.system_size)
    Window.fullscreen = 'auto'

    MyApp().run()
