# -*- coding: utf-8 -*-
import math

GMs = 1.32712442099 * (10 ** 11)

#r_e = 6771.0      #[km]
#r_m = 4389.0      #[km]
#GMe = 3.986004418 * (10 ** 5)
#GMm = 4.28320000 * (10 ** 4)
#v_e = math.sqrt(GMe / r_e)
#v_m = math.sqrt(GMm / r_m)
#print(str(v_e) + ', vm = ' + str(v_m))



##################################

def vector_minus(a, b):
    c = [a[0] - b[0], a[1] - b[1]]
    return c


def function_c(z):
    if (z > 0):
        c = (1.0 - math.cos(math.sqrt(z))) / z
    elif (z < 0):
        c = (math.cosh(math.sqrt(z * (-1))) - 1.0) / (z * (-1))
    else:
        c = 1.0 / 2.0
    return c

def function_s(z):
    if (z > 0):
        s = (math.sqrt(z) - math.sin(math.sqrt(z))) / math.pow(math.sqrt(z), 3.0)
        #print(str(s))
    elif (z < 0):
        za = z * (-1)
        s = (math.sinh(math.sqrt(za)) - math.sqrt(za)) / math.pow(math.sqrt(za), 3.0)
        #print(str(s))
    else:
        s = 1.0 / 6.0
    return s

def function_y(z, A, r1, r2):
    y = r1 + r2 + A * (z * function_s(z) - 1.0) / math.sqrt(function_c(z))
    return y


def function_f(z, dt, A, r1, r2):
    fz = math.pow((function_y(z, A, r1, r2) / function_c(z)), 3.0/2.0) * function_s(z) + A * math.sqrt(function_y(z, A, r1, r2)) - dt * math.sqrt(GMs)
    return fz

def function_f_dif(z, A, r1, r2):
    yc = function_y(z, A, r1, r2) / function_c(z)
    sc = function_s(z) / function_c(z)
    if (z == 0):
        y0 = function_y(0, A, r1, r2)
        fz_dif = math.sqrt(2.0) * math.pow(y0, 3.0/2.0) / 40.0 + A * (math.sqrt(y0) + A * math.sqrt(1 / (2 * y0))) / 8.0
    else:
        fz_dif = math.pow(yc, 3.0/2.0) * ((function_c(z) - 3.0 * sc / 2.0) / (2.0 * z) + 3.0 * sc * function_s(z) / 4.0) + A * (3 * sc * math.sqrt(function_y(z, A, r1, r2)) + A / math.sqrt(yc)) / 8

    return fz_dif

'''Lambert問題計算する関数'''
def lambert(days, r1, r2, degree_f):
    sita =  degree_f + 360.0 * days / 687
    rad = math.radians(sita)         #始点と終点のなす角
    r1_x = r1
    r1_y = 0
    r2_x = r2 * math.cos(rad)
    r2_y = r2 * math.sin(rad)

    #velocity of the planetary orbit
    V_firstplanet = math.sqrt(GMs / r1)
    V_secondplanet = math.sqrt(GMs / r2)

    V_vector_firstplanet = [0, V_firstplanet]
    V_vector_secondplanet = [V_secondplanet * math.cos(rad + math.pi / 2), V_secondplanet * math.sin(rad + math.pi / 2)]

    A = math.sin(rad) * math.sqrt(r1 * r2 / (1.0 - math.cos(rad)))

    dt = days * 24 * 60 * 60.0        #[s], trans time

    dz = 1.0
    nz = 0.0
    success = True

    for i in range(100):
        z = 0 + i * 50
        while (dz > 0.0001):
            e = True
            try:
                z_new = z - function_f(z, dt, A, r1, r2) / function_f_dif(z, A, r1, r2)
            except OverflowError:
                e = False
                break
            except ZeroDivisionError:
                e = False
                break

            dz = z_new - z

            #print(str(z_new))

            if (dz < 0):
                dz = dz * (-1)
            z = z_new
            nz += 1
            if (nz > 30):
                break

        if (nz > 30):
            continue
        elif (e == True):
            break



    y = function_y(z, A, r1, r2)

    #lagrange functions
    f = 1.0 - y / r1
    g = A * math.sqrt(y / GMs)
    g_dif = 1.0 - y / r2

    v1_vector = [(r2_x - f * r1_x) / g, (r2_y - f * r1_y) / g]
    v2_vector = [(g_dif * r2_x - r1_x) / g, (g_dif * r2_y - r1_y) / g]
    r2_0_degree = math.degrees(rad) - 360.0 * days / 687.0


    #calculation of delta V
    deltaV_1a_vector = vector_minus(v1_vector, V_vector_firstplanet)
    deltaV_2a_vector = vector_minus(V_vector_secondplanet, v2_vector)

    deltaV_1a = math.sqrt(math.pow(deltaV_1a_vector[0], 2.0) + math.pow(deltaV_1a_vector[1], 2.0))
    deltaV_2a = math.sqrt(math.pow(deltaV_2a_vector[0], 2.0) + math.pow(deltaV_2a_vector[1], 2.0))

    deltaV = deltaV_1a + deltaV_2a
    #print(str(deltaV))

    if (z == 2500):
        deltaV = 40
    return deltaV

'''
print('deltaV_1a = ' + str(deltaV_1a) + ', deltaV_2a = ' + str(deltaV_2a))
'''
'''
deltaV1 = deltaV_1a - v_e
deltaV2 = deltaV_2a - v_m

if (deltaV1 < 0):
    deltaV1 = deltaV1 * (-1)

if (deltaV2 < 0):
    deltaV2 = deltaV2 * (-1)

deltaV = deltaV1 + deltaV2

print('v_e = ' + str(v_e) + ', v_m = ' + str(v_m))
print('deltaV = ' + str(deltaV))
'''
