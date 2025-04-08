from menu import main_menu

def continue_work():
     while True: # Бесконечный цикл для многократного возврата в начало программы
         print("\nЧтобы вернуться в начало программы, нажмите 1")
         print("Чтобы завершить программу, нажмите 0")

         choice_continue = input("Укажите ваш выбор: ")
         print("\n________________________________________________________________________________________________")

         if choice_continue == "1":
             return True
         elif choice_continue == "0":
             print("Программа завершена.")
             return False
         else:
             print("Неверный выбор. Программа завершена.")

if __name__ == "__main__":
    while True:     # Основной цикл программы
        main_menu()
        if not continue_work():
            break   # Выход из цикла при выборе "2"
