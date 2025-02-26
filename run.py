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


if __name__ == "__main__":
    run()

    ## 210686