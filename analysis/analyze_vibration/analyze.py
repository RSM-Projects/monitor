import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from pathlib import Path
import scipy.signal

def list_peaks(freq, amp, fs, n_samples, f_max=250, min_sep_hz=2.0,
               min_height=0.002, min_prominence=0.001):
    bin_spacing = fs / n_samples
    distance = max(1, int(min_sep_hz / bin_spacing))

    mask = freq <= f_max
    f = freq[mask]
    a = amp[mask]

    peaks, props = scipy.signal.find_peaks(
        a, height=min_height, prominence=min_prominence, distance=distance
    )
    return f[peaks], a[peaks]


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"

fan_off_01_path = DATA_DIR / "fan_off_02.csv"
fan_on_01_path = DATA_DIR / "fan_on_05.csv"

fan_off_01 = pd.read_csv(fan_off_01_path)
fan_on_01 = pd.read_csv(fan_on_01_path)

# Print dimensions (rows, columns)
print("Fan off 01 shape:", fan_off_01.shape)
print("Fan on 01 shape:", fan_on_01.shape)

# Display first five rows
print("\nFan off 01:")
print(fan_off_01.head())

print("\nFan on 01:")
print(fan_on_01.head())

off_intervals = fan_off_01["timestamp_us"].diff().dropna()
on_intervals = fan_on_01["timestamp_us"].diff().dropna()

# Print interval statistics
print("\nFan OFF sampling intervals (microseconds):")
print(off_intervals.describe())

print("\nFan ON sampling intervals (microseconds):")
print(on_intervals.describe())

# Estimate sampling rate using the mean interval
off_fs = 1_000_000 / off_intervals.mean()
on_fs = 1_000_000 / on_intervals.mean()

print(f"\nEstimated fan OFF sampling rate: {off_fs:.2f} Hz")
print(f"Estimated fan ON sampling rate: {on_fs:.2f} Hz")

print(on_intervals.head())


# Convert timestamps from microseconds to seconds
off_time = (
                   fan_off_01["timestamp_us"] - fan_off_01["timestamp_us"].iloc[0]
           ) / 1_000_000

on_time = (
                  fan_on_01["timestamp_us"] - fan_on_01["timestamp_us"].iloc[0]
          ) / 1_000_000

fan_off_01["accel_x_g"] = fan_off_01["raw_x"] / 16384
fan_on_01["accel_x_g"] = fan_on_01["raw_x"] / 16384

fan_off_01["accel_y_g"] = fan_off_01["raw_y"] / 16384
fan_on_01["accel_y_g"] = fan_on_01["raw_y"] / 16384

fan_off_01["accel_z_g"] = fan_off_01["raw_z"] / 16384
fan_on_01["accel_z_g"] = fan_on_01["raw_z"] / 16384

off_mask = (off_time >=0)
on_mask = (on_time >= 0)

off_x = fan_off_01.loc[off_mask, "accel_x_g"]
on_x = fan_on_01.loc[on_mask, "accel_x_g"]

off_vibration = off_x - off_x.mean()
on_vibration = on_x - on_x.mean()

off_std = off_vibration.std()
on_std = on_vibration.std()

off_rms = np.sqrt(np.mean(off_vibration**2))
on_rms = np.sqrt(np.mean(on_vibration**2))


off_y = fan_off_01.loc[off_mask, "accel_y_g"]
on_y = fan_on_01.loc[on_mask, "accel_y_g"]

off_vibration_y = off_y - off_y.mean()
on_vibration_y = on_y - on_y.mean()

off_std_y = off_vibration_y.std()
on_std_y = on_vibration_y.std()

off_rms_y = np.sqrt(np.mean(off_vibration_y**2))
on_rms_y = np.sqrt(np.mean(on_vibration_y**2))


off_z = fan_off_01.loc[off_mask, "accel_z_g"]
on_z = fan_on_01.loc[on_mask, "accel_z_g"]

off_vibration_z = off_z - off_z.mean()
on_vibration_z = on_z - on_z.mean()

off_std_z = off_vibration_z.std()
on_std_z = on_vibration_z.std()

off_rms_z = np.sqrt(np.mean(off_vibration_z**2))
on_rms_z = np.sqrt(np.mean(on_vibration_z**2))





