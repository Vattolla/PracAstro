import numpy as np
import math as mt
import Interpol as It

Stars_15 = [[18, 05.5], [2, 30], 4.02, 6.01, 'K0V', 'K5V', 88.3, 4.56]
#Stars_15 = [[18, 05.5], [2, 30], 4.20, 5.99, 'K0V', 'K4V', 88.13, 4.550]
Stars_18 = [[16, 41.3], [31, 36], 2.90, 5.53, 'G0IV', 'G7V', 34.49, 1.360]

Stars_00 = [[14, 39.6], [-60, -50], -0.04, 1.17, 'G2V', 'K0V', 79.92, 17.52]
M_sun = 1
a_e = 140e6

pi_priv_15 = 0
pi_15 = Stars_15[7] * ((Stars_15[6])**2 * (2*M_sun))**(-1/3)
print('70 Oph')
print(f'pi_2M = {round(pi_15, 4)}')
v = 0
while abs(pi_priv_15 - pi_15) > 0.001:
    Q_V = [[0, 5], [-0.19, -0.6]]
    QQ_1 = [[4.7, 2.7], [0, 0.2]]
    QQ_2 = [[6.6, 4.7], [-0.2, 0]]
    if v != 0:
        pi_15 = pi_priv_15
    M_abs_15 = np.array([Stars_15[i] + 5 + 5 * mt.log10(pi_15) for i in range(2, 4)])
    M_bol_15 = M_abs_15 + [It.Int2(Q_V, int(Stars_15[4][1])), It.Int2(Q_V, int(Stars_15[5][1]))]
    lg_MM_sun_15 = np.append((10 ** It.Int2(QQ_1, M_bol_15[0])), (10 ** It.Int2(QQ_2, M_bol_15[1])))
    pi_priv_15 = Stars_15[7] * ((Stars_15[6]) ** 2 * (lg_MM_sun_15.sum())) ** (-1 / 3)
    v += 1
print(f'M_v = {M_abs_15} \nM_bol = {M_bol_15}')
print(f'Массы звезд = {lg_MM_sun_15} \nОбщая масса = {round(lg_MM_sun_15.sum(), 3)} \npi = {round(pi_priv_15, 4)} \nv = {v} \n---------------')



print('-'*20)


pi_priv_18 = 0
pi_18 = Stars_18[7] * ((Stars_18[6])**2 * (2*M_sun))**(-1/3)
print('40 ζ Her')
print(f'pi_2M = {round(pi_18, 4)}')
v = 0
while abs(pi_priv_18 - pi_18) > 0.001:
    Q_V_1 = [[0, 5], [-0.03, -0.07]]
    Q_V_2 = [[5, 10], [-0.017, -0.19]]
    QQ_1 = [[4.7, 2.7], [0, 0.2]]
    QQ_2 = [[6.6, 4.7], [-0.2, 0]]
    if v != 0:
        pi_18 = pi_priv_18
    M_abs_18 = np.array([Stars_18[i] + 5 + 5 * mt.log10(pi_18) for i in range(2, 4)])
    M_bol_18 = M_abs_18 + [It.Int2(Q_V_1, int(Stars_18[4][1])), It.Int2(Q_V_2, int(Stars_18[5][1]))]
    lg_MM_sun_18 = np.append((10 ** It.Int2(QQ_1, M_bol_18[0])), (10 ** It.Int2(QQ_2, M_bol_18[1])))
    pi_priv_18 = Stars_18[7] * ((Stars_18[6]) ** 2 * (lg_MM_sun_18.sum())) ** (-1 / 3)
    v += 1
print(f'M_v = {M_abs_18} \nM_bol = {M_bol_18}')
print(f'Массы звезд = {lg_MM_sun_18} \nОбщая масса = {round(lg_MM_sun_18.sum(), 3)} \npi = {round(pi_priv_18, 4)} \nv = {v} \n---------------')