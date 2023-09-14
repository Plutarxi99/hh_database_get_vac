import psycopg2


# def close_conn(connection):
#     except (Exception, psycopg2.Error) as error:
#         print("Ошибка при работе с PostgreSQL", error)
#
#     finally:
#         if connection:
#         cursor.close()
#         connection.close()
#         print("Соединение с PostgreSQL закрыто")

class DBManager:
    # list_column_names = ['НАЗВАНИЕ ВАКАНСИИ',
    #                      'НАЗВАНИЕ КОМПАНИИ',
    #                      'ЗАРПЛАТА',
    #                      'НАЗВАНИЕ КОМПАНИИ ИЗ ЗАПРОСА',
    #                      'ССЫЛКА НА ВАКАНСИЮ']
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
            data_db = cur.fetchall()
            self.conn.close()

        # except (Exception, psycopg2.Error) as error:
        #     print("Ошибка при работе с PostgreSQL", error)
        #
        # finally:
        #     if self.conn:
        #         # cursor.close()
        #         self.conn.close()
        #         print("Соединение с PostgreSQL закрыто")
        return data_db

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy_name, company_name, CONCAT(salary_from, '-', salary_to) AS salary, vacancy_url, company_name_from_search
                from vacancy
                INNER JOIN company USING (company_id);
                """
            )
            data_db = cur.fetchall()
            self.conn.close()
        return data_db

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy_name, salary_from, salary_to
                FROM vacancy
                """
            )
            data_db = cur.fetchall()
            list_vac_sal = []
            for x in data_db:
                vac_name = x[0]
                s_from = x[1]
                s_to = x[2]
                if s_from is None:
                    tuple_s_from = (vac_name, s_to)
                    list_vac_sal.append(tuple_s_from)
                    continue
                elif s_to is None:
                    tuple_s_to = (vac_name, s_from)
                    list_vac_sal.append(tuple_s_to)
                    continue
                else:
                    tuple_ = (vac_name, round((s_from + s_to) / 2))
                    list_vac_sal.append(tuple_)
                    continue
            self.conn.close()
        return list_vac_sal

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
	                SELECT AVG(COALESCE(salary_from,0) + COALESCE(salary_to,0)) from vacancy
                )
                ORDER BY sum_salary_avg;
                """
            )
            data_db = cur.fetchall()
            self.conn.close()
        return data_db

    def get_vacancies_with_keyword(self, word_search: str):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        :return:
        """
        # Создаем список для полученных значений
        list_vac_with_keyw = []
        # Делаем кортеж из полученного слова и того слова с уменьшенным регистром
        word_rigester = (word_search, word_search.lower())
        # Запускаем цикл по получение результата из базы данных
        for word in word_rigester:
            with self.conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT vacancy_name
                    FROM vacancy
                    WHERE vacancy_name LIKE '%{word}%'
                    """
                )
                data_db = cur.fetchmany(6)
                # Делаем проверку на количество кортежей в списке, чтобы отображение было корректно
                if len(data_db) > 1:
                    for x in range(0, len(data_db), ):
                        list_vac_with_keyw.append(data_db[x])
                else:
                    list_vac_with_keyw.append(data_db[0])
        # self.conn.close()
        # close_conn(self.conn)
        return list_vac_with_keyw

    # def print_vac_header(self, column_names: list):
    #     list_column_names = ['НАЗВАНИЕ ВАКАНСИИ',
    #                          'НАЗВАНИЕ КОМПАНИИ',
    #                          'ЗАРПЛАТА',
    #                          'НАЗВАНИЕ КОМПАНИИ ИЗ ЗАПРОСА',
    #                          'ССЫЛКА НА ВАКАНСИЮ']
    #     """Печатает заголовок таблицы в консоль."""
    #     l_c_n = ', '.join(column_names)
    #     l = 'ЗАРПЛАТА, НАЗВАНИЕ КОМПАНИИ ИЗ ЗАПРОСА'
    #     print(
    #         f"| {l} ", end=" | ", sep=' | '
    #     )
    #     print(l)

