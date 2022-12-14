#!/bin/bash

jq -r .capif_host=\"$CAPIFHOST\" capif_registration.json >> tmp.json && mv tmp.json capif_registration.json
jq -r .capif_http_port=\"$CAPIFHTTP\" capif_registration.json >> tmp.json && mv tmp.json capif_registration.json
jq -r .capif_https_port=\"$CAPIFHTTPS\" capif_registration.json >> tmp.json && mv tmp.json capif_registration.json
jq -r .capif_callback_url=\"http://$CALLBACK_ADDRESS\" capif_registration.json >> tmp.json && mv tmp.json capif_registration.json

evolved5g register-and-onboard-to-capif --config_file_full_path="/usr/src/app/capif_registration.json"

flask db init
flask db migrate -m "First migration"
flask db upgrade
python main.py