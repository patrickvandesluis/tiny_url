#/bin/bash

cd /www/tiny_url
source venv/bin/activate
gunicorn -b localhost:8001 tiny_url.wsgi
