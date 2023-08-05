from threading import Thread
import json
import time
import datetime
from datetime import datetime, timedelta
from requests import get, post
from os import environ

def process(app):
    thr = Thread(target=check_new_data, args=(app,))
    thr.daemon = True
    thr.start()

def send_telegram_message(token, chat_id, text):
    api_url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = post(api_url, data=data)
    return response.json()

def check_new_data(app):
    with app.app_context():
        id = 0
        updated = True
        notify_telegram = False
        diff = None
        time.sleep(60)
        while 1:
            if id == 0:
                h = json.loads(get(environ.get('NETAPPDIR')+"/api/historics/").content)
                if len(h) == 0:
                    send_telegram_message(environ.get('TELEGRAM_TOKEN'), environ.get('TELEGRAM_CHAT_ID'), "Error. No data.")
                elif datetime.utcnow() - datetime.strptime(h[-1]["timestamp"], "%Y-%m-%dT%H:%M:%S.%f") > timedelta(minutes=15):
                    id = h[-1]["id"]
                    last = json.loads(get(environ.get('NETAPPDIR') + "/api/historics/").content)[-1]["timestamp"]
                    diff = datetime.utcnow() - datetime.strptime(last, "%Y-%m-%dT%H:%M:%S.%f")
                    notify_telegram = True
                else:
                    id = h[-1]["id"]
                    print("starting last id = " + str(id))
                    notify_telegram = False
                    updated = True
            else:
                h = json.loads(get(environ.get('NETAPPDIR')+"/api/historics?from="+str(id)).content)
                if len(h) > 0:
                    id = h[-1]["id"]
                    print("id = " + str(id))
                    print("New entries")
                    notify_telegram = False
                    updated = True
                elif updated:
                    last = json.loads(get(environ.get('NETAPPDIR')+"/api/historics/").content)[-1]["timestamp"]
                    diff = datetime.utcnow() - datetime.strptime(last, "%Y-%m-%dT%H:%M:%S.%f")
                    notify_telegram = True
                else:
                    print("Error, but warning has already been sent")
            if notify_telegram and diff is not None:
                notify_telegram = False
                updated = False
                send_telegram_message(environ.get('TELEGRAM_TOKEN'), environ.get('TELEGRAM_CHAT_ID'), "Error. No data since "+str(diff))
            time.sleep(900)