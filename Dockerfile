# Используйте официальный образ Python в качестве базового образа
FROM python:3.11

# Установка переменной окружения PYTHONUNBUFFERED для предотвращения проблем с выводом в консоль
ENV PYTHONUNBUFFERED=1

# Установка рабочего каталога в /app
WORKDIR /app

# Установка зависимостей системы для Tesseract OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей проекта в контейнер
COPY requirements.txt /app/

# Установка зависимостей проекта
RUN pip install -r requirements.txt

# Копирование всех файлов проекта в контейнер
COPY . /app/