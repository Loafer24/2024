import tkinter as tk
from tkinter import messagebox, filedialog
from logger import Logger
from naive_operations import NaiveMatrixOperations
from strassen_operations import StrassenMatrixMultiplication
from transpose_operations import InPlaceTranspose
from inverse_operations import GaussJordanInverse

# Класс возведения матрицы в квадрат
class MatrixOperations:

    @staticmethod
    def square_matrix(matrix):
        """Возведение матрицы в квадрат (умножение матрицы на саму себя)"""
        return StrassenMatrixMultiplication.strassen_multiply(matrix, matrix)

# Основной класс
class MainForm:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Matrix Operations")
        self._build_interface()
        self.entry_matrix_a.focus_set()  # Устанавливаем фокус на первое поле при запуске
        self.root.mainloop()

    # Создание интерфейса
    def _build_interface(self):
        # Поля для ввода матриц
        tk.Label(self.root, text="Матрица A (строки, разделенные новой строкой):").grid(row=0, column=0, columnspan=3)
        self.entry_matrix_a = tk.Text(self.root, height=10, width=60)
        self.entry_matrix_a.grid(row=1, column=0, columnspan=2)
        self.entry_matrix_a.bind("<KeyRelease>", self.validate_matrix_input)  # Проверка при каждом вводе

        tk.Button(self.root, text="Загрузить из файла",
                  command=lambda: self.load_matrix_from_file(self.entry_matrix_a)).grid(row=1, column=2)
        tk.Button(self.root, text="Очистить",
                  command=lambda: self.clear_matrix(self.entry_matrix_a)).grid(row=1, column=3)

        tk.Label(self.root, text="Матрица B (строки, разделенные новой строкой):").grid(row=2, column=0, columnspan=3)
        self.entry_matrix_b = tk.Text(self.root, height=10, width=60)
        self.entry_matrix_b.grid(row=3, column=0, columnspan=2)
        self.entry_matrix_b.bind("<KeyRelease>", self.validate_matrix_input)  # Проверка при каждом вводе

        tk.Button(self.root, text="Загрузить из файла",
                  command=lambda: self.load_matrix_from_file(self.entry_matrix_b)).grid(row=3, column=2)
        tk.Button(self.root, text="Очистить",
                  command=lambda: self.clear_matrix(self.entry_matrix_b)).grid(row=3, column=3)

        # Выпадающий список операций
        self.operation_var = tk.StringVar(value="Операции")
        tk.Label(self.root, text="Выбрать операцию:").grid(row=4, column=0)
        tk.OptionMenu(self.root, self.operation_var, "Сложение", "Вычитание", "Умножение",
                      "Транспонировать A", "Транспонировать B", "Обратная A", "Обратная B", "Возвести A в квадрат", "Возвести B в квадрат").grid(row=4, column=1,
                                                                                                     columnspan=2)

        # Кнопка выполнения
        tk.Button(self.root, text="Выполнить", command=self.execute_operation).grid(row=5, column=0, columnspan=3)

        # Поле вывода результата
        tk.Label(self.root, text="Результат:").grid(row=6, column=0, columnspan=3)
        self.result_text = tk.Text(self.root, height=10, width=60, state="disabled")
        self.result_text.grid(row=7, column=0, columnspan=3)

        # Кнопка сохранения результата
        tk.Button(self.root, text="Сохранить в файл", command=self.save_result_to_file).grid(row=8, column=0,
                                                                                             columnspan=3)

        # Настройка тега для подсветки ошибок
        self.entry_matrix_a.tag_configure("error", background="red", foreground="white")
        self.entry_matrix_b.tag_configure("error", background="red", foreground="white")

        # Флаг ошибки для проверки ввода
        self.has_errors_a = False
        self.has_errors_b = False

    # Проверка ввода матрицы при каждом изменении текста
    # Проверка ввода матрицы при каждом изменении текста
    def validate_matrix_input(self, event):
        entry_widget = event.widget
        content = entry_widget.get("1.0", tk.END).strip()

        # Очистка предыдущих подсветок
        entry_widget.tag_remove("error", "1.0", "end")

        try:
            # Попытка разобрать матрицу и определить строки с ошибками
            matrix_lines = content.split('\n')
            has_error = False

            for i, line in enumerate(matrix_lines):
                # Проверка элементов строки
                elements = line.split()
                start_index = 0  # Указывает начальную позицию элемента в строке

                for element in elements:
                    # Проверка на допустимые символы: цифры, точка, запятая, минус в начале и дроби
                    if not self.is_valid_element(element):
                        element_start = f"{i + 1}.{start_index}"
                        element_end = f"{i + 1}.{start_index + len(element)}"
                        entry_widget.tag_add("error", element_start, element_end)
                        has_error = True
                    else:
                        # Преобразование дробей в десятичное число
                        if '/' in element:
                            try:
                                decimal_value = self.convert_fraction_to_decimal(element)
                                # Преобразуем дробь в десятичное число и заменяем в тексте
                                entry_widget.delete(f"{i + 1}.{start_index}", f"{i + 1}.{start_index + len(element)}")
                                entry_widget.insert(f"{i + 1}.{start_index}", str(decimal_value))
                            except ValueError:
                                # Ошибка при конвертации дроби
                                element_start = f"{i + 1}.{start_index}"
                                element_end = f"{i + 1}.{start_index + len(element)}"
                                entry_widget.tag_add("error", element_start, element_end)
                                has_error = True

                    start_index += len(element) + 1  # +1 для учета пробела между элементами

                # Проверка двойных пробелов и их подсветка
                for j in range(len(line) - 1):
                    if line[j:j + 2] == '  ':
                        position_start = f"{i + 1}.{j}"
                        position_end = f"{i + 1}.{j + 2}"
                        entry_widget.tag_add("error", position_start, position_end)
                        has_error = True

            # Установка флага ошибки для матрицы
            if entry_widget == self.entry_matrix_a:
                self.has_errors_a = has_error
            else:
                self.has_errors_b = has_error

        except Exception as e:
            # Если произошла ошибка при разборе всей строки, подсвечиваем весь текст
            entry_widget.tag_add("error", "1.0", "end")
            if entry_widget == self.entry_matrix_a:
                self.has_errors_a = True
            else:
                self.has_errors_b = True

    # Метод проверки валидности элемента (числа)
    def is_valid_element(self, element):
        # Если элемент состоит только из минуса (например, "-"), это ошибка
        if element == '-':
            return False
        
        # Если элемент начинается с минуса, удаляем его и проверяем остальную часть
        if element.startswith('-'):
            element = element[1:]  # Убираем минус для проверки

        # Проверяем, что оставшаяся часть состоит только из цифр, запятых, точек или дробей
        if '/' in element:
            # Проверка на корректную дробь, например, "1/2" или "-3/4"
            parts = element.split('/')
            if len(parts) != 2 or not all(part.replace('.', '', 1).isdigit() for part in parts):
                return False

        return all(char.isdigit() or char in '.,/' for char in element)

    # Метод для преобразования дроби в десятичное число
    def convert_fraction_to_decimal(self, fraction):
        # Преобразуем дробь в десятичное число
        try:
            numerator, denominator = fraction.split('/')
            decimal_value = float(numerator) / float(denominator)
            return decimal_value
        except ValueError:
            raise ValueError(f"Некорректная дробь: {fraction}")


     # Выполнение выбранной операции
    # Выполнение выбранной операции
    def validate_matrix_input(self, event):
        entry_widget = event.widget
        content = entry_widget.get("1.0", tk.END).strip()

        # Очистка предыдущих подсветок
        entry_widget.tag_remove("error", "1.0", "end")

        try:
            matrix_lines = content.split('\n')
            has_error = False

            # Находим максимальное количество элементов в строках
            max_elements = max(len(line.split()) for line in matrix_lines)

            for i, line in enumerate(matrix_lines):
                elements = line.split()
                start_index = 0  # Начальная позиция элемента в строке

                for element in elements:
                    if not self.is_valid_element(element):
                        element_start = f"{i + 1}.{start_index}"
                        element_end = f"{i + 1}.{start_index + len(element)}"
                        entry_widget.tag_add("error", element_start, element_end)
                        has_error = True
                    start_index += len(element) + 1  # +1 для пробела между элементами

                # Подсветка строк с недостаточным количеством элементов
                if len(elements) < max_elements:
                    line_start = f"{i + 1}.0"
                    line_end = f"{i + 1}.{len(line)}"
                    entry_widget.tag_add("error", line_start, line_end)
                    has_error = True

            # Если есть ошибки, устанавливаем флаг
            if entry_widget == self.entry_matrix_a:
                self.has_errors_a = has_error
            else:
                self.has_errors_b = has_error

        except Exception as e:
            entry_widget.tag_add("error", "1.0", "end")
            if entry_widget == self.entry_matrix_a:
                self.has_errors_a = True
            else:
                self.has_errors_b = True

    def execute_operation(self):
        # Проверка наличия ошибок перед выполнением операции
        if self.has_errors_a or self.has_errors_b:
            messagebox.showerror("Ошибка", "Введены недопустимые символы. Пожалуйста, исправьте ошибки.")
            
            # Перемещение курсора к последней ошибке в матрицах
            if self.has_errors_a:
                last_error_position = self.entry_matrix_a.tag_ranges("error")[-1]  # Последняя ошибка в A
                self.entry_matrix_a.mark_set("insert", last_error_position)
                self.entry_matrix_a.see(last_error_position)
                self.entry_matrix_a.focus_set()
            elif self.has_errors_b:
                last_error_position = self.entry_matrix_b.tag_ranges("error")[-1]  # Последняя ошибка в B
                self.entry_matrix_b.mark_set("insert", last_error_position)
                self.entry_matrix_b.see(last_error_position)
                self.entry_matrix_b.focus_set()
            return

        try:
            self.clear_error_highlighting()  # Очистка выделения ошибок перед выполнением
            self.result_text.config(state='normal')
            self.result_text.delete("1.0", tk.END)

            matrix_a_str = self.entry_matrix_a.get("1.0", tk.END).strip()
            matrix_b_str = self.entry_matrix_b.get("1.0", tk.END).strip()
            operation = self.operation_var.get()

            # Проверка и парсинг матриц
            matrix_a = NaiveMatrixOperations.parse_matrix(matrix_a_str)
            matrix_b = NaiveMatrixOperations.parse_matrix(matrix_b_str)

            # Выполнение операции
            if operation == "Сложение":
                result_matrix = NaiveMatrixOperations.add_matrices(matrix_a, matrix_b)
            elif operation == "Вычитание":
                result_matrix = NaiveMatrixOperations.subtract_matrices(matrix_a, matrix_b)
            elif operation == "Умножение":
                result_matrix = StrassenMatrixMultiplication.strassen_multiply(matrix_a, matrix_b)
            elif operation == "Транспонировать A":
                result_matrix = InPlaceTranspose.transpose_matrix(matrix_a)
            elif operation == "Транспонировать B":
                result_matrix = InPlaceTranspose.transpose_matrix(matrix_b)
            elif operation == "Обратная A":
                result_matrix = GaussJordanInverse.gauss_jordan_inverse(matrix_a)
            elif operation == "Обратная B":
                result_matrix = GaussJordanInverse.gauss_jordan_inverse(matrix_b)
            elif operation == "Возвести A в квадрат":
                result_matrix = MatrixOperations.square_matrix(matrix_a)
            elif operation == "Возвести B в квадрат":
                result_matrix = MatrixOperations.square_matrix(matrix_b)
            else:
                raise ValueError("Выберите операцию из списка.")

            # Отображение результата
            result = NaiveMatrixOperations.matrix_to_string(result_matrix)
            self.result_text.insert(tk.END, result)
            self.result_text.config(state='disabled')

            # После выполнения операции проверяем на ошибки и подсвечиваем неполные строки
            self.highlight_incomplete_lines(self.entry_matrix_a)
            self.highlight_incomplete_lines(self.entry_matrix_b)

        except Exception as e:
            Logger.log_error(operation, str(e))
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    # Проверка и подсветка неполных строк в матрице
    def highlight_incomplete_lines(self, entry_widget):
        content = entry_widget.get("1.0", tk.END).strip()

        # Очистка предыдущих подсветок
        entry_widget.tag_remove("error", "1.0", "end")

        try:
            matrix_lines = content.split('\n')
            max_elements = max(len(line.split()) for line in matrix_lines)

            # Подсветка неполных строк
            for i, line in enumerate(matrix_lines):
                elements = line.split()
                if len(elements) < max_elements:
                    # Подсвечиваем неполные строки
                    line_start = f"{i + 1}.0"
                    line_end = f"{i + 1}.{len(line)}"
                    entry_widget.tag_add("error", line_start, line_end)

                    # Перемещаем курсор на первую неполную строку
                    start_index = f"{i + 1}.0"
                    entry_widget.mark_set("insert", start_index)
                    entry_widget.see(start_index)
                    entry_widget.focus_set()

        except Exception as e:
            Logger.log_error("Подсветка ошибок", str(e))
            messagebox.showerror("Ошибка", f"Не удалось подсветить строки с ошибками: {e}")

    # Очистка подсветки ошибок
    def clear_error_highlighting(self):
        self.entry_matrix_a.tag_remove("error", "1.0", "end")
        self.entry_matrix_b.tag_remove("error", "1.0", "end")

    # Загрузка матрицы из файла
    def load_matrix_from_file(self, entry_widget):
        file_path = filedialog.askopenfilename(filetypes=[["Text Files", "*.txt"]])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    matrix_data = file.read()
                    entry_widget.delete("1.0", tk.END)
                    entry_widget.insert(tk.END, matrix_data)
                    entry_widget.focus_set()
            except Exception as e:
                Logger.log_error("Загрузка матрицы", str(e))
                messagebox.showerror("Ошибка", f"Не удалось загрузить матрицу: {e}")

    # Сохранение результата в файл
    def save_result_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[["Text Files", "*.txt"]])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.result_text.get("1.0", tk.END).strip())
            except Exception as e:
                Logger.log_error("Сохранение результата", str(e))
                messagebox.showerror("Ошибка", f"Не удалось сохранить результат: {e}")

    # Очистка содержимого поля для матрицы
    def clear_matrix(self, entry_widget):
        entry_widget.delete("1.0", tk.END)
        entry_widget.focus_set()

if __name__ == "__main__":
    MainForm()
