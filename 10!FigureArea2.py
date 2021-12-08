# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 18:54:20 2021

@author: Alex Akinin

Программа для нахождения площади фигуры

Замечания и пояснения:
1) Фигура - множество, ограниченное со всех сторон 
2) Контур - ВНЕШНЕЕ очертание фигуры (то, чем ограничена фигура).
    То есть, если некоторый отрезок полностью находится в контуре, то он не является частью контура 
3) Программа выводит площадь фигуры относительно всего поля в процентах

Contains:
    class Cells - класс сетки 
        Cells.__init__ - метод инициализации объекта Cells
        Cells.setRandPoints - метод создания новых рандомных точек
        Cells.createLine - метод создания одной пиксельной прямой на сетке между двумя точками
        Cells.createLines - метод создания линий между всеми точками объекта Cells
        Cells.draw - метод отрисовки сетки в окне Pygame
        Cells.fillOutside - метод заливки внешней (по отношению к фигуре) части сетки
        Cells.fillStep - 
"""


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


import pygame as pg
import numpy as np


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


class Cells:
    def __init__(self) -> None:
        '''
        Метод инициализации объекта Cells
        Создаёт сектку и задает M_glob рандомных точек
        '''
        
        # Переменные сетки
        self.col = N
        self.row = N

        # Задать M_glob рандомных точек
        self.M = M_glob
        self.points = [(round(np.random.rand() * self.col), round(np.random.rand() * self.row)) for _ in range(self.M)]

        # Переменные для Pygame
        self.width = WIDTH / self.col
        self.height = HEIGHT / self.row
        self.tRect = [[pg.Rect(i*self.width, j*self.height, self.width, self.height)
                       for j in range(self.row)] for i in range(self.col)]
        self.tSurf = [[pg.Surface((self.width, self.height)) 
                        for j in range(self.row)] for i in range(self.col)]
        self.colors = [['white' for j in range(self.row+1)] for i in range(self.col+1)]
        self.updP = []


    def setRandPoints(self, M) -> None:
        '''
        Метод создания M новых рандомных точек
        Записывает точки в переменную self.points (как при инициализации)

        Parameters
        ----------
        M : int
            Количество рандомных точек
        '''

        self.M = M
        self.points = [(np.random.rand() * self.col, np.random.rand() * self.row) for _ in range(M)]
    

    def createLine(self, p1, p2) -> None:
        '''
        Метод создания одной пиксельной прямой на сетке между двумя точками 

        Parameters
        ----------
        p1: tuple
            Координаты первой точки
        p2: tuple
            Кооринаты второй точки
        '''

        x1, y1 = p1
        x2, y2 = p2
        
        dx = x2 - x1
        dy = y2 - y1

        # Алгоритм отрисовки линии
        # Если угол меньше 45 градусов
        if abs(dx) > abs(dy):

            # Если dx > 0:
            if x1 < x2:
                for x in range(x1, x2):
                    y = round(y1 + dy*(x-x1)/dx)
                    self.colors[x][y] = 'black'
                    self.updP.append((x,y))

            # Если dx <= 0:
            else:
                for x in range(x2, x1):
                    y = round(y1 + dy*(x-x1)/dx)
                    self.colors[x][y] = 'black'
                    self.updP.append((x,y))
        
        # Если угол больше 45 градусов
        else:

            # Если dy > 0:
            if y1 < y2:
                for y in range(y1, y2):
                    x = round(x1 + dx*(y-y1)/dy)
                    self.colors[x][y] = 'black'
                    self.updP.append((x,y))
            
            # Если dy <= 0:
            else:
                for y in range(y2, y1):
                    x = round(x1 + dx*(y-y1)/dy)
                    self.colors[x][y] = 'black'
                    self.updP.append((x,y))

    
    def createLines(self) -> None:
        '''
        Метод создания "многоугольника"
        Соединение всех точек self.points методом createLine()
        '''
        # Перебираем все точки
        for i in range(self.M-1):
            self.createLine(self.points[i], self.points[i+1])
        
        # Первую и последнюю дополнительно
        self.createLine(self.points[0], self.points[-1])

    
    def draw(self) -> None:
        '''
        Метод отрисовки сетки в окне Pygame
        '''

        for point in self.points:
            x, y = point
            self.colors[x][y] = 'blue'
            self.updP.append((x,y))

        # for i in range(self.col):
        #     for j in range(self.row):
        
        for i,j in self.updP:

            # Проверка цвета клетки
            if self.colors[i][j] == 'red':
                self.tSurf[i][j].fill((255,0,0))
            elif self.colors[i][j] == 'green':
                self.tSurf[i][j].fill((0,255,0))
            elif self.colors[i][j] == 'blue':
                self.tSurf[i][j].fill((0,0,255))
            elif self.colors[i][j] == 'black':
                self.tSurf[i][j].fill((0,0,0))
            else:
                self.tSurf[i][j].fill((255,255,255))
            
            # Отрисовка клетки
            DISPLAYSURF.blit(self.tSurf[i][j], self.tRect[i][j])
        
        # Отчистка self.updP
        self.updP = []
    

    def fillOutside(self, show=False):
        '''
        Метод заполнения внешней (по отношению к фигуре) части сетки
        Тк площадь фигуры равна площади сетки минус площадь внешней части, то мы считаем именно внешнюю часть
        Алгоритм работает на подобии алгоритма заражения из программы 9!Percolation pygame.py

        Parameters
        ----------
        show : bool
            выбор режима - обновлять окно или нет 
        
        Returns
        -------
        Площадь не заполненной части сетки (площадь фигуры)
        '''

        #Массив зеленых клеток
        self.greens = []

        for i in range(self.col):
            if self.colors[i][0] == 'white':
                self.colors[i][0] = 'green'
                self.greens.append((i,0))
                self.updP.append((i,0))
            if self.colors[i][self.row-1] == 'white':
                self.colors[i][self.row-1] = 'green'
                self.greens.append((i,self.row-1))
                self.updP.append((i,self.row-1))
        for j in range(self.row):
            if self.colors[0][j] == 'white':
                self.colors[0][j] = 'green'
                self.greens.append((0,j))
                self.updP.append((0,j))
            if self.colors[self.col-1][j] == 'white':
                self.colors[self.col-1][j] = 'green'
                self.greens.append((self.col-1,j))
                self.updP.append((self.col-1,j))
        
        # Счетчик клеток 
        # Окно Pygame обновляется только когда счетчик привысит PPF (points per frame)
        tmp_pixel_counter = 0
        green_exist = True
        while green_exist:

            # Вызов шага заливки
            if not self.fillStep():
                green_exist = False

            # Обновление окна Pygame
            if show:
                tmp_pixel_counter += 1
                if tmp_pixel_counter > PPF:
                    tmp_pixel_counter = 0
                    try:
                        self.draw()
                        pg.display.update()
                        clock.tick(FPS)
                    except: pass
        
        # Подсчёт красных клеток 
        reds = 0
        for i in range(self.col):
            for j in range(self.row):
                if self.colors[i][j] == 'red':
                    reds += 1
        
        # Отчистка красных креток
        for i in range(self.col):
            for j in range(self.row):
                if self.colors[i][j] == 'red':
                    self.colors[i][j] = 'white'
                    self.updP.append((i,j))
        
        return (1 - reds / (self.col * self.row))*100

    
    def fillStep(self) -> None:
        '''
        Метод одного шага функции fillOutside()

        Returns
        -------
        bool
            True: есть зеленая клетка - продлжаем цикл
            False: нет зеленых клеток - прерываем цикл
        '''

        # Проверка существования зеленой клетки
        if len(self.greens) == 0:
            return False

        # Проверка нахождение зеленой клетки
        curX,curY = self.greens[-1]
        self.greens.pop()
        
        self.colors[curX][curY] = 'red'
        self.updP.append((curX,curY))

        # Окрашивание соседей клетки в красный 
        if curX > 0:
            if self.colors[curX-1][curY] == 'white':
                self.colors[curX-1][curY] = 'green'
                self.greens.append((curX-1,curY))
                self.updP.append((curX-1,curY))
        if curX < self.col-1:
            if self.colors[curX+1][curY] == 'white':
                self.colors[curX+1][curY] = 'green'
                self.greens.append((curX+1,curY))
                self.updP.append((curX+1,curY))
        if curY > 0:
            if self.colors[curX][curY-1] == 'white':
                self.colors[curX][curY-1] = 'green'
                self.greens.append((curX,curY-1))
                self.updP.append((curX,curY-1))
        if curY < self.row-1:
            if self.colors[curX][curY+1] == 'white':
                self.colors[curX][curY+1] = 'green'
                self.greens.append((curX,curY+1))
                self.updP.append((curX,curY+1))
        
        return True


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# Переменные алгоритма
N = 700
M_glob = 20

# Переменные для модуля Pygame
WIDTH, HEIGHT = 700, 700
BGCOLOR = (255,255,255)
FPS = 100
PPF = N**2/100

# Инициализация окна Pygame
pg.init()
DISPLAYSURF = pg.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(BGCOLOR)
pg.display.set_caption("Figure AREA! (by AlexAkinin)")
clock = pg.time.Clock()

# Создание объекта сетки
cells = Cells()
cells.createLines()
cells.draw()
pg.display.update()

# Заливка внешней части красным
area1 = cells.fillOutside(show=True)
print(f'Относительная площадь фигуры : {area1} %')

gameLoop = True
while gameLoop:

    # Pygame эвенты
    for ev in pg.event.get():
            if ev.type == pg.QUIT:
                gameLoop = False
    
    clock.tick(FPS)
    pg.display.update()

pg.quit()