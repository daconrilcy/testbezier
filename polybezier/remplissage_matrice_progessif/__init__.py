# Classe creer à partir du travail python-test/remplissage_matrice_progessif.py
import numpy as np
from easing_functions import *


class MatriceProgessive:
    def __init__(self, precision=None, nbpointref=None, degres=3):
        self.precision = precision
        self.nbpoint_ref = nbpointref
        self.nbcourbe = nbpointref - 3
        self.qeio = QuadEaseInOut(start=0, end=1, duration=precision)
        self.precision_totale = self.nbcourbe * precision
        self.degres = degres
        self.coef_base = np.array([1, 3, 3, 1])
        self.t = None
        self.t1 = None
        self.all_t = None
        self.mat_mult = None
        self.mat_finale = None

        self.make_all_calculation()

    def dupliquer_coef(self):
        tt = self.coef_base
        tmp = []
        for n in range(self.nbcourbe - 1):
            tmp = np.concatenate((self.coef_base, tt))
            tt = tmp
        self.coef_base = tmp

    def creer_paliers_intermediaires(self):
        self.t = np.arange(0, 1 + 1 / self.precision_totale, 1 / (self.precision_totale - 1))
        self.t1 = 1 - self.t
        # mise en puissance :
        t_temp = []
        t1_temp = []
        # passage des coefs en fonction des puissances : t^0, t^1, t^2, t^3
        for n in range(0, self.degres + 1):
            m = self.degres - n
            t_temp.append(np.power(self.t, n))
            t1_temp.append(np.power(self.t1, m))
        t_temp = np.array(t_temp, float).transpose()
        t1_temp = np.array(t1_temp, float).transpose()
        self.all_t = np.multiply(t_temp, t1_temp)

    def creer_matrice_multiplicative(self):
        # creation d'une matrice de multiplication pour annuler ou pas des sequences de coefficent
        self.mat_mult = []
        pr = 0
        v = 0
        for p in range(self.precision_totale):
            tmp = []
            for n in range(0, self.nbcourbe * 4):
                if (n >= v * 4) & (n < v * 4 + 4):
                    tmp.append(self.qeio.ease(self.precision - pr))
                elif (n >= v * 4 + 4) & (n < v * 4 + 8):
                    tmp.append(self.qeio.ease(pr))
                else:
                    tmp.append(0)
            if p >= (v + 1) * self.precision_totale / self.nbcourbe - 1:
                v += 1
            pr += 1
            if (pr == self.precision) | (p >= self.precision_totale - self.precision):
                pr = 0
            # muliplication de la matrice de base par les coefficients sequencés
            tmp = np.multiply(self.coef_base, tmp)
            self.mat_mult.append(tmp)

        self.mat_mult = np.array(self.mat_mult)

    def creer_coef_mult_eq_finale(self):
        t0 = []
        for p in range(0, len(self.all_t)):
            tt = self.all_t[p]
            tmp = []
            for n in range(self.nbcourbe - 1):
                tmp = np.concatenate((self.all_t[p], tt))
                tt = tmp
                pass
            t0.append(tmp)
        t = np.array(t0)
        self.mat_finale = np.multiply(t, self.mat_mult)

    def make_all_calculation(self):
        self.dupliquer_coef()
        self.creer_paliers_intermediaires()
        self.creer_matrice_multiplicative()
        self.creer_coef_mult_eq_finale()
