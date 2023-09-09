import json
import requests
from files import *


class GetDataHH:
    """
    Класс для работы ссылкой, для работы с файлом json
    """
    # Ссылка на json файл
    data_json_file = file_path_vac_hh

    true_search_fields = ['name', 'company_name', 'description']

    def __init__(self,
                 *name_vacation: list,
                 ):

        self.file_json = None

        # Название ваканскии при инициализации класса
        self.name_vacation = name_vacation
        self.search_fields = self.true_search_fields[1]
        self.file_json = self.get_data_json()

    def get_data_json(self, ):
        """
        Получение json запроса
        """
        url = 'https://api.hh.ru/vacancies?'

        par = {'text': self.name_vacation,
               'search_fields': self.search_fields,
               'only_with_salary': 'true'
               }

        response = requests.get(url=url, params=par)
        if response.status_code == 200:
            pass
        else:
            raise Exception('Запрос не выполнен')
        data_j = response.json()
        file_json = data_j
        return file_json

    def write_in_data_on_filter(self):
        """
        Используется для записи в файл для пользователя
        """
        pass

    def __iter__(self):
        pass

    def __next__(self):
        if self.name_vacation + self.step < self.stop:
            self.name_vacation += self.step
            return self.name_vacation
        else:
            raise StopIteration
