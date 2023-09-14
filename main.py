import psycopg2
import os
from src import class_dbmanager, class_getdata, function, config

def main():
    print("Привет! Напиши компании, которые тебя интересуют")
    list_user = ["Юнипро", "СберБанк", "РОСАТОМ", "Газпром нефть", "Азбука вкуса", "МегаФон", "Магнит", "Bayer", "Зарубежнефть", "Металлоинвест"]
    # list_user = input().split(" ")
    # print(list_user.split(" "))
    print(
        "1: Создать базу данных",
        "2: Если создана база данных нажми сюда",
        "3: Узнать названия созданных баз данных"
        , sep="\n"
    )
    choise_user = int(input("Введите цифру: "))
    if choise_user == 1:
        data_vac_hh = class_getdata.GetDataHH(list_user)
        db_name = input("Введите название новой базы данных\n")
        par = config.config()
        function.create_database(db_name, params=par)
        for x in data_vac_hh:
            x
        list_data_in_request = data_vac_hh.list_data
        function.write_in_database(list_data_in_request, db_name, params=par)
    elif choise_user == 2:
        db_name = input("Введите название базы данных\n")
        while True:
            print(
                "1: Получает список всех компаний и количество вакансий у каждой компании.",
                "2: Получает список всех вакансий с указанием названия компании, "
                "названия вакансии и зарплаты и ссылки на вакансию.",
                "3: Получает среднюю зарплату по вакансиям.",
                "4: Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.",
                "5: Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."
                "0: Закончить программу",
                sep="\n"
            )
            work_user_db = int(input("Введите цифру: "))
            par = config.config()
            db_1 = class_dbmanager.DBManager(database_name=db_name, params=par)
            if work_user_db == 1:
                exemplar_1 = db_1.get_companies_and_vacancies_count()
                print(exemplar_1)
                continue
            elif work_user_db == 2:
                exemplar_2 = db_1.get_all_vacancies()
                print(exemplar_2)
                continue
            elif work_user_db == 3:
                exemplar_3 = db_1.get_avg_salary()
                print(exemplar_3)
                continue
            elif work_user_db == 4:
                exemplar_4 = db_1.get_vacancies_with_higher_salary()
                print(exemplar_4)
                continue
            elif work_user_db == 5:
                word_search = input("Введите искомое слово")
                exemplar_5 = db_1.get_vacancies_with_keyword(word_search)
                print(exemplar_5)
                continue
            elif work_user_db == 0:
                break
    elif choise_user == 3:
        print(os.system("cd files && sudo -S -u postgres psql -c 'SELECT datname FROM pg_database;' > names_db.txt"))


if __name__ == '__main__':
    # list_company = ["Юнипро", "СберБанк", "РОСАТОМ", "Газпром нефть", "Азбука вкуса", "МегаФон", "Магнит", "Bayer", "Зарубежнефть", "Металлоинвест"]
    # q = class_get_data.GetDataHH(list_company)
    # print(q)
    # for x in q:
    #     print(x)
    #
    # db_name = 'db_hh'
    # par = config.config()
    # function.create_database(db_name, params=par)
    # q = class_get_data.GetDataHH(list_company)
    # for x in q:
    #     x
    # l = q.list_data
    # function.write_in_database(l, db_name, params=par)
    # db_1 = class_dbmanager.DBManager(database_name=db_name, params=par)
    # qw = db_1.get_vacancies_with_keyword('Аналитик')
    # qw_1 = db_1.get_vacancies_with_higher_salary()
    # print(qw)
    # print(qw_1)
    # print(len(qw))
    # print(db_1.get_companies_and_vacancies_count())
    main()