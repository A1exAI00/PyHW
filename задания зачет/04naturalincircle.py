'''
Найдите, сколько точек c целочисленными координатами попадает в круг радиуса R с центром в точке (х,у)
R - действительное число
Построить график.
'''

import numpy as np
import matplotlib.pyplot as plt


def calcNumberOfPoints(R=10, x=5, y=10):

    # Посчитаем натуральные только в четверти окружности
    coord_x = []
    coord_y = []
    number_of_points = 0
    for i in range(round(x-R), round(x+R)):
        for j in range(round(y-R), round(y+R)):
            if np.sqrt((x-i)**2 + (y-j)**2) < R:
                coord_x.append(i)
                coord_y.append(j)
                number_of_points += 1

    # Если надо выводить число 
    # print(f'Количество точек с натуральными координатами равно {number_of_points}')

    # Если надо вывести на графике
    plt.plot(coord_x, coord_y, 'D')
    plt.grid()
    plt.axhline(y=0, xmin=0, xmax=10, color=(0,0,0)) 
    plt.axvline(x=0, ymin=0, ymax=10, color=(0,0,0))
    plt.show()

    return number_of_points


# Просто вывод точек
calcNumberOfPoints()

# Для вывода графика
# r_max = 20
# r_span = list(np.linspace(1, 20, num=100))
# num_points = list(map(calcNumberOfPoints, r_span))
# plt.plot(r_span, num_points)
# plt.show()