FROM python:slim

EXPOSE 10001

#Update the so of the image
RUN apt-get -y update

WORKDIR usr/src/app

COPY requirements.txt .
RUN apt-get install -y jq
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir -p certs
COPY src src
COPY boot.sh main.py config.py capif_registration.json ./

RUN chmod +x boot.sh

ENTRYPOINT ["./boot.sh"]

