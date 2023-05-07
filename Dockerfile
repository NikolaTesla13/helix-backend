FROM python:3.8-slim-buster

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir tmp

RUN apt-get update && \
    apt-get install -y g++ docker

COPY . .

EXPOSE 80

CMD ["python3", "run.py"]
