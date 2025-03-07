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
