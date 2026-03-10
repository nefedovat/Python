# Программа для подсчета сумм строк и столбцов матрицы

print("Введите размерность матрицы:")
n = int(input("Количество строк: "))
m = int(input("Количество столбцов: "))

# Создаем матрицу
a = []
print("Введите элементы матрицы:")

# Ввод матрицы
for i in range(n):
    row = []
    for j in range(m):
        x = int(input(f"a[{i}][{j}] = "))
        row.append(x)
    a.append(row)

# Считаем суммы строк
row_sums = []
for i in range(n):
    s = 0
    for j in range(m):
        s = s + a[i][j]
    row_sums.append(s)

# Считаем суммы столбцов
col_sums = []
for j in range(m):
    s = 0
    for i in range(n):
        s = s + a[i][j]
    col_sums.append(s)

# Выводим результат
print("\nРезультат:")
for i in range(n):
    for j in range(m):
        print(a[i][j], end=" ")
    print(row_sums[i])

# Выводим суммы столбцов
for j in range(m):
    print(col_sums[j], end=" ")
print()