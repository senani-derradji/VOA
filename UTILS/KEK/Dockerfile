FROM python:3.11-alpine

RUN addgroup -S appkek && adduser -S kek -G appkek
WORKDIR /app

COPY kek_server.py .

RUN apk add openssl
RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
RUN pip install --no-cache-dir flask cryptography

RUN chown -R kek:appkek /app
USER kek

EXPOSE 5555

CMD ["python", "kek_server.py"]