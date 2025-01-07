# shorturl_service

Short URL Service — это REST API для создания коротких ссылок. Реализован с использованием **FastAPI** и базы данных **SQLite**, с поддержкой контейнеризации через **Docker**.

---

## Функциональность
- **Создание короткой ссылки** — преобразование длинной ссылки в короткую.
- **Редирект по короткой ссылке** — перенаправление на оригинальный URL.
- **Получение статистики** — информация о кликах по ссылке.

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
Swagger UI: http://127.0.0.1:8000/docs
Redoc: http://127.0.0.1:8000/redoc

---

### Через Docker
1. **Соберите Docker-образ:**
   ```bash
   docker build -t shorturl-service .
2. **Запустите контейнер:**
   ```bash
   docker run -d -p 8000:80 -v shorturl_data:/app/data shorturl-service

---

## Эндпоинты
- **Основные маршруты**
  | Метод  | URL                 | Описание                       |
  |--------|---------------------|--------------------------------|
  | POST   | `/shorten`          | Создать короткую ссылку        |
  | GET    | `/{short_id}`       | Редирект по короткой ссылке    |
  | GET    | `/stats/{short_id}` | Получить статистику по ссылке  |



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
    "short_url": "http://127.0.0.1:8000/abc123"
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
