FROM python:3.12.8

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Устанавливаем netcat для ожидания базы
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Ждём базу перед стартом приложения
CMD ["sh", "-c", "until nc -z $POSTGRES_HOST $POSTGRES_PORT; do echo 'Waiting for Postgres...'; sleep 2; done && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
