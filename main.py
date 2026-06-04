import tkinter as tk

import customtkinter
import sqlite3


def db_start():
    print("Запуск БД")
    global conn, cur

    conn = sqlite3.connect("note.db")
    cur = conn.cursor()
    print("БД подключилась успешно")

    #Создание базы данных, если её ещё нет
    cur.execute("""CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY,note TEXT)""")


def update_notes_list():
    print("Обновление списка заметок")
    notes_list.delete(0, customtkinter.END)

    #Получаем заметки хранящиеся в БД
    cur.execute("SELECT * FROM notes")
    notes = cur.fetchall()

    #Отображаем заметки в listbox
    for note in notes:
        note_text = note[1]
        notes_list.insert(customtkinter.END, note_text)


def save_note():
    print("Нажали кнопку Save")
    note = note_entry.get()
    cur.execute("INSERT INTO notes (note) VALUES(?)", (note,))
    conn.commit()
    update_notes_list()
    note_entry.delete(0, customtkinter.END)


def delete_note():
    print("Нажали кнопку Delete")
    index = notes_list.curselection()
    if index:
        selected_note = notes_list.get(index)
        cur.execute("DELETE FROM notes WHERE note = ?", (selected_note,))
        conn.commit()
        update_notes_list()


#ОФОРМЛЕНИЕ
#Настройка темы
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

#Смена темы (Спасибо GPT что помог с этим)
current_theme = "dark"

def change_theme():
    global current_theme

    #Смена темы Listbox вместе с остальными виджетами
    if current_theme == "dark":
        customtkinter.set_appearance_mode("light")

        notes_list.config(
            bg="white",
            fg="black",
            selectbackground="#1f6aa5",
            selectforeground="white"
        )

        current_theme = "light"
        theme_button.configure(text="🌙 Тёмная тема")

    else:
        customtkinter.set_appearance_mode("dark")

        notes_list.config(
            bg="#212121",
            fg="white",
            selectbackground="#1f6aa5",
            selectforeground="white"
        )

        current_theme = "dark"
        theme_button.configure(text="☀️ Светлая тема")


#Окно приложения
root = customtkinter.CTk()
root.title("📒 NoteBook by Zebo")
root.geometry("500x650")
root.resizable(False, False)

#Заголовок
title_label = customtkinter.CTkLabel(
    root,
    text="📒 Мои заметки",
    font=("Segoe UI", 24, "bold")
)
title_label.pack(pady=(20, 15))

#Кнопка смены темы
theme_button = customtkinter.CTkButton(
    root,
    text="☀️ Светлая тема",
    command=change_theme,
    width=180,
    height=35
)
theme_button.pack(pady=(0, 15))

#Подпись
note_label = customtkinter.CTkLabel(
    root,
    text="Введите новую заметку",
    font=("Segoe UI", 14)
)
note_label.pack(pady=(5, 5))

#Поле ввода
note_entry = customtkinter.CTkEntry(
    root,
    width=400,
    height=40,
    font=("Segoe UI", 14),
    placeholder_text="Напишите заметку..."
)
note_entry.pack(pady=(0, 15))

#Кнопка добавления
save_button = customtkinter.CTkButton(
    root,
    text="➕ Добавить заметку",
    command=save_note,
    width=220,
    height=40,
    font=("Segoe UI", 14, "bold"),
    corner_radius=10
)
save_button.pack(pady=5)

#Кнопка удаления
delete_button = customtkinter.CTkButton(
    root,
    text="🗑 Удалить заметку",
    command=delete_note,
    width=220,
    height=40,
    font=("Segoe UI", 14, "bold"),
    fg_color="#c0392b",
    hover_color="#a93226",
    corner_radius=10
)
delete_button.pack(pady=(5, 15))

#Рамка для списка заметок (чуть более светлая рамка notes_list)
list_frame = customtkinter.CTkFrame(
    root,
    width=450,
    height=350,
    corner_radius=15
)
list_frame.pack(padx=15, pady=10, fill="both", expand=True)

#Список заметок (Поле снизу)
notes_list = tk.Listbox(
    list_frame,
    font=("Segoe UI", 12),
    bg="#212121",
    fg="white",
    selectbackground="#1f6aa5",
    selectforeground="white",
    borderwidth=0,
    highlightthickness=0
)

notes_list.pack(
    padx=10,
    pady=10,
    fill="both",
    expand=True
)


#НЕ ТРОГАТЬ
#Запуск базы данных
db_start()

update_notes_list()

#Запуск приложения
root.mainloop()

#Закрываем соединение с БД после запуска приложения
conn.close()
