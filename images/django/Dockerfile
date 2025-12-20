FROM python:3.8

ARG USER_ID=1000
ARG GROUP_ID=1000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN  apt-get update && \
     apt-get install -y gcc libc-dev libpq-dev sudo && \
     apt-get -y autoclean && \
     rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./app/requirements.txt /tmp/
COPY ./.env /.env

RUN pip install -U pip
RUN pip install -Ur /tmp/requirements.txt

# Создаем группу и пользователя с переданными ID
RUN groupadd -g $GROUP_ID krl && \
    useradd -m -u $USER_ID -g krl -s /bin/bash krl && \
    echo "krl ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

WORKDIR /app

# Копируем файлы и меняем владельца
COPY --chown=krl:krl ./app /app

USER krl