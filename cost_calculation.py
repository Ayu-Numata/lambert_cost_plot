#片道分のみ計算したい

import math
import vehicle_sizing


g = 9.80665

single_vehicle_costbase = 1.0
operation_cost_base = 0.1    #燃料コスト
launch_cost_base = 1.0    #Launch_payload1回打ち上げる時のコスト

#サイズ基準値:ペイロード5t, 月まで(だいたい)
massTotal_base = 19010.0
massStr_base = 1130.0
massProp_base = 9880.0

Ttotrk = 74058.296 * 0.224  #[N]*0.224=[Ibf]
Mengine_che = (0.00766 * Ttotrk + 0.00033 * Ttotrk * pow(100, 0.5) + 130) * 0.45359237 #[Ib]*0.45359237=[kg]

#1機あたりのpayloadの値は指定しない
def cal_cost(mass_Payload, Launch_payload, deltaV, Isp):
    neuton0 = deltaV * 10000
    neuton1 = deltaV * 10100
    #通常のサイジング:1機ずつ
    massPropellant = vehicle_sizing.massProp(neuton0, neuton1, mass_Payload, Isp, deltaV)
    massTotal = massPropellant / (1 - math.exp((-1) * deltaV * 1000 / (Isp * g)))
    massStr = massTotal - massPropellant - mass_Payload
    over = False

    if (massPropellant == 100000):
        over = True
        Totalcost = -1
    else:
        vehicle_cost = math.pow((massStr * single_vehicle_costbase / massStr_base), 0.46)
        operationCost =(massPropellant / massProp_base) * operation_cost_base
        Launchcost = (massTotal / Launch_payload) * launch_cost_base

        Totalcost = vehicle_cost + operationCost + Launchcost
    print(Totalcost)
    return Totalcost
