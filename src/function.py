import json
from typing import Any

import psycopg2
from files import file_path_vac_hh


def write_in_json(content):
    """
    Чтение запроса и запись его в файл json
    """
    for x in range(len(content['items'])):
        # Название вакансии
        vac_name = content['items'][x]['name']
        # Ссылка на вакансию
        vac_url = content['items'][x]['alternate_url']
        # Что требуется при устройстве на вакансию
        vac_snippet = content['items'][x]['snippet']["requirement"]
        # Название компании работадателя
        vac_work_app_name = content['items'][x]['employer']['name']

        searching_data = {'items': [{
            'Название ваканскии': vac_name,
            # 'Тип занятости': vac_employment,
            # 'Опыт работы': vac_experience,
            # 'Зарплата от': vac_salary_from,
            # 'Зарплата до': vac_salary_to,
            # 'Валюта': vac_currency,
            'API': 'HeadHunter',
            'url': vac_url,
            'Требования': vac_snippet,
            'Название компании': vac_work_app_name,
            # 'Адрес': vac_address
        }]}
        searching_data_app = {'items': {
            'Название ваканскии': vac_name,
            # 'Тип занятости': vac_employment,
            # 'Опыт работы': vac_experience,
            # 'Зарплата от': vac_salary_from,
            # 'Зарплата до': vac_salary_to,
            # 'Валюта': vac_currency,
            'API': 'HeadHunter',
            'url': vac_url,
            'Требования': vac_snippet,
            'Название компании': vac_work_app_name,
            # 'Адрес': vac_address
        }}

        with open(file_path_vac_hh, 'r+') as f_1:
            try:
                contic = json.load(f_1)
                with open(file_path_vac_hh, 'r+') as file:
                    file_data = json.load(file)
                    # Объединяем всё единый формат
                    file_data["items"].append(searching_data_app['items'])
                    # Устанавливаем текущее положение файла со смещением
                    file.seek(0)
                    # преобразоваем обратно в json
                    json.dump(file_data, file, indent=2, ensure_ascii=False)
            except:
                with open(file_path_vac_hh, "w") as file:
                    # Записываем данные в файл JSON
                    json.dump(searching_data, file, indent=2, ensure_ascii=False)


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о компании и вакансиях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    # cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE company
            (
                company_id SERIAL PRIMARY KEY,
                company_name_from_search VARCHAR(255) NOT NULL,
                company_url TEXT
                )
            """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancy (
                vacancy_id SERIAL PRIMARY KEY,
                company_id INT REFERENCES company(company_id),
                vacancy_name VARCHAR(255) NOT NULL,
                salary_from INT,
                salary_to INT,
                vacancy_requirement TEXT,
                vacancy_responsibility TEXT,
                vacancy_url TEXT,
                vacancy_experience VARCHAR(40),
                vacancy_employment VARCHAR(40),
                company_name VARCHAR(100)
            )
        """)

    conn.commit()
    conn.close()


def write_in_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о каналах и видео в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for company in data:
            company_data = company['data']['items'][0]
            cur.execute(
                """
                INSERT INTO company (company_name_from_search, company_url)
                VALUES (%s, %s)
                RETURNING company_id
                """,
                (company['company_name_from_search'], company_data['employer']['alternate_url'])
            )
            company_id = cur.fetchone()[0]
            # cur.execute('TRUNCATE TABLE company RESTART IDENTITY')
            vacancy_data = company['data']['items']
            for vacancy_data_items in vacancy_data:
                cur.execute(
                    """
                    INSERT INTO vacancy (company_id, vacancy_name, salary_from, salary_to, vacancy_requirement,
                    vacancy_responsibility, vacancy_url, vacancy_experience, vacancy_employment, company_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (company_id, vacancy_data_items['name'], vacancy_data_items['salary']['from'],
                     vacancy_data_items['salary']['to'],
                     vacancy_data_items['snippet']['requirement'], vacancy_data_items['snippet']['responsibility'],
                     vacancy_data_items['alternate_url'], vacancy_data_items['experience']['name'],
                     vacancy_data_items['employment']['name'],
                     vacancy_data_items['employer']['name']
                     )
                )

    conn.commit()
    conn.close()

def print_vac_header() -> None:
    """Печатает заголовок таблицы в консоль."""

    print(
        "| НАЗВАНИЕ ВАКАНСИИ                           | ПРОСМОТРОВ | ЛАЙКОВ | РЕЙТИНГ | ССЫЛКА НА ВАКАНСИЮ                               |")


def print_vac_info(video_info: dict) -> None:
    """Печатает информацию о видео в консоль в виде строки таблицы."""
    print(
        f"| {video_info['title']:<40} | {video_info['view_count']:<10} | {video_info['like_count']:<6} | {video_info['ratio']:<7} | {video_info['url']:<35} |")
