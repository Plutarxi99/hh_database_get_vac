# hh_database_get_vac
Привет! 
!!! Не забудь заполнить файл своими данным files/database_example.ini => и изменить имя файла на files/database.ini!!!

!!! Установи зависимости из <requirements.txt> !!! 

Программы получает от пользователя список компаний по которым требуется произвести запрос с сайта "https://hh.ru/".

Далее с помощью блока кода <src/function.py: create_database> cоздается база данных.

С помощью <src/function.py: write_in_database> записываются запрос полученный от  <src/class_getdata.py: GetData>.

Далее с помощью пользовательского интерфейса можно зайти в управление базой данных. И получать в терминале ввиде таблиц выборку данных.

Также <files/names_db.txt> здесь после нажатия в <main.py> ("3: Узнать названия созданных баз данных на этом устройстве",) записывается текстовый файл с вашими базами данных, которые созданы на вашем устройстве.