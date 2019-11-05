FROM alpine:latest

ENV CLOUDSQL_CONNECTION_NAME=esoteric-life-258022:us-central1:private-sql
ENV CLOUDSQL_DATABASE=database
ENV CLOUDSQL_USER=root
ENV CLOUDSQL_PASSWORD=panda
ENV CLOUDSQL_IP=10.1.64.3

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip
        
WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["main.py"]
