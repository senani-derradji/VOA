FROM python:3.9-slim

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/* && apt-get install -y curl
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["bash", "/app/start.sh"]