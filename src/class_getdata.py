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
        """
        Получение json запроса
        """
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
        # # Запись ваканский компаний в json файл
        # self.get_attributes(file_json)
        return file_json

    # def get_attributes(self, content):
    #     """
    #     Чтение запроса и запись его в файл json
    #     """
    #     for x in range(len(content['items'])):
    #         # Название вакансии
    #         vac_name = content['items'][x]['name']
    #         # Ссылка на вакансию
    #         vac_url = content['items'][x]['alternate_url']
    #         # Что требуется при устройстве на вакансию
    #         vac_snippet = content['items'][x]['snippet']["requirement"]
    #         # Название компании работадателя
    #         vac_work_app_name = content['items'][x]['employer']['name']
    #
    #         searching_data = {'items': [{
    #             'Название ваканскии': vac_name,
    #             # 'Тип занятости': vac_employment,
    #             # 'Опыт работы': vac_experience,
    #             # 'Зарплата от': vac_salary_from,
    #             # 'Зарплата до': vac_salary_to,
    #             # 'Валюта': vac_currency,
    #             'API': 'HeadHunter',
    #             'url': vac_url,
    #             'Требования': vac_snippet,
    #             'Название компании': vac_work_app_name,
    #             # 'Адрес': vac_address
    #         }]}
    #         searching_data_app = {'items': {
    #             'Название ваканскии': vac_name,
    #             # 'Тип занятости': vac_employment,
    #             # 'Опыт работы': vac_experience,
    #             # 'Зарплата от': vac_salary_from,
    #             # 'Зарплата до': vac_salary_to,
    #             # 'Валюта': vac_currency,
    #             'API': 'HeadHunter',
    #             'url': vac_url,
    #             'Требования': vac_snippet,
    #             'Название компании': vac_work_app_name,
    #             # 'Адрес': vac_address
    #         }}
    #
    #         with open(self.data_json_file, 'r+') as f_1:
    #             try:
    #                 contic = json.load(f_1)
    #                 with open(self.data_json_file, 'r+') as file:
    #                     file_data = json.load(file)
    #                     # Объединяем всё единый формат
    #                     file_data["items"].append(searching_data_app['items'])
    #                     # Устанавливаем текущее положение файла со смещением
    #                     file.seek(0)
    #                     # преобразоваем обратно в json
    #                     json.dump(file_data, file, indent=2, ensure_ascii=False)
    #             except:
    #                 with open(self.data_json_file, "w") as file:
    #                     # Записываем данные в файл JSON
    #                     json.dump(searching_data, file, indent=2, ensure_ascii=False)

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

    def __add__(self, other):
        return self.name_vacation + other.name_vacation

#
# list_company = ["Юнипро", "СберБанк", "РОСАТОМ", "Газпром нефть", "Азбука вкуса", "МегаФон", "Магнит", "Bayer", "Зарубежнефть", "Металлоинвест"]
# #
# q = GetDataHH(list_company)
# print(q)
# for x in q:
#     print(x)
