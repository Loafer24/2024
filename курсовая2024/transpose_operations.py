#Класс транспонирования матриц
class InPlaceTranspose:
    @staticmethod
    def transpose_matrix(matrix):
        n, m = len(matrix), len(matrix[0])
        #Проверка размерности матрицы: квадратная матрица - In-place метод
        if n == m:
            for i in range(n):
                for j in range(i + 1, n):
                    matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
            return matrix
        #Матрица не квадратная - наивный метод
        transposed = [[0] * n for _ in range(m)]
        for i in range(n):
            for j in range(m):
                transposed[j][i] = matrix[i][j]
        return transposed