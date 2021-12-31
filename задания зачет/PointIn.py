'''
Задача:
Дано N точек, соединенных последовательно - образуется многоугольник
Определить, является точка с координатами (x0,y0) внутри или вне многоугольника

Алгоритм: 
1. Многоугольник разбивается на отрезки
2. Проверяется количество пересечений отрезка х=х0 (0<y<y0) с отрезками многоугольника
    Если количество пересечений чётное - точка вне многоугольника
    Если количество пересечений нечёрное - точка внутри многоугольника
'''



import numpy as np
import matplotlib.pyplot as plt



def create_sections(p_list):
    '''
    Функция разбивает многоугольник на отрезки 
    Возвращает список с параметрами отрезов
        1. Коэфф наклона
        2. y0 = y(x=0)
        3. x1
        4. y1 
        5. x2
        6. y2
    '''

    # Списки для параметров отрезков
    tan_list = []
    y0_list = []
    x1_list, y1_list = [], []
    x2_list, y2_list = [], []

    for i in range(-1, len(p_list)-1):

        # Временное сохранение параметров начальной и конечной точек отрезка
        p1x, p1y = p_list[i]
        p2x, p2y = p_list[i+1]

        # Вычислить параметры отрезка
        tan_tmp = (p2y-p1y)/(p2x-p1x) if p2x != p1x else 1e100
        y0_tmp = p1y - tan_tmp * p1x
        x1_tmp, y1_tmp = p1x, p1y
        x2_tmp, y2_tmp = p2x, p2y

        # Записать параметры отрезка
        tan_list.append(round(tan_tmp, 3))
        y0_list.append(round(y0_tmp, 2))
        x1_list.append(x1_tmp)
        y1_list.append(y1_tmp)
        x2_list.append(x2_tmp)
        y2_list.append(y2_tmp)

    # Свернуть всё в один список
    segm_param = list(zip(tan_list, y0_list, x1_list, y1_list, x2_list, y2_list))

    return segm_param



def count_intersect(segm_param, x0, y0):
    '''
    Функция считает количество пересечений отрезка х=х0 (0<y<y0) 
    со всеми отрезками многоугольника
    '''

    intersect = 0

    for segm in segm_param:
        tan_t, y0_t, x1_t, y1_t, x2_t, y2_t = segm

        # Проверка, удволетворяет ли X параметрам отрезка
        if not (x0 > min(x1_t, x2_t) and x0 < max(x1_t, x2_t)):
            continue

        # Проверка, удволетворяет ли Y параметрам отрезка
        y_int = tan_t * x0 + y0_t
        if y_int > y0:
            continue
        if not (y_int > min(y1_t, y2_t) and y_int < max(y1_t, y2_t)):
            continue
        
        # Если удволетворяют = записываем пересечение
        intersect += 1

    return intersect



# Параметры поля
Px_max = 10
Py_max = 10
N_points = 7

# Создание многоугольника
random_x = lambda: round(Px_max * np.random.rand(), 2)
random_y = lambda: round(Py_max * np.random.rand(), 2)
points = [(random_x(), random_y()) for _ in range(N_points)]

# Параметры точки для проверки
x_check, y_check = 5, 5

aa = create_sections(points)
# print(aa)

# Проверка количества пересечений
inter = count_intersect(aa, x_check, y_check)
# print(inter)

# Вывод ответа
print('НЕТ : Точка вне многоугольника' if inter%2 == 0 else 'ДА : Точка внутри многоугольника')

# Отрисовка многоугольника и точки
x_list, y_list = map(list, zip(*points))
x_list.append(x_list[0])
y_list.append(y_list[0])
plt.plot(x_list, y_list, 'D-')
plt.plot(x_check, y_check, 'D')
plt.grid(True)
plt.xlim(0, Px_max)
plt.ylim(0, Py_max)
plt.show()