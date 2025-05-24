FROM python:3.10-slim

WORKDIR /myapp

# Build dependencies needed by psycopg2 etc.
RUN apt-get update && apt-get install -y gcc libpq-dev

COPY requirements.txt .

RUN pip install --upgrade pip && pip install gunicorn && pip install -r requirements.txt

COPY . .

# Flask port
ENV PORT=10000

# Use Gunicorn to start app
CMD gunicorn --bind 0.0.0.0:$PORT app:app
