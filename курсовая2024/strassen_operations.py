#Класс умножения матриц с использованием алшоритма Штрассена
class StrassenMatrixMultiplication:

    @staticmethod
    def strassen_multiply(matrix_a, matrix_b):
        # Проверка на правильность размеров матриц для умножения
        rows_a, cols_a = len(matrix_a), len(matrix_a[0])
        rows_b, cols_b = len(matrix_b), len(matrix_b[0])
        
        if cols_a != rows_b:
            raise ValueError("Количество столбцов в матрице A должно быть равно количеству строк в матрице B")

        # Дополнение матриц до квадратного размера, если необходимо
        new_size = max(rows_a, cols_a, rows_b, cols_b)
        new_size = 1 << (new_size - 1).bit_length()  # Округление до следующей степени двойки

        matrix_a_padded = StrassenMatrixMultiplication.pad_matrix(matrix_a, new_size, new_size)
        matrix_b_padded = StrassenMatrixMultiplication.pad_matrix(matrix_b, new_size, new_size)

        # Базовый случай для матрицы 1x1
        if new_size == 1:
            return [[matrix_a_padded[0][0] * matrix_b_padded[0][0]]]

        # Разделение матрицы на подматрицы
        a11, a12, a21, a22 = StrassenMatrixMultiplication.split_matrix(matrix_a_padded)
        b11, b12, b21, b22 = StrassenMatrixMultiplication.split_matrix(matrix_b_padded)

        # Рекурсивные вызовы для промежуточных матриц
        p1 = StrassenMatrixMultiplication.strassen_multiply(StrassenMatrixMultiplication.add(a11, a22), StrassenMatrixMultiplication.add(b11, b22))
        p2 = StrassenMatrixMultiplication.strassen_multiply(StrassenMatrixMultiplication.add(a21, a22), b11)
        p3 = StrassenMatrixMultiplication.strassen_multiply(a11, StrassenMatrixMultiplication.subtract(b12, b22))
        p4 = StrassenMatrixMultiplication.strassen_multiply(a22, StrassenMatrixMultiplication.subtract(b21, b11))
        p5 = StrassenMatrixMultiplication.strassen_multiply(StrassenMatrixMultiplication.add(a11, a12), b22)
        p6 = StrassenMatrixMultiplication.strassen_multiply(StrassenMatrixMultiplication.subtract(a21, a11), StrassenMatrixMultiplication.add(b11, b12))
        p7 = StrassenMatrixMultiplication.strassen_multiply(StrassenMatrixMultiplication.subtract(a12, a22), StrassenMatrixMultiplication.add(b21, b22))

        # Сбор результатов в подматрицы для итогового результата
        c11 = StrassenMatrixMultiplication.add(StrassenMatrixMultiplication.add(p1, p4), StrassenMatrixMultiplication.subtract(p7, p5))
        c12 = StrassenMatrixMultiplication.add(p3, p5)
        c21 = StrassenMatrixMultiplication.add(p2, p4)
        c22 = StrassenMatrixMultiplication.add(StrassenMatrixMultiplication.subtract(p1, p2), StrassenMatrixMultiplication.add(p3, p6))

        # Объединение подматриц в одну матрицу
        result = []
        for i in range(len(c11)):
            result.append(c11[i] + c12[i])
        for i in range(len(c21)):
            result.append(c21[i] + c22[i])

        # Возврат изначального размера матрицы (удаление лишних нулей)
        return [row[:cols_b] for row in result[:rows_a]]
    
    #Разделение матрицы на четыре подматрицы
    @staticmethod
    def split_matrix(matrix):
        n = len(matrix)
        mid = n // 2
        a11 = [row[:mid] for row in matrix[:mid]]
        a12 = [row[mid:] for row in matrix[:mid]]
        a21 = [row[:mid] for row in matrix[mid:]]
        a22 = [row[mid:] for row in matrix[mid:]]
        return a11, a12, a21, a22
    
    #Сложение матриц
    @staticmethod
    def add(matrix_a, matrix_b):
        return [[matrix_a[i][j] + matrix_b[i][j] for j in range(len(matrix_a[0]))] for i in range(len(matrix_a))]

    #Разность матриц
    @staticmethod
    def subtract(matrix_a, matrix_b):
        return [[matrix_a[i][j] - matrix_b[i][j] for j in range(len(matrix_a[0]))] for i in range(len(matrix_a))]
    
    #Дополнение матрицы нулями до заданного размера
    @staticmethod
    def pad_matrix(matrix, target_rows, target_cols):
        padded = [[0] * target_cols for _ in range(target_rows)]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                padded[i][j] = matrix[i][j]
        return padded