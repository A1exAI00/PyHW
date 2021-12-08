# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 21:23:48 2021

@author: Alex Akinin

Задача перколяции
ПРОГРАММА ❌НЕ РАБОТАЕТ❌ по трём причинам:
    мой алгоритм почему-то не работает
    алгоритм Hoshen-Kopelman тоже 💩
    программа долго думает

Существует вторая версия задачи перколяции  -  9!Percolation pygame.py


Contains: 
    class Cell - класс, хранящий в себе все переменные одной клетки 
    PathExists() - функция, определяющая, существует ли путь между 
        двумя конкретными клетками
    checkHorisontalSides() - функция, определяющая, существует ли путь 
        между левой-правой гранями
    checkVerticalSides() - функция, определяющая, существует ли путь 
        между нижней-верхней гранями
    checkSides() - вызывает checkHorisontalSides() и checkVerticalSides()
    mod_checkSides() - модифицированный алгоритм определения, есть ли путь
    draw_prob_ro_dependency() - функция определения зависимости 
        вероятности пробоя от величины ро
    drawGrid() - функция, отрисовывающая сетку из клеток
"""


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


import numpy as np
import matplotlib.pyplot as plt
import time


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


class Cell:
    ''' Класс, хранящий в себе все переменные одной клетки '''
    def __init__(self, pos, pass_val=None) -> None:
        '''
        Метод инициализации (создания) объекта класса Cell

        Parameters
        ----------
        pos : 2D tuple
            Позиция клетки.
        pass_val : int, optional
            Значение, которое можно привоить клетке при создании. The default is None.
        '''
        self.x, self.y = pos
        if pass_val == None:
            self.val = 0 if np.random.rand() > ro else 1
        else:
            self.val = pass_val
        self.open = None
        self.marker = None

    def setOpen(self) -> None:
        '''
        Присваивает клетке статус открытой, если она уже не была 
            закрыта или если значение клетки равно 0 (клетка непроводящая)
        Используется в функции PathExists()
        '''

        if self.open != False and self.val != 0:
            self.open = True

    def setClosed(self) -> None:
        ''' Setter значения False для self.open '''
        self.open = False

    def isOpen(self):
        '''
        Вызов значения self.open - открытая ли или закрытая клетка

        Returns
        -------
        boolean
            True : если открыта
            False : если закрыта.
        '''

        return True if self.open == True else False

    def openReset(self) -> None:
        ''' Reset для статуса открытости '''
        if self.open != None:
            self.open = None

    def setVal(self, pass_val) -> None:
        ''' Setter для self.val '''
        self.val = pass_val

    def getVal(self):
        ''' Getter для self.val '''
        return self.val

    def getMarker(self):
        ''' Setter для self.marker '''
        return self.marker

    def setMarker(self, m) -> None:
        ''' Setter для self.marker '''
        if self.val != 0:
            self.marker = m


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def PathExists(gr, p1, p2, tmp_N=None):
    '''
    Определяет, существует ли путь от р1 до р2 по проводящим клеткам
    Алгоритм кратко:
        1. Начальной клетке присваивается статус открытой
        2. Цикл while:
            Из всех клеток находится та, у которой статус открытой
            Если эта клетка является конечной, то возвращается True
            Если больше не осталось открытых клеток, то возвращается False
            Этой клетке присваивается старус закрытой
            Соседям этой клетки присваивается статус открытых


    Parameters
    ----------
    gr : 2D NxN array of Cells
        Квадратный массив из клеток.
    p1 : 2D tuple
        Позиция начальной клетки.
    p2 : 2D tuple
        Позиция конечной клетки.
    tmp_N : int, optional
        Размер массива. The default is None.

    Returns
    -------
    bool
        True - существует путь
        False - не существует путь.
    '''
    x1, y1 = p1
    x2, y2 = p2

    # Проверить если значения р1 или р2 равны 0
    if gr[x1][y1].val == 0 or gr[x2][y2].val == 0:
        return False

    # Унаследовать N или взять глобальную
    if tmp_N == None:
        tmp_N = N

    # Сделать ПОЛНУЮ копию сетки из клеток
    # gr = copy.deepcopy(grid)

    # Отчистить информацию о том, открыта клетка или нет
    # Это замена полной копии объектов сетки
    # Полная копия занимает очень много времени
    for i in range(tmp_N):
        for j in range(tmp_N):
            gr[x1][y1].openReset()

    # Задать нынешнюю клетку и делаем её открытой
    curX, curY = p1
    gr[curX][curY].setOpen()

    loop = True
    while loop:

        # Найти свободную клетку и сделать её нынешней
        Open_exist = False
        for i in range(tmp_N):
            for j in range(tmp_N):

                # Проверить если клетка является открытой
                if gr[i][j].isOpen():
                    Open_exist = True
                    curX, curY = i, j
                    break

            if Open_exist:
                break

        # Проверить если не осталось открытых клеток
        if not Open_exist:
            loop = False
            return False

        # Сделать нынешнюю клетку из закрытой
        gr[curX][curY].setClosed()

        # Проверить если нынешняя кретка является целью
        if (curX, curY) == p2:
            loop = False
            return True

        # Сделать соседние клетки свободными для анализа
        if curX > 0:
            gr[curX-1][curY].setOpen()
        if curX < tmp_N-1:
            gr[curX+1][curY].setOpen()
        if curY > 0:
            gr[curX][curY-1].setOpen()
        if curY < tmp_N-1:
            gr[curX][curY+1].setOpen()


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def Hoshen_Kopelman(grid, tmp_N=None):

    # Задание размера массива
    if tmp_N == None:
        tmp_N = N

    # Отчистка маркеров
    for i in range(tmp_N):
        for j in range(tmp_N):
            grid[i][j].setMarker(None)

    highest_marker = 0

    # Главный цикл алгоритма
    for i in range(tmp_N):
        for j in range(tmp_N):
            neighbors = []

            # Сбор маркеров соседей
            # Маркер слева
            if i > 0:
                l_neighbor = grid[i-1][j].getMarker()
                if l_neighbor != None:
                    neighbors.append(l_neighbor)

            # Маркер снизу
            if j > 0:
                d_neighbor = grid[i][j-1].getMarker()
                if d_neighbor != None:
                    neighbors.append(d_neighbor)

            # Маркер справа
            if i < tmp_N-1:
                r_neighbor = grid[i+1][j].getMarker()
                if r_neighbor != None:
                    neighbors.append(r_neighbor)

            # Маркер сверху
            if j < tmp_N-1:
                u_neighbor = grid[i][j+1].getMarker()
                if u_neighbor != None:
                    neighbors.append(u_neighbor)

            # Анализ собраных маркеров
            if len(neighbors) == 1:
                grid[i][j].setMarker(neighbors[0])

            if len(neighbors) == 2:
                low_mark = sorted(neighbors)[0]
                other_mark = sorted(neighbors)[1]
                grid[i][j].setMarker(neighbors[0])
                for i in range(tmp_N):
                    for j in range(tmp_N):
                        if grid[i][j].getMarker() == other_mark:
                            grid[i][j].setMarker(low_mark)

            if len(neighbors) == 0:
                highest_marker += 1
                grid[i][j].setMarker(highest_marker)


""" 
def union(gr, set_mark, other_mark, tmp_N=None):
    if tmp_N == None:
        tmp_N = N
    
    for i in range(tmp_N):
        for j in range(tmp_N):
            if gr[i][j].getMarker() == other_mark:
                gr[i][j].setMarker(set_mark) 
 """


def checkHoshen_Kopelman(grid, tmp_N=None):

    # Наследование размера массива
    if tmp_N == None:
        tmp_N = N

    Hoshen_Kopelman(grid, tmp_N)

    for i in range(tmp_N):
        for j in range(N):
            m_1 = grid[0][i].getMarker()
            m_2 = grid[tmp_N-1][j].getMarker()
            if m_1 != None and m_2 != None:
                if m_1 == m_2:
                    print(1, i, j, m_1, m_2)
                    return True

    for i in range(tmp_N):
        for j in range(N):
            m_1 = grid[i][0].getMarker()
            m_2 = grid[j][tmp_N-1].getMarker()
            if m_1 != None and m_2 != None:
                if m_1 == m_2:
                    print(2, i, j, m_1, m_2)
                    return True

    return False


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def checkHorisontalSides(grid):
    '''
    По очереди ставит в пару каждой клетке с левой грани 
        клетку с правой грани и определяет, существует ли путь между ними 
    Эта функция показала свою неэффективность из-за очень частого вызова 
        функции PathExists()

    Parameters
    ----------
    grid : 2D NxN array of Cells
        Квадратный массив из клеток.

    Returns
    -------
    bool
        True - существует путь
        False - не существует путь.
    '''
    for i in range(N):
        for j in range(N):
            if PathExists(grid, (i, 0), (j, N-1)):
                return True
    return False


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def checkVerticalSides(grid):
    '''
    По очереди ставит в пару каждой клетке с нижней грани 
        клетку с верхней грани и определяет, существует ли путь между ними 
    Эта функция показала свою неэффективность из-за очень частого вызова 
        функции PathExists()

    Parameters
    ----------
    grid : 2D NxN array of Cells
        Квадратный массив из клеток.

    Returns
    -------
    bool
        True - существует путь
        False - не существует путь.
    '''
    for i in range(N):
        for j in range(N):
            if PathExists(grid, (0, i), (N-1, j)):
                return True
    return False


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def checkSides(grid):
    '''
    Вызывает функции checkVerticalSides() и checkHorisontalSides()
    Если хоть одна из них возврвщает True, возвращает True
    Эта функция показала свою неэффективность из-за вызова неэффективных 
        checkVerticalSides() и checkHorisontalSides()

    Parameters
    ----------
    grid : 2D NxN array of Cells
        Квадратный массив из клеток.

    Returns
        bool
            True - существует путь
            False - не существует путь.

    '''
    if checkVerticalSides(grid):
        return True
    if checkHorisontalSides(grid):
        return True
    return False


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def mod_checkSides(grid):
    '''
    Более эффективная функция определения, существует ли путь 
        между двумя параллельными гранями

    Краткий алгоритм:
        1. Создается вспомогательный массив со стороной на 2 клетки больше
        2. Значения из изначального массива присваиваются внутренним клеткам 
            мод. массива (будто весь изначальный массив окружили 
            непроводящими клетками)
        3. Создаются проводящие пластины слева-справа и определяется, 
            есть ли путь от середины одной пластины до середины другой
            Затем пластины убираются 
        4. Создаются проводящие пластины сверху-снизу и определяется, 
            есть ли путь от середины одной пластины до середины другой
            Затем пластины убираются

    Этот алгоритм более эффективный, потому что созволяет связать все 
        проводящие клетки с одной грани, эффективно, в одну, и одним 
        вызовом функции PathExists() проверить, существует ли путь 

    Parameters
    ----------
    grid : 2D NxN array of Cells
        Квадратный массив из клеток.

    Returns
        bool
            True - существует путь
            False - не существует путь.

    '''
    mod_N = N+2

    p1 = (0, round(mod_N/2))
    p2 = (mod_N-1, round(mod_N/2))
    p3 = (round(mod_N/2), 0)
    p4 = (round(mod_N/2), mod_N-1)

    # Создать модифицированную сетку, ширина и длина на 2 кретки больше
    # Значения каждой клетки равны изначально 1
    mod_grid = [[Cell((i, j), pass_val=0) for j in range(mod_N)]
                for i in range(mod_N)]

    # Передать значения изначальной сетки внутренней части мод. сетки
    for i in range(N):
        for j in range(N):
            mod_grid[i+1][j+1].setVal(grid[i][j].getVal())

    # # Сделать углы мод. сетки непроводящими (значения = 0)
    mod_grid[0][0].setVal(0)
    mod_grid[mod_N-1][0].setVal(0)
    mod_grid[0][mod_N-1].setVal(0)
    mod_grid[mod_N-1][mod_N-1].setVal(0)

    # Создать 2 пластины слева и справа
    for i in range(N):
        mod_grid[0][i+1].setVal(1)
        mod_grid[mod_N-1][i+1].setVal(1)

    # Проверить, есть ли между пластинами лево-право путь
    if PathExists(mod_grid, p1, p2, mod_N):
        return True

    # Убрать 2 пластины слева и справа
    for i in range(N):
        mod_grid[0][i+1].setVal(0)
        mod_grid[mod_N-1][i+1].setVal(0)

    # Создать 2 пластины сверху и снизу
    for i in range(N):
        mod_grid[i+1][0].setVal(1)
        mod_grid[i+1][mod_N-1].setVal(1)

    # Проверить, есть ли между пластинами верх-низ путь
    if PathExists(mod_grid, p3, p4, mod_N):
        return True
    return False


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def draw_prob_ro_dependency():
    '''
    Варьирует ro глобально и для каждого значения несколько раз 
        определяет, существует ли путь по проводящим клеткам
    Записывает частоту нахождения путей и выводит график
        зависимости вероятности от ro
    К сожалению, занимает много времени - десятки минут
    Поэтому для демонсрационных задач рекомендуется выставить 
        размер массива и количество проверок поменьше 
    При настройках этих параметров как 50, 3 соответственно 
        программа выполняется около минуты и выдаёт картину, 
        близкую к желаемой

    Returns
        None.
    '''
    global ro

    ro_st, ro_ed, ro_num = 0, 1, 51
    ro_arr = np.linspace(ro_st, ro_ed, ro_num, endpoint=True)

    prob = []
    for ro in ro_arr:
        N_list = []
        for _ in range(number_of_checks):
            cellsList = [[Cell((i, j)) for j in range(N)] for i in range(N)]
            if mod_checkSides(cellsList):
                N_list.append(1)
            else:
                N_list.append(0)

        prob.append(np.mean(N_list))

    plt.plot(ro_arr, prob)
    plt.grid()


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def drawGrid(grid, tmp_N=None):
    '''
    Функция, отрисовывающая сетку из клеток

    Parameters
    ----------
    grid : 2D NxN array of Cells
        Квадратный массив из клеток.
    tmp_N : int
        Размер массива.

    Returns
        None.
    '''
    if tmp_N == None:
        tmp_N = N

    x1 = []
    y1 = []

    for i in range(tmp_N):
        for j in range(tmp_N):
            if grid[i][j].val == 1:
                x1.append(i)
                y1.append(j)

    plt.plot(x1, y1, 'ro')


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


st = time.perf_counter()

N = 50  # Размер массива
ro = 0.5
number_of_checks = 10  # Количество проверок


# Как создается двумерный массив с объектами Cell
cellsList = [[Cell((i, j)) for j in range(N)] for i in range(N)]

# Нарисовать сетку в Matplotlib
# drawGrid(cellsList)


draw_prob_ro_dependency()

# Hoshen_Kopelman(cellsList)

# print(f'Норм проверка {checkSides(cellsList)}')
# print(f'Мод проверка {mod_checkSides(cellsList)}')
# print(f'H проверка {checkHoshen_Kopelman(cellsList)}')

# plt.show()


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


print(f'Eval took: {time.perf_counter() - st} sec')
