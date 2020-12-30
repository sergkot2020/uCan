FROM python:3.7-slim as base
EXPOSE 8000
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install requirements
FROM base as install_requirements
RUN mkdir /install
WORKDIR /install
COPY ./bot/requirements.txt /requirements.txt
RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip install -r /requirements.txt

# Copy and run code
FROM install_requirements
COPY ./bot /srv/www/bot
WORKDIR /srv/www/bot
COPY ./bot/entrypoint.sh /srv/www/bot/entrypoint.sh
COPY ./bot/gunicorn_config.py /srv/www/bot/gunicorn_config.py

ENTRYPOINT ["sh", "/srv/www/bot/egunicorn_config.py"]
ENTRYPOINT ["sh", "/srv/www/bot/entrypoint.sh"]








