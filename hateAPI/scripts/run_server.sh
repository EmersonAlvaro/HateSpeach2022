
exec gunicorn server:app \
--bind 0.0.0.0:8080 \
--timeout 600 \
--workers 1 \
--name "hateSpeachAPI"