# University Database Management System

Проект для управління базою даних університету з використанням SQLAlchemy, PostgreSQL та Alembic.

## Структура проекту

```
university-database/
├── models.py              # Моделі SQLAlchemy
├── database.py            # Налаштування підключення до БД
├── seed.py               # Скрипт заповнення тестовими даними
├── my_select.py          # 10 запитів до бази даних
├── docker-compose.yml    # Конфігурація Docker для PostgreSQL + Adminer
├── pyproject.toml        # Залежності Poetry
├── alembic.ini          # Конфігурація Alembic
└── alembic/
    └── versions/         # Файли міграцій
```

## Вимоги

- Python 3.12+
- Docker та Docker Compose

## Встановлення та запуск

### 1. Клонування проекту

```bash
git clone <repository-url>
cd university-database
```

### 2. Встановлення залежностей

```bash
# Створення віртуального оточення Python
python -m venv env

# Активація віртуального оточення
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate

# Встановлення залежностей
pip install -r requirements.txt
```

### 3. Запуск бази даних

```bash
# Запуск PostgreSQL та Adminer через Docker
docker-compose up -d

# Перевірка статусу контейнерів
docker-compose ps
```

### 4. Виконання міграцій

```bash
# Застосування міграцій до бази даних
alembic upgrade head

# Перевірка поточної версії
alembic current
```

### 5. Заповнення тестовими даними

```bash
# Запуск скрипту seed.py для створення тестових даних
python seed.py
```

### 6. Тестування запитів

```bash
# Запуск всіх 10 запитів
python my_select.py
```

## Веб-інтерфейс бази даних (Adminer)

Після запуску Docker контейнерів, відкрийте браузер:

**URL:** http://localhost:8081

**Параметри підключення:**
- Система: PostgreSQL
- Сервер: postgres
- Користувач: postgres
- Пароль: mysecretpassword
- База даних: university_db

## Опис функціоналу

### Моделі бази даних

- **Group** - Групи студентів (IT-21, CS-22, AI-23)
- **Student** - Студенти з посиланням на групу
- **Teacher** - Викладачі
- **Subject** - Предмети з посиланням на викладача
- **Grade** - Оцінки студентів з предметів з датою отримання

### Реалізовані запити (my_select.py)

1. **select_1()** - 5 студентів із найбільшим середнім балом з усіх предметів
2. **select_2(subject_name)** - Студент із найвищим середнім балом з певного предмета
3. **select_3(subject_name)** - Середній бал у групах з певного предмета
4. **select_4()** - Середній бал на потоці (по всій таблиці оцінок)
5. **select_5(teacher_name)** - Курси, які читає певний викладач
6. **select_6(group_name)** - Список студентів у певній групі
7. **select_7(group_name, subject_name)** - Оцінки студентів у окремій групі з певного предмета
8. **select_8(teacher_name)** - Середній бал, який ставить певний викладач
9. **select_9(student_name)** - Список курсів, які відвідує певний студент
10. **select_10(student_name, teacher_name)** - Курси, які певному студенту читає певний викладач

### Тестові дані

Скрипт `seed.py` створює:
- 3 групи студентів
- 50 студентів (розподілених по групах)
- 5 викладачів
- 8 предметів (призначених викладачам)
- 500-1000 оцінок (по 10-20 для кожного студента)

## Корисні команди

### Docker
```bash
# Запуск контейнерів
docker-compose up -d

# Зупинка контейнерів
docker-compose down

# Перегляд логів PostgreSQL
docker-compose logs postgres

# Підключення до PostgreSQL через консоль
docker-compose exec postgres psql -U postgres -d university_db
```

### Alembic
```bash
# Створення нової міграції
alembic revision --autogenerate -m "Description"

# Застосування міграцій
alembic upgrade head

# Відкат до попередньої версії
alembic downgrade -1

# Перегляд історії міграцій
alembic history
```

### Python Virtual Environment
```bash
# Створення нового віртуального оточення
python -m venv env

# Активація оточення
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate

# Деактивація оточення
deactivate

# Встановлення додаткових пакетів
pip install package-name

# Збереження поточних залежностей
pip freeze > requirements.txt
```

## Приклади використання

### Виконання окремих запитів

```python
from my_select import *

# Найкращі студенти
top_students = select_1()
for student in top_students:
    print(f"{student.fullname}: {student.avg_grade}")

# Найкращий студент з певного предмету
best_in_subject = select_2("Математика")
print(f"Найкращий з математики: {best_in_subject.fullname}")

# Студенти групи
students = select_6("IT-21")
for student in students:
    print(student.fullname)
```

### Очищення та повторне заповнення даних

```bash
# Очищення та створення нових тестових даних
python seed.py
```

## Зв'язки між таблицями

```
Group (1) ──→ (∞) Student (∞) ──→ (∞) Grade (∞) ──→ (1) Subject (∞) ──→ (1) Teacher
```

## Технології

- **SQLAlchemy 2.0** - ORM для роботи з базою даних
- **PostgreSQL 15** - Реляційна база даних
- **Alembic** - Інструмент для міграцій схеми БД
- **Faker** - Генерація випадкових тестових даних
- **Docker Compose** - Контейнеризація сервісів
- **Adminer** - Веб-інтерфейс для управління БД
- **Poetry** - Управління залежностями Python

## Автор

Створено для виконання домашнього завдання з курсу Python Web Development.