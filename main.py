from datetime import datetime

# Функция для преобразования строки в объект datetime
def parse_datetime(line):
    line = line.strip()
    try:
        return datetime.strptime(line, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        return datetime.strptime(line, "%Y-%m-%d %H:%M:%S")

# Чтение данных из файла
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.readlines()

# Фильтрация данных по диапазону
def filter_lines(lines, min_datetime, max_datetime):
    filtered_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        dt = parse_datetime(line)
        if min_datetime <= dt <= max_datetime:
            filtered_lines.append(line)
    return filtered_lines

# Запись данных в файл
def write_file(filename, lines):
    with open(filename, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')

# Функция для вывода общего числа строк в файле
def print_line_count(filename, stage):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        print(f"Общее число строк на этапе {stage}: {len(lines)}")

# Основная функция
def main():
    input_file = 'timestamp_input.txt'  # Имя входного файла
    output_file = 'timestamp_output.txt'  # Имя выходного файла
    results_file = 'timestamp_output_results.txt'  # Имя файла с результатами

    # 1. Считываем все строки из файла
    lines = read_file(input_file)

    # 2. Выводим общее число строк на первом этапе
    print_line_count(input_file, "1 (из timestamp_input.txt)")

    # 3. Сортируем строки по убыванию и заменяем "T" на пробел
    datetime_objects = [parse_datetime(line.replace("T", " ")) for line in lines]
    sorted_datetime_objects = sorted(datetime_objects, reverse=True)
    sorted_lines = [dt.strftime("%Y-%m-%d %H:%M:%S.%f").rstrip('0').rstrip('.') for dt in sorted_datetime_objects]

    # 4. Сохраняем отсортированные данные в файл
    write_file(output_file, sorted_lines)

    # 5. Выводим минимальное и максимальное значение временного диапазона
    min_datetime = parse_datetime(sorted_lines[-1])
    max_datetime = parse_datetime(sorted_lines[0])
    print(f"Минимальное значение временного диапазона: {min_datetime}")
    print(f"Максимальное значение временного диапазона: {max_datetime}")
    print()

    # 6. Запрашиваем у пользователя новые границы диапазона
    min_input = input("Введите новое минимальное значение временного диапазона (формат: YYYY-MM-DD HH:MM:SS.MS): ")
    max_input = input("Введите новое максимальное значение временного диапазона (формат: YYYY-MM-DD HH:MM:SS.MS): ")
    print()

    # Преобразуем введенные значения в объекты datetime
    min_datetime = parse_datetime(min_input)
    max_datetime = parse_datetime(max_input)

    # Проверяем, что минимальная дата не больше максимальной
    if min_datetime > max_datetime:
        print("Ошибка: минимальная дата позже максимальной")
        return

    # 7. Читаем данные из файла timestamp_output.txt
    lines_from_output = read_file(output_file)

    # 8. Фильтруем строки по новому диапазону
    filtered_lines = filter_lines(lines_from_output, min_datetime, max_datetime)

    # 9. Записываем отфильтрованные данные в файл
    write_file(results_file, filtered_lines)

    # 10. Выводим общее число строк на втором этапе
    print_line_count(results_file, "2 (из timestamp_output_results.txt)")

    # 11. Выводим минимальное и максимальное значение нового временного диапазона
    if filtered_lines:
        new_min_datetime = parse_datetime(filtered_lines[-1])
        new_max_datetime = parse_datetime(filtered_lines[0])
        print()
        print(f"Минимальное значение нового временного диапазона: {new_min_datetime}")
        print(f"Максимальное значение нового временного диапазона: {new_max_datetime}")
    else:
        print("Нет данных в указанном диапазоне")

# Запуск программы
if __name__ == "__main__":
    main()