#!/bin/bash
source venv/bin/activate
flask db init
flask db migrate -m "First migration"
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - main:app