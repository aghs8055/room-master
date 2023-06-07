FROM python:3.11.2-alpine3.17 AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN apk update && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

FROM python:3.11.2-alpine3.17

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

COPY --chown=appuser:appgroup . .

USER appuser
