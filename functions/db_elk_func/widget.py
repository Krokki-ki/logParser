from menu import main_menu

def widget(service_name: str):
    print(f"\nПрограмма пока не умеет работать с сервисом {service_name}")
    input("Нажмите Enter для возврата в меню...")
    main_menu()