from .db_msos import match_DB_MSOS
from .db_elk import match_DB_ELK
from .msos_elk import match_MSOS_ELK

def match_menu():
    """Основная функция модуля сравнения"""
    while True:
        print("\n" + "="*40)
        print("МЕНЮ СРАВНЕНИЯ ЛОГОВ".center(40))
        print("1 - Сравнение БД и Marathon")
        print("2 - Сравнение БД и Kibana")
        print("3 - Сравнение Marathon и Kibana")
        print("0 - Возврат в главное меню")
        print("Enter - Выход из программы")

        choice = input("Укажите ваш выбор: ").strip()

        if choice == "1":
            match_DB_MSOS()
        elif choice == "2":
            match_DB_ELK()
        elif choice == "3":
            match_MSOS_ELK()
        elif choice == "0":
            return  # Корректный выход в главное меню
        elif not choice:  # Обработка пустой строки (Enter)
            print("\nПрограмма завершена.")
            exit()
        else:
            print("\nНеверный ввод. Пожалуйста, укажите правильный вариант")
            continue  # Повторяем цикл

            # После выполнения операции снова показываем меню
        print("\n" + "=" * 50)  # Разделитель для улучшения читаемости

if __name__ == "__main__":
    match_menu()