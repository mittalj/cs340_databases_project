#this file is used to run your flask-based-database-interacting-website persistently!

from webapp import app
#source ./venv/bin/activate
#gunicorn run:app -b 0.0.0.0:6353 -D
