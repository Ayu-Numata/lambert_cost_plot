# -*- coding: utf-8 -*-
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import Lambert_base
import cost_calculation


mass_Payload = 5000.0    #ペイロード質量(固定値)[kg]
Launch_payload = 20000.0
r_sun_earth = 1.496 * (10 ** 8)    #km, sun-earth
r_sun_mars = 2.279 * (10 ** 8)    #km, sun-mars
Isp = 450    #[s]

def keisan(x, y):
    deltaV = Lambert_base.lambert(y, r_sun_earth, r_sun_mars, x)
    z = cost_calculation.cal_cost(mass_Payload, Launch_payload, deltaV, Isp)
    return z


#軸の描画範囲の生成
x_set = np.arange(0, 600, 2.0)    #地球と火星の初期相対角度
y_set = np.arange(100, 400, 1.0)    #航行日数
nx = len(x_set)
ny = len(y_set)
z_set = np.empty([nx, ny])

for i, xi in enumerate(x_set):
    for j, yi in enumerate(y_set):
        zi = keisan(xi, yi)
        z_set[i][j] = zi

X, Y = np.meshgrid(x_set, y_set)
Z = z_set

#出力する　pandas
df = pd.DataFrame([x_set, y_set, z_set])
df.to_csv("result.csv", header = False, index = False)

'''
#等高線図の生成
cont=plt.contour(X,Y,Z,  5, vmin = 5.0, vmax = 20.0, colors=['black'])
cont.clabel(fmt='%1.1f', fontsize=14)


plt.xlabel('X', fontsize=24)
plt.ylabel('Y', fontsize=24)


plt.pcolormesh(X,Y,Z, cmap='Spectral') #カラー等高線図
pp = plt.colorbar (orientation="vertical") # カラーバーの表示
pp.set_label("Label",  fontsize=24)

plt.show()
'''
