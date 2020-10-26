# 绘制进程权重分布图
from matplotlib import pyplot as plt
import random

plt.figure(figsize=(10,6))
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

plt.title('进程权重分布示意图(部分)')
plt.xlabel('进程')
plt.ylabel('权重')

process = []
weights = []
count = 1
with open('weight_result.txt', 'r') as f:
    for line in f.readlines():
        kv = line.strip().split(':')
        show = random.random() * (100/count)
        if show > 0.8:
            proc = ':'.join(kv[0:-1])
            weight = kv[-1]
            process.append(proc)
            weights.append(float(weight))
        count += 1


# plt.tight_layout()
plt.plot(process, weights, '.')
plt.xticks(rotation=-90)    # 设置x轴标签旋转角度
plt.show()
