FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY backend/requirements /app/requirements

RUN pip install --upgrade pip && \
    pip install -r requirements/base.txt

COPY backend /app
