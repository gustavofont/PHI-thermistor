import numpy as np
from scipy.io.wavfile import write

def main():
    beta = 3548
    R0 = 10000
    T0 = 25 + 273 # 25 Celsius to Kelvin

    tempo = np.arange(0, 100 * np.pi, 0.1)
    T = (np.sin(tempo) + 2) * 20 + 273
    V = R0 * np.exp(beta * (1 / T - 1 / T0))

    with open("waveform.txt", "w") as f:
        for point in zip(tempo, V):
            f.write('%f %f\n' % (point[0], point[1]))

main()