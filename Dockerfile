FROM python:3.10-slim-buster

EXPOSE 5000

RUN mkdir -p "/usr/app/instance"
COPY . /usr/app
WORKDIR /usr/app
RUN pip install -r requirements.txt

CMD python -m flask run --host=0.0.0.0