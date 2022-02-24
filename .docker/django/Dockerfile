FROM python:alpine
WORKDIR /opt
COPY requirements.txt .
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev mariadb-dev \
    && apk add --no-cache mariadb-connector-c \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del build-deps
COPY . .
