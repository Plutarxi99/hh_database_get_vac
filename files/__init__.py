import os
import pathlib

# Создаем абсолютный путь до папки с файлами
script_dir = os.path.dirname(__file__)


file_path_vac_hh = (pathlib.PurePath(f'{script_dir}')
        .joinpath('vacation_on_hh.json'))
"""
HeadHunter
Создаем путь до нужного файла,
где хранятся записанные ваканскии с заданными параметрами
"""

file_path_db_init = (pathlib.PurePath(f'{script_dir}')
        .joinpath('database.ini'))
"""
Путь до файла с данным для подключения к базе данных
"""