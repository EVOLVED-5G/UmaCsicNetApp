FROM python:slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY netapp netapp
COPY boot.sh main.py .flaskenv config.py ./
RUN chmod +x boot.sh

ENV FLASK_APP main.py


EXPOSE 5000

ENTRYPOINT ["./boot.sh"]

