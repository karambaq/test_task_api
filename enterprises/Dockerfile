FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /code
RUN apt-get update
RUN apt-get -y install --fix-missing libpq-dev gcc musl-dev postgresql

RUN pip install poetry
ADD pyproject.toml poetry.lock /code/

RUN poetry config virtualenvs.create false \
    && poetry install  --no-interaction --no-ansi

COPY . .


RUN chmod +x docker-entrypoint.sh
# EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]

# CMD python manage.py runserver 0.0.0.0:8000
# CMD gunicorn --workers=4 --threads=3 exchange_rate.wsgi:application --bind 0.0.0.0:8000