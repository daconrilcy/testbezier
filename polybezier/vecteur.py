import numpy as np

coef_base = [[0], [1, 2, 1]]
precision = 2
points = [[1., 2.], [2., 2.], [3., 2.]]
degres = len(points) - 1
points2 = np.mat([[1, 2, 3], [2, 2, 2]])
print(degres)
t1 = []
t2 = []
for n in range(0, precision):
    t = n/precision
    tmp1 = []
    tmp2 = []
    for d in range(degres + 1):
        r = degres - d
        tmp1.append((1- t) ** r)
        tmp2.append(t ** d)
    t1.append(tmp1)
    t2.append(tmp2)
t1 = np.mat(t1)
t2 = np.mat(t2)
t3 = np.multiply(t1, t2)

coef = np.ones(degres + 1)


def caclul_coef():
    coef_temp = []
    if degres > len(coef_base):
        for n in range(1, degres - 1):
            coef_temp = [1]
            for s in range(1, len(coef_base[n])):
                coef_temp.append(coef_base[n][s] + coef_base[n][s - 1])
            coef_temp.append(1)
            coef_base.append(coef_temp)

caclul_coef()

coef_degres_encours = coef_base[degres - 1]

print("t1:", t1)
print("t2:", t2)
print("t3:", t3)
print("points:", points)
print("coef:", coef_degres_encours)
print("t3xpoints", t3 * points)
print("t3xcoef", np.multiply(t3, coef_degres_encours))
print("coord", np.multiply(t3, coef_degres_encours) * points)


def calcul_t():
    print("calcul t")
