import psycopg2
from prettytable import from_db_cursor


class DBManager:
    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params
        self.conn = psycopg2.connect(dbname=database_name, **params)

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                    SELECT company_name_from_search, COUNT(*) AS list_count_vac_in_cmpn
                    FROM vacancy
                    INNER JOIN company USING (company_id)
                    GROUP BY company_name_from_search
                    ORDER BY COUNT(*);
                    """
            )
            mytable = from_db_cursor(cursor=cur)
            self.conn.close()
            return mytable

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy_name, company_name, CONCAT(salary_from, '-', salary_to) 
                AS salary, vacancy_url, company_name_from_search
                from vacancy
                INNER JOIN company USING (company_id);
                """
            )
            mytable = from_db_cursor(cursor=cur)
            self.conn.close()
            return mytable

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy_name, (salary_from + salary_to)/2 AS salary
                FROM vacancy
                """
            )
            mytable = from_db_cursor(cursor=cur)
            self.conn.close()
            return mytable

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy_name, (COALESCE(salary_from,0) + COALESCE(salary_to,0))/2 AS sum_salary_avg
                FROM vacancy
                WHERE (COALESCE(salary_from,0) + COALESCE(salary_to,0))/2 > 
                (
                    SELECT AVG((salary_from + salary_to)/2) FROM vacancy
                )
                ORDER BY sum_salary_avg;
                """
            )
            mytable = from_db_cursor(cursor=cur)
            self.conn.close()
            return mytable

    def get_vacancies_with_keyword(self, word_search: str):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT vacancy_name
                FROM vacancy
                WHERE vacancy_name LIKE '%{word_search}%';
                """
                )
            mytable = from_db_cursor(cursor=cur)
            self.conn.close()
            return mytable
