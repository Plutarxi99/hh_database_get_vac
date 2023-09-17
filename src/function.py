from typing import Any
import psycopg2
from psycopg2 import ProgrammingError, OperationalError


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о компании и вакансиях."""
    # Подключение к базе данных
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    # Создание базы данных
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    # Блок создания базы данных
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
                company_name VARCHAR(255)
            )
        """)

    conn.commit()
    conn.close()


def drop_database(database_name: str, params: dict):
    """Удаление базы данных."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(f"DROP DATABASE {database_name}")
        conn.close()
    except ProgrammingError:
        print('Названия базы данных не правильное')
    except OperationalError:
        print('Названия базы данных правильное. Закройте соединение с ней')


def write_in_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о вакансиях в базу данных."""

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
            vacancy_data = company['data']['items']
            for vacancy_data_items in vacancy_data:

                # Если зарплаты нет в одной из ячейки, то она дублируется в отсутствующую ячейку
                vac_from = vacancy_data_items['salary']['from']
                vac_to = vacancy_data_items['salary']['to']
                if vac_from is None:
                    vac_from = vac_to
                elif vac_to is None:
                    vac_to = vac_from

                cur.execute(
                    """
                    INSERT INTO vacancy (company_id, vacancy_name, salary_from, salary_to, vacancy_requirement,
                    vacancy_responsibility, vacancy_url, vacancy_experience, vacancy_employment, company_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (company_id, vacancy_data_items['name'],
                     vac_from,
                     vac_to,
                     vacancy_data_items['snippet']['requirement'], vacancy_data_items['snippet']['responsibility'],
                     vacancy_data_items['alternate_url'], vacancy_data_items['experience']['name'],
                     vacancy_data_items['employment']['name'],
                     vacancy_data_items['employer']['name']
                     )
                )

    conn.commit()
    conn.close()
