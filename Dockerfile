FROM ubuntu:xenial

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y --force-yes gcc wget python-dev python-opencv libjpeg-dev zlibc libwebp-dev libtiff-dev git

RUN wget -P /usr/src/app https://bootstrap.pypa.io/get-pip.py
RUN python /usr/src/app/get-pip.py
RUN rm -rf /usr/src/app/get-pip.py

RUN pip install pika
RUN pip install gcloud
RUN pip install boto3

ADD pycv .
ADD creds.json creds.json
ADD aws.config aws.config

ENV AWS_CONFIG_FILE aws.config

CMD ["python", "cloudy.py"]