
from src import class_dbmanager, class_get_data

if __name__ == '__main__':
    list_company = ["Юнипро", "СберБанк", "РОСАТОМ", "Газпром нефть", "Okko", "NVIDIA", "Huawei", "Bayer", "Зарубежнефть", "Usetech"]
    data = class_get_data.GetDataHH(list_company)
    print(data.get_data_json())