# menu.py
from matchLog.matchMenu import match_menu
from parseLogFromMSOS.parsing import parsing
from parseLogFromELK.parsing_easy import parsing_easy

def main_menu():
    print("Чтобы выбрать режим обработки логов из Marathon, нажмите 1")
    print("Чтобы выбрать режим обработки логов из ELK, нажмите 2")
    print("Чтобы выбрать режим сравнения логов, нажмите 3")

    choice = input("Укажите ваш выбор: ")

    if choice == "1":
        parsing()
    elif choice == "2":
        parsing_easy()
    elif choice == "3":
        match_menu()
    else:
        print("Неверный выбор. Программа завершена.")