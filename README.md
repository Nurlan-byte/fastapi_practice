# FastAPI Practice

Учебный REST API на FastAPI для работы с пользователями, постами и голосами.
Проект использует PostgreSQL, SQLAlchemy ORM, Alembic для миграций и JWT-аутентификацию.

## Возможности

- регистрация пользователей;
- вход по email и паролю с выдачей JWT-токена;
- создание, чтение, обновление и удаление постов;
- поиск и пагинация постов;
- голосование за посты;
- документация API через Swagger UI.

## Стек

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic Settings
- PyJWT
- Passlib + bcrypt

## Структура проекта

```text
app/
  routers/
    auth.py      # авторизация
    post.py      # посты
    user.py      # пользователи
    vote.py      # голоса
  config.py      # настройки приложения из .env
  database.py    # подключение к базе данных
  main.py        # создание FastAPI-приложения
  models.py      # SQLAlchemy-модели
  oauth2.py      # JWT и текущий пользователь
  schemas.py     # Pydantic-схемы
  utils.py       # хеширование и проверка паролей
alembic/
  versions/      # миграции базы данных
```

## Установка

1. Создайте и активируйте виртуальное окружение:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Установите зависимости:

```powershell
pip install -r requirements.txt
```

3. Создайте файл `.env` в корне проекта:

```env
database_url=postgresql+psycopg://postgres:password@localhost:5432/fastapi
secret_key=your-secret-key
algorithm=HS256
access_token_expire_minutes=30
```

Замените `postgres`, `password` и `fastapi` на свои данные PostgreSQL.

## Миграции базы данных

Применить миграции:

```powershell
alembic upgrade head
```

Создать новую миграцию после изменения моделей:

```powershell
alembic revision --autogenerate -m "migration message"
```

## Запуск

```powershell
uvicorn app.main:app --reload
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:8000
```

Документация API:

```text
http://127.0.0.1:8000/docs
```

## Аутентификация

Для получения токена отправьте `POST /login`.

Важно: эндпоинт использует `OAuth2PasswordRequestForm`, поэтому данные нужно отправлять как form-data:

```text
username=user@example.com
password=your-password
```

В ответе вернется JWT:

```json
{
  "access_token": "token",
  "token_type": "bearer"
}
```

Для защищенных эндпоинтов передавайте токен в заголовке:

```http
Authorization: Bearer token
```

## Основные эндпоинты

| Метод | Путь | Описание | Авторизация |
| --- | --- | --- | --- |
| GET | `/` | Проверка работы API | Нет |
| POST | `/users/` | Создать пользователя | Нет |
| GET | `/users/` | Получить список пользователей | Да |
| GET | `/users/{id}` | Получить пользователя по ID | Да |
| POST | `/login` | Получить JWT-токен | Нет |
| GET | `/posts/` | Получить список постов с количеством голосов | Да |
| POST | `/posts/` | Создать пост | Да |
| GET | `/posts/{id}` | Получить пост по ID с количеством голосов | Да |
| PUT | `/posts/{id}` | Обновить пост | Да |
| DELETE | `/posts/{id}` | Удалить пост | Да |
| POST | `/votes/` | Добавить или удалить голос | Да |

## Примеры запросов

Создать пользователя:

```http
POST /users/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}
```

Создать пост:

```http
POST /posts/
Authorization: Bearer token
Content-Type: application/json

{
  "title": "My first post",
  "content": "Post content",
  "published": true
}
```

Получить посты с поиском и пагинацией:

```http
GET /posts/?limit=10&skip=0&search=fastapi
Authorization: Bearer token
```

Добавить голос:

```http
POST /votes/
Authorization: Bearer token
Content-Type: application/json

{
  "post_id": 1,
  "sign": 1
}
```

Удалить голос:

```http
POST /votes/
Authorization: Bearer token
Content-Type: application/json

{
  "post_id": 1,
  "sign": 0
}
```
