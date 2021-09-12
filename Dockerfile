FROM python:3.8

COPY . /code
WORKDIR /code

CMD python script.py
