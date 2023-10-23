FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app
WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 80

CMD ["daphne", "-b", "0.0.0.0", "-p", "80", "unimeet.asgi:application"]