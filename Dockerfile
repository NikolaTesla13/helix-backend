FROM python:3.8-slim-buster

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir temp

RUN apt-get update && \
    apt-get install -y g++

# https://docs.docker.com/engine/install/ubuntu/
# TODO

COPY . .

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "run:app"]
