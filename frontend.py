# import tkinter as tk
# from ctypes import CDLL, c_void_p, c_int, c_char_p, c_bool
#
# # Завантаження бібліотеки
# lib = CDLL('./libtime.so')
#
# # Визначення функцій з C++
# lib.createClock.argtypes = [c_char_p, c_bool, c_int, c_int, c_int]
# lib.createClock.restype = c_void_p
#
# lib.deleteClock.argtypes = [c_void_p]
# lib.deleteClock.restype = None
#
# lib.clockPlusSecond.argtypes = [c_void_p]
# lib.clockPlusSecond.restype = None
#
# lib.getClockInfo.argtypes = [c_void_p]
# lib.getClockInfo.restype = c_char_p
#
# # Клас Clock у Python (обгортка для C++)
# class Clock:
#     def __init__(self, brand, is24, h, m, s):
#         self.obj = lib.createClock(brand.encode('utf-8'), is24, h, m, s)
#
#     def __del__(self):
#         lib.deleteClock(self.obj)
#
#     def plusSecond(self):
#         lib.clockPlusSecond(self.obj)
#
#     def getInfo(self):
#         return lib.getClockInfo(self.obj).decode('utf-8')
#
# # Головне вікно з описом
# class WelcomeWindow:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Опис програми")
#         self.root.geometry("400x250")
#
#         description = """Ця програма дозволяє працювати з об'єктами часу та годинника.\n
# ✅ Збільшення часу на 1 секунду.\n
# ✅ Відображення у 12- або 24-годинному форматі.\n
# ✅ Відображення назви виробника годинника.\n
# Натисніть кнопку, щоб розпочати!"""
#
#         self.label = tk.Label(root, text=description, font=("Arial", 12), justify="left")
#         self.label.pack(pady=20)
#
#         self.start_button = tk.Button(root, text="Перейти до годинника", command=self.open_clock_window)
#         self.start_button.pack()
#
#     def open_clock_window(self):
#         self.root.destroy()
#         main_clock_window()
#
# # Вікно годинника
# class ClockWindow:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Годинник")
#         self.root.geometry("350x200")
#
#         self.clock = Clock("Rolex", True, 23, 59, 50)  # Початковий час
#
#         self.label = tk.Label(root, text=self.clock.getInfo(), font=("Arial", 12), justify="left")
#         self.label.pack(pady=20)
#
#         self.button = tk.Button(root, text="Додати секунду", command=self.update_time)
#         self.button.pack()
#
#     def update_time(self):
#         self.clock.plusSecond()
#         self.label.config(text=self.clock.getInfo())
#
# # Функція для запуску головного вікна
# def main_clock_window():
#     root = tk.Tk()
#     app = ClockWindow(root)
#     root.mainloop()
#
# # Запуск вікна з описом
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = WelcomeWindow(root)
#     root.mainloop()

import tkinter as tk
from tkinter import messagebox
from ctypes import CDLL, c_char_p, c_bool, c_int, c_void_p

# Завантажуємо бібліотеку
lib = CDLL("./libtime.so")

lib.createClock.argtypes = [c_char_p, c_bool, c_int, c_int, c_int]
lib.createClock.restype = c_void_p

lib.deleteClock.argtypes = [c_void_p]
lib.clockPlusSecond.argtypes = [c_void_p]
lib.getClockInfo.argtypes = [c_void_p]
lib.getClockInfo.restype = c_char_p

clock = None  # Глобальний об'єкт годинника


def create_clock():
    global clock
    brand = brand_entry.get().encode('utf-8')
    hours = int(hours_entry.get())
    minutes = int(minutes_entry.get())
    seconds = int(seconds_entry.get())
    format_24 = format_var.get()

    if clock:
        lib.deleteClock(clock)

    clock = lib.createClock(brand, format_24, hours, minutes, seconds)
    messagebox.showinfo("Годинник створено", "Новий годинник успішно створено!")


def show_info():
    if not clock:
        messagebox.showwarning("Помилка", "Спочатку створіть годинник!")
        return
    info = lib.getClockInfo(clock).decode("utf-8")
    messagebox.showinfo("Інформація про годинник", info)


def add_second():
    if not clock:
        messagebox.showwarning("Помилка", "Спочатку створіть годинник!")
        return
    lib.clockPlusSecond(clock)
    messagebox.showinfo("Оновлення", "Одна секунда додана!")


# Графічний інтерфейс
root = tk.Tk()
root.title("Годинник")

# Опис програми
description = tk.Label(root, text="Ця програма дозволяє створити годинник,\n"
                                  "вибрати 12/24-годинний формат, встановити час\n"
                                  "та додавати секунди.",
                       font=("Arial", 12))
description.pack(pady=10)

# Введення параметрів
tk.Label(root, text="Назва годинника:").pack()
brand_entry = tk.Entry(root)
brand_entry.pack()

tk.Label(root, text="Години:").pack()
hours_entry = tk.Entry(root)
hours_entry.pack()

tk.Label(root, text="Хвилини:").pack()
minutes_entry = tk.Entry(root)
minutes_entry.pack()

tk.Label(root, text="Секунди:").pack()
seconds_entry = tk.Entry(root)
seconds_entry.pack()

# Вибір формату часу
format_var = tk.BooleanVar()
format_var.set(True)
tk.Checkbutton(root, text="24-годинний формат", variable=format_var).pack()

# Кнопки
tk.Button(root, text="Створити годинник", command=create_clock).pack(pady=5)
tk.Button(root, text="Додати секунду", command=add_second).pack(pady=5)
tk.Button(root, text="Показати інформацію", command=show_info).pack(pady=5)

# Запуск
root.mainloop()
