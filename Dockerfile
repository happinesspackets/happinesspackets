# pull official base image
FROM python:3.13-alpine

RUN pip install uv

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=happinesspackets.settings.deployment

# create the app directory - and switch to it
RUN mkdir -p /app
WORKDIR /app

# copy project
COPY . /app/

# install dependencies
RUN uv sync --no-dev --frozen \
    && rm -rf /root/.cache/uv

RUN uv run --no-sync python ./manage.py collectstatic --noinput

# expose port 8000
EXPOSE 8000

CMD ["./docker-startup.sh"]
