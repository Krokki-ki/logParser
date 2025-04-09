# -*- mode: python -*-
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Все файлы .py в подпапках
datas = [
    ('functions\\*.py', 'functions'),
    ('functions\\db_elk_func\\*.py', 'functions\\db_elk_func'),
    ('functions\\db_msos_func\\*.py', 'functions\\db_msos_func'),
    ('functions\\msos_elk_func\\*.py', 'functions\\msos_elk_func'),
    ('matchLog\\*.py', 'matchLog'),
    ('parseLogFromELK\\*.py', 'parseLogFromELK'),
    ('parseLogFromMSOS\\*.py', 'parseLogFromMSOS'),
    ('duplicate\\*.py', 'duplicate'),
    ('icon.ico', '.')
]

# Все скрытые импорты (включая menu и config_services)
hiddenimports = [
    'menu',
    'config_services',
    'tqdm',
    'functions.db_elk_func',
    'functions.db_msos_func',
    'functions.msos_elk_func',
    'matchLog.db_elk',
    'matchLog.db_msos',
    'matchLog.msos_elk',
    'matchLog.matchMenu',
    'parseLogFromELK.parsing_easy',
    'parseLogFromMSOS.parsing'
]

a