# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 20:33:59 2021

@author: Alex Akinin

Улучшеная (и что самое главное работающая) программа для задачи о перколяции
Не работает только алгоритм Hoshen-Kopelman 


Contains:
    class Cells - класс всей сетки клеток (в предыдущей программе каждая 
        клетка была свим отдельным объектом)
    pygame_window() - функция вывода сетки клеток в окне pygame
    draw_prob_ro_depend() - функция определения зависимости 
        вероятности пробоя от величины ро
"""


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


from time import process_time_ns
import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
import time as tm


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


class Cells:
    ''' Класс сетки клеток '''
    def __init__(self, N, passed_val=None) -> None:
        '''
        Метод инициализации (создания) объекта сетки Cells

        Parameters
        ----------
        N : int
            Размер сетки
        passed_val : int, optional
            Значение, которое можно привоить клетке при создании. The default is None.
        '''

        self.col = N
        self.row = N

        self.run = 0
        self.markerdict = {}

        # Задать случайные значения
        randomizer = lambda: 0 if np.random.rand() > ro else 1
        if passed_val == None:
            self.val = [[randomizer() for j in range(self.row)] for i in range(self.col)]
        else:
            self.val = [[passed_val for j in range(self.row)] for i in range(self.col)]
        
        # Переменные для алгоритмов 
        self.open = [[None for j in range(self.row)] for i in range(self.col)]
        self.marker = [[None for j in range(self.row)] for i in range(self.col)]

        # Переменные для Pygame
        self.width = round(WIDTH / self.col)
        self.height = round(HEIGHT / self.row)
        self.tRect = [[pg.Rect(i*self.width, j*self.height, self.width, self.height)
                       for j in range(self.row)] for i in range(self.col)]
        self.tSurf = [[pg.Surface((self.width, self.height)) 
                        for j in range(self.row)] for i in range(self.col)]
        self.colors = [[((255,255,255) if self.val[i][j] == 0 else (0,0,0)) 
                        for j in range(self.row)] for i in range(self.col)]
    

    def draw(self, DISPLAYSURF, marker=False) -> None:
        '''
        Метод обновления объектов в окне Pygame

        Parameters
        ----------
        DISPLAYSURF : pygame display surface
            Объект плоскости окна
        marker : bool
            Переменная режима вывода цветов
                True - вывод цветов маркеров
                False - вывод цветов алгоритма "заражения" метода infection
        '''

        for i in range(self.col):
            for j in range(self.row):

                # Выбор режима маркеров либо режима открытости
                if marker:
                    if self.val == 0:
                        self.colors[i][j] = (255,255,255)
                    elif self.val == 1:
                        self.colors[i][j] = (0,0,0)
                    if self.marker != None:
                        self.colors[i][j] = self.markerdict.get(self.marker[i][j])
                    if self.colors[i][j] == None:
                        self.colors[i][j] = (0,0,0)
                else:
                    if self.isOpen(i, j):
                        if self.run == 0:
                            self.colors[i][j] = (255,0,0)
                        if self.run == 1:
                            self.colors[i][j] = (0,255,0)

                # Обновление цвета объектов прямоугольников модуля Pygame
                self.tSurf[i][j].fill(self.colors[i][j])
                DISPLAYSURF.blit(self.tSurf[i][j], self.tRect[i][j])
    

    def resetOpen(self):
        ''' Метод очистки открытости клеток для метода my_alg '''
        self.open = [[None for j in range(self.row)] for i in range(self.col)]
    

    def setOpen(self, i, j):
        ''' Метод задания статуса "открыто" для метода my_alg '''
        if self.open[i][j] != False and self.val[i][j] == 1:
            self.open[i][j] = True
    

    def setClosed(self, i, j):
        ''' Метод задания статуса "закрыто" для метода my_alg '''
        if self.val[i][j] != 0:
            self.open[i][j] = False
    

    def isOpen(self, i, j):
        ''' Метод вывода открытости клетки '''
        if self.open[i][j] == True:
            return True
        else:
            return False
    

    def getMarker(self, i, j):
        ''' Getter для self.marker для алгоритма Hoshen_Kopelman '''
        return self.marker[i][j]


    def setMarker(self, i, j, mark):
        ''' Setter для self.marker для алгоритма Hoshen_Kopelman '''
        if self.val[i][j] == 1:
            self.marker[i][j] = mark
    

    def shuffle(self):
        ''' Метод рандомазации значений клеток (как при создании объекта)'''
        randomizer = lambda: 0 if np.random.rand() > ro else 1
        self.val = [[randomizer() for j in range(self.row)] for i in range(self.col)]
    

    def addMarkerColor(self, mark):
        ''' Метод добавления маркера в словарь цветов '''
        self.markerdict[mark] = tuple([round(np.random.rand()*200 + 20) for _ in range(3)])
    

    def infection(self, show):
        ''' 
        Мой алгоритм кластеризации 
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
        show : bool
            Режим постепенной отрисовки "заражения" клеток
            True - будет постепенно отрисовываться на окне Pygame
            False - не будет
        '''
        loop = True
        while loop:

            # Проверка наличия открытых клеток
            open_exist = False
            for i in range(self.col):
                for j in range(self.row):
                    if self.isOpen(i, j):
                        curX, curY = i, j
                        open_exist = True
                        break
                if open_exist:
                    break
            
            # Если нет открытых креток
            if not open_exist:
                loop = False
                return False
            
            self.setClosed(curX, curY)

            if self.run == 0:
                # Проверить если клетка является верхней границей
                for i in range(self.col):
                    if self.isOpen(i, self.row-1):
                        loop = False
                        return True
            elif self.run == 1:
                # Проверить если клетка является правой границей
                for j in range(self.col):
                    if self.isOpen(self.col-1, j):
                        loop = False
                        return True

            # Сделать соседние клетки свободными для анализа
            if curX > 0:
                self.setOpen(curX-1, curY)
            if curX < self.col-1:
                self.setOpen(curX+1, curY)
            if curY > 0:
                self.setOpen(curX, curY-1)
            if curY < self.row-1:
                self.setOpen(curX, curY+1)
            
            if show:
                try:
                    self.draw(DISPLAYSURF)
                    clock.tick(FPS)
                    pg.display.update()
                except: pass


    def my_alg(self, show=False):
        '''
        Метод изначального заражения клеток и вызов метода infection

        Parameters
        ----------
        show : bool
            Режим постепенной отрисовки "заражения" клеток
            True - будет постепенно отрисовываться на окне Pygame
            False - не будет
        '''

        # Сначала проверить верхнюю-нижнюю проводимость
        self.run = 0

        # Отчистить информацию об открытости
        self.resetOpen()
        
        # Сделать клетки нижней грани открытыми
        for i in range(self.col):
            self.setOpen(i, 0)
        
        # Вызов метода infection
        if self.infection(show):
            return True
        

        # Потом проверить левую-правую проводимость
        self.run = 1

        # Повторно отчистить информацию об открытости
        self.resetOpen()

        # Сделать клетки левой грани открытыми
        for j in range(self.col):
            self.setOpen(0, j)
        
        # Повторный вызов метода infection
        if self.infection(show):
            return True
        
        # Если дошли до этого момента, то пути не существует
        return False


    def union(self, true_marker, other_marker):
        ''' Метод объединения кластеров для метода Hoshen_Kopelman '''
        for i in range(self.col):
            for j in range(self.row):
                if self.getMarker(i, j) == other_marker:
                    self.setMarker(i, j, true_marker)


    def Hoshen_Kopelman(self, show=False):
        '''
        Алгоритм кластеризации Hoshen-Kopelman

        Parameters
        ----------
        show : bool
            Режим постепенной отрисовки "заражения" клеток
            True - будет постепенно отрисовываться на окне Pygame
            False - не будет
        '''

        # Ввести самый большой маркер
        self.highest_marker = 0
        for i in range(self.col):
            for j in range(self.row):

                # Отчистка предыдущих маркеров
                l_neighbor, d_neighbor, neighbors = None, None, []

                if self.val[i][j] == 1:
                    # Сбор маркеров соседей
                    # Маркер слева
                    if i > 0:
                        l_neighbor = self.getMarker(i-1, j)
                    else:
                        l_neighbor = None

                    # Маркер снизу
                    if j > 0:
                        d_neighbor = self.getMarker(i, j-1)
                    else:
                        d_neighbor = None
                    
                    print(l_neighbor, d_neighbor)

                    # Анализ собраных маркеров
                    if l_neighbor == None and d_neighbor == None:
                        self.highest_marker += 1
                        self.setMarker(i, j, self.highest_marker)
                        self.addMarkerColor(self.highest_marker)

                    elif l_neighbor != None and d_neighbor == None:
                        self.setMarker(i, j, l_neighbor)
                    
                    elif l_neighbor == None and d_neighbor != None:
                        self.setMarker(i, j, d_neighbor)

                    else:
                        if l_neighbor == d_neighbor:
                            self.setMarker(i, j, l_neighbor)
                        else:
                            neighbors = [l_neighbor, d_neighbor]
                            low_mark = sorted(neighbors)[0]
                            other_mark = sorted(neighbors)[1]
                            self.setMarker(i, j, neighbors[0])
                            self.union(low_mark, other_mark)
                            self.highest_marker = low_mark
                
                
                
                if show:
                    try:
                        self.draw(DISPLAYSURF, marker=True)
                        clock.tick(FPS)
                        pg.display.update()
                    except: pass


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def pygame_window(cells, mode=0):
    '''
    Функция отрисовки постепенного решения задачи кластеризации для cells

    Parameters
    ----------
    cells : object Cells
        Объект, для которого решается задачи кластеризации
    mode : int
        Выбор алгоритма
        0 - my_alg
        1 - Hoshen_Kopelman
    '''
    global DISPLAYSURF, clock

    # Инициализация окна Pygame
    pg.init()
    DISPLAYSURF = pg.display.set_mode((WIDTH, HEIGHT))
    DISPLAYSURF.fill(BGCOLOR)
    pg.display.set_caption("PERCOLATION")
    clock = pg.time.Clock()

    # Выбор режима (алгоритма)
    if mode == 0:
        print(cells.my_alg(show=True))
    elif mode == 1:
        print(cells.Hoshen_Kopelman(show=True))

    # Основной цикл отрисовки 
    gameLoop = True
    while gameLoop:
        # DISPLAYSURF.fill(BGCOLOR)

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                gameLoop = False
        
        cells.draw(DISPLAYSURF)
        pg.display.update()
        clock.tick(FPS)

    pg.quit()



def draw_prob_ro_depend():
    '''
    Варьирует ro глобально и для каждого значения несколько раз 
        определяет, существует ли путь по проводящим клеткам
    Записывает частоту нахождения путей и выводит график
        зависимости вероятности от ro
    
    ПРЕИМУЩЕСТВО ПЕРЕПИСАННОЙ ПРОГРАММЫ!
    После переписания программы - функция стала работать намного быстрее 
    Например: N = 50, number_of_checks = 10
        Старая программа - 119 сек
        Данная программа - 23 сек

    Returns
        None.
    '''
    global ro

    ro_st, ro_ed, ro_num = 0, 1, 51
    ro_arr = np.linspace(ro_st, ro_ed, ro_num, endpoint=True)

    test_cells = Cells(N)

    prob = []
    for ro in ro_arr:
        N_list = []
        for _ in range(number_of_checks):
            test_cells.shuffle()
            if test_cells.my_alg():
                N_list.append(1)
            else:
                N_list.append(0)
        print(ro)
        prob.append(np.mean(N_list))

    plt.plot(ro_arr, prob)
    plt.grid()
    plt.show()


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# Переменные для модуля Pygame
WIDTH = 700
HEIGHT = 700
BGCOLOR = (255,255,255)
FPS = 100

N = 50 # Размер сетки
ro = 0.60
number_of_checks = 50 # Количество проверок для каждого ro


cells = Cells(N)
# print(cells.my_alg())

# Отрисовка постепенной кластеризации стеки
# pygame_window(cells, mode=0)

# Вывод зависимости вероятности от значения ro
draw_prob_ro_depend()

