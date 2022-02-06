FROM python:3.8-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install ca-certificates -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    useradd --create-home --no-log-init --user-group clavis

RUN mkdir -p /app/clavis && mkdir -p /rpc

COPY requirements.txt setup.py /app
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

COPY clavis/ /app/clavis/
RUN pip install --no-cache-dir /app

WORKDIR /data
RUN chown -R clavis:clavis /data && chown -R clavis:clavis /rpc

USER clavis

ENV CLAVIS_MODE release

ENTRYPOINT ["clavis"]