'''
На плоскости заданы N точек со своими координатами
Найти минимальный периметр многоугольника, содержащего все точки
3 < N < 1000
-10000 < xi, yi < 10000
xi, yi являются целыми
'''


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def get_perimeter(p_list, show=False):
    '''
    Функция определения периметра многоугольника, содержащего все точки массива

    Алгоритм:
        Определяется самая нижняя точка
        Через неё проводится прямая, (почти) параллельная оси абсцисс
        Затем эта прямая начинает вращаться* против часовой стрелки, пока не пересечется** с другой точкой массива
        Теперь эта точка является поворотной для прямой - относительно неё вращяется прямая 
        Так происходит, пока мы не обогнем всю фигуру
    
    * - угол fi изменяется в пределах от 0 до 2pi с некоторым шагом
    ** - пересечение определяется таким неравенством y </> tan(fi) * x, что ему удволетворяет облась, 
        находящаяся "по другую строну" от основного множества точек
        Постепенным вращением угла fi мы можем "зачерпнуть" какую-то точку - через неё будет проходить линия периметра
    
    Визуальная аналогия: 
        Точки - вбитые в доску гвозди
        Мы обходим их ниточкой и связываем
    
    Parameters
    ----------
    p_list : list of tuple
        Список картежей координат точек
    show : bool
        Режим вывода 
        True - вывод графика
        False - нет вывода графика
    
    Returns
    -------
    tot_dist : float
        Длина линии периметра получившегося многоугольника
    '''

    # Сделать переменные для вывода точек на графике
    x_list, y_list = zip(*p_list)

    # Поиск самой нижней точки 
    min_y_val = 1e100
    min_val_index = 0
    for i, coord in enumerate(p_list):
        if coord[1] < min_y_val:
            min_y_val = coord[1]
            min_val_index = i

    # Создание переменной линии периметра
    line_list = []
    line_list.append(p_list[min_val_index])

    fi_span = np.linspace(1e-5, 2*np.pi, 10000)
    pivX, pivY = p_list[min_val_index]
    for fi in fi_span:

        next_p_found = False

        # Если fi является "плохим", то пропустить его
        if fi in [0, np.pi/2, np.pi, 3/2 * np.pi, 2 * np.pi]:
            continue

        # Определение режима неравенства
        if fi < np.pi/2 or fi > 3/2 * np.pi:
            mode = 0
        else:
            mode = 1
        
        # Проверка, удволетворяет ли какая то точка неравенству
        for i, coord in enumerate(p_list):
            x,y = coord
            if mode == 0:
                if y-pivY < np.tan(fi) * (x-pivX):
                    pivX, pivY = coord
                    line_list.append(coord)
                    next_p_found = True
                    break
            else:
                if y-pivY > np.tan(fi) * (x-pivX):
                    pivX, pivY = coord
                    line_list.append(coord)
                    next_p_found = True
                    break
        
        # Проверка, является ли точка начальной
        if next_p_found:
            if (pivX, pivY) == line_list[0]:
                break
    
    # Oпределение длины сегментов периметра 
    # и определение длины всего периметра
    dist = [np.sqrt((line_list[i][0]-line_list[i+1][0])**2 + (line_list[i][1]-line_list[i+1][1])**2) \
        for i in range(len(line_list)-1)]
    dist.append(np.sqrt((line_list[0][0]-line_list[-1][0])**2 + (line_list[0][1]-line_list[-1][1])**2))
    tot_dist = sum(dist)
    
    # Сделать переменные для вывода линии периметра на графике
    x_line, y_line = zip(*line_list)
    
    if show:
        plt.plot(x_list, y_list, 'D')  # Просто точки
        plt.plot([p_list[min_val_index][0]], [p_list[min_val_index][1]], 'D')  # Нижняя точка
        plt.plot(x_line, y_line)  # Линия периметра
        plt.show()

    return tot_dist


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# Создание точек 
coord_max = 10000
point_num = 20
coord_gen = lambda: round(coord_max * (np.random.rand() - 0.5))
points_list = [(coord_gen(), coord_gen()) for _ in range(point_num)]


print(get_perimeter(points_list, show=True))