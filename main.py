import GetSetPos as gp
import read_obs_rinex as ror
import numpy as np
import math

def RotSatPos(sat: gp.GpsSat, obs):
    STT = obs/299_792_458
    ome_e = 7.2921151467e-5
    rota = ome_e * STT
    R_e = np.array([[math.cos(rota), math.sin(rota), 0], [-1 * math.sin(rota), math.cos(rota), 0], [0, 0, 1]])
    P_SatPos = np.array([sat.xk, sat.yk, sat.zk]).T
    SatPos = R_e @ P_SatPos
    sat.xk, sat.yk, sat.zk = SatPos[0], SatPos[1], SatPos[2]

APPROX_POSITION_XYZ = [-3062023.5630, 4055449.0330, 3841819.2130]
calc_time = [1, 45, 0] # hour, min, GPS_Week_day
tgpt = ror.tot_sat_pos # Total Gps Pos for time (dict)
keys = list(tgpt.keys())
# 15  2  1  0  0  0.0000000
time_dist = float("inf")
best_time = None
for i in keys:
    tmp_str = ""
    for num, j in enumerate(i):
        if j == " " and i[num+1] == " ":
            pass
        else:
            tmp_str += j

    time_list = tmp_str.split(" ")
    tmp_dist = (calc_time[0] - int(time_list[3]))*3600 + \
    (calc_time[1] - int(time_list[4]))*60 + 0 - float(time_list[5])
    # TODO 해당 시각의 정보를 포함하는지, 포함하지 않는지 알아야됨. 그래야 > 0인지 >= 0인지 알 수 있음
    if tmp_dist > 0 and time_dist > tmp_dist:
        time_dist = tmp_dist
        best_time = i

_15osat = tgpt[best_time]
obs_sats = list(_15osat.keys())
obs_gps_sats = []
for i in obs_sats:
    if i[0] == "G":
        obs_gps_sats.append(i)
    else:
        pass

tot_data = {} # 관측된 모든 GPS 위성이 들었는 dict 객체

for i in obs_gps_sats:
    if i[1] == "0":
        GpsSat_list = gp.read_data(i[2])
    else:
        GpsSat_list = gp.read_data(i[1:])
    bd_sat = gp.find_best_time(GpsSat_list, calc_time)
    bd_sat.calc_gps_pos(calc_time)
    tot_data[i] = bd_sat
gps_prn_list = list(tot_data.keys())

H = np.zeros((len(gps_prn_list), 4))
y = np.zeros(len(gps_prn_list))

for num, i in enumerate(gps_prn_list):

    CA_code = float(_15osat[i]["C1"][0].strip())
    RotSatPos(tot_data[i], CA_code)

    cal_x = tot_data[i].xk - APPROX_POSITION_XYZ[0]
    cal_y = tot_data[i].yk - APPROX_POSITION_XYZ[1]
    cal_z = tot_data[i].zk - APPROX_POSITION_XYZ[2]
    rho = math.sqrt(cal_x**2 + cal_y**2 + cal_z**2)

    y[num] = CA_code - rho
    H[num][0] = -1 * (cal_x)/rho
    H[num][1] = -1 * (cal_y)/rho
    H[num][2] = -1 * (cal_z)/rho
    H[num][3] = 299_792_458 # (m)

print("H array : ")
print(H)
print("y array : ")
print(y)