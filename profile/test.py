import numpy as np
import matplotlib
from matplotlib import pyplot as plt
font = {
    'family':'SimHei',
    'weight':'bold',
    'size':12
}
matplotlib.rc("font", **font)  #解决中文乱码
matplotlib.rcParams['axes.unicode_minus'] =False  #解决负号显示乱码
def test1():
    plt.figure(figsize=(8,4),dpi=80)  #设置图形大小，分辨率
    plt.plot([0,2,4,6,8],[3,1,4,5,2])
    plt.ylabel('Grade')
    plt.xlabel('x轴')
    plt.axis([-1,10,0,10]) #确定x，y轴的范围 前两个x轴小大，后两个y轴小大
    # plt.savefig('test1',dpi=600) #保存图形，默认png
    plt.show()

def test2():
    def f(t):
        return np.exp(-t) * np.cos(2 * np.pi * t)

    a = np.arange(0, 5, 0.2)
    plt.subplot(211)
    plt.plot(a, f(a))
    plt.subplot(212)
    #linestyle线段什么样式，marker节点什么样式
    plt.plot(a, np.cos(2 * np.pi * a), color='r', linestyle='--',
             marker='.')  # 等价于plt.plot(a,np.cos(2*np.pi*a),'r--.')
    # plt.savefig('test2')
    plt.show()

def test3(): #绘制多条线
    a = np.arange(10)
    #x轴不能省
    # plt.plot(a, a * 1.5, a, a * 2.5, a, a * 3.5, a, a * 4.5) #自动分配颜色
    #自定义样式
    plt.plot(a, a * 1.5, 'go:', a, a * 2.5, 'rx', a, a * 3.5, '^', a, a * 4.5, 'bd-.')
    plt.title('f(a)=cos(2\pi a)')
    plt.show()

def test4():
    a = np.arange(0, 3, 0.02)
    plt.figure(figsize=(10, 8), dpi=80)  # 设置图形大小
    plt.xlabel('横轴:时间', fontproperties='SimHei', fontsize=20)
    plt.ylabel('纵轴：振幅', fontproperties='SimHei', fontsize=10)
    plt.title('$f(a)=cos(2\pi a)$')
    plt.plot(a, np.cos(2 * np.pi * a))
    plt.savefig('test4', dpi=600)
    plt.show()

def test5():
    # 划分子区域并实例化
    fig, ax = plt.subplots(1)
    # 绘图
    ax.plot(np.random.randn(1000).cumsum(), label='line0')
    ax.plot(np.random.randn(1000).cumsum(), label='line1')
    ax.plot(np.random.randn(1000).cumsum(), label='line2')
    # 设置刻度
    # plt.xlim([0,500])
    ax.set_xlim([0, 600])

    # 设置显示的刻度
    # plt.xticks([0,500])
    ax.set_xticks(range(0, 600, 100))

    # 设置刻度标签
    # ax.set_yticklabels(['Jan', 'Feb', 'Mar'])

    # 设置坐标轴标签
    ax.set_xlabel('Number')
    ax.set_ylabel('Month')

    # 设置标题
    ax.set_title('Example')

    # 图例

    ax.legend()
    ax.legend(loc='best')  #选择最佳位置
    # plt.legend()

    plt.show()

def test6():
    np.random.seed(1)
    x = np.random.rand(10)
    y = np.random.rand(10)

    colors = np.random.rand(10)
    area = (30 * np.random.rand(10)) ** 2
    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.show()


if __name__ == '__main__':
    # test1()
    # test2()
    # test3()
    # test4()
    # test5()
    test6()