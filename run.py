#this file is used to run your flask-based-database-interacting-website persistently!

from webapp import app
#then from the commandline run:
#./venv/bin/activate
#gunicorn run:app -b 0.0.0.0:SOME_NUMBER_BETWEEN_1025_and_65535
#eg. gunicorn run:app -b 0.0.0.0:8842
