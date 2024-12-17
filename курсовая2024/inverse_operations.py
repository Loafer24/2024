#Класс для нахождения обратной матрицы методом Гаусса-Жордана
class GaussJordanInverse:
    @staticmethod
    def gauss_jordan_inverse(matrix, precision=2):
        
        n = len(matrix)  # Размерность матрицы
        # Создание расширенной матрицы: объединение исходной матрицы и единичной матрицы
        augmented = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]

        # Прямой ход метода Гаусса-Жордана
        for k in range(n):
            # Поиск строки с максимальным абсолютным значением в текущем столбце для выбора ведущего элемента
            max_row = k
            for i in range(k + 1, n):
                if abs(augmented[i][k]) > abs(augmented[max_row][k]):
                    max_row = i

            # Обмен строк, если строка с максимальным элементом не текущая
            if max_row != k:
                augmented[k], augmented[max_row] = augmented[max_row], augmented[k]

            # Проверка на наличие нулевого ведущего элемента (матрица необратима)
            if abs(augmented[k][k]) < 1.0e-12:
                raise ValueError("Эта матрица не является обратимой из-за нулевого детерминанта")

            # Нормализация текущей строки: деление всех элементов строки на ведущий элемент
            pivot = augmented[k][k]
            for j in range(2 * n):
                augmented[k][j] /= pivot

            # Зануление всех элементов текущего столбца, кроме ведущего элемента
            for i in range(n):
                if i == k:  # Пропуск текущей строки
                    continue
                factor = augmented[i][k]
                for j in range(2 * n):
                    augmented[i][j] -= factor * augmented[k][j]

        # Извлечение обратной матрицы из правой половины расширенной матрицы
        return [[round(value, precision) for value in row[n:]] for row in augmented]
