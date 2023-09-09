import psycopg2

from src import class_dbmanager, class_get_data, function, config


if __name__ == '__main__':
    list_company = ["Юнипро", "СберБанк", "РОСАТОМ", "Газпром нефть", "Азбука вкуса", "МегаФон", "Магнит", "Bayer", "Зарубежнефть", "Металлоинвест"]
    # q = class_get_data.GetDataHH(list_company)
    # print(q)
    # for x in q:
    #     print(x)

    db_name = 'db_hh'
    par = config.config()
    function.create_database(db_name, params=par)
    q = class_get_data.GetDataHH(list_company)
    for x in q:
        x
    l = q.list_data
    function.write_in_database(l, db_name, params=par)
