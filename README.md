<h1 align="center">Добро пожаловать на страницу проекта <a href="" target="_blank">Продуктовый помощник</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>

Данный сервис серпозволяет пользователям публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

К проекту подключен REDOC, в ктором можно ознакомиться с  эндпоинтами и методами, а также с примерами запросов, ответов и кода: http://localhost/api/docs/

Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
git clone git@github.com:Anastasia7Si/foodgram-project-react.git
cd foodgram-project-react 

Cоздать и активировать виртуальное окружение:
python -m venv venv
source venv/Scripts/activate

Установить зависимости из файла requirements.txt:
pip install -r requirements.txt

Выполнить миграции:
python manage.py makemigrations
python manage.py migrate

Запустить проект:
python manage.py runserver

Клонирование базы:
python manage.py convert_csv_to_bd

Технологии:

Python 3.7
Django 3.2
Django REST framework 3.12
Simple JWT 4.7.2


Автор:

- Анастасия Пушкарная(https://github.com/Anastasia7Si)
