import turtle as tt
import numpy as np
import matplotlib.pyplot as plt
import time


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def set_angle(turt, p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if (y2-y1) < 0 and (x2-x1) < 0:
        turt.setheading((np.arctan((y2-y1)/(x2-x1)) * 180/np.pi)-180)
    elif (y2-y1) < 0 and (x2-x1) > 0:
        turt.setheading((np.arctan((y2-y1)/(x2-x1)) * 180/np.pi))
    elif (y2-y1) >= 0 and (x2-x1) < 0:
        turt.setheading((np.arctan((y2-y1)/(x2-x1)) * 180/np.pi)-180)
    else:
        tan = np.arctan((y2-y1)/(x2-x1)) * 180/np.pi if (x2-x1) != 0 else 90
        turt.setheading(tan)


def draw_4turt():

    # Задание параметров turtle
    wn = tt.Screen()
    tt.speed(0)
    wn.tracer(1000)

    # Создание переменных скорости и ребра
    Vel = 1e-2
    a = 1000

    # Создание 4 черепах
    turt1 = tt.Turtle()
    turt2 = tt.Turtle()
    turt3 = tt.Turtle()
    turt4 = tt.Turtle()

    turt1.speed(0)
    turt2.speed(0)
    turt3.speed(0)
    turt4.speed(0)

    # Рассчет начальных позиций
    st1 = ( a/2,  a/2)
    st2 = (-a/2,  a/2)
    st3 = (-a/2, -a/2)
    st4 = ( a/2, -a/2)

    # Перемещение черепах на начальные позиции 
    turt1.penup()
    turt2.penup()
    turt3.penup()
    turt4.penup()
    turt1.goto(st1)
    turt2.goto(st2)
    turt3.goto(st3)
    turt4.goto(st4)
    turt1.pendown()
    turt2.pendown()
    turt3.pendown()
    turt4.pendown()

    turt1.penup()
    turt2.penup()
    turt3.penup()
    turt4.penup()

    
    print(f'Теоретическое время: a/V = {a/Vel}') # Вывод теоретического времени

    t = 0
    while True:
        
        # Сохранить начальные позиции черепах 
        turt1_pos = turt1.pos()
        turt2_pos = turt2.pos()
        turt3_pos = turt3.pos()
        turt4_pos = turt4.pos()

        
        if np.sqrt(turt1_pos[0]**2 + turt1_pos[1]**2) <= Vel*2:
            break

        # Первая охотится за второй
        set_angle(turt1, turt1.pos(), turt2_pos)
        turt1.forward(Vel)

        # Вторая охотится за третьей
        set_angle(turt2, turt2.pos(), turt3_pos)
        turt2.forward(Vel)

        # Третья охотится за четвертой
        set_angle(turt3, turt3.pos(), turt4_pos)
        turt3.forward(Vel)

        # Четвертая охотится за первой
        set_angle(turt4, turt4.pos(), turt1_pos)
        turt4.forward(Vel)

        
        t += 1
        wn.update()

    
    print(f'Практическое время: {t}') # Вывод практического времени


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def draw_Nturt(N=4, V=0.5, r=300):

    wn = tt.Screen()
    tt.speed(0)
    wn.tracer(N)

    turts = [tt.Turtle() for _ in range(N)] # Создание N черепах

    # Перемещение черепах на начальные позиции 
    for i, turt in enumerate(turts):
        turt.penup()
        turt.goto((r*np.cos(i*2*np.pi/N),r*np.sin(i*2*np.pi/N)))
        turt.pendown()
    
    t = 0
    while True:

        turt_pos = [turts[i].pos() for i in range(N)]

        if np.sqrt(turt_pos[i][0]**2 + turt_pos[i][1]**2) <= 2:
            break
        
        # i-я охотится за (i+1)-ой
        for i in range(N-1):
            set_angle(turts[i], turts[i].pos(), turt_pos[i+1])
            turts[i].forward(V)
        
        # N-я охотится за первой
        set_angle(turts[N-1], turts[N-1].pos(), turt_pos[0])
        turts[N-1].forward(V)

        t += 1 
        # wn.update()
    
    print(f'Практическое время: {t}') # Вывод практического времени

    wn.clear()
    return t


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def test_time(N_max=10):
    n = []
    t = []
    for i in range(3, N_max):
        n.append(i)
        t.append(draw_Nturt(i))

    print(t)

    plt.plot(n,t)
    plt.grid(True)
    plt.show()
    return t


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def ant_and_bucket():
    
    # Задание начальных условий
    L = 300
    R = 70
    xc, yc = 100, 50
    perim = 2*np.pi*R

    # Тангенсы наклона левых линий
    T1 = (xc*yc + R*np.sqrt(xc**2 + yc**2 - R**2))/(xc**2-R**2)
    T2 = (xc*yc - R*np.sqrt(xc**2 + yc**2 - R**2))/(xc**2-R**2)

    # Тангенсы наклона правых линий
    N1 = ((L-xc)*yc + R*np.sqrt((L-xc)**2 + yc**2 - R**2))/((L-xc)**2-R**2)
    N2 = ((L-xc)*yc - R*np.sqrt((L-xc)**2 + yc**2 - R**2))/((L-xc)**2-R**2)

    # Координаты точки A
    Ax = (xc**3 + xc*yc**2 - xc*R**2 - yc*R*np.sqrt(xc**2 + yc**2 - R**2))/(xc**2 + yc**2)
    Ay = T1*Ax
    len_A = np.sqrt(Ax**2 + Ay**2)

    # Координаты точки B
    Bx = (xc**3 + xc*yc**2 - xc*R**2 + yc*R*np.sqrt(xc**2 + yc**2 - R**2))/(xc**2 + yc**2)
    By = T2*Bx
    len_B = np.sqrt(Bx**2 + By**2)

    # Координаты точки C
    Cx = -((L-xc)**3 + (L-xc)*yc**2 - (L-xc)*R**2 - yc*R*np.sqrt((L-xc)**2 + yc**2 - R**2))/((L-xc)**2 + yc**2)
    Cy = -N1*Cx
    len_C = np.sqrt(Cx**2 + Cy**2)
    Cx += L

    # Координаты точки D
    Dx = -((L-xc)**3 + (L-xc)*yc**2 - (L-xc)*R**2 + yc*R*np.sqrt((L-xc)**2 + yc**2 - R**2))/((L-xc)**2 + yc**2)
    Dy = -N2*Dx
    len_D = np.sqrt(Dx**2 + Dy**2)
    Dx += L

    # Длина отрезков AC и BD
    AC = np.sqrt((Ax-Cx)**2 + (Ay-Cy)**2)
    BD = np.sqrt((Bx-Dx)**2 + (By-Dy)**2)

    # Относительный угол дуг AC и BD
    Oac = 2*np.arcsin(AC/(2*R))/(2*np.pi)
    Obd = 2*np.arcsin(BD/(2*R))/(2*np.pi)

    # Длина дуг AC и BD
    AC_arc = perim*Oac
    BD_arc = perim*Obd

    print(AC_arc, BD_arc)
    print(f'Путь сверху: {len_A+AC_arc+len_C}')
    print(f'Путь снизу: {len_B+BD_arc+len_D}')

    # Отрисовка поля 
    wn = tt.Screen()
    tt.speed(0)
    wn.tracer(1)
    turt_numba_one = tt.Turtle()
    turt_numba_one.goto((L,0))
    turt_numba_one.penup()
    turt_numba_one.goto((xc, yc-R))
    turt_numba_one.pendown()
    turt_numba_one.circle(R, steps=50)
    turt_numba_one.penup()
    turt_numba_one.goto((0,0))
    
    # Левая верхняя линия
    set_angle(turt_numba_one, (0,0), (1,T1))
    turt_numba_one.pendown()
    turt_numba_one.forward(len_A)
    turt_numba_one.penup()
    turt_numba_one.goto((0,0))

    # Левая нижняя линия
    set_angle(turt_numba_one, (0,0), (1,T2))
    turt_numba_one.pendown()
    turt_numba_one.forward(len_B)
    turt_numba_one.penup()
    turt_numba_one.goto((0,0))

    # Правая верхняя линия
    turt_numba_one.goto((L,0))
    set_angle(turt_numba_one, (0,0), (-1,N1))
    turt_numba_one.pendown()
    turt_numba_one.forward(len_C)
    turt_numba_one.penup()
    turt_numba_one.goto((0,0))

    # Правая нижняя линия
    turt_numba_one.goto((L,0))
    set_angle(turt_numba_one, (0,0), (-1,N2))
    turt_numba_one.pendown()
    turt_numba_one.forward(len_D)
    turt_numba_one.penup()
    turt_numba_one.goto((0,0))

    time.sleep(3)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


draw_4turt()
# draw_Nturt(200)

# test_time(N_max=20)

# ant_and_bucket()