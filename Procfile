web: gunicorn bidr.wsgi:application --pythonpath="$PWD/bidr" --bind emerald.iondune.net:8040 --log-file "logs/gunicorn" --log-level info --preload --workers 3 --timeout 300
