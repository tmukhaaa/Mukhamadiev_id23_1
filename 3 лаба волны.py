import tkinter as tk
import math
from tkinter import simpledialog, messagebox


waves = [
    {"amplitude": 1, "period": 2, "speed": 1},
    {"amplitude": 0.5, "period": 3, "speed": 0.8},
]

buoys = [
    {"mass": 1, "volume": 1, "position": 2},
    {"mass": 1.5, "volume": 1.2, "position": 5},
    {"mass": 0.8, "volume": 0.9, "position": 8},
]

# Настройки окна
WIDTH = 800
HEIGHT = 400

# окно
root = tk.Tk()
root.title("Симуляция волн и поплавков")

# рисование
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# Функция для рисования волн
def draw_wave(wave, frame):
    for x in range(0, WIDTH):
        y = wave["amplitude"] * math.sin(2 * math.pi * (x / (WIDTH / wave["period"]) - frame * wave["speed"] / 100))
        canvas.create_line(x, HEIGHT // 2 - y * 50, x + 1, HEIGHT // 2 - y * 50, fill="blue", width=2)

# Функция для рисования поплавков с арихимедом
def draw_buoy(buoy, frame):
    wave_height = sum(
        wave["amplitude"] * math.sin(2 * math.pi * (buoy["position"] * 50 / wave["period"] - frame * wave["speed"] / 100))
        for wave in waves
    )
    buoy_y = HEIGHT // 2 - wave_height * 50 - (buoy["mass"] - buoy["volume"]) * 10  # Применение силы Архимеда
    canvas.create_oval(buoy["position"] * 100 - 10, buoy_y - 10, buoy["position"] * 100 + 10, buoy_y + 10, fill="red")

# аниматор
def update(frame):
    canvas.delete("all")  # Очистка канваса для обновления графика

    # волны
    for wave in waves:
        draw_wave(wave, frame)

    # поплавки
    for buoy in buoys:
        draw_buoy(buoy, frame)

    # Плавное обновление через 30 миллисекунд
    root.after(30, update, frame + 1)

# Функции интерфейса для добавления/удаления волн и поплавков
def add_wave():
    try:
        amplitude = float(simpledialog.askstring("Добавить волну", "Введите амплитуду:"))
        period = float(simpledialog.askstring("Добавить волну", "Введите период:"))
        speed = float(simpledialog.askstring("Добавить волну", "Введите скорость:"))
        waves.append({"amplitude": amplitude, "period": period, "speed": speed})
        update(0)
    except (ValueError, TypeError):
        messagebox.showerror("Ошибка", "Некорректный ввод. Введите числовые значения.")

def add_buoy():
    try:
        mass = float(simpledialog.askstring("Добавить поплавок", "Введите массу:"))
        volume = float(simpledialog.askstring("Добавить поплавок", "Введите объем:"))
        position = float(simpledialog.askstring("Добавить поплавок", "Введите позицию:"))
        buoys.append({"mass": mass, "volume": volume, "position": position})
        update(0)
    except (ValueError, TypeError):
        messagebox.showerror("Ошибка", "Некорректный ввод. Введите числовые значения.")

def delete_wave():
    if waves:
        waves.pop()
        update(0)  # Обновляем график после удаления волны

def delete_buoy():
    if buoys:
        buoys.pop()
        update(0)  # Обновляем график после удаления поплавка

# Функция для обновления графика
def reset_graph():
    update(0)

# Панель кнопок для управления
control_frame = tk.Frame(root)
control_frame.pack(side=tk.BOTTOM, fill=tk.X)

tk.Button(control_frame, text="Добавить волну", command=add_wave).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(control_frame, text="Удалить волну", command=delete_wave).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(control_frame, text="Добавить поплавок", command=add_buoy).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(control_frame, text="Удалить поплавок", command=delete_buoy).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(control_frame, text="Обновить график", command=reset_graph).pack(side=tk.LEFT, padx=5, pady=5)

update(0)

# Запуск интерфейса
root.mainloop()
