import statistics
import matplotlib.pyplot as plt
import numpy as np
import math as mt
import Defin as Dd
import Interpol as It
import os                                       # Работа с операционной системой
import shutil                                   # Работа с файлами и документами
import pandas as pd                             # Работа с файлами(блокноты, таблицы и тп)
from decimal import Decimal
import requests as res

DataFrame = pd.read_table('simbad (1).tsv', engine='python', index_col=0)
DataFrame = DataFrame.iloc[2:len(DataFrame)]
DataFrame = DataFrame[DataFrame['  Mag U  '] != '     ~   ']
DataFrame = DataFrame[DataFrame['  Mag B  '] != '     ~   ']
DataFrame = DataFrame[DataFrame['  Mag V  '] != '     ~   ']

UB = np.array([float(DataFrame['  Mag U  '][i]) - float(DataFrame['  Mag B  '][i]) for i in range(len(DataFrame))])
BV = np.array([float(DataFrame['  Mag B  '][i]) - float(DataFrame['  Mag V  '][i]) for i in range(len(DataFrame))])

UB, BV = list(set(UB)), list(set(BV))
Nored_X = [-0.35, -0.31, -0.16, 0, 0.13, 0.27, 0.42, 0.58, 0.7, 0.89, 1.18, 1.45, 1.63]
Nored_Y = [-1.15, -1.06, -0.55, -0.02, 0.1, 0.07, 0.03, 0.05, 0.19, 0.47, 1.1, 1.28, 1.2]

m_v = np.array([float(DataFrame['  Mag V  '][i]) for i in range(len(DataFrame))])
m_v = list(set(m_v))
M_v = [-5.8, -4.1, -1.1, 0.7, 2, 2.6, 3.4, 4.4, 5.1, 5.9, 7.3, 9, 11.6]

#-----------------------Интерполяция кривых-----------------------------------------------------------------------------
x_help = np.arange(-0.4, 0.7, 0.001) # интерполяция непокрасненной кривой
y_help = np.array([It.newton_interpol(x_help[i], Nored_X, Nored_Y) for i in range(len(x_help))])

x_help_second = np.arange(-0.36 , 0.75, 0.001) # интерполяция ГП
y_help_second = np.array([It.newton_interpol(x_help_second[i], Nored_X, M_v) for i in range(len(x_help_second))])

#-----------------------Вспомогательные линии первого графика-----------------------------------------------------------
b = np.array([UB[i] - 0.72 * BV[i] for i in range(len(UB))])
x_sub = [np.arange(-0.5, BV[i], 0.01) for i in range(len(BV))]
y_sub = []
for index in range(len(UB)):
    rows_of_y = np.array([0.72*x_sub[index][element] + b[index] for element in range(len(x_sub[index]))])
    y_sub.append(rows_of_y)

#-----------------------Точки пересечения прямых и кривой---------------------------------------------------------------
y_cross = []; x_cross = []
UB_leave_star = [] ;BV_leave_star = []
delet_index=[]
for element in range(len(UB)):
    x_1 = []; y_1 = []
    UB_leave_star_1 = []; BV_leave_star_1 = []
    for i in range(len(y_sub[element])):
        for j in range(len(y_help)):
            if abs(y_help[j] - y_sub[element][i]) <= 0.01 and abs(x_help[j] - x_sub[element][i]) <= 0.01:
                y_1.append(y_help[j]); x_1.append(x_help[j])
                BV_leave_star_1.append(BV[element]); UB_leave_star_1.append(UB[element])
    if x_1 == [] and y_1 == []:
        x_1, y_1 = [0, 0], [0, 0]
        BV_leave_star_1, UB_leave_star_1 = [0, 0], [0, 0]
        delet_index.append(element)
    x_cross.append(x_1); y_cross.append(y_1)
    BV_leave_star.append(BV_leave_star_1); UB_leave_star.append(UB_leave_star_1)

x_cross = np.array([statistics.mean(x_cross[i]) for i in range(len(UB))])
y_cross = np.array([statistics.mean(y_cross[i]) for i in range(len(UB))])
BV_leave_star = np.array([statistics.mean(BV_leave_star[i]) for i in range(len(UB))])
UB_leave_star = np.array([statistics.mean(UB_leave_star[i]) for i in range(len(UB))])

UB_leave_star, BV_leave_star = UB_leave_star[UB_leave_star != 0], BV_leave_star[BV_leave_star != 0] #показатели цвета для звезд, пересекающих непокрасненную кривую
x_cross, y_cross = x_cross[x_cross != 0], y_cross[y_cross != 0] #точки пересечения sub прямых звезд
m_v_cross = [value for index, value in enumerate(m_v) if index not in delet_index] #m_V только для пересекающих звезд

#суммарные значения для определения средней точки
UB_summ, BV_summ, m_v_summ = statistics.mean(UB_leave_star), statistics.mean(BV_leave_star), statistics.mean(m_v_cross)


