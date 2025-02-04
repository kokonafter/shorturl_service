# shorturl_service

Short URL Service — это REST API для создания коротких ссылок. Реализован с использованием **FastAPI** и базы данных **SQLite**, с поддержкой контейнеризации через **Docker**.

---

## Функциональность
- **Сокращение URL** — создание короткой ссылки.
- **Редирект** — перенаправление на полный URL по короткой ссылке.
- **Статистика переходов** — подсчет кликов по каждой ссылке.
- **Истечение срока действия** — возможность указать срок действия для ссылки.
- **Удаление устаревших ссылок** — автоматическое удаление неактуальных записей.

---

## Установка и запуск

### Локально
1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/kokonafter/shorturl_service.git
   cd shorturl_service
2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
3. **Запустите сервер:**
   ```bash
   uvicorn main:app --reload
4. **Откройте документацию API:**
Swagger UI: http://127.0.0.1:8001/docs
Redoc: http://127.0.0.1:8001/redoc

---

### Через Docker
1. **Соберите Docker-образ:**
   ```bash
   docker build -t shorturl-service .
2. **Запустите контейнер:**
   ```bash
   docker run -d -p 8000:8001 -v shorturl_data:/app/data shorturl-service

---

## Эндпоинты
- **Основные маршруты**
  | Метод  | URL                 | Описание                       |
  |--------|---------------------|--------------------------------|
  | POST   | `/shorten`          | Создать короткую ссылку        |
  | GET    | `/{short_id}`       | Редирект по короткой ссылке    |
  | GET    | `/stats/{short_id}` | Получить статистику по ссылке  |
  | DELETE | `/cleanup`          | Получить статистику по ссылке  |


- **Пример создания короткой ссылки**
POST /shorten
**Тело запроса:**
  ```json
  {
    "url": "https://example.com"
  }
**Ответ:**
   ```json
  {
  "short_url": "http://127.0.0.1:8000/abc123",
  "expires_at": "2025-01-15T00:00:00"
}

```

---

## Структура проекта
 ```bash
shorturl_app/
├── main.py           # Основной файл приложения
├── models.py         # Модели базы данных
├── database.py       # Конфигурация базы данных
├── requirements.txt  # Зависимости проекта
├── Dockerfile        # Конфигурация Docker
└── data/             # Данные SQLite
