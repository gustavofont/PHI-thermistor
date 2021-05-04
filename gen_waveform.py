import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

def plot(x, y):
    plt.plot(x, y)

    plt.xlabel("time (s)")
    plt.ylabel("T")
    plt.grid()
    plt.tight_layout()

    plt.show()


def main():
    beta = 3548
    R0 = 10000
    T0 = 25 + 273 # 25 Celsius to Kelvin
    K = 2 * 1e-3 # 2mW/°C
    I = 500e-6 # 500 uA

    # Get NTC resistence when temperature is T
    def R_of_T(T):
        return R0 * np.exp(beta * (1 / T - 1 / T0))

    # Get temperature when resistance is R
    def T_of_R(R):
        return beta / np.log(R / (R0 * np.exp(-beta/T0)))


    t = np.arange(0, 100 * np.pi, 0.1)
    
    T_ambiente = (np.sin(t) + 1) * 50 + 273 # Kelvin
    T_ntc = R_of_T(T_ambiente) * I * I / K + T_ambiente # Kelvin

    # Ambient temperature voltage
    VTEMP = I * R_of_T(T_ambiente) 

    # Self-heating temperature voltage (noise)
    VNOISE = I * R_of_T(T_ntc) - I * R_of_T(T_ambiente) # NTC -> greater T -> lower R -> lower V = I * R

    V = VTEMP + VNOISE

    V1_ntc = np.min(V)
    V2_ntc = np.max(V)

    # Range de tensão do conversor AD
    V1_ad = 0
    V2_ad = 1

    G = (V2_ad - V1_ad) / (V2_ntc - V1_ntc)
    DC = V1_ad - V1_ntc * G

    print("AC = %f" % (G * 1000))
    print("DC = %f" % DC)

    #plot(t, T_ambiente - 273)
    #plot(t, T_ntc - 273)
    #plot(t, T_ntc - T_ambiente)

    with open("VTEMP_waveform.txt", "w") as f:
        for point in zip(t, VTEMP):
            f.write('%f %f\n' % (point[0], point[1]))

    with open("VNOISE_waveform.txt", "w") as f:
        for point in zip(t, VNOISE):
            f.write('%f %f\n' % (point[0], point[1]))

main()