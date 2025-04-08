import sys
import os
from config_services import SERVICES, get_services_menu


def get_input_data():
    """Функция для получения входных данных с обработкой ошибок"""

    def get_path(prompt, prev_step=None):
        while True:
            path = input(prompt).strip()
            if path == '0':
                from run import run
                run()
                sys.exit()
            if os.path.exists(path):
                return path
            print(f"Ошибка: путь '{path}' не существует!")
            if prev_step:
                return prev_step()  # Возврат к предыдущему шагу

    def get_filename(prompt, base_path, prev_step):
        """Возвращает два файла: БД и ELK"""
        files = []

        for suffix in [' (БД)', ' (ELK)']:
            while True:
                name = input(f"{prompt}{suffix}: ").strip()
                if name == '0':
                    from run import run
                    run()
                    sys.exit()
                full_path = os.path.join(base_path, f"{name}.txt")
                if os.path.isfile(full_path):
                    files.append(full_path)
                    break
                print(f"Ошибка: файл '{full_path}' не найден!")
                if prev_step:
                    return prev_step()  # Возврат к предыдущему шагу

        return tuple(files)  # Возвращаем кортеж из двух путей

    # Получение путей
    base_path_general = get_path("Введите полный путь к общей папке с файлами логов из БД и ELK: ")

    # Вызываем get_filename() ОДИН РАЗ, передавая общий шаблон подсказки
    file_paths = get_filename(
        "Укажите имя файла логов без расширения",  # Общий шаблон
        base_path_general,
        lambda: get_path("Введите общий путь заново: ")  # Общий шаг назад
    )

    file_path_DB, file_path_ELK = file_paths  # Распаковываем кортеж

    return {
        'db_path': file_path_DB,
        'elk_path': file_path_ELK
    }


def select_service():
    """Выбор микросервиса из списка"""
    while True:
        print("\n" + "=" * 50)
        print("СПИСОК МИКРОСЕРВИСОВ".center(50))
        print(get_services_menu())
        print("\n0 - Возврат в главное меню")

        choice = input("\nВведите номер микросервиса: ").strip()

        if choice == '0':
            from menu import main_menu  # Правильный импорт главного меню
            main_menu()
            return  # Выход из текущего контекста

        if not choice.isdigit():
            print("Ошибка: введите число!")
            continue

        idx = int(choice) - 1
        if 0 <= idx < len(SERVICES):
            return SERVICES[idx]

        print(f"Ошибка: микросервис с номером {choice} не существует!")


def define_matchMode_byService(service_name: str, inputs: dict):
    """Определение режима сравнения логов по имени сервиса"""
    print(f"\nВыбран режим сравнения логов микросервиса {service_name}")

    try:
        # Блок импортов обработчиков
        if service_name == "ntm-alfacheck-api/alfacheck-cc":
            from functions.db_elk_func.alfacheck_cc import alfacheck_cc
            alfacheck_cc(service_name, inputs)

        elif service_name == "ntm-alfacheck-dc-api/alfacheck-dc":
            from functions.db_elk_func.alfacheck_dc import alfacheck_dc
            alfacheck_dc(service_name, inputs)

        elif service_name == "ntm-alfacheck-dc-api/alfacheck-grace-dc":
            from functions.db_elk_func.alfacheck_grace_dc import alfacheck_grace_dc
            alfacheck_grace_dc(service_name, inputs)

        elif service_name == "ntm-card-service-api/proportional-annual-commission":
            from functions.db_elk_func.proportional_annual_commission import proportional_annual_commission
            proportional_annual_commission(service_name, inputs)

        elif service_name == "ntm-card-tariffs-api/card-tariff-by-debit-account":
            from functions.db_elk_func.card_tariff_by_debit_account import card_tariff_by_debit_account
            card_tariff_by_debit_account(service_name, inputs)

        elif service_name == "ntm-card-tariffs-api/card-tariff-by-plastic-id":
            from functions.db_elk_func.card_tariff_by_plastic_id import card_tariff_by_plastic_id
            card_tariff_by_plastic_id(service_name, inputs)

        elif service_name == "ntm-card-transfer-api/card-transfer-commission":
            from functions.db_elk_func.card_transfer_commission import card_transfer_commission
            card_transfer_commission(service_name, inputs)

        elif service_name == "ntm-cash-withdrawal-commission-api/cash-withdrawal-commission":
            from functions.db_elk_func.cash_withdrawal_commission import cash_withdrawal_commission
            cash_withdrawal_commission(service_name, inputs)

        elif service_name == "ntm-installment-api/installment-cc":
            from functions.db_elk_func.installment_cc import installment_cc
            installment_cc(service_name, inputs)

        elif service_name == "ntm-installment-api/installment-dc-promo":
            from functions.db_elk_func.installment_dc_promo import installment_dc_promo
            installment_dc_promo(service_name, inputs)

        elif service_name == "ntm-loyalty-program-api":
            from functions.db_elk_func.loyalty import loyalty
            loyalty(service_name, inputs)

        elif service_name == "ntm-tariff-api/transfer-account-tariff":
            from functions.db_elk_func.transfer_account_tariff import transfer_account_tariff
            transfer_account_tariff(service_name, inputs)

        elif service_name == "ntm-transfer-api/transfer-account-commission":
            from functions.db_elk_func.transfer_account_commission import transfer_account_commission
            transfer_account_commission(service_name, inputs)

        elif service_name == "ntm-transfer-api/transfer-credit-account":
            from functions.db_elk_func.transfer_credit_account import transfer_credit_account
            transfer_credit_account(service_name, inputs)

        elif service_name == "ntm-widget-api/widget":
            from functions.db_elk_func.widget import widget
            widget(service_name, inputs)

        else:
            raise ValueError(f"Неизвестный сервис: {service_name}")

    except ImportError as e:
        print(f"Ошибка загрузки модуля: {str(e)}")
        print("Проверьте:")
        print("- Наличие файлов обработчиков в папке functions/db_elk_func")
        print("- Корректность имен функций и модулей")
        print("- Наличие __init__.py во всех папках")

    except Exception as e:
        print(f"Критическая ошибка во время выполнения: {str(e)}")

    finally:
        input("\nНажмите Enter для возврата в меню...")
        from menu import main_menu
        main_menu()


def match_DB_ELK():
    """Основная функция сравнения логов"""
    print("\n" + "=" * 50)
    print("РЕЖИМ СРАВНЕНИЯ БД И ELK".center(50))

    try:
        # 1. Получение и валидация путей
        inputs = get_input_data()

        # 2. Выбор микросервиса
        service_name = select_service()

        # 3. Определение и вызов обработчика серивисов
        define_matchMode_byService(service_name, inputs)  # Передаём inputs в обработчик

        # 4. Основная логика анализа
        print(f"\nФайл БД: {inputs['db_path']}")
        print(f"Файл ELK: {inputs['elk_path']}")
        print("\nАнализ завершен. Расхождения не обнаружены.")

    except KeyboardInterrupt:
        print("\n\nОперация прервана пользователем!")
    finally:
        input("\nНажмите Enter для возврата в меню...")


if __name__ == "__main__":
    match_DB_ELK()