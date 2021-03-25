import numpy as np
def calc_ent(x):
    """
        calculate shanno ent of x
    """

    x_value_list = set([x[i] for i in range(x.shape[0])])
    ent = 0.0
    for x_value in x_value_list:
        p = float(x[x == x_value].shape[0]) / x.shape[0]
        logp = np.log2(p)
        ent -= p * logp

    return ent

x1= np.array([1,2,3,4,5])
x2 = np.array([2,2,3,3,3])
x3 = np.array([2,2,2,2,2])
x4 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6])
x5 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 15, 0, 7, 0, 19, 15, 16, 2, 0, 6, 2, 4, 0, 0])
print(calc_ent(x1))
print(calc_ent(x2))
print(calc_ent(x3))
print(calc_ent(x4))
print(calc_ent(x5))