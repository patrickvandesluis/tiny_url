FROM python:3
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tiny_url.wsgi"]