print(f"Fan OFF standard deviation x-axis: {off_std:.6f} g")
print(f"Fan ON standard deviation x-axis:  {on_std:.6f} g")

print(f"Fan OFF vibration RMS x-axis: {off_rms:.6f} g")
print(f"Fan ON vibration RMS x-axis:  {on_rms:.6f} g")

print(f"Fan OFF standard deviation y-axis: {off_std_y:.6f} g")
print(f"Fan ON standard deviation y-axis:  {on_std_y:.6f} g")

print(f"Fan OFF vibration RMS y-axis: {off_rms_y:.6f} g")
print(f"Fan ON vibration RMS y-axis:  {on_rms_y:.6f} g")

print(f"Fan OFF standard deviation z-axis: {off_std_z:.6f} g")
print(f"Fan ON standard deviation z-axis:  {on_std_z:.6f} g")

print(f"Fan OFF vibration RMS z-axis: {off_rms_z:.6f} g")
print(f"Fan ON vibration RMS z-axis:  {on_rms_z:.6f} g")


#fft
off_signal = off_vibration.to_numpy()
window = np.hanning(len(off_signal))
han_signal = off_signal * window
fft_off_x = np.fft.rfft(han_signal)
amp_off = (2* fft_off_x) / window.sum()
amp_off_mag = abs(amp_off)

fs_off = 1_000_000 / off_intervals.mean()      # measured sampling rate in Hz
freq_off = np.fft.rfftfreq(len(off_signal), d=1/fs_off)

on_signal = on_vibration.to_numpy()
window_on = np.hanning(len(on_signal))
han_signal_on = on_signal * window_on
fft_on_x = np.fft.rfft(han_signal_on)
amp_on = (2* fft_on_x) / window_on.sum()
amp_on_mag = abs(amp_on)

fs_on = 1_000_000 / on_intervals.mean()
freq_on = np.fft.rfftfreq(len(on_signal), d=1/fs_on)

on_f, on_a = list_peaks(freq_on, amp_on_mag, fs_on, len(on_signal))
print(f"Fan ON resolution: {fs_on / len(on_signal):.3f} Hz")
for f, a in zip(on_f, on_a):
    print(f"{f:7.2f} Hz   {a:.4f} g")

off_f, off_a = list_peaks(freq_off, amp_off_mag, fs_off, len(off_signal))
print(f"\nFan OFF: {len(off_f)} peaks found")
for f, a in zip(off_f, off_a):
    print(f"{f:7.2f} Hz   {a:.4f} g")

#test
fs = 1000
duration = 13
N = int(fs * duration)
t= np.arange(N) / fs
signal = 1.0 * np.sin(2 * np.pi * 40 * t)
han_window = np.hanning(N)
signal_han = signal * han_window
fft_test = np.fft.rfft(signal_han)
test_amp = (fft_test *2) / han_window.sum()
test_amp_mag = abs(test_amp)

freq_test = np.fft.rfftfreq(len(signal),d = 1/fs)

peak_index = np.argmax(test_amp_mag)
print(freq_test[peak_index], test_amp_mag[peak_index])

plt.figure()
plt.plot(freq_test, test_amp_mag, label="test")
plt.show()









plt.figure(figsize=(10, 5))

plt.plot(freq_off, amp_off_mag, label="Fan OFF")
plt.plot(freq_on, amp_on_mag, label="Fan ON")

plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (g)")
plt.title("Fan Vibration Frequency Spectrum — X-axis")
plt.xlim(0, 200)

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()







t_mask_off = (off_time > 0.2) & (off_time < 0.3)
fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True, sharey=True)

axes[0].plot(off_time[t_mask_off].to_numpy(), off_vibration[t_mask_off].to_numpy())
axes[0].set_title("Fan OFF - X-axis vibration (mean removed)")
axes[0].set_ylabel("acceleration (g)")
axes[0].grid(True)

t_mask_on = (on_time > 0.2) & (on_time < 0.3)

axes[1].plot(on_time[t_mask_on].to_numpy(), on_vibration[t_mask_on].to_numpy())
axes[1].set_title("Fan ON - X-axis vibration (mean removed)")
axes[1].set_ylabel("acceleration (g)")
axes[1].grid(True)




plt.tight_layout()
plt.show()





