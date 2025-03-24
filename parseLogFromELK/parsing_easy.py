import os
from datetime import datetime
import re
from collections import OrderedDict

def get_input_files():
    """Получение путей к файлам от пользователя"""
    base_path = input("Введите полный путь к папке с файлами: ").strip()
    while not os.path.exists(base_path):
        print("Указанный путь не существует!")
        base_path = input("Введите полный путь к папке с файлами логов из ELK Kibana: ").strip()

    num_files = int(input("Введите количество файлов для обработки: "))
    files_prompt = f"Укажите через запятую имена {num_files} файла(-ов) без расширения (либо имя одного файла): "
    file_names = [f"{name.strip()}.txt" if not name.strip().endswith('.csv') else f"{name.strip()}.csv" for name in input(files_prompt).split(',')]

    return base_path, [os.path.join(base_path, fname) for fname in file_names]

def read_files(file_paths):
    """Чтение данных из файлов с обработкой ошибок и удалением заголовков"""
    lines = []
    for path in file_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                file_lines = f.readlines()
                # Удаляем первую строку, если она короткая (заголовок)
                if len(file_lines) > 0 and len(file_lines[0].strip()) <= 300:
                    file_lines = file_lines[1:]
                lines.extend(file_lines)
        except Exception as e:
            print(f"Ошибка чтения файла {path}: {str(e)}")
    return lines

def write_file(file_path, lines):
    """Запись данных в файл"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def deduplicate(lines):
    """Удаление дубликатов с сохранением порядка"""
    return list(OrderedDict.fromkeys(lines))

def filter_lines(lines, filter_str):
    """Фильтрация строк по подстроке"""
    return [line for line in lines if filter_str in line]

def convert_date_format(date_str):
    """Преобразование формата даты"""
    dt = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S.%f")
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Обрезаем до 3 знаков в миллисекундах

def extract_timestamp_old(line):
    """Извлечение даты из строки (старое регулярное выражение)"""
    match = re.search(r'\d{2}\.\d{2}\.\d{4}\s*\d{2}:\d{2}:\d{2}\.\d{3}', line)
    return match.group(0) if match else None

def extract_timestamp_new(line):
    """Извлечение даты из строки (новое регулярное выражение)"""
    match = re.search(r'\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2}\.\d{3}', line)
    return match.group(0) if match else None

def parsing_easy():
    # Шаг 1: Получение и обработка файлов
    base_path, file_paths = get_input_files()

    # Создаём папку ELK_output, если её нет
    output_dir = os.path.join(base_path, "ELK_output")
    os.makedirs(output_dir, exist_ok=True)

    # Шаг 2: Создание общего файла
    all_lines = read_files(file_paths)
    general_elk_path = os.path.join(output_dir, 'general_ELK.txt')
    write_file(general_elk_path, all_lines)
    print("Группировка указанных файлов завершена.")

    # Шаг 3: Конвертация и сортировка строк
    converted_lines = []
    for line in all_lines:
        timestamp = extract_timestamp_old(line)
        if timestamp:
            new_timestamp = convert_date_format(timestamp)
            converted_line = line.replace(timestamp, new_timestamp)
            converted_lines.append(converted_line)
        else:
            converted_lines.append(line)

    sorted_lines = sorted(converted_lines, reverse=True, key=lambda x: extract_timestamp_new(x) or "")
    write_file(general_elk_path, sorted_lines)
    print("Конвертация форматов и сортировка строк по datetime завершена.")

    # Шаг 4: Подсчёт числа строк и вывод на консоль
    print(f"Общее число записей в объединённом файле: {len(sorted_lines)}")
    if sorted_lines:
        print(f"Максимальное значение datetime: {extract_timestamp_new(sorted_lines[0])}")
        print(f"Минимальное значение datetime: {extract_timestamp_new(sorted_lines[-1])}")

    # Шаг 5: Запрос строки для фильтрации
    filter_str = input("\nВведите строку для детальной фильтрации (например, \"valueType=IN_NOTNULL\"): ")
    filtered_lines = filter_lines(sorted_lines, filter_str)
    general_elk_filter_path = os.path.join(output_dir, 'general_ELK_filter.txt')
    write_file(general_elk_filter_path, filtered_lines)
    print(f"Число записей по указанному фильтру: {len(filtered_lines)}")
    print(f'Результат сохранён в файл "{general_elk_filter_path}"')

    if filtered_lines:
        print(f"Максимальное значение datetime: {extract_timestamp_new(filtered_lines[0])}")
        print(f"Минимальное значение datetime: {extract_timestamp_new(filtered_lines[-1])}")

    # Шаг 6: Запрос на проверку дубликатов
    dedup_choice = input("Вы хотите выполнить проверку на дубли записей?\n1 - Да, 2 - Нет\n")
    if dedup_choice == "1":
        unique_lines = deduplicate(filtered_lines)
        general_elk_deduplicate_path = os.path.join(output_dir, 'general_ELK_filter_deduplicate.txt')
        write_file(general_elk_deduplicate_path, unique_lines)
        print(f"Число уникальных записей: {len(unique_lines)}")
        print(f'Результат сохранён в файл "{general_elk_deduplicate_path}"')

        if unique_lines:
            print(f"Максимальное значение datetime: {extract_timestamp_new(unique_lines[0])}")
            print(f"Минимальное значение datetime: {extract_timestamp_new(unique_lines[-1])}")

        input_file = general_elk_deduplicate_path
    elif dedup_choice == "2":
        input_file = general_elk_filter_path
    else:
        print("Неверный выбор. Программа завершена.")
        return

    # Шаг 7: Запрос временного диапазона
    min_time = input("Введите минимальное значение нового временного диапазона (формат: YYYY-MM-DD HH:MM:SS.MS): ")
    max_time = input("Введите максимальное значение нового временного диапазона (формат: YYYY-MM-DD HH:MM:SS.MS): ")

    # Чтение строк из файла
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Фильтрация по временному диапазону
    filtered_by_time = [line for line in lines if min_time <= extract_timestamp_new(line) <= max_time]
    custom_elk_datetime_path = os.path.join(output_dir, 'custom_ELK_datetime_output.txt')
    write_file(custom_elk_datetime_path, filtered_by_time)
    print(f"Число записей по новым границам: {len(filtered_by_time)}")
    print(f'Результат сохранён в файл "{custom_elk_datetime_path}"')

    if filtered_by_time:
        print(f"Минимальное значение нового временного диапазона: {extract_timestamp_new(filtered_by_time[-1])}")
        print(f"Максимальное значение нового временного диапазона: {extract_timestamp_new(filtered_by_time[0])}")

if __name__ == "__main__":
    parsing_easy()