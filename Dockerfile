# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE happinesspackets.settings.dev

# create the app directory - and switch to it
RUN mkdir -p /app
WORKDIR /app

# install dependencies
COPY requirements /tmp/requirements
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements/production.txt && \
    rm -rf /root/.cache/

# copy project
COPY . /app/

RUN python ./manage.py collectstatic --noinput

# expose port 8000
EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "happinesspackets.wsgi:application"]
