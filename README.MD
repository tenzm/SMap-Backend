
##Описание проекта
Данный проект необходим для получения данных из базы данных, их обработки и возвращения на frontend.

##Установка
####1) Сборка проекта
`sudo docker compose up --build`

####2) Ввод данных в базу данных о местоположении гидропостов
Перейдите по сслыке http://localhost:8000/docs#/hydroposts/load_hydroposts_load_hydroposts_post, выберите файл данных о местоположении гидропостов (datasets/hydroposts.txt) и нажмите Execute.

Аналогично перейдите по сслыке http://localhost:8000/docs#/hydroposts/load_meteostations_load_meteostations_post, выберите post_type = 1 и файл данных о местоположении метеостанций (datasets/meteo_data.csv) и нажмите Execute.

####1) Запустите Frontend