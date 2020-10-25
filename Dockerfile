FROM python:3.8-alpine
MAINTAINER Galen Guyer <galen@galenguyer.com>

RUN ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime

WORKDIR /opt/app

ADD requirements.txt /opt/app

RUN pip install -r requirements.txt

ADD . /opt/app

CMD ["gunicorn", "ritdiningapi:APP", "--bind=0.0.0.0:5000", "--access-logfile=-"]
