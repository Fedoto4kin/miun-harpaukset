FROM python:3.8

# 1. Сначала установка системных зависимостей и uWSGI КАК ROOT
RUN apt-get update && \
    apt-get install -y gcc libc-dev libpq-dev sudo && \
    apt-get -y autoclean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 2. Установка uWSGI СИСТЕМНО (до создания пользователя!)
RUN pip install -U pip
RUN pip install uWSGI==2.0.31

# 3. Копирование зависимостей и их установка
COPY ./app/requirements.txt /tmp/
COPY ./.env /.env
RUN pip install -Ur /tmp/requirements.txt

# 4. Создание пользователя (после установки uWSGI!)
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g $GROUP_ID krl && \
    useradd -m -u $USER_ID -g krl -s /bin/bash krl && \
    echo "krl ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# 5. Настройка времени и переменных среды
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

# 6. Копирование приложения
COPY --chown=krl:krl ./app /app

USER krl
