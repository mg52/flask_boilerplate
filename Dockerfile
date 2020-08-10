FROM python:3.6.2

WORKDIR /project

ADD . /project

RUN pip install -r requirements.txt

ENTRYPOINT ["./gunicorn_starter.sh"]