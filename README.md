# Warehouse

В корне проекта делаем подготовительные запросы и инициализируем БД
```
python manage.py makemigrations api
python manage.py migrate
python manage.py createsuperuser
```

Запускаем проект
```
python manage.py runserver
```

доступные ссылки на API  
    "user": "http://localhost:8000/user/",
    "warehouses": "http://localhost:8000/warehouses/",
    "goods": "http://localhost:8000/goods/",
    "inventory": "http://localhost:8000/inventory/"

Логинемся под суперпользователем, которого мы создали и создаем два user с двумя разными признаками: Либо provider, либо customer. 
Создаем как минимум один warehouses и goods. 
Переходим на вкладку inventory и там доступны два действия: Supply и Withdraw

