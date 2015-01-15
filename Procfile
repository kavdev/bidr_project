web: gunicorn bidr.wsgi:application --pythonpath="$PWD/bidr"  --log-file - --log-level debug
dev: gunicorn bidr.wsgi:application --pythonpath="$PWD/bidr" --bind 0.0.0.0:8020 --log-file "log/gunicorn" --log-level debug --preload
