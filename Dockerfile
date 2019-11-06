FROM alpine:latest

ENV CLOUDSQL_DATABASE=
ENV CLOUDSQL_USER=
ENV CLOUDSQL_PASSWORD=
ENV CLOUDSQL_IP=

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip
        
WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["main.py"]
