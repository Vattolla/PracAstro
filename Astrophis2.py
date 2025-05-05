import statistics

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import UnivariateSpline
import scipy as sc
import pandas as pd                             # Работа с файлами(блокноты, таблицы и тп)
# import statistics
# import math as mt
# import Defin as Dd
# import Interpol as It
# import os                                       # Работа с операционной системой
# import shutil                                   # Работа с файлами и документами
# from decimal import Decimal
# from scipy.interpolate import interpolate as Int
# import requests as res

DataTab1 = pd.read_table('TabAstro2', skiprows=1, engine='python', header=None, sep='   ')
Colors = pd.read_table('TabColorsAstro2', engine='python', sep='   ')

Period = 9.481614
# Fi_1 = 0.263333348; Fi_2 = 0.63727311
# V_1 = 8.387663; V_2 = 8.548178
X_phase = np.arange(0, 1, 0.01)

# f = sc.interpolate.interp1d(DataTab1[0], DataTab1[1], kind='cubic')
# Y_help = f(x_sub)
#
# Omega = 2 * mt.pi / Period
# A = (max(DataTab1[1]) - min(DataTab1[1])) / 2
# X_sub = np.arange(DataTab1[0][0] - 1, DataTab1[0][len(DataTab1) - 1], 0.1)
# Y_sub = A + A * np.sin(Omega * X_sub)
#
# Y_app = Akima1DInterpolator(XPhase_sort, YPhase_sort, method='akima')(X_app)
#
# A, B, C, D, E, F = np.polyfit(XPhase_sort, YPhase_sort, 5)
# Y_app = np.array([A*X_app[i]**5 + B*X_app[i]**4 + C*X_app[i]**3 + D*X_app[i]**2 + E*X_app[i] + F for i in range(len(X_app))])
#
# 3 случай


# ----------------------------Линия равного показателя цвета------------------------------------------------------------
Y_line = np.full(1000, 1.35)
X_line = np.arange(0, 1, 0.001)


# Нахождение пересечения прямой и графика показателя цвета
Cross_points = []
v = 0
for i in range(len(X_line)):
    for j in range(len(Colors['B-V'])):
        if abs(X_line[i] - X_phase[j]) < 0.01 and abs(Y_line[i] - Colors['B-V'][j]) < 0.01:
            Cross_points.append(X_phase[j])

''' Нахождение индекса элемента, не относящегося к первой точке пересечения'''
v = [i for i in range(len(Cross_points)) if abs(Cross_points[i] - Cross_points[i - 1]) > 0.1][1]

Fi_points = [statistics.mean(Cross_points[0:v:1]), statistics.mean(Cross_points[v::1])]


# Нахождение точек V для полученных фаз
Cross_points_V = []
for i in range(len(X_phase)):
    for j in range(len(Fi_points)):
        if abs(X_phase[i] - Fi_points[j]) < 0.01:
            Cross_points_V.append(Colors['V'][i])

g = [i for i in range(len(Cross_points_V)) if abs(Cross_points_V[i] - Cross_points_V[i - 1]) > 0.1][1]

V_points = [statistics.mean(Cross_points_V[0:g:1]), statistics.mean(Cross_points_V[g::1])]

# ---------------------------------Перевод JD в фазу и сортировка-------------------------------------------------------
XPhase = np.array([(DataTab1[0][i] / Period - 0.31) % 1 for i in range(len(DataTab1))])
YPhase = DataTab1[1]

XPhase_sort = np.sort(XPhase)
YPhase_sort = []
for jndex, value2 in enumerate(XPhase_sort):
    for index, value in enumerate(XPhase):
        if value not in YPhase_sort and value == value2:
            YPhase_sort.append(YPhase[index])

# ----------------------------------------------------------------------------------------------------------------------


# -----------------------------Аппроксимация графика скоростей----------------------------------------------------------
X_app = np.arange(min(XPhase_sort), max(XPhase_sort), 0.00001)
Y_app = UnivariateSpline(XPhase_sort, YPhase_sort)(X_app)
# ----------------------------------------------------------------------------------------------------------------------

# Интеграл средней скорости по фазе
Vgamma = sc.integrate.trapz(y=Y_app, x=X_app)

# Интеграл Delta_D
V_int = np.array([Y_app[i] for i in range(len(Y_app)) if Fi_points[0] < X_app[i] < Fi_points[1]])
F_int = np.array([X_app[i] for i in range(len(X_app)) if Fi_points[0] < X_app[i] < Fi_points[1]])

# Интеграл по отрезку фаз
Arg_D = V_int - Vgamma
Delta_D = sc.integrate.trapz(y=Arg_D, x=F_int)

R = -3.07 * (Delta_D/(V_points[1] - V_points[0]))

print(R); print(Vgamma, Delta_D) ; print(Fi_points); print(V_points)
# ----------------------------------- Графики --------------------------------------------------------------------------

plt.figure()
Fig1 = plt.subplot(3, 1, 1)
Fig1.plot(X_phase, Colors['V'], color='red')
plt.xlim([-0.1, 1.1])
plt.gca().invert_yaxis()
plt.grid()

Fig2 = plt.subplot(3, 1, 2)
Fig2.scatter(X_phase, Colors['B-V'], color='red', s=6)
Fig2.plot(X_line, Y_line, color='grey')
plt.xlim([-0.1, 1.1])
plt.grid()

Fig3 = plt.subplot(3, 1, 3)
Fig3.plot(X_app, Y_app, color='black')
Fig3.plot(F_int, V_int, color='pink')
Fig3.scatter(XPhase_sort, YPhase_sort, color='red', s=6)
plt.xlim([-0.1, 1.1])
plt.grid()


plt.show()


