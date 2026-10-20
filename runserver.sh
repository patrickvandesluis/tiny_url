#!/bin/bash
# Local/manual start only; production uses deploy/tiny_url.service.
cd "$(dirname "$0")"
source venv/bin/activate
exec gunicorn --bind 127.0.0.1:8001 tiny_url.wsgi