#-----------------------Точка пересечения прямой средней точки и кривой-------------------------------------------------
bb = UB_summ - 0.72 * BV_summ
x_sr_point_sub = np.arange(-0.5, BV_summ, 0.01)
y_sr_point_sub = np.array([0.72 * x_sr_point_sub[element] + bb for element in range(len(x_sr_point_sub))])

y_point_cross = []; x_point_cross = []
for i in range(len(x_sr_point_sub)):
    for j in range(len(x_help)):
        if abs(x_help[j] - x_sr_point_sub[i]) <= 0.01 and abs(y_help[j] - y_sr_point_sub[i]) <= 0.01:
            y_point_cross.append(y_help[j]); x_point_cross.append(x_help[j])
y_summ_point_cross, x_summ_point_cross = statistics.mean(y_point_cross), statistics.mean(x_point_cross)

#непокрасненные показатели цвета для звезд (исправленные)
UB_corrected = UB_leave_star - (UB_summ - y_summ_point_cross)
BV_corrected = BV_leave_star - (BV_summ - x_summ_point_cross)
UB_corrected_summ, BV_corrected_summ = statistics.mean(UB_corrected), statistics.mean(BV_corrected)

#-----------------------Вспомогательная линия второго графика-----------------------------------------------------------
x_sub_second = np.array([BV_corrected_summ for i in range(len(x_help_second))])
y_sub_second = np.arange(m_v_summ, -5, [(-5 - m_v_summ)/len(x_sub_second)])

#-----------------------Точки пересечения вспомогательной прямой и ГП---------------------------------------------------
y_cross_second = []; x_cross_second = []
for i in range(len(x_sub_second)):
    for j in range(len(x_help_second)):
        if abs(x_help_second[j] - x_sub_second[i]) <= 0.01 and abs(y_help_second[j] - y_sub_second[i]) <= 0.01:
            y_cross_second.append(y_help_second[j]); x_cross_second.append(x_help_second[j])
y_cross_second, x_cross_second = statistics.mean(y_cross_second), statistics.mean(x_cross_second)

#-----------------------Рассчет расстояния------------------------------------------------------------------------------
r = 10**((m_v_summ - y_cross_second + 5 - 3.1 * (BV_summ - x_summ_point_cross)) / 5)
print(m_v_summ, y_cross_second); print(r)


#--------------------------------Графики--------------------------------------------------------------------------------
fig = plt.figure(1)

Graph = plt.subplot(2, 1, 1)
Graph.scatter(BV, UB, alpha=0.6, marker='*')    #звезды до изменения
Graph.scatter(BV_summ, UB_summ, marker='*', color='black') #средняя точка
Graph.scatter(x_help, y_help, s=3, marker='.', color='grey')  #интерполяция
Graph.scatter(Nored_X, Nored_Y, color='red', s=10) #непокраснение
for i in range(len(UB)): Graph.plot(x_sub[i], y_sub[i], alpha=0.3, color='pink')
Graph.scatter(x_cross, y_cross, s=10)
Graph.plot(x_sr_point_sub, y_sr_point_sub, color='black')
Graph.scatter(x_summ_point_cross, y_summ_point_cross, s=10, color='black')
plt.gca().invert_yaxis()
plt.xlabel('B-V'); plt.ylabel('U-B')
plt.grid()

Graph_m_M = plt.subplot(2,1,2)
Graph_m_M.scatter(BV, m_v, marker='*', alpha=0.6)
Graph_m_M.scatter(x_help_second, y_help_second, s=3, marker='.', color='grey')
Graph_m_M.scatter(Nored_X, M_v, color='red', s=10)
plt.gca().invert_yaxis()
plt.xlabel('B-V'); plt.ylabel('M_v, m_v')
plt.grid()

#-----------------------------------------------------------------------------------------------------------------------
fig = plt.figure(2)

Graph = plt.subplot(2, 1, 1)
Graph.scatter(BV_corrected, UB_corrected, alpha=0.6, marker='*')    #звезды после изменения
Graph.scatter(x_help, y_help, s=3, marker='.', color='grey')  #интерполяция
Graph.scatter(Nored_X, Nored_Y, color='red', s=10) #непокраснение
Graph.scatter(x_summ_point_cross, y_summ_point_cross, color='black', s=10, marker='*')   #средняя точка
plt.gca().invert_yaxis()
plt.xlabel('B-V'); plt.ylabel('U-B')
plt.grid()


Graph_m_M = plt.subplot(2,1,2)
Graph_m_M.scatter(BV_corrected, m_v_cross, marker='*', alpha=0.6)
Graph_m_M.scatter(x_help_second, y_help_second, s=3, marker='.', color='grey')
Graph_m_M.scatter(BV_corrected_summ, m_v_summ, color='black', s=10, marker='*')   #средняя точка
Graph_m_M.scatter(Nored_X, M_v, color='red', s=10)
Graph_m_M.plot(x_sub_second, y_sub_second, alpha=1, color='black')
Graph_m_M.scatter(x_cross_second, y_cross_second, s=10, color='black')
plt.gca().invert_yaxis()
plt.xlabel('B-V'); plt.ylabel('M_v, m_v')
plt.grid()

#-----------------------------------------------------------------------------------------------------------------------
plt.show()