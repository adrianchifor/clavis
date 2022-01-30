FROM python:3.8-slim

WORKDIR /app
COPY clavis requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

USER 1001

CMD python3 clavis/main.py