FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN python manage.py makemigrations
RUN python manage.py makemigrations shrtnr
RUN python manage.py migrate
CMD ["gunicorn", "tiny_url.wsgi"]

