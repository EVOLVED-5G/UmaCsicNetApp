FROM python:slim

EXPOSE 10001

#Update the so of the image
RUN apt-get -y update

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY certs certs
COPY src src
COPY boot.sh main.py config.py .
RUN chmod +x boot.sh

ENTRYPOINT ["./boot.sh"]

