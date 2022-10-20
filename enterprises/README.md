
# Запуск

`docker-compose up --build`

Статика, миграции и пользователи загрузятся с помощью `entrypoint`

Это для удобства проверки, миграции не должны запускаться автоматически

# Пользователи

1) Админ
   username: admin
   password: admin

2) Не админ
   username: test
   password: Test123!

# Получение токена

 ```
curl --location --request POST 'http://localhost:8000/api/token/' \
--form 'username="test"' \
--form 'password="Test123!"'
```

# Прмер запроса через `curl`

```
curl --location --request GET 'http://localhost:8000/organizations/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY2MjY2NjQwLCJpYXQiOjE2NjYyNjYzNDAsImp0aSI6IjA1NzU2MGNlYTVjYzQwZDk5Mzc4NDZjOWVjZjExYzRiIiwidXNlcl9pZCI6MX0.uHcdc8l-VGQWuzFaDfeOwdbGyJe351tiTrVIFdBgc1s'
```

# Тесты

```
cd enterprises
poetry install 
poetry shell
pytest
```

# Автор

@karambaq
