#!/bin/bash
flask db init
flask db migrate -m "First migration"
flask db upgrade
python main.py