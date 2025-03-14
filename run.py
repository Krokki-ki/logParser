from parseLogFromMSOS.parsing import parsing
from parseLogFromELK.parsing_easy import parsing_easy


def run():
    print("Чтобы выбрать режим обработки логов из Marathon, нажмите 1")
    print("Чтобы выбрать режим обработки логов из ELK, нажмите 2")

    choice = input("Укажите ваш выбор: ")

    if choice == "1":
        parsing()
    elif choice == "2":
        parsing_easy()
    else:
        print("Неверный выбор. Программа завершена.")

def continue_work():
     while True: # Бесконечный цикл для многократного возврата в начало программы
         print("\nЧтобы вернуться в начало программы, нажмите 1")
         print("Чтобы завершить программу, нажмите 2")

         choice_continue = input("Укажите ваш выбор: ")
         print("\n________________________________________________________________________________________________")

         if choice_continue == "1":
             return True
         elif choice_continue == "2":
             print("Программа завершена.")
             return False
         else:
             print("Неверный выбор. Программа завершена.")




if __name__ == "__main__":
    while True:     # Основной цикл программы
        run()
        if not continue_work():
            break   # Выход из цикла при выборе "2"
