<h1 align="center">Добро пожаловать на страницу проекта <a href="http://foodrgam.ddns.net/recipes/" target="_blank">Продуктовый помощник</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>

Данный сервис серпозволяет пользователям публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Как запустить проект локально:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Anastasia7Si/foodgram-project-react.git
cd foodgram-project-react 
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py makemigrations
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver

Клонирование базы:
```
python manage.py convert_csv_to_bd
```
К проекту подключен REDOC, в ктором можно ознакомиться с  эндпоинтами и методами, а также с примерами запросов, ответов и кода: http://localhost/api/docs/

### Запуск проекта на удалённом сервере
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Anastasia7Si/foodgram-project-react.git
cd foodgram-project-react 
```
В корне проекта создать файл .env и прописать в него свои данные.
Пример:
```
POSTGRES_DB=example
POSTGRES_USER=example_user
POSTGRES_PASSWORD=example_password
DB_HOST=example_db
DB_PORT=5432
```
Запустить проект через docker-compose:
```
docker compose -f docker-compose.yml up
```
Выполнить миграции:
```
docker compose -f docker-compose.yml exec backend python manage.py migrate
```
Создать суперюзера:
```
sudo docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
```
Собрать статику и скопировать ее:
```
docker compose -f docker-compose.yml exec backend python manage.py collectstatic
docker compose -f docker-compose.yml exec backend cp -r /app/static_backend/. /backend_static/static/
docker compose -f docker-compose.yml exec backend python manage.py convert_csv_to_bd
```
Технологии:
- Python
- Django
- Django REST Framework
- Simple JWT
- Gunicorn 
- Фронтенд-приложение на React 
- npm
- Docker
- DockerHub
- CI/CD
- GitHub Actions
- PostgreSQL
- Docker network


Автор:

- Анастасия Пушкарная(https://github.com/Anastasia7Si)

Проект доступен по адресу:
- foodrgam.ddns.net

Для входа в админку:
Почта: pu@ya.ru
Пароль: Nicole089