'''
Дано N точек (то есть даны их координаты)
Найти такую точку, сумма расстояний от которой до этих N точек была бы минимальной
PS: в данной программе так же показано, почему ответ не "центр масс"
'''


import numpy as np
import matplotlib.pyplot as plt


def dist_field(d_lis):

    # Разбить координаты точек на 2 листа - с Хкоорд и Yкоорд
    x_list, y_list = [], []
    for dot in d_lis:
        x,y = dot
        x_list.append(x)
        y_list.append(y)
    
    # найти координаты центра масс
    x_mean = np.mean(x_list)
    y_mean = np.mean(y_list)

    # Найдем поле расстояний
    # Вычисляем поле расстояний для каждой точки 
    Z = []
    Z_sum = 0
    vals = np.linspace(0, 9, num=100)
    for i in range(len(d_lis)):
        tmp_X, tmp_Y = d_lis[i][0], d_lis[i][1]
        X1 = X - tmp_X  # X1 и Y1 являются массивами, потому что X является массивом
        Y1 = Y - tmp_Y
        Z.append(np.sqrt(X1**2 + Y1**2))
    
    # Находим суперпозицию полей
    Z_sum = sum(Z)


    # Отрисовка картинок
    fig = plt.figure(facecolor='white')
    
    ax1 = fig.add_subplot(1,2,1)
    curves = ax1.contour(X, Y, Z_sum, vals, alpha=0.9)
    plt.plot(x_list, y_list, 'D')
    plt.plot(x_mean, y_mean, 'D')
    # ax1.clabel(curves)
    
    ax2 = fig.add_subplot(1,2,2)
    ax2.contourf(X, Y, Z_sum, vals, alpha=0.9, cmap='jet') 
    plt.plot(x_list, y_list, 'D')
    plt.plot(x_mean, y_mean, 'D')
    plt.show()


N_dots = 10
t = np.linspace(0, 1, num=100)
X, Y = np.meshgrid(t, t)

dot_list = [(np.random.rand(), np.random.rand()) for _ in range(N_dots)]

dist_field(dot_list)