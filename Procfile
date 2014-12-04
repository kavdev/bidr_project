web: gunicorn bidr.wsgi --log-file - --pythonpath="$PWD/bidr"
prod: gunicorn bidr.wsgi:application --pythonpath="$PWD/bidr"  --log-file - --log-level debug
dev: gunicorn bidr.wsgi:application --pythonpath="$PWD/bidr" --bind 0.0.0.0:8020 --log-file "logs/gunicorn" --log-level debug --preload
