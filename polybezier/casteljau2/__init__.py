import numpy as np
from polybezier.remplissage_matrice import MatriceProgessive


class Casteljau2:
    def __init__(self, points=None, precision=20):
        self.npoints = 0
        if points is None:
            points = np.mat(0, 0)
        self.points = None
        self.precision = precision
        self.precision_list = np.mat
        self.coord = []
        self.degres = 3
        self.coef_en_cours = None
        self.coef_eq = None
        self.pre_calc_t()
        self.pre_calc_coef()
        self.pre_calc_eq()
        self.index_courbes = []
        self.nb_courbes = 0
        self.matrice_eq_entendu = None
        self.points_etendu = []
        self.is_etendu = False

        self.transf_listtuple_to_mat(points)
        if self.npoints > 4:
            self.is_etendu = True
            self.pre_calc_coef_eq_etendu()
            self.creer_matrice_points_etendu()
            self.calc_coordonnees_etendues()
        else:
            self.pre_calc_t()
            self.pre_calc_coef()
            self.pre_calc_eq()
            self.caculcoordonnees()

    def transf_listtuple_to_mat(self, points):
        t = None
        if isinstance(points, np.matrix):
            self.npoints = len(points)
            self.points = points
        if isinstance(points, list):
            if isinstance(points[0], int) | isinstance(points[0], float):
                x = []
                for n in range(0, len(points)):
                    p = n + 2
                    x.append(points[n:p])
                self.points = np.mat(x)
                self.npoints = len(self.points)
            elif isinstance(points[0], tuple) | isinstance(points[0], list):
                self.points = np.mat(points)
                self.npoints = len(self.points)
            else:
                self.points = 1
                self.npoints = np.mat(0, 0)

    def pre_calc_t(self):
        precision_list = np.arange(0, 1 + 1 / self.precision, 1 / self.precision)
        # precision_list = np.array([1,2,3])
        t = []
        t1 = []
        for n in range(0, self.degres + 1):
            m = self.degres - n
            tmp = 1 - precision_list
            t.append(np.power(precision_list, n))
            t1.append(np.power(tmp, m))
        self.precision_list = np.multiply(t, t1).transpose()

    def pre_calc_coef(self):
        coef_base = [[0], [1, 1], [1, 2, 1], [1, 3, 3, 1]]
        self.coef_en_cours = coef_base[self.degres]

    def pre_calc_eq(self):
        self.coef_eq = np.multiply(self.precision_list, self.coef_en_cours)

    def caculcoordonnees(self):
        self.coord = self.coef_eq * self.points

    def pre_calc_coef_eq_etendu(self):
        matrice_entendu = MatriceProgessive(precision=self.precision, nbpointref=self.npoints)
        self.matrice_eq_entendu = np.array(matrice_entendu.matrice_finale)
        self.nb_courbes = matrice_entendu.nbcourbe

    def creer_matrice_points_etendu(self):
        self.points_etendu = []
        for n in range(self.nb_courbes):
            tmp = []
            for p in range(n, n + 4):
                tmp.append(self.points[p])
            self.points_etendu.append(tmp)
        self.points_etendu = np.asmatrix(np.array(self.points_etendu).reshape(4 * self.nb_courbes, 2))

    def calc_coordonnees_etendues(self):
        self.coord = self.matrice_eq_entendu * self.points_etendu

    def set_points_aslist(self, points):
        self.points = points
        if self.is_etendu:
            self.creer_matrice_points_etendu()
            self.calc_coordonnees_etendues()
        else:
            self.caculcoordonnees()
