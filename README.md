<h1 align="center">Hi there, I'm <a href="https://vk.com/plutarxi99" target="_blank">Plutarx</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
<h3 align="center">Работяга с завода, который пытается освоить IT-сферу &#x1f527</h3>

[![trophy](https://github-profile-trophy.vercel.app/?username=plutarxi99)](https://github.com/ryo-ma/github-profile-trophy)

&#10071;&#10071;&#10071; Не забудь заполнить файл своими данным files/database_example.ini => и изменить имя файла на files/database.ini &#10071;&#10071;&#10071;

&#10071;&#10071;&#10071; Установи зависимости из <requirements.txt> &#10071;&#10071;&#10071;

Программы получает от пользователя список компаний по которым требуется произвести запрос с сайта "https://hh.ru/".

Далее с помощью блока кода <src/function.py: create_database> cоздается база данных.

С помощью <src/function.py: write_in_database> записываются запрос полученный от <src/class_getdata.py: GetData>.

Далее с помощью пользовательского интерфейса можно зайти в управление базой данных. И получать в терминале ввиде таблиц выборку данных.

Также <files/names_db.txt> здесь после нажатия в <main.py> ("3: Узнать названия созданных баз данных на этом устройстве",) записывается текстовый файл с вашими базами данных, которые созданы на вашем устройстве.
