import math

g = 9.80665

###thrust of the LOX/LH2 engine
Ttotrk = 74058.296 * 0.224  #[N]*0.224=[Ibf]

###mass of the vehicle engine
Mengine_che = (0.00766 * Ttotrk + 0.00033 * Ttotrk * pow(100, 0.5) + 130) * 0.45359237 #[Ib]*0.45359237=[kg]

### the function for mass of fuel tank
def massTank(Mprop):        #LOX/LH2
    pH2 = 70.8   #[kg/m^3]
    pO2 = 1140 #[kg/m^3]
    pth = 1.75  #[lb/ft^3]
    pto = 1.25  #[lb/ft^3]

    massH2 = Mprop / 6.5            #[kg]
    massO2 = Mprop * 5.5 / 6.5      #[kg]

    volumeH2 = massH2 * math.pow(3.2808, 3) / pH2  #[ft^3]
    volumeO2 = massO2 * math.pow(3.2808, 3) / pO2  #[ft^3]

    #print(str(volumeH2))
    tankmass_H2 = (0.4856 * volumeH2 + 800.0 + 0.58 * math.pow(volumeH2, 2/3) * 5.616) / 2.2046    #[kg]
    tankmass_O2 = (1.085 * volumeO2 + 700.0 + 0.23 * math.pow(volumeO2, 2/3) * 5.616) / 2.2046    #[kg]

    tankmass = tankmass_H2 + tankmass_O2

    return tankmass
'''
def massTank_methan(Mprop):
    pCH4 = 415 #[kg/m^3]
    pO2 = 1140 #[kg/m^3]

    massCH4 = Mprop / 4
    massO2 = Mprop * 3 / 4

    volumeCH4 = massCH4 * math.pow(3.2808, 3) / pCH4
    volumeO2 = massO2 * math.pow(3.2808, 3) / pO2  #[ft^3]

    tankmass_CH4 = (0.4856 * volumeCH4 + 800) / 2.2046 #[kg]
    tankmass_O2 = (1.085 * volumeO2 + 700 + 0.23 * math.pow(volumeO2, 2/3) * 5.616) / 2.2046 #[kg]

    tankmass = tankmass_CH4 + tankmass_O2
    return tankmass
'''

def massProp_a(massPay, massStructure, Isp):
    massProp = (massStructure + massPay) * (math.exp(dV * 1000/Isp/g)-1)
    return massProp

def f_chemical(Mprop, Mpay, Isp, dV):
    Mt = massTank(Mprop)
    #print('deltaV = ' + str(dV))
    #Mt = massTank_methan(Mprop)
    M_total = Mprop / (1 - math.exp((-1) * dV * 1000 / (Isp * g)))
    f = M_total - (Mprop + Mpay + Mengine_che + Mt)
    return f


def f_chemical2(Mprop, Mpay, Isp):
    Mt = massTank(Mprop)
    #Mt = massTank_methan(Mprop)
    Mstr = Mt + Mengine_che
    Mprop2 = massProp_a(0, Mstr, Isp)
    M_total = (Mprop - Mprop2) / (1 - math.exp((-1) * dV * 1000 / (Isp * g)))
    f = M_total - (Mprop + Mpay + Mengine_che + Mt)
    return f

def g_chemical(x_0, x_1, massPay, Isp, deltaV):
    g = (f_chemical(x_0, massPay, Isp, deltaV) - f_chemical(x_1, massPay, Isp, deltaV)) / (x_0 - x_1)
    return g

def g_chemical2(x_0, x_1, massPay, Isp):
    g = (f_chemical2(x_0, massPay, Isp) - f_chemical2(x_1, massPay, Isp)) / (x_0 - x_1)
    return g



def massProp(x0, x1, massPay, Isp, deltaV):
    dx = x0 - x1
    if (dx < 0):
        dx = dx * (-1)
    x_new = 1

    while(dx > 0.00001):
        #print(str(g_chemical(x0, x1, massPay, Isp, deltaV)))
        x_new = x1 - f_chemical(x1, massPay, Isp, deltaV) / g_chemical(x0, x1, massPay, Isp, deltaV)

        dx = x_new - x1
        if (dx < 0):
            dx = dx * (-1)

        x0 = x1
        x1 = x_new
        #print('massProp = '+ str(x_new))

        if (x_new < 0):
            x_new = 100000
            return x_new
            break

    return x_new
