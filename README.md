# Simple Custom Url Shortener

Created by Patrick van de Sluis.

## Deploy
1. `python3 -m venv venv && venv/bin/pip install -r requirements.txt`
2. Copy `.env.example` to `.env`, fill in a fresh `SECRET_KEY` and `ADMIN_URL`, then `chmod 600 .env`.
3. `venv/bin/python manage.py migrate && venv/bin/python manage.py collectstatic`
4. Install `deploy/tiny_url.service` (systemd) and `deploy/nginx-vandesluis.com.conf` (nginx).
5. `venv/bin/python manage.py check --deploy`

## Tests
`SECRET_KEY=x ALLOWED_HOSTS=testserver venv/bin/python manage.py test shrtnr`
