import matplotlib.pyplot as plt
import math as mt
import pandas as pd

def Int2( up_element, down_element, Need_to_interpol):
    a = (Need_to_interpol[3] - up_element[3]) / (down_element[3] - up_element[3])
    Interpol_element = round(up_element[1] + a * (down_element[1] - up_element[1]), 2)
    return Interpol_element


def Priv(deg, min, sec):
    Time_priv = deg + (min + sec/60)/60
    return  Time_priv

def Privedenie_time_in_deg(hour, min, sec):
    Time_priv = int(hour) + (int(min) + int(sec)/60)/60
    Time_priv_deg = Time_priv/24*360
    return Time_priv_deg

def Privedenie_time(hour, min, sec):
    Time_priv = int(hour) + (int(min) + int(sec)/60)/60
    return Time_priv

def Obratnoe_time(Time):
    min = (Time - int(Time))*60
    sec = round((min - int(min))*60, 0)
    if sec >= 60:
        min = min + 1
        sec = sec - 60
    Time_Obr = f'[{int(Time)}:{round(min, 1)}],'

    return Time_Obr

Tabler = pd.read_table('gg1.txt', engine='python',  sep='    ')
print(Tabler)
print('-'*20)
V_filter = []
Time = []
Tabler_object_V = 0
Tabler_object_Time = 0
v = 0
check = 0
Prived_Tabler = []
for j in range(63):
    V_filter.append(int(Tabler['V'][j]))
    Time_not_found = Tabler['Time'][j].split(':')
    Time_found = Privedenie_time(Time_not_found[0], Time_not_found[1], Time_not_found[2])
    Time.append(Time_found)
for i in range(0, 62):
    if Tabler['Object'][i] == Tabler['Object'][i+1]:
        Tabler_object_V += int(Tabler['V'][i])
        Tabler_object_Time += Time[i]
        v += 1
    else:
        Tabler_object_V += int(Tabler['V'][i])
        Tabler_object_Time += Time[i]
        v += 1
        Tabler_object_V = round(Tabler_object_V/v, 0)
        Tabler_object_Time = round(Tabler_object_Time/v, 8)
        Tabler_object_Time_return = Obratnoe_time(Tabler_object_Time)
        print(Tabler['Object'][i], Tabler_object_V, Tabler_object_Time_return, Tabler_object_Time)
        Prived_Tabler.append([Tabler['Object'][i], Tabler_object_V, Tabler_object_Time_return, Tabler_object_Time])
        Tabler_object_V = 0
        Tabler_object_Time = 0
        v = 0
        check +=1
Tabler_object_V += int(Tabler['V'][62])
Tabler_object_Time += Time[62]
v += 1
Tabler_object_V = round(Tabler_object_V/v, 0)
Tabler_object_Time = round(Tabler_object_Time/v, 8)
Tabler_object_Time_return = Obratnoe_time(Tabler_object_Time)
print(Tabler['Object'][62], Tabler_object_V, Tabler_object_Time_return, Tabler_object_Time)
Prived_Tabler.append([Tabler['Object'][62], Tabler_object_V, Tabler_object_Time_return, Tabler_object_Time])
Tabler_object_V = 0
Tabler_object_Time = 0
v = 0
check +=1
print(len(Time), len(V_filter), check)
print('-'*20)

k = 1.002738
S_0 = 1.0932432778
lamda_h = 2.7633333334
lamda_deg = 41.45
a = 18.815
b = 0.6
f = 43.8166666667

N_v_tabler = []
M_tabler = []
m_v_tabler = []
t_tabler = []

#for i in range(1, len(Prived_Tabler)-2, 2):
#    Interpol_comp = Int2(Prived_Tabler[i], Prived_Tabler[i+2], Prived_Tabler[i+1])
#    N_v = round((Prived_Tabler[i+1][1] - Interpol_comp)/10, 1)
#    N_v_tabler.append(N_v)
#    m = Prived_Tabler[i+1][3] - 3 - 1 + lamda_h
#    S = S_0 + m * k
#    t = S - a
#    t_deg = t / 24 * 360
#    M = 1 / (mt.sin(mt.radians(f)) * mt.sin(mt.radians(b)) + mt.cos(mt.radians(f)) * mt.cos(mt.radians(b)) * mt.cos(mt.radians(t_deg)))
#    m_v = -2.5 * mt.log10(N_v)
#    M_tabler.append(M)
#    m_v_tabler.append(m_v)
#    t_tabler.append(t)
#    print(M, m_v)
#print('-'*20)
Time_priv = []
for i in range(len(Prived_Tabler)-2):
    if Prived_Tabler[i][0] == 'fon':
        Interpol_comp = Int2(Prived_Tabler[i], Prived_Tabler[i+2], Prived_Tabler[i+1])
        N_v = round((Prived_Tabler[i+1][1] - Interpol_comp)/10, 1)
        N_v_tabler.append(N_v)
        m = Prived_Tabler[i+1][3] - 3 - 1 + lamda_h
        S = S_0 + m * k
        t = S - a
        t_deg = t / 24 * 360
        M = 1 / (mt.sin(mt.radians(f)) * mt.sin(mt.radians(b)) + mt.cos(mt.radians(f)) * mt.cos(mt.radians(b)) * mt.cos(mt.radians(t_deg)))
        m_v = -2.5 * mt.log10(N_v)
        M_tabler.append(M)
        m_v_tabler.append(m_v)
        t_tabler.append(t)
        Time_priv.append(Prived_Tabler[i+1][3])
        #print(Prived_Tabler[i+1][2], Obratnoe_time(m), Obratnoe_time(S), Obratnoe_time(t), M, m_v)
        print( M, m_v)
print('-'*20)


a_tabler = []
time_tabler = []
for i in range(len(M_tabler)):
    if i+1 != len(m_v_tabler):
        a = (m_v_tabler[i] - m_v_tabler[i+1])/(M_tabler[i] - M_tabler[i+1])
        time_i = (Time_priv[i] + Time_priv[i+1])/2
        time_tabler.append(time_i)
        a_tabler.append(a)
        print(time_i, a)

print(len(a_tabler), len(time_tabler))
graf = plt.subplot(2,1,1)
graf.plot(M_tabler, m_v_tabler, '.')
graf.invert_yaxis()
plt.xlabel('Воздушная масса, M')
plt.ylabel('Блеск звезды,m')
plt.grid(True)

graf_a = plt.subplot(2,1,2)
graf_a.plot(time_tabler, a_tabler, '.', color='red')
plt.xlabel('Время Т')
plt.ylabel('Бугеровский коэффициент экстинкции, a')
plt.grid(True)

plt.show()

