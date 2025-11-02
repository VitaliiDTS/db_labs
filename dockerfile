FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc default-libmysqlclient-dev pkg-config \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production \
    AWS_REGION=eu-north-1 \
    DB_SECRET_NAME=lab/mysql

EXPOSE 8080

CMD ["python", "-u", "app.py"]

