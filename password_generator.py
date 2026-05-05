import random
import string
import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        # Настройки по умолчанию
        self.password_length = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        # Символьные наборы
        self.digits_set = string.digits
        self.letters_set = string.ascii_letters
        self.symbols_set = "!@#$%^&*()-_=+[]{}|;:,.<>?/"

        # История паролей
        self.history_file = "history.json"
        self.history = self.load_history()

        # Построение интерфейса
        self.create_widgets()
        self.update_history_table()

        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Рамка для настроек
        settings_frame = ttk.LabelFrame(self.root, text="Настройки пароля", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)

        # Ползунок длины пароля
        ttk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky="w", padx=5)
        self.length_scale = ttk.Scale(settings_frame, from_=4, to=32, variable=self.password_length, orient="horizontal")
        self.length_scale.grid(row=0, column=1, sticky="ew", padx=5)
        self.length_label = ttk.Label(settings_frame, textvariable=self.password_length)
        self.length_label.grid(row=0, column=2, padx=5)
        ttk.Label(settings_frame, text="(4-32)").grid(row=0, column=3, padx=5)

        # Чекбоксы
        ttk.Checkbutton(settings_frame, text="Цифры (0-9)", variable=self.use_digits).grid(row=1, column=0, sticky="w", padx=5)
        ttk.Checkbutton(settings_frame, text="Буквы (A-Z a-z)", variable=self.use_letters).grid(row=1, column=1, sticky="w", padx=5)
        ttk.Checkbutton(settings_frame, text="Спецсимволы", variable=self.use_symbols).grid(row=1, column=2, sticky="w", padx=5)

        # Кнопка генерации
        gen_button = ttk.Button(settings_frame, text="Сгенерировать пароль", command=self.generate_password)
        gen_button.grid(row=2, column=0, columnspan=4, pady=10)

        # Поле для отображения сгенерированного пароля
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(settings_frame, textvariable=self.password_var, font=("Courier", 12), width=30)
        password_entry.grid(row=3, column=0, columnspan=3, padx=5, sticky="ew")
        copy_button = ttk.Button(settings_frame, text="Копировать", command=self.copy_to_clipboard)
        copy_button.grid(row=3, column=3, padx=5)

        # Рамка для истории
        history_frame = ttk.LabelFrame(self.root, text="История паролей", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Таблица истории
        columns = ("Дата и время", "Пароль")
        self.history_table = ttk.Treeview(history_frame, columns=columns, show="headings")
        self.history_table.heading("Дата и время", text="Дата и время")
        self.history_table.heading("Пароль", text="Пароль")
        self.history_table.column("Дата и время", width=150)
        self.history_table.column("Пароль", width=300)
        self.history_table.pack(fill="both", expand=True)

        # Кнопки управления историей
        button_frame = ttk.Frame(history_frame)
        button_frame.pack(fill="x", pady=5)
        clear_button = ttk.Button(button_frame, text="Очистить историю", command=self.clear_history)
        clear_button.pack(side="left", padx=5)
        save_button = ttk.Button(button_frame, text="Сохранить историю", command=self.save_history)
        save_button.pack(side="left", padx=5)

        # Настройка весов для масштабирования
        settings_frame.columnconfigure(1, weight=1)

    def generate_password(self):
        """Генерация пароля на основе выбранных параметров"""
        length = self.password_length.get()
        use_digits = self.use_digits.get()
        use_letters = self.use_letters.get()
        use_symbols = self.use_symbols.get()

        # Валидация: хотя бы один набор символов выбран
        if not (use_digits or use_letters or use_symbols):
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return

        # Формирование пула символов
        char_pool = ""
        if use_digits:
            char_pool += self.digits_set
        if use_letters:
            char_pool += self.letters_set
        if use_symbols:
            char_pool += self.symbols_set

        # Генерация пароля
        password = ''.join(random.choice(char_pool) for _ in range(length))
        self.password_var.set(password)

        # Сохранение в историю
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({"timestamp": timestamp, "password": password})
        self.save_history()
        self.update_history_table()

        # Дополнительно: копирование не требуется, но можно уведомить
        messagebox.showinfo("Успех", "Пароль сгенерирован и добавлен в историю!")

    def copy_to_clipboard(self):
        """Копирование текущего пароля в буфер обмена"""
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Копирование", "Пароль скопирован в буфер обмена")
        else:
            messagebox.showwarning("Предупреждение", "Нет сгенерированного пароля для копирования")

    def update_history_table(self):
        """Обновление таблицы истории из self.history"""
        # Очистка таблицы
        for row in self.history_table.get_children():
            self.history_table.delete(row)
        # Добавление записей (последние сверху)
        for entry in reversed(self.history):
            self.history_table.insert("", "end", values=(entry["timestamp"], entry["password"]))

    def save_history(self):
        """Сохранение истории в JSON-файл"""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

    def load_history(self):
        """Загрузка истории из JSON-файла"""
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def clear_history(self):
        """Очистка истории с подтверждением"""
        if messagebox.askyesno("Подтверждение", "Очистить всю историю паролей?"):
            self.history = []
            self.save_history()
            self.update_history_table()
            messagebox.showinfo("Очистка", "История очищена")

    def on_closing(self):
        """Действия при закрытии окна"""
        self.save_history()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
