FROM python:3
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN ./setup.bash
CMD ["gunicorn", "tiny_url.wsgi"]

