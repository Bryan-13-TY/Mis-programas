#fft14

import numpy as np
import scipy.fftpack as fourier
import pandas as pd
from openpyxl import Workbook
wb = Workbook
import matplotlib.pyplot as plt
from pathlib import Path

Ts = 0.01
Fs=1/Ts

s = Path(__file__).parent
e1 = s / "data00.xlsx"
e2 = s / "data01.csv"

x1 = pd.read_excel(e1,)
x2 = np.genfromtxt(e2,)
n = Ts*np.arange(0, len(x1)) # longitud de los datos
plt.subplot(2,1,1)
plt.plot(n,x1,'.-') # se gráfica con guines
plt.xlabel('Tiempo (s)', fontsize='14')
plt.ylabel('Amplitud', fontsize='14')
Ns = len(x2) # longitud de la señal para la transformada
L = Ns/2 # se gráfica la mitas de la gráfica
print(Fs)
print(len(x2))

gk = fourier.fft(x2) # se calcula la transformada rápida de fourier
M_gk = abs(gk)

F = Fs*np.arange(0, len(x2))/len(x2) # frecuencia
print(F)

plt.subplot(2,1,2)
plt.stem(F, M_gk)

plt.show()