FROM python:3.8-slim

WORKDIR /app
COPY clavis/*.py requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

USER 1001

CMD uvicorn main:app --host 0.0.0.0 --port 8080