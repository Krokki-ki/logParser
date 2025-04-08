import os

SERVICES = [
    "ntm-alfacheck-api/alfacheck-cc",
    "ntm-alfacheck-dc-api/alfacheck-dc",
    "ntm-alfacheck-dc-api/alfacheck-grace-dc",
    "ntm-card-service-api/proportional-annual-commission",
    "ntm-card-tariffs-api/card-tariff-by-debit-account",
    "ntm-card-tariffs-api/card-tariff-by-plastic-id",
    "ntm-card-transfer-api/card-transfer-commission",
    "ntm-cash-withdrawal-commission-api/cash-withdrawal-commission",
    "ntm-installment-api/installment-cc",
    "ntm-installment-api/installment-dc-promo",
    "ntm-loyalty-program-api",
    "ntm-tariff-api/transfer-account-tariff",
    "ntm-transfer-api/transfer-account-commission",
    "ntm-transfer-api/transfer-credit-account",
    "ntm-widget-api/widget"
]

def get_services_menu():
    """Генерирует текстовое меню микросервисов"""
    menu = []
    for idx, service in enumerate(SERVICES, 1):
        menu.append(f"{idx} - {service}")
    return "\n".join(menu)