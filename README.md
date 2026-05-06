<div align="center">

# 🏔️ TravelKG

### Платформа для путешествий по Кыргызстану

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-REST_API-red?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![CI/CD](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)

<br/>

> 🌿 Откройте для себя красоту Кыргызстана — горы, озёра, юрты и приключения ждут вас!

</div>

---

## 📌 О проекте

**TravelKG** — это веб-платформа для планирования и бронирования путешествий по Кыргызстану. Проект объединяет туристов и местных гидов, предлагая удобный поиск туров, маршрутов и достопримечательностей по всей стране.

Проект создан командой из трёх стажёров в рамках intern-программы.

---

## ✨ Возможности

- 🗺️ Просмотр туров и маршрутов по Кыргызстану
- 🔍 Поиск и фильтрация путешествий
- 📝 Бронирование туров через REST API
- 👤 Регистрация и авторизация пользователей
- 🖼️ Галереи фотографий мест и достопримечательностей
- 🐳 Полная контейнеризация и автоматический деплой через CI/CD

---

## 🛠️ Технологический стек

| Слой             | Технология                        |
|------------------|-----------------------------------|
| Backend          | Python 3.11+, Django 4.x          |
| API              | Django REST Framework             |
| Frontend         | JavaScript (ES6+), CSS3, HTML5    |
| Контейнеризация  | Docker, Docker Compose            |
| CI/CD            | GitHub Actions                    |

---

## 🚀 Быстрый старт

### Предварительные требования

Убедись, что установлены:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Установка и запуск

```bash
# 1. Клонируй репозиторий
git clone https://github.com/SalahidinAI/TravelKG.git
cd TravelKG

# 2. Создай файл переменных окружения
cp .env.example .env
# Отредактируй .env под свои настройки

# 3. Запусти контейнеры
docker compose up -d --build

# 4. Примени миграции
docker compose exec web python manage.py migrate

# 5. Загрузи начальные данные (опционально)
docker compose exec web python manage.py loaddata fixtures/initial_data.json

# 6. Создай суперпользователя
docker compose exec web python manage.py createsuperuser
```

Приложение будет доступно по адресу: **http://localhost:8000**  
Панель администратора: **http://localhost:8000/admin**

---

## ⚙️ Переменные окружения

Создай файл `.env` в корне проекта:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=travelkg_db
POSTGRES_USER=travelkg_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

## 📡 API Endpoints

| Метод    | URL                          | Описание                        |
|----------|------------------------------|---------------------------------|
| `GET`    | `/api/tours/`                | Список всех туров               |
| `GET`    | `/api/tours/{id}/`           | Детали тура                     |
| `POST`   | `/api/tours/{id}/book/`      | Забронировать тур               |
| `GET`    | `/api/places/`               | Список достопримечательностей   |
| `GET`    | `/api/places/{id}/`          | Детали места                    |
| `POST`   | `/api/auth/register/`        | Регистрация пользователя        |
| `POST`   | `/api/auth/token/`           | Получить токен авторизации      |
| `POST`   | `/api/auth/token/refresh/`   | Обновить токен                  |

> Полная документация API: `/api/schema/swagger-ui/`

---

## 📁 Структура проекта

```
TravelKG/
├── .github/
│   └── workflows/         # GitHub Actions CI/CD
├── mysite/
│   ├── manage.py
│   ├── mysite/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── apps/
│       ├── tours/         # Туры и маршруты
│       ├── places/        # Достопримечательности
│       └── users/         # Пользователи
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## 🔄 CI/CD

Проект настроен с автоматическим деплоем через **GitHub Actions**:

- ✅ Автоматическая проверка кода при каждом `push` и `pull request`
- 🐳 Сборка и публикация Docker-образа
- 🚀 Автоматический деплой на сервер при мерже в `master`

---

## 👥 Команда

Проект разработан командой стажёров:

| Участник | GitHub |
|----------|--------|
| Salahidin | [![GitHub](https://img.shields.io/badge/SalahidinAI-181717?style=flat&logo=github)](https://github.com/SalahidinAI) |
| Erzhan | [![GitHub](https://img.shields.io/badge/KadyrovErjan-181717?style=flat&logo=github)](https://github.com/KadyrovErjan) |
| Miraida | [![GitHub](https://img.shields.io/badge/Miraida-181717?style=flat&logo=github)](https://github.com) |

---

## 🧪 Запуск тестов

```bash
docker compose exec web python manage.py test
```

---

<div align="center">

**🇰🇬 Сделано с любовью к Кыргызстану**

</div>
