# Проект MDM на Django
Небольшой учебный проект по веденнию справочников.

## Составляющие:

1. `meta_app` - приложениие для описания основных метаданных справочников

## TODO

`# TODO: Локализация` - Для последующей локализации

## Порядок миграций

python manage.py makemigrations user_app
python manage.py migrate auth
python manage.py migrate user_app
python manage.py migrate
python manage.py makemigrations meta_app
python manage.py migrate meta_app
python manage.py makemigrations dynamic_tables_app
python manage.py migrate dynamic_tables_app