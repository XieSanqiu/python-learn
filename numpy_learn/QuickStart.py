import numpy as np
import matplotlib.pyplot as plt

def basic_operate():
    a = np.arange(15).reshape(3, 5)
    print(a)
    '''
    [[ 0  1  2  3  4]
     [ 5  6  7  8  9]
     [10 11 12 13 14]]
    '''
    # 维度数、类型名、元素字节大小、元素数、数组类型
    print(a.ndim, a.dtype.name, a.itemsize, a.size, type(a))  # 2 int32 4 15 <class 'numpy.ndarray'>

    # 数组创建
    b = np.array([2, 3, 4])
    c = np.array([2.3, 4.5, 6])
    print(b.dtype, c.dtype)  # int32 float64
    d = np.array([[1, 2], [3, 4]], dtype=complex)  # 显示指定数组的类型，复数
    print(d)
    e = np.zeros((2, 3))
    print(e)
    f = np.arange(10, 30, 5)  # [10 15 20 25]
    print(f)
    g = np.linspace(0, 2, 9)  # [0.   0.25 0.5  0.75 1.   1.25 1.5  1.75 2.  ]
    print(g)

    # 基本操作
    print(c - b)  # [0.3 1.5 2. ]
    print(b ** 2)  # [ 4  9 16]
    print(b > 3)  # [False False  True]
    print(b * c)
    print(b @ c)  # 矩阵乘积
    b *= 2
    print(b)  # [4 6 8]


def mandelbrot(h, w, maxit=20):
    """Returns an image of the Mandelbrot fractal of size (h,w)."""
    y, x = np.ogrid[-1.4:1.4:h * 1j, -2:0.8:w * 1j]
    c = x + y * 1j
    z = c


    divtime = maxit + np.zeros(z.shape, dtype=int)

    for i in range(maxit):
        z = z ** 2 + c
        diverge = z * np.conj(z) > 2 ** 2  # who is diverging
        div_now = diverge & (divtime == maxit)  # who is diverging now
        divtime[div_now] = i  # note when
        z[diverge] = 2  # avoid diverging too much

    return divtime

if __name__ == '__main__':
    # basic_operate()
    plt.imshow(mandelbrot(20, 20))
    plt.show()