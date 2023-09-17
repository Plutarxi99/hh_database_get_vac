import os

from src import class_dbmanager, class_getdata, function, config


def main():
    while True:
        print("Привет! Используй программу с удовольствием.",
              "Следуй дальнейшим подсказам и у тебя получиться её использовать.",
              "Не забудь заполнить файл своими данным files/database_example.ini =>",
              "=> и изменить имя файла на files/database.ini\n",
              sep="\n")
        print(
            "1: Дописать в базу данных новые данные",
            "2: Получения данных из базы данных",
            "3: Узнать названия созданных баз данных на этом устройстве",
            "4: Удалить базу данных",
            "5: Создать базу данных",
            "0: Закончить программу",
            sep="\n")
        choise_user = int(input("Введите цифру: "))
        # Получаем данные для подключения к базе данных
        # с помощью files/database.ini
        par = config.config()
        if choise_user == 1:
            print("Привет! Напиши компании, которые тебя интересуют")
            # list_user = str(input()).split(" ")
            list_user = ['дорога', 'вкусно и точка']
            # Отправляем список в класс для получения данных
            data_vac_hh = class_getdata.GetDataHH(list_user, stop=len(list_user))
            # Делаем итерацию в классе и получаем список данных
            # for x in data_vac_hh:
            #     x
            iter_class = [x for x in data_vac_hh]
            # iter_class = [x for x in data_vac_hh]
            list_data_in_request = data_vac_hh.list_data
            # Пользователь вводит названия базы данных
            db_name = input("Введите название базы данных куда хотите записать\n")
            # Записываем в базу данных полученные данные вакансий
            function.write_in_database(list_data_in_request, db_name, params=par)
            continue

        elif choise_user == 2:
            # Блок управления базой данных
            db_name = input("Введите название базы данных\n")
            while True:
                print(
                    "1: Список всех компаний и количество вакансий у каждой компании.",
                    "2: Список всех вакансий с указанием названия компании, "
                    "названия вакансии и зарплаты и ссылки на вакансию.",
                    "3: Получает среднюю зарплату по вакансиям.",
                    "4: Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.",
                    "5: Получает список всех вакансий, в названии которых содержатся "
                    "переданные в метод слова",
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
                    word_search = str(input("Введите искомое слово"))
                    exemplar_5 = db_1.get_vacancies_with_keyword(word_search)
                    print(exemplar_5)
                    continue
                elif work_user_db == 0:
                    break

        elif choise_user == 3:
            os.system("cd files && sudo -S -u postgres psql -c 'SELECT datname FROM pg_database;' > names_db.txt")
            with open('files/names_db.txt', encoding='UTF-8') as f:
                print(f.read())
            input("Нажми Enter, чтобы продолжить")
            continue

        elif choise_user == 4:
            db_n_for_drop = str(input("Введите названия базы данных"))
            function.drop_database(database_name=db_n_for_drop, params=par)
            continue

        elif choise_user == 5:
            # Пользователь вводит названия базы данных
            db_name = input("Введите название новой базы данных\n")
            # Создаем базу данных
            function.create_database(db_name, params=par)
            continue
        elif choise_user == 0:
            print("Спасибо за использование программы")
            break


if __name__ == '__main__':
    main()
