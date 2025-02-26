from collections import Counter

# Программа считывает файл, затем сортирует и убирает дубли
def read_file(filename):
    """Чтение строк из файла."""
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]


def write_file(filename, lines):
    """Запись строк в файл."""
    with open(filename, 'w') as file:
        file.write('\n'.join(lines))


def process_lines(lines):
    """Обработка строк: сортировка, удаление дубликатов, вывод статистики."""
    # Подсчёт общего числа строк до обработки
    total_lines = len(lines)
    print(f"Общее число строк до обработки: {total_lines}")

    # Удаление дубликатов и подсчёт их количества
    counter = Counter(lines)
    duplicates = {line: count for line, count in counter.items() if count > 1}

    # Сортировка строк от большего к меньшему
    sorted_lines = sorted(lines, reverse=True)

    if duplicates:
        print(f"Найдено дубликатов строк: {len(duplicates)}")
        # Удаление дубликатов
        unique_lines = list(counter.keys())
        # Запись уникальных строк в файл
        write_file("deduplicated_strings.txt", sorted(unique_lines, reverse=True))
        print(f"Число строк без дубликатов: {len(unique_lines)}")
    else:
        print("Дубликаты не найдены.")
        print(f"Число строк: {len(lines)}")

    # Вывод максимального и минимального значения
    print(f"Максимальное значение: {max(lines)}")
    print(f"Минимальное значение: {min(lines)}")


def duplicate():
    input_file = "initial_input_datetime.txt"
    lines = read_file(input_file)

    if not lines:
        print("Файл пуст или содержит только пустые строки.")
        return

    process_lines(lines)


if __name__ == "__main__":
    duplicate()