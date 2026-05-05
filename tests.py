import unittest
import random
import string
from password_generator import PasswordGeneratorApp
import tkinter as tk

class TestPasswordGenerator(unittest.TestCase):
    def setUp(self):
        # Создаём корневое окно tkinter для тестов (скрытое)
        self.root = tk.Tk()
        self.app = PasswordGeneratorApp(self.root)
        self.root.withdraw()  # Скрываем окно

    def tearDown(self):
        self.root.destroy()

    def test_generation_with_digits_only(self):
        """Позитивный тест: только цифры"""
        self.app.use_digits.set(True)
        self.app.use_letters.set(False)
        self.app.use_symbols.set(False)
        self.app.password_length.set(10)
        self.app.generate_password()
        password = self.app.password_var.get()
        self.assertEqual(len(password), 10)
        self.assertTrue(all(c in string.digits for c in password))

    def test_generation_with_letters_only(self):
        """Позитивный тест: только буквы"""
        self.app.use_digits.set(False)
        self.app.use_letters.set(True)
        self.app.use_symbols.set(False)
        self.app.password_length.set(15)
        self.app.generate_password()
        password = self.app.password_var.get()
        self.assertEqual(len(password), 15)
        self.assertTrue(all(c in string.ascii_letters for c in password))

    def test_generation_with_all_types(self):
        """Позитивный тест: все типы символов"""
        self.app.use_digits.set(True)
        self.app.use_letters.set(True)
        self.app.use_symbols.set(True)
        self.app.password_length.set(20)
        self.app.generate_password()
        password = self.app.password_var.get()
        self.assertEqual(len(password), 20)
        # Проверяем, что есть хотя бы один символ из каждого набора
        self.assertTrue(any(c in string.digits for c in password))
        self.assertTrue(any(c in string.ascii_letters for c in password))
        self.assertTrue(any(c in self.app.symbols_set for c in password))

    def test_no_character_set_selected(self):
        """Негативный тест: ни один чекбокс не выбран"""
        self.app.use_digits.set(False)
        self.app.use_letters.set(False)
        self.app.use_symbols.set(False)
        # Генерация должна вызвать messagebox, но мы перехватим отсутствие пароля
        self.app.generate_password()
        self.assertEqual(self.app.password_var.get(), "")  # Пароль не установлен

    def test_minimum_length(self):
        """Граничный тест: минимальная длина (4)"""
        self.app.password_length.set(4)
        self.app.use_digits.set(True)
        self.app.use_letters.set(False)
        self.app.use_symbols.set(False)
        self.app.generate_password()
        password = self.app.password_var.get()
        self.assertEqual(len(password), 4)

    def test_maximum_length(self):
        """Граничный тест: максимальная длина (32)"""
        self.app.password_length.set(32)
        self.app.use_digits.set(True)
        self.app.use_letters.set(False)
        self.app.use_symbols.set(False)
        self.app.generate_password()
        password = self.app.password_var.get()
        self.assertEqual(len(password), 32)

    def test_history_saving_and_loading(self):
        """Тест сохранения и загрузки истории"""
        self.app.history = []
        test_entry = {"timestamp": "2025-01-01 12:00:00", "password": "test123"}
        self.app.history.append(test_entry)
        self.app.save_history()
        # Загружаем заново
        loaded = self.app.load_history()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["password"], "test123")
        # Очищаем
        self.app.clear_history()
        self.assertEqual(len(self.app.history), 0)

if __name__ == "__main__":
    unittest.main()
