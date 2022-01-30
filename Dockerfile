FROM python:3.8-slim

WORKDIR /app
RUN mkdir -p clavis

COPY requirements.txt setup.py /app
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY clavis/ /app/clavis/
RUN pip install --no-cache-dir .

USER 1001

ENTRYPOINT ["clavis"]