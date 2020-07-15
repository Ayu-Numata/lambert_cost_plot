# -*- coding: utf-8 -*-
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

'''pandasに直す
with open('./result.csv') as f:
    reader = csv.reader(f)
    print(f.read())

'''
df = pd.read_csv("result.csv",index_col = 0)
print(df)

x_set = df.columns
y_set = df.index

xs=[]
ys=[]
for x in x_set:
    xs+=[x]

for y in y_set:
    ys+=[y]
print(type(xs))
print(xs)




#x_set, y_set, z_set = np.loadtxt("./result.csv", comments = "", unpack = True)

X, Y = np.meshgrid(xs, ys)

X_=X.tolist()
Y_=Y.tolist()
Z = df.values.tolist()


#等高線図の生成

cont = plt.contour(X_,Y_,Z,  5, vmin = 5.0, vmax = 20.0, colors=['black'])
cont.clabel(fmt='%1.1f', fontsize=14)


plt.xlabel('X', fontsize=24)
plt.ylabel('Y', fontsize=24)


plt.pcolormesh(X,Y,Z, cmap='Spectral') #カラー等高線図
pp = plt.colorbar (orientation="vertical") # カラーバーの表示
pp.set_label("Label",  fontsize=24)

plt.show()
