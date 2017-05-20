# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 18:42:34 2017

Автор: Р.В. Шамин
"""

import math

import random

# имя файла
name = "t.txt"

# Загрузка исходных данных из файла
X = list()
XS = list() # символьные значения
f = open(name, "r")

for s in f:
    s = s.strip()
    SS = s.split("\t")
    X.append(SS)
    XS.append(s)
    
f.close()

# массивы для хранения коэффициентов для нормировки
As = list()
Bs = list()

# нормировка исходных данных
for i in range(len(X[0])):
    M = float(X[0][i])
    m = float(X[0][i])
    for j in range(len(X)):
        #print("<" + X[j][i].__str__() + ">")
        X[j][i] = float(X[j][i])
        
        if abs(X[j][i]) > M:
            M = abs(X[j][i])
        else:
            if abs(X[j][i]) < m:
                m = abs(X[j][i])
# коэффициенты нормирования
    a = 1 / (M - m)
    b = -m / (M - m)
# сохранить коэффициенты    
    As.append(a)
    Bs.append(b)
# нормировать    
    for j in range(len(X)):
        X[j][i] = a * X[j][i] + b

# создать массив для весов
W = list()

K = 2 # количество классов

M = len(X) # количество исходных данных

N = len(X[0]) # размерность векторов

# получить случайное значение для инициализирования весов       
def get_w():
    z = random.random() * (2.0 / math.sqrt(M))
    return 0.5 - (1 / math.sqrt(M)) + z
    
# инициализировать веса
for i in range(K):
    W.append(list())
    for j in range(N):
        W[i].append(get_w() * 0.5)

la = 0.3 # коэффициент обучения
dla = 0.05 # уменьшение коэффициента обучения

# расстояние между векторами
def rho(w, x):
    r = 0
    for i in range(len(w)):
        r = r + (w[i] - x[i])*(w[i] - x[i])
    
    r = math.sqrt(r)
    return r

# поиск ближайшего вектора 
def FindNear(W, x):
    wm = W[0]
    r = rho(wm, x)
    
    i = 0
    i_n = i
    
    for w in W:
        if rho(w, x) < r:
            r = rho(w, x)
            wm = w
            i_n = i
        i = i + 1
    
    return (wm, i_n)

# начать процесс обучения
while la >= 0:
    for k in range(10): #  повторять 10 раз обучение
        for x in X:
            wm = FindNear(W, x)[0]
            for i in range(len(wm)):
                wm[i] = wm[i] + la * (x[i] - wm[i]) # корректировка весов

    la = la - dla # уменьшение коэффициента обучения

# массив для денормированных весов
WX = list() 
    
# денормировать веса
for i in range(K):
    WX.append(list())
    for j in range(N):
        WX[i].append((W[i][j] - Bs[j]) / As[j])
    
print(WX) # печать денормированных весов

# печать первых компонент весов
for wx in WX:
    print(wx[0])

# создать классы     
Data = list() 

for i in range(len(W)):
    Data.append(list())

# отнести исходные данные к своему классу    
DS = list()
i = 0
for x in X:
    i_n = FindNear(W, x)[1]
    Data[i_n].append(x)
    DS.append([i_n, XS[i]])
    i = i + 1

# напечатать количество элементов в классах
i = 0
class_n = list()
for d in Data:
    print("Класс "+i.__str__()+" состоит из "+len(d).__str__()+" элементов")
    class_n.append(len(d))
    i = i + 1

class_n.sort()
print(class_n)

# распечатать по классам
f = list()
for i in range(K):
    f.append(open(i.__str__() + name, "w"))
for ds in DS:
    f[ds[0]].write(ds[1])
    f[ds[0]].write("\n")
for i in range(K):
    f[i].close()

    
    
    
    
    
    
    
    
    
    
    
    