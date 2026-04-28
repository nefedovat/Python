# Использовании ИИ - 95%

import numpy as np
import matplotlib.pyplot as plt
import wave
import re
import time


# Проверка имени файла
while True:
    file_name = input("Введите имя файла (должен быть 24.wav): ")
    if re.match(r'^24\.wav$', file_name):
        break
    else:
        print("Ошибка. Попробуйте снова.")

# Ввод количества отсчетов
while True:
    try:
        N = int(input("Введите количество отсчетов: "))
        if N > 0:
            break
        else:
            print("Ошибка: количество отсчетов должно быть положительным числом")
    except ValueError:
        print("Ошибка: нужно ввести целое число")

# Засекаем время выполнения
start_time = time.time()


# ЧТЕНИЕ WAV-ФАЙЛА с обработкой ошибок
while True:
    try:
        wav_file = wave.open(file_name, 'r')
        break
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_name}' не найден")
        file_name = input("Введите правильное имя файла: ")
    except Exception as e:
        print(f"Ошибка при открытии файла: {e}")
        file_name = input("Введите правильное имя файла: ")

# Получаем параметры файла
n_channels, sampwidth, framerate, n_frames, _, _ = wav_file.getparams()

print("Частота дискретизации:", framerate, "Гц")

# Проверка формата (только предупреждение, но не остановка)
if n_channels != 1:
    print(f"\nВНИМАНИЕ: файл содержит {n_channels} канала(ов), ожидается моно")
if sampwidth != 2:
    print(f"\nВНИМАНИЕ: файл имеет битность {sampwidth*8} бит, ожидается 16 бит")
if framerate != 96000:
    print(f"\nВНИМАНИЕ: частота {framerate} Гц, ожидается 96000 Гц")

# Проверка, что N не превышает количество кадров в файле
if N > n_frames:
    print(f"\nВНИМАНИЕ: запрошено {N} отсчетов, но в файле только {n_frames} отсчетов")
    print(f"Будут использованы {n_frames} отсчетов")
    N = n_frames

# Читаем весь сигнал
frames = wav_file.readframes(n_frames)
full_signal = np.frombuffer(frames, dtype=np.int16)

# Если стерео - берем только левый канал
if n_channels > 1:
    full_signal = full_signal[::n_channels]

# Для отображения берем N отсчетов
if N > len(full_signal):
    N = len(full_signal)
signal = full_signal[:N]

# Создаем временную ось
time_axis = np.arange(len(signal)) / framerate


# 1. СТОЛБЧАТАЯ ДИАГРАММА для считанных отсчетов


plt.figure()
plt.bar(np.arange(len(signal)), signal, width=1)
plt.title("Столбчатая диаграмма отсчетов сигнала (первые {} отсчетов)".format(N))
plt.xlabel("Номер отсчета")
plt.ylabel("Амплитуда")
plt.grid(alpha=0.3)


# 2. ОСЦИЛЛОГРАММА


plt.figure()
plt.plot(time_axis, signal)
plt.title("Осциллограмма сигнала")
plt.xlabel("Время (сек)")
plt.ylabel("Амплитуда")
plt.grid(alpha=0.3)


# 3. СПЕКТРАЛЬНЫЙ АНАЛИЗ ВСЕГО СИГНАЛА


fft_full = np.fft.fft(full_signal)
freq_full = np.fft.fftfreq(len(full_signal), d=1/framerate)

# Квадрат ДПФ = Re² + Im²
spectrum = np.real(fft_full)**2 + np.imag(fft_full)**2
spectrum_log = np.log1p(spectrum)  # логарифм для наглядности

half = len(freq_full) // 2

plt.figure()
plt.bar(freq_full[:half], spectrum_log[:half], width=freq_full[1]-freq_full[0])
plt.title("Энергетический спектр сигнала (квадрат ДПФ = Re² + Im²)\nв логарифмическом масштабе")
plt.xlabel("Частота (Гц)")
plt.ylabel("log(1 + Re² + Im²)")
plt.grid(alpha=0.3)


# 4. ГИСТОГРАММА


plt.figure()
plt.title("Гистограмма распределения амплитуд отсчетов сигнала")
plt.xlabel("Амплитуда")
plt.ylabel("Количество отсчетов")
plt.grid(alpha=0.3)


# ВРЕМЯ ВЫПОЛНЕНИЯ

print("Время выполнения программы:", time.time() - start_time, "секунд")


plt.show()
