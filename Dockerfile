FROM python:3.12

WORKDIR /app
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc\
    gettext \
    vim \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
