from src import mail
from threading import Thread
import json
import time
import datetime
from datetime import datetime, timedelta
from requests import get
from os import environ



def process(app):
    thr = Thread(target=check_new_data, args=(app,))
    thr.daemon = True
    thr.start()


def check_new_data(app):
    with app.app_context():
        id = 0
        updated = True
        notify_mail = False
        diff = None
        time.sleep(60)
        while 1:
            
            if id == 0:
                h = json.loads(get(environ.get('NETAPPDIR')+"/api/historics").content)
                if len(h) == 0:
                    notify_mail = True
                elif datetime.utcnow() - datetime.strptime(h[-1]["timestamp"], "%Y-%m-%dT%H:%M:%S.%f") > timedelta(minutes=15):
                    id = h[-1]["id"]
                    last = json.loads(get(environ.get('NETAPPDIR') + "/api/historics").content)[-1]["timestamp"]
                    diff = datetime.utcnow() - datetime.strptime(last, "%Y-%m-%dT%H:%M:%S.%f")
                    notify_mail = True
                else:
                    id = h[-1]["id"]
                    print("starting last id = " + str(id))
                    notify_mail = False
                    updated = True
            else:
                h = json.loads(get(environ.get('NETAPPDIR')+"/api/historics?from="+str(id)).content)
                if len(h) > 0:
                    id = h[-1]["id"]
                    print("id = " + str(id))
                    print("New entries")
                    notify_mail = False
                    updated = True
                elif updated:
                    last = json.loads(get(environ.get('NETAPPDIR')+"/api/historics").content)[-1]["timestamp"]
                    diff = datetime.utcnow() - datetime.strptime(last, "%Y-%m-%dT%H:%M:%S.%f")
                    notify_mail = True
                else:
                    print("Error, but mail has already been sent")
            if notify_mail and diff is not None:
                notify_mail = False
                updated = False
                mail.send_message(
                    subject="NetApp",
                    sender=environ.get('MAIL_USERNAME'),
                    recipients=[environ.get("MAIL_RECIPIENT")],
                    body="Error. No data since "+str(diff)
                )
            time.sleep(900)