#!/bin/bash

python manage.py makemigrations

python manage.py makemigrations shrtnr

python manage.py migrate

# TODO fix statement below.
if [[ -v "${DJANGOSUPERUSER_NAME}" ]]; then
    echo "from django.contrib.auth.models import User; User.objects.create_superuser($DJANGOSUPERUSER_NAME', '$DJANGOSUPERUSER_MAIL', '$DJANGOSUPERUSER_PASS')" | python manage.py shell
fi