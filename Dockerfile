FROM python:3.8-slim-buster

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir temp

RUN apt-get update && \
    apt-get install -y g++

RUN apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
    apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io

COPY . .

EXPOSE 80

CMD ["python3", "run.py"]
