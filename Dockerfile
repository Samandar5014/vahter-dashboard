# Используем официальный Python slim (маленький, но надёжный)
FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем зависимости сначала (для кэша слоёв)
COPY requirements.txt .

# Устанавливаем пакеты
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

# Порт сайта (3000) и метрик (если отдельно, но у нас всё на 3000)
EXPOSE 3000

# Запуск приложения
ENTRYPOINT ["python", "app.py"]