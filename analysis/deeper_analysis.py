import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, periodogram, spectrogram
from scipy.stats import linregress, skew, kurtosis

# -----------------------------
# User settings
# -----------------------------
data = np.loadtxt('data.csv', delimiter=',')
timestamps = data[:,0] / 1000.0  # convert ms → s
signal = data[:,1]

# Calculate sampling frequency from timestamps
fs = 1 / np.mean(np.diff(timestamps))

# -----------------------------
# 1. Compare PSD Estimation Methods
# -----------------------------
f_welch, Pxx_welch = welch(signal, fs, nperseg=8192)
f_period, Pxx_period = periodogram(signal, fs)

plt.figure(figsize=(8,5))
plt.loglog(f_welch, Pxx_welch, label='Welch')
plt.loglog(f_period, Pxx_period, label='Periodogram')
plt.xlabel('Frequency [Hz]')
plt.ylabel('PSD')
plt.title('PSD Comparison')
plt.legend()
plt.grid(True, which='both', ls='--', lw=0.5)
plt.show()

# -----------------------------
# 2. Time-Varying Spectra (Spectrogram)
# -----------------------------
f_spec, t_spec, Sxx = spectrogram(signal, fs=fs, nperseg=1024)
plt.figure(figsize=(8,5))
plt.pcolormesh(t_spec, f_spec, 10*np.log10(Sxx+1e-20), shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [s]')
plt.title('Spectrogram of Light Sensor Signal')
plt.colorbar(label='PSD [dB]')
plt.show()

# -----------------------------
# 3. Slope Estimation of 1/f Noise
# -----------------------------
f_max = 1  # Hz, upper cutoff
mask = (f_welch > 0) & (f_welch <= f_max)
log_f = np.log10(f_welch[mask])
log_P = np.log10(Pxx_welch[mask])

slope, intercept, r_value, p_value, std_err = linregress(log_f, log_P)
print(f"Estimated alpha (1/f slope): {-slope:.2f}")

plt.figure(figsize=(8,5))
plt.loglog(f_welch, Pxx_welch, label='Welch PSD')
plt.loglog(f_welch[mask], 10**(intercept + slope*log_f), 'r--', label=f'Fit slope: {-slope:.2f}')
plt.xlabel('Frequency [Hz]')
plt.ylabel('PSD')
plt.title('1/f Noise Slope Estimation')
plt.legend()
plt.grid(True, which='both', ls='--', lw=0.5)
plt.show()

# -----------------------------
# 4. Noise Statistics
# -----------------------------
mean_val = np.mean(signal)
var_val = np.var(signal)
skew_val = skew(signal)
kurt_val = kurtosis(signal)

print("Noise Statistics:")
print(f"Mean: {mean_val:.3f}")
print(f"Variance: {var_val:.3f}")
print(f"Skewness: {skew_val:.3f}")
print(f"Kurtosis: {kurt_val:.3f}")

# -----------------------------
# 5. Sampling Rate Sensitivity
# -----------------------------
downsample_factor = 10
signal_down = signal[::downsample_factor]
fs_down = fs / downsample_factor

f_ds, Pxx_ds = welch(signal_down, fs=fs_down, nperseg=1024)

plt.figure(figsize=(8,5))
plt.loglog(f_welch, Pxx_welch, label='Original 10Hz')
plt.loglog(f_ds, Pxx_ds, label=f'Downsampled {fs_down}Hz')
plt.xlabel('Frequency [Hz]')
plt.ylabel('PSD')
plt.title('Effect of Downsampling on PSD')
plt.legend()
plt.grid(True, which='both', ls='--', lw=0.5)
plt.show()
