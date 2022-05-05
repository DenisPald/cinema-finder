## ЗАПУСК ##
Запуск происходит при помощи docker network и проводится в 2 этапа - первоначальная настройка(проводится один раз) и дальнейший запуск

### НАСТРОЙКА ###
Для начала переименуйте .env.example в .env, и заполните файл по описанной внутри инструкции
Далее расмотрим отдельно настройку апи и бота
#### АПИ ####
Создадим docker network - `docker network create cinema-finder-network`
Запустим в сети postgres - `docker run --name postgres -e POSTGRES_PASSWORD=<пароль который вы указали в .env> -p 5432:5432 --network cinema-finder-network -d docker.io/postgres:alpine  `
Соберем локально image нашего flask приложения - `docker build -f DockerfileAPI -t cinema-finder-api `
Запустим flask - `docker run --name cinema-finder-api --network cinema-finder-network -p 5000:5000 cinema-finder-api`

Теперь у нас есть обычное flask приложение с postgres базой данных с хостом на 0.0.0.0:5000

#### БОТ ####
Соберем локально image нашего бота - `docker build -f DockerfileBOT -t cinema-finder-bot` 
Запускаем - `docker run --name cinema-finder-bot cinema-finder-bot`
Или, если доступ к апи нужно получить локально(не забудьте указать в .env) - `docker run --name cinema-finder-bot --network cinema-finder-network cinema-finder-bot`

### ЗАПУСК ###
postgres - `docker start postgres`
api - `docker start cinema-finder-api`
bot - `docker start cinema-finder-bot`
