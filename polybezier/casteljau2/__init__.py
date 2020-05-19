import numpy as np


class Casteljau2:
    def __init__(self, points = None, precision=20):
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

        self.transf_listtuple_to_mat(points)
        self.pre_calc_t()
        self.pre_calc_coef()
        self.pre_calc_eq()
        self.caculcoordonnees()
        self.def_groupe_points(3)

    def transf_listtuple_to_mat(self, points):
        t = None
        print(type(points[0]))
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
        pt = self.points
        self.coord = self.coef_eq * self.points

    def caculcoordonnees_etendu(self):
        pass

    def def_groupe_points(self, np):
        self.nb_courbes = self.npoints-3
        for p in range(0, self.nb_courbes):
            tmp = []
            for n in range(0, 4):
                t = n + p
                tmp.append(self.points[t])
            self.index_courbes.append(tmp)

    def pre_calc_t_etendu(self,ncourbe=3):
        #self.precision = self.precision * self.nb_courbes
        self.precision = self.precision * ncourbe
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
        print("transpose",  self.precision_list)
        for n in range(ncourbe):

            pass
        self.pre_calc_eq()

