# exemple de polynome de Bernstein de degrés 3 :
# (1-t)3+3t(1-t)²+3t²(1-t)+t3
# depart : ((1-t)+t)3
# exemple de polynome de Bernstein de degrés 2 :
# (1-t)²+2t(1-t)+2t+t²
# depart : ((1-t)+t)²
from kivy.vector import Vector

import numpy as np


# !!!! Attention les points doivent être envoyé sous forme de tableau vecteur !!!!!! #
class Polybezier:
    def __init__(self, points=None, precision=100):
        if points is None:
            points = [[0, 0], [0, 0]]
        if precision == 0:
            precision = 1
        self.__points = points
        self.__npoints = 0
        self.__ncoef = 0
        self.__degres = len(points) - 1
        self.__precision = precision
        self.__allcoef = [[0], [1, 1], [1, 2, 1], [1, 3, 3, 1]]
        self.__puisA = []
        self.__puisB = []
        self.__coef = []
        self.__coord = None
        self.__calcNeedUpdate = False
        self.__recalPuisCoef = False
        self.__preCalculed_t = None
        self.__pre_calculed_tcoef = None
        self.__precalcNeedUpdate = True
        self.coorda = None

        self.__calc_coef()
        self.__pre_calcul_tcoef()
        self.__calcul_coord2()
        self.__calc_puissance()

    def get_points(self):
        return self.__points

    def set_points(self, points=None):
        if points is None:
            points = [[0, 0], [0, 0]]
        if self.__npoints != len(points):
            self.__degres = len(points) - 1
            self.__calc_coef()
        self.__points = points
        self.__npoints = len(points)
        self.__calcNeedUpdate = True

    def get_precision(self):
        return self.__precision

    def set_precision(self, precision=100):
        self.__precision = precision
        self.__precalcNeedUpdate = True

    def get_coord(self):
        if self.__calcNeedUpdate:
            self.__calcul_coord2()
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
                coeft = [1]
                start = self.__allcoef[maxcoefprev]
                for p in range(1, len(start)):
                    k = start[p - 1] + start[p]
                    coeft.append(k)
                coeft.append(1)
                self.__allcoef.append(coeft)
                maxcoefprev = n + 1
                self.__coef = coeft
                self.__ncoef = len(coeft)
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
        ln = len(self.__coef)
        eq = ''
        for n in range(ln):
            c = str(self.__coef[n]) + "x"
            pa = '(1-t)^' + str(self.__puisA[n])
            b = 'xt^' + str(self.__puisB[n])
            p = "xP" + str(n) + "+"
            if self.__coef[n] == 1:
                c = ''
            if self.__puisA[n] == 0:
                pa = ''
                b = 't^' + str(self.__puisB[n])
                p = "xP" + str(n)
            if self.__puisB[n] == 0:
                b = ''
            if self.__puisA[n] == 1:
                pa = '(1-t)'
            if self.__puisB[n] == 1:
                b = 'xt'

            eq += c + pa + b + p
        return eq

    def __pre_calcul_tcoef(self):
        t1 = []
        t2 = []
        for n in range(0, self.__precision + 1):
            t = n / self.__precision
            tmp1 = []
            tmp2 = []
            for d in range(self.__degres + 1):
                r = self.__degres - d
                tmp1.append((1 - t) ** r)
                tmp2.append(t ** d)
            t1.append(tmp1)
            t2.append(tmp2)
        t1 = np.mat(t1)
        t2 = np.mat(t2)
        self.__preCalculed_t = np.multiply(t1, t2)
        self.__pre_calculed_tcoef = np.multiply(self.__preCalculed_t, self.__coef)
        self.__calcNeedUpdate = False

    def __calcul_coord2(self):
        if self.__precalcNeedUpdate:
            self.__pre_calcul_tcoef()
        self.__coord = np.array(self.__pre_calculed_tcoef * self.__points).tolist()
        self.__calcNeedUpdate = False
