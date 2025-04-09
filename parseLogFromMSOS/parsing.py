import os
import re
from collections import OrderedDict
from tqdm import tqdm  # Добавлен импорт прогресс-бара

def get_input_files():
    """Получение путей к файлам от пользователя"""
    base_path = input("Введите полный путь к папке с файлами: ").strip()
    while not os.path.exists(base_path):
        print("Указанный путь не существует!")
        base_path = input("Введите полный путь к папке с файлами логов из Marathon: ").strip()

    num_files = int(input("Введите количество файлов для обработки: "))
    files_prompt = f"Укажите через запятую имена {num_files} файла(-ов) без расширения (либо имя одного файла): "
    file_names = [f"{name.strip()}.txt" for name in input(files_prompt).split(',')]

    return base_path, [os.path.join(base_path, fname) for fname in file_names]

def read_files(file_paths):
    """Чтение данных из файлов с обработкой ошибок"""
    lines = []
    for path in tqdm(file_paths, desc="Чтение файлов", unit="файл"):  # Прогресс-бар
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

def extract_timestamp(line):
    """Извлечение временной метки из строки"""
    match = re.search(r'"@timestamp":"([^"]+)"', line)
    return match.group(1) if match else None

def sort_lines_by_timestamp(lines):
    """Сортировка строк по временной метке (по убыванию)"""
    return sorted(lines, key=lambda x: extract_timestamp(x), reverse=True)

def filter_by_time_range(lines, min_time, max_time):
    """Фильтрация строк по временному диапазону"""
    return [line for line in lines if min_time <= extract_timestamp(line) <= max_time]

def process_timestamps_in_file(file_path):
    """Обработка временных меток в файле: замена T на пробел и удаление временной зоны"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    processed_lines = []
    for line in tqdm(lines, desc="Обработка временных меток", unit="строка"):  # Прогресс-бар
        # Шаг 1: Удаляем символ "T" только в подстроке, соответствующей временной метке
        line = re.sub(
            r'([0-9]{4}-[0-9]{2}-[0-9]{2})T([0-9]{2}:[0-9]{2}:[0-9]{2})(\.[0-9]+)?\+[0-9]{2}:[0-9]{2}',
            r'\1 \2\3',
            line
        )
        # Шаг 2: Удаляем временную зону "+ZZ:ZZ" только в подстроке, соответствующей временной метке
        line = re.sub(
            r'([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?)\+[0-9]{2}:[0-9]{2}',
            r'\1',
            line
        )
        processed_lines.append(line)

    # Перезаписываем файл с обработанными строками
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)

def parsing():
    # Шаг 1: Получение и обработка файлов
    base_path, file_paths = get_input_files()

    # Создаём папку MSOS_output, если её нет
    output_dir = os.path.join(base_path, "MSOS_output")
    os.makedirs(output_dir, exist_ok=True)

    # Шаг 2: Создание общего файла
    all_lines = read_files(file_paths)
    general_msos_path = os.path.join(output_dir, 'general_MSOS.txt')
    write_file(general_msos_path, all_lines)
    print("Группировка указанных файлов завершена.")

    # Обработка временных меток в файле general_MSOS.txt
    process_timestamps_in_file(general_msos_path)

    # Шаг 2.3: Подсчёт числа строк и вывод на консоль
    with open(general_msos_path, 'r', encoding='utf-8') as f:
        general_MSOS_lines = f.readlines()
    print(f"Общее число записей в объединённом файле: {len(general_MSOS_lines)}")
    print(f'Результат сохранён в файл "{general_msos_path}"')

    # Шаг 2.4: Запрос строки для фильтрации
    filter_str = input("\nВведите строку для фильтрации (например 'GET method /installment-dc-promo, request ='): ")

    # Шаг 2.5: Фильтрация строк
    filtered_lines = filter_lines(general_MSOS_lines, filter_str)
    general_msos_filter_path = os.path.join(output_dir, 'general_MSOS_filter.txt')
    write_file(general_msos_filter_path, filtered_lines)
    print(f"Число записей по указанному фильтру: {len(filtered_lines)}")
    print(f'Результат сохранён в файл "{general_msos_filter_path}"')

    # Шаг 2.6: Сортировка строк по временной метке
    sorted_lines = sort_lines_by_timestamp(filtered_lines)
    write_file(general_msos_filter_path, sorted_lines)

    # Вывод первой и последней временной метки
    if sorted_lines:
        print(f"Максимальное значение: {extract_timestamp(sorted_lines[0])}")
        print(f"Минимальное значение: {extract_timestamp(sorted_lines[-1])}")

    # Шаг 3: Запрос на проверку дубликатов
    dedup_choice = input("\nВы хотите выполнить проверку на дубли записей?\n1 - Да, 2 - Нет\n")
    if dedup_choice == "1":
        # Шаг 4: Удаление дубликатов
        unique_lines = deduplicate(sorted_lines)
        general_msos_deduplicate_path = os.path.join(output_dir, 'general_MSOS_filter_deduplicate.txt')
        write_file(general_msos_deduplicate_path, unique_lines)
        print(f"Число уникальных записей: {len(unique_lines)}")
        print(f'Результат сохранён в файл "{general_msos_deduplicate_path}"')

        # Вывод первой и последней временной метки после дедубликации
        if unique_lines:
            print(f"Максимальное значение: {extract_timestamp(unique_lines[0])}")
            print(f"Минимальное значение: {extract_timestamp(unique_lines[-1])}")

        # Шаг 5: Фильтрация по временному диапазону
        input_file = general_msos_deduplicate_path
    elif dedup_choice == "2":
        input_file = general_msos_filter_path
    else:
        print("Неверный выбор. Программа завершена.")
        return

    # Шаг 5.1: Запрос временного диапазона
    min_time = input("Введите минимальное значение нового временного диапазона (формат: YYYY-MM-DD HH:MM:SS.MS): ")
    max_time = input("Введите максимальное значение нового временного диапазона (формат: YYYY-MM-DD HH:MM:SS.MS): ")

    # Чтение строк из файла
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Фильтрация по временному диапазону
    filtered_by_time = filter_by_time_range(lines, min_time, max_time)
    custom_msos_datetime_path = os.path.join(output_dir, 'custom_MSOS_datetime_output.txt')
    write_file(custom_msos_datetime_path, filtered_by_time)
    print(f"Число записей по новым границам: {len(filtered_by_time)}")
    print(f'Результат сохранён в файл "{custom_msos_datetime_path}"')

    # Вывод минимального и максимального значения нового диапазона
    if filtered_by_time:
        print(f"Минимальное значение нового временного диапазона: {extract_timestamp(filtered_by_time[-1])}")
        print(f"Максимальное значение нового временного диапазона: {extract_timestamp(filtered_by_time[0])}")

if __name__ == "__main__":
    parsing()