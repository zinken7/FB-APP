#! /bin/bash
source env/bin/activate
export FLASK_ENV=development
export FLASK_APP=run.py
flask run --port=5000