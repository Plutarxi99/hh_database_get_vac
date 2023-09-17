import json
import requests

from files import file_path_vac_hh


class GetDataHH:
    """
    Класс для работы ссылкой, для работы с файлом json
    """
    # Ссылка на json файл
    data_json_file = file_path_vac_hh
    list_data = []

    true_search_fields = ['name', 'company_name', 'description']

    def __init__(self,
                 name_vacation: list, start=0, stop=10, step=1
                 ):

        self.file_json = None

        # Название ваканскии при инициализации класса
        self.start = start
        self.step = step
        self.stop = stop
        self.value = self.start - self.step
        self.name_vacation = name_vacation
        self.search_field = self.true_search_fields[1]

    def get_data_json(self, name_company):
        """Получение json запроса"""
        url = 'https://api.hh.ru/vacancies?'

        par = {'text': name_company,
               'search_field': self.search_field,
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
    def __iter__(self):
        self.value = self.start - self.step
        return self

    def __next__(self):
        if self.value + self.step < self.stop:
            self.value += self.step
            # Возвращает запрос в json {Название компании:{json запрос}}
            self.list_data.append(
                {"company_name_from_search": self.name_vacation[self.value], "data": self.get_data_json(self.name_vacation[self.value])})

            return {self.name_vacation[self.value]: self.get_data_json(self.name_vacation[self.value])}
        else:
            raise StopIteration

    def __repr__(self):
        return (f"{self.__class__.__name__}(f'Список переданных компаний: {self.name_vacation}', \n"
                f"Область поиска: {self.search_field}'\n"
                f"Путь до файла json: {self.data_json_file}")


