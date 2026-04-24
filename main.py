import tkinter as tk
from tkinter import ttk, messagebox
import json

# Создание главного окна
root = tk.Tk()
root.title("Movie Library")

# Поля ввода
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Название").grid(row=0, column=0)
title_entry = tk.Entry(frame)
title_entry.grid(row=0, column=1)

tk.Label(frame, text="Жанр").grid(row=1, column=0)
genre_entry = tk.Entry(frame)
genre_entry.grid(row=1, column=1)

tk.Label(frame, text="Год выпуска").grid(row=2, column=0)
year_entry = tk.Entry(frame)
year_entry.grid(row=2, column=1)

tk.Label(frame, text="Рейтинг").grid(row=3, column=0)
rating_entry = tk.Entry(frame)
rating_entry.grid(row=3, column=1)

# Таблица
columns = ("Title", "Genre", "Year", "Rating")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack(padx=10, pady=10)

# Список для хранения данных
movies = []

def add_movie():
    title = title_entry.get()
    genre = genre_entry.get()
    year = year_entry.get()
    rating = rating_entry.get()

    # Валидация
    if not year.isdigit():
        messagebox.showerror("Ошибка", "Год должен быть числом.")
        return
    if not rating.replace('.', '', 1).isdigit() or not (0 <= float(rating) <= 10):
        messagebox.showerror("Ошибка", "Рейтинг должен быть в диапазоне от 0 до 10.")
        return

    movie = {
        "Title": title,
        "Genre": genre,
        "Year": int(year),
        "Rating": float(rating)
    }
    movies.append(movie)
    refresh_table()
    save_to_json()

def refresh_table(filter_genre=None, filter_year=None):
    for item in tree.get_children():
        tree.delete(item)
    for m in movies:
        if filter_genre and m['Genre'] != filter_genre:
            continue
        if filter_year and str(m['Year']) != filter_year:
            continue
        tree.insert('', tk.END, values=(m['Title'], m['Genre'], m['Year'], m['Rating']))

def save_to_json():
    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

def load_from_json():
    try:
        with open('movies.json', 'r', encoding='utf-8') as f:
            global movies
            movies = json.load(f)
            refresh_table()
    except FileNotFoundError:
        pass

def filter_by_genre():
    genre = genre_filter_entry.get()
    refresh_table(filter_genre=genre)

def filter_by_year():
    year = year_filter_entry.get()
    refresh_table(filter_year=year)

# Кнопки
add_btn = tk.Button(root, text="Добавить фильм", command=add_movie)
add_btn.pack(pady=5)

filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="Фильтр по жанру").grid(row=0, column=0)
genre_filter_entry = tk.Entry(filter_frame)
genre_filter_entry.grid(row=0, column=1)
tk.Button(filter_frame, text="Фильтр", command=filter_by_genre).grid(row=0, column=2)

tk.Label(filter_frame, text="Фильтр по году").grid(row=1, column=0)
year_filter_entry = tk.Entry(filter_frame)
year_filter_entry.grid(row=1, column=1)
tk.Button(filter_frame, text="Фильтр", command=filter_by_year).grid(row=1, column=2)

# Загружаем данные при запуске
load_from_json()

# Запуск GUI
root.mainloop()