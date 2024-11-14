import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import butter, filtfilt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Hàm tạo tín hiệu sin
def generate_sine_wave(freq, duration, amplitude=1.0, phase=0, sampling_rate=1000):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    signal = amplitude * np.sin(2 * np.pi * freq * t + phase)
    return t, signal


# Phép biến đổi Fourier nhanh
def compute_fft(signal, sampling_rate):
    N = len(signal)
    yf = fft(signal)
    xf = fftfreq(N, 1 / sampling_rate)[:N // 2]
    return xf, 2.0 / N * np.abs(yf[0:N // 2])


# Thiết kế bộ lọc thông thấp
def low_pass_filter(signal, cutoff, sampling_rate, order=5):
    nyquist = 0.5 * sampling_rate
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal


# Cập nhật và hiển thị tín hiệu gốc
def update_signal():
    try:
        freq = float(entry_freq.get())
        amplitude = float(entry_amplitude.get())
        t, signal = generate_sine_wave(freq, 1, amplitude)

        ax.clear()
        ax.plot(t, signal, label="Tín hiệu gốc")
        ax.set_title(f"Tín hiệu sin với tần số {freq} Hz")
        ax.set_xlabel("Thời gian (s)")
        ax.set_ylabel("Biên độ")
        ax.legend()

        canvas.draw()
        global current_signal
        current_signal = signal  # Lưu tín hiệu để sử dụng cho các chức năng khác
    except ValueError:
        print("Vui lòng nhập giá trị hợp lệ cho tần số và biên độ.")


# Hiển thị phổ Fourier của tín hiệu hiện tại
def show_fft():
    try:
        xf, yf = compute_fft(current_signal, 1000)
        ax_fft.clear()
        ax_fft.plot(xf, yf, label="Phổ Fourier")
        ax_fft.set_title("Phổ Fourier của tín hiệu")
        ax_fft.set_xlabel("Tần số (Hz)")
        ax_fft.set_ylabel("Biên độ")
        ax_fft.legend()

        canvas.draw()
    except Exception as e:
        print("Vui lòng vẽ tín hiệu trước khi thực hiện FFT.")


# Lọc tín hiệu và hiển thị kết quả
def filter_signal():
    try:
        cutoff = float(entry_cutoff.get())
        filtered_signal = low_pass_filter(current_signal, cutoff, 1000)

        ax.clear()
        ax.plot(np.linspace(0, 1, len(current_signal)), current_signal, label="Tín hiệu gốc")
        ax.plot(np.linspace(0, 1, len(filtered_signal)), filtered_signal, linestyle='--', label="Tín hiệu sau lọc")
        ax.set_title("Tín hiệu trước và sau khi lọc")
        ax.set_xlabel("Thời gian (s)")
        ax.set_ylabel("Biên độ")
        ax.legend()

        canvas.draw()
    except Exception as e:
        print("Vui lòng vẽ tín hiệu trước khi thực hiện lọc tín hiệu.")


# Tạo giao diện Tkinter
root = tk.Tk()
root.title("Phần mềm hỗ trợ xử lý tín hiệu số")

# Khung nhập các thông số tín hiệu
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Tần số (Hz):").grid(row=0, column=0)
entry_freq = tk.Entry(frame)
entry_freq.grid(row=0, column=1)
entry_freq.insert(0, "5")

tk.Label(frame, text="Biên độ:").grid(row=1, column=0)
entry_amplitude = tk.Entry(frame)
entry_amplitude.grid(row=1, column=1)
entry_amplitude.insert(0, "1")

tk.Label(frame, text="Tần số cắt (Hz):").grid(row=2, column=0)
entry_cutoff = tk.Entry(frame)
entry_cutoff.grid(row=2, column=1)
entry_cutoff.insert(0, "2.5")

button_update = tk.Button(frame, text="Vẽ tín hiệu", command=update_signal)
button_update.grid(row=3, columnspan=2, pady=5)

button_fft = tk.Button(frame, text="Hiển thị FFT", command=show_fft)
button_fft.grid(row=4, columnspan=2, pady=5)

button_filter = tk.Button(frame, text="Lọc tín hiệu", command=filter_signal)
button_filter.grid(row=5, columnspan=2, pady=5)

# Thiết lập biểu đồ Matplotlib cho giao diện Tkinter
fig, (ax, ax_fft) = plt.subplots(2, 1, figsize=(5, 8))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Khởi tạo biến lưu trữ tín hiệu hiện tại
current_signal = None

root.mainloop()
