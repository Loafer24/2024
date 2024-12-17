from fractions import Fraction

class NaiveMatrixOperations:
    """Класс для базовых операций над матрицами."""

    @staticmethod
    def parse_number(value):
        """Преобразует строку в число, поддерживая дроби и десятичные числа."""
        try:
            value = value.strip().replace(',', '.') # Удаляем пробелы по краям
            if '/' in value:  # Проверка на дробь
                return float(Fraction(value))
            return float(value)  # Попытка преобразования в число с плавающей запятой
        except ValueError:
            raise ValueError(f"Неверный формат числа: {value}")

    @staticmethod
    def parse_matrix(matrix_str):
        """Парсинг строки матрицы в двумерный список чисел."""
        rows = matrix_str.strip().split("\n")
        return [[NaiveMatrixOperations.parse_number(num) for num in row.split()] for row in rows]

    @staticmethod
    def matrix_to_string(matrix):
        return "\n".join(" ".join(str(num) for num in row) for row in matrix)

    @staticmethod
    def add_matrices(matrix_a, matrix_b):
        if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
            raise ValueError("Матрицы должны быть одного размера.")
        return [[matrix_a[i][j] + matrix_b[i][j] for j in range(len(matrix_a[0]))] for i in range(len(matrix_a))]

    @staticmethod
    def subtract_matrices(matrix_a, matrix_b):
        if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
            raise ValueError("Матрицы должны быть одного размера.")
        return [[matrix_a[i][j] - matrix_b[i][j] for j in range(len(matrix_a[0]))] for i in range(len(matrix_a))]


