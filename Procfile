prod: gunicorn bidr.wsgi:application --pythonpath="$PWD/bidr"  --log-file "logs/gunicorn" --log-level info --preload --workers 3 --timeout 300
dev: gunicorn bidr.wsgi:application --pythonpath="$PWD/bidr" --bind localhost:8020 --log-file "logs/gunicorn" --log-level debug --preload
