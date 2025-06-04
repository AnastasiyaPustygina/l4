FROM python:3.9-slim

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y gcc libpq-dev

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
