# -*- coding: utf-8 -*-
import numpy as np

# ref. 1976 standard atmosphere
# ジオポテンシャル高度を基準として標準大気の各層の気温減率から各大気値を算出
# 高度86 kmまで対応
def std_atmo(altitude):
  # altitude [m]
  R = 287.1
  gamma = 1.4
  Re = 6378.137e3 # Earth Radius [m]
  g0 = 9.80665

  # atmospheric layer
  h_list  = [0.0, 11.0e3, 20.0e3, 32.0e3, 47.0e3, 51.0e3, 71.0e3, 84.852e3] # geopotential height [m]
  TG_list = [-6.5e-3, 0.0, 1.0e-3, 2.8e-3, 0, -2.8e-3, -2.0e-3, 0.0] # Temp. gradient [K/m]
  T_list  = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65, 186.946] # [K]
  P_list  = [101325.0, 22632.0, 5474.9, 868.02, 110.91, 66.939, 3.9564, 0.3734] # [Pa]

  h = altitude * Re / (Re + altitude) # geometric altitude => geopotential height

  k = 0 # dafault layer
  for i in range(8):
    if h < h_list[i]:
      k = i - 1
      break
    elif h >= h_list[7]:
      k = 7
      break
  
  Temperature = T_list[k] + TG_list[k] * (h - h_list[k]) # [K]
  if TG_list[k] == 0.0:
    Pressure = P_list[k] * np.exp(g0 / R * (h_list[k] - h) / T_list[k])
  else:
    Pressure = P_list[k] * np.power(T_list[k] / Temperature, g0 / R / TG_list[k]) # [Pa]
  Density = Pressure / (R * Temperature) # [kg/m^3]
  SoundSpeed = np.sqrt(gamma * R * Temperature) # [m/s]
  
  return Temperature, Density, SoundSpeed

def gravity(altitude):
  # altitude [m]
  Re = 6378.137e3 # Earth Radius [m]
  g0 = 9.80665
  gravity = g0 * (Re / (Re + altitude)) ** 2 # [m/s^2]
  return gravity

if __name__ == '__main__':
  import matplotlib.pyplot as plt
  altitude = np.empty(0)
  dencity = np.empty(0)
  for alt in range(-1000, 87000, 100):
    T, rho = std_atmo(alt)
    g = gravity(100000.0)
    print (T, rho, g)
    altitude = np.append(altitude,alt)
    dencity = np.append(dencity, rho)

  plt.figure(0)
  plt.plot(altitude, dencity)
  plt.show()