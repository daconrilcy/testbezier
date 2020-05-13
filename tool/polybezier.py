# exemple de polynome de Bernstein de degrés 3 :
# (1-t)3+3t(1-t)²+3t²(1-t)+t3
# depart : ((1-t)+t)3
# exemple de polynome de Bernstein de degrés 2 :
# (1-t)²+2t(1-t)+2t+t²
# depart : ((1-t)+t)²
from kivy.vector import Vector


class Polybezier:
    def __init__(self, points=None, precision=100):
        if points is None:
            points = [[0, 0], [0, 0]]
        if precision == 0:
            precision = 1
        self.__points = points
        self.__degres = len(points) - 1
        self.__precision = precision
        self.__allcoef = [[0], [1, 1], [1, 2, 1]]
        self.__puisA = []
        self.__puisB = []
        self.__coef = []
        self.__coord = None
        self.__calcNeedUpdate = False
        self.__recalPuisCoef = False

        self.__calc_coef()
        self.__calc_puissance()
        self.__do_all_calc()

    def get_points(self):
        return self.__points

    def set_points(self, points=None):
        if points is None:
            points = [[0, 0], [0, 0]]
        if len(self.__points) != len(points):
            self.__recalPuisCoef = True
        self.__points = points
        self.__degres = len(points) - 1
        self.__calcNeedUpdate = True

    def get_precision(self):
        return self.__precision

    def set_precision(self, precision=100):
        self.__precision = precision
        self.__calcNeedUpdate = True

    def get_coord(self):
        if self.__calcNeedUpdate:
            self.__do_all_calc()
        return self.__coord

    def get_degres(self):
        return self.__degres

    def get_coef(self):
        return self.__coef

    def get_puissances(self):
        return self.__puisA, self.__puisB

    def __calc_coef(self):
        maxcoefprev = len(self.__allcoef) - 1
        if self.__degres > maxcoefprev:
            for n in range(maxcoefprev, self.__degres):
                coefT = [1]
                start = self.__allcoef[maxcoefprev]
                for p in range(1, len(start)):
                    k = start[p - 1] + start[p]
                    coefT.append(k)
                coefT.append(1)
                self.__allcoef.append(coefT)
                maxcoefprev = n + 1
                self.__coef = coefT
        else:
            self.__coef = self.__allcoef[self.__degres]
        self.__degreshaschanged = False

    def __calc_puissance(self):
        step = self.__degres + 1
        pa = []
        pb = []
        for n in range(0, step):
            m = self.__degres - n
            pa.append(m)
            pb.append(n)
        self.__puisA = pa
        self.__puisB = pb

    def print_formule(self):
        l = len(self.__coef)
        eq = ''
        pa = ''
        b = ''
        c = ''
        for n in range(l):
            c = str(self.__coef[n]) + "x"
            pa = '(1-t)^' + str(self.__puisA[n])
            b = 'xt^' + str(self.__puisB[n])
            P = "xP" + str(n) + "+"
            if self.__coef[n] == 1:
                c = ''
            if self.__puisA[n] == 0:
                pa = ''
                b = 't^' + str(self.__puisB[n])
                P = "xP" + str(n)
            if self.__puisB[n] == 0:
                b = ''
            if self.__puisA[n] == 1:
                pa = '(1-t)'
            if self.__puisB[n] == 1:
                b = 'xt'

            eq += c + pa + b + P
        return eq

    def __cal_result_t(self, tic_brute):

        if len(self.__points) < len(self.__coef):
            print("pas assez de points pour le calcul")
            return None
        l = len(self.__coef)
        caltmp = Vector(0, 0)
        k = 0
        tic = tic_brute / self.__precision
        for n in range(0, l):
            co = self.__coef[n]
            pa = self.__puisA[n]
            pb = self.__puisB[n]
            pv = Vector(self.__points[n])
            k = co * (1 - tic) ** pa * tic ** pb * pv
            caltmp += k
        return caltmp

    def __do_all_calc(self):
        coord = []
        if self.__recalPuisCoef:
            self.__calc_puissance()
            self.__calc_coef()
            self.__recalPuisCoef = False

        for pr in range(self.__precision):
            coord.append(self.__cal_result_t(pr))
        self.__coord = coord