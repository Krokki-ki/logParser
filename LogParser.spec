# LogParser.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Абсолютный путь к корневой папке проекта
base_dir = 'D:/Python Projects/logParser'

a = Analysis(
    [f'{base_dir}/run.py'],  # Точка входа
    pathex=[base_dir],  # Пути для поиска модулей
    binaries=[],  # Бинарные файлы (если есть)
    datas=[  # Включаем все необходимые файлы и папки
        (f'{base_dir}/icon.ico', '.'),  # Иконка
        (f'{base_dir}/config_services.py', '.'),  # Конфигурационный файл
        (f'{base_dir}/functions/*.py', 'functions'),  # Файлы из functions
        (f'{base_dir}/functions/db_elk_func/*.py', 'functions/db_elk_func'),  # Подпакет
        (f'{base_dir}/functions/db_msos_func/*.py', 'functions/db_msos_func'),
        (f'{base_dir}/functions/msos_elk_func/*.py', 'functions/msos_elk_func'),
        (f'{base_dir}/matchLog/*.py', 'matchLog'),  # Модули matchLog
        (f'{base_dir}/parseLogFromELK/*.py', 'parseLogFromELK'),  # Парсинг ELK
        (f'{base_dir}/parseLogFromMSOS/*.py', 'parseLogFromMSOS'),  # Парсинг MSOS
        (f'{base_dir}/duplicate/*.py', 'duplicate'),  # Папка duplicate
        (f'{base_dir}/__init__.py', '.'),  # Необходимый __init__.py
    ],
    hiddenimports=[  # Скрытые зависимости
        'menu',  # Модуль menu.py
        'config_services',  # config_services.py
        'tqdm',  # Прогресс-бар
        'functions.db_elk_func',  # Подпакеты
        'functions.db_msos_func',
        'functions.msos_elk_func',
        'matchLog.matchMenu',  # Модули из matchLog
        'parseLogFromELK.parsing_easy',  # Модули парсинга
        'parseLogFromMSOS.parsing',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LogParser',  # Имя выходного файла
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # UPX отключен по вашему требованию
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Включена консоль
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[f'{base_dir}/icon.ico'],  # Иконка
    argv_emulation=False,
)