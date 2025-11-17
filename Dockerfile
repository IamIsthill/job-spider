FROM mcr.microsoft.com/playwright/python:v1.55.0-noble

RUN useradd -ms /bin/sh -u 1234 app
USER app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY  --chown=app:app . .

