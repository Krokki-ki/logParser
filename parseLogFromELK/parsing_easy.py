import os
from datetime import datetime
import re

# Функция для чтения файла
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

# Функция для записи в файл
def write_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

# Функция для преобразования формата даты
def convert_date_format(date_str):
    dt = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S.%f")
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Обрезаем до 3 знаков в миллисекундах

# Функция для извлечения даты из строки (старое регулярное выражение)
def extract_timestamp_old(line):
    match = re.search(r'\d{2}\.\d{2}\.\d{4}\s*\d{2}:\d{2}:\d{2}\.\d{3}', line)
    return match.group(0) if match else None

# Функция для извлечения даты из строки (новое регулярное выражение)
def extract_timestamp_new(line):
    match = re.search(r'\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2}\.\d{3}', line)
    return match.group(0) if match else None

# Главный метод
def parsing_easy():
    # 1. Запрос пути и имени файла
    base_path = input("Укажите путь к файлу логов (например, C:\\путь\\к\\папке): ")
    file_name = input("Укажите имя файла без расширения (например, fileName1): ")
    file_path = os.path.join(base_path, file_name + ".txt")

    # 2. Чтение файла и запись строк в general_output.txt
    lines = read_file(file_path)
    general_output_ELK_path = os.path.join(base_path, "general_output_ELK.txt")

    # 3. Конвертация формата datetime в general_output.txt (по старому регулярному выражению)
    converted_lines = []
    for line in lines:
        # Пропускаем заголовок (первую строку)
        if line.startswith('"@timestamp"'):
            continue
        timestamp = extract_timestamp_old(line)
        if timestamp:
            # Преобразуем дату в новый формат
            new_timestamp = convert_date_format(timestamp)
            converted_line = line.replace(timestamp, new_timestamp)
            converted_lines.append(converted_line)
        else:
            converted_lines.append(line)

    # 4. Сортировка строк по убыванию datetime
    sorted_lines = sorted(converted_lines, reverse=True, key=lambda x: extract_timestamp_new(x) or "")

    # 5. Запись отсортированных строк обратно в файл
    write_file(general_output_ELK_path, sorted_lines)

    # 6. Вывод сообщения о завершении
    print("Конвертация форматов и сортировка строк по datetime завершена. Данные сохранены в 'general_output_ELK.txt'")

    # 7. Подсчёт числа строк
    line_count = len(sorted_lines)
    print(f"Число строк в файле: {line_count}")

    # 8. Поиск и вывод максимального и минимального значения datetime (по новому регулярному выражению)
    if sorted_lines:
        first_line = sorted_lines[0]
        last_line = sorted_lines[-1]
        first_timestamp = extract_timestamp_new(first_line)
        last_timestamp = extract_timestamp_new(last_line)
        print(f"Максимальное значение datetime: {first_timestamp}")
        print(f"Минимальное значение datetime: {last_timestamp}")

# Запуск программы
if __name__ == "__main__":
    parsing_easy()