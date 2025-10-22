import numpy as np
from scipy.signal import welch
import matplotlib.pyplot as plt

data = np.loadtxt('data.csv', delimiter=',')
timestamps = data[:,0] / 1000.0  # convert ms → s
sensor = data[:,1]

# Calculate sampling frequency from timestamps
fs = 1 / np.mean(np.diff(timestamps))

f, Pxx = welch(sensor, fs, nperseg=8192)

plt.loglog(f, Pxx)
plt.xlabel('Frequency [Hz]')
plt.ylabel('PSD')
plt.title('LDR Noise (1/f)')
plt.grid(True)
plt.show()

plt.plot(timestamps, sensor)
plt.xlabel('Time [ms]')
plt.ylabel('ADC Readings')
plt.title('Photoresistor Voltage vs. Time')
plt.grid(True)
plt.show()